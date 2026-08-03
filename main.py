import hashlib, random, uuid, json, os
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

from models import SessionLocal, init_db, Usuario, Rig, RigGrupo, MineralInventario, PiezaInstalada, OrdenMercado, OrdenElectricidad
from reglas import MINERALES, RECETAS, SLOTS_RIG, BONUS_RIG_COMPLETO, DIFICULTAD_DISPOSITIVO, RECOMPENSA_POR_SHARE, META_ORO_SEMANAL, COSTO_DIARIO_USDT, ROTACION_JOB_SEGUNDOS, PAQUETES_ELECTRICIDAD, calcular_nivel

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "SilkAdmin41")

def verificar_admin(x_admin_password: str = Header(None)):
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(401, "No autorizado")
    return True


def verificar_usuario(usuario_id: str, password: str, db: Session) -> Usuario:
    """Si el usuario no tiene password todavía, la primera que mande queda fijada.
    Si ya tiene una, debe coincidir."""
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(404, "Usuario no existe")
    if not password:
        raise HTTPException(401, "Falta password")
    if usuario.password is None:
        usuario.password = password
        db.commit()
    elif usuario.password != password:
        raise HTTPException(401, "Password incorrecta")
    return usuario

app = FastAPI(title="Miner Backend")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción real, restringir al dominio real del panel
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()


def job_descontar_electricidad():
    db = SessionLocal()
    try:
        for rig in db.query(Rig).filter_by(activo=True).all():
            if rig.dias_electricidad_prepagados > 0:
                rig.dias_electricidad_prepagados -= 1
            rig.fecha_ultimo_descuento = datetime.utcnow()
        db.commit()
        print(f"[cron] electricidad descontada — {datetime.utcnow().isoformat()}")
    finally:
        db.close()


def job_ajustar_recompensa():
    db = SessionLocal()
    try:
        shares_semana = sum(len(s) for s in shares_por_job.values())
        if shares_semana > 0:
            estado_recompensa["valor"] = META_ORO_SEMANAL / shares_semana
        print(f"[cron] recompensa ajustada a {estado_recompensa['valor']} — shares: {shares_semana}")
    finally:
        db.close()


@app.on_event("startup")
def iniciar_scheduler():
    scheduler.add_job(job_descontar_electricidad, "interval", hours=24, id="descuento_diario")
    scheduler.add_job(job_ajustar_recompensa, "interval", weeks=1, id="ajuste_semanal")
    scheduler.start()
    print("[cron] scheduler iniciado: descuento diario (24h) + ajuste semanal (7d)")


@app.on_event("shutdown")
def detener_scheduler():
    scheduler.shutdown()

# Recompensa actual por share — variable en runtime, se recalcula semanalmente
estado_recompensa = {"valor": RECOMPENSA_POR_SHARE}

current_job = {
    "job_id": str(uuid.uuid4()),
    "prev_hash": hashlib.sha256(b"genesis").hexdigest(),
    "difficulty": DIFICULTAD_DISPOSITIVO,
    "created_at": datetime.utcnow(),
}
shares_por_job: dict[str, set] = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def rotar_job_si_expiro():
    if (datetime.utcnow() - current_job["created_at"]).seconds >= ROTACION_JOB_SEGUNDOS:
        current_job["job_id"] = str(uuid.uuid4())
        current_job["prev_hash"] = hashlib.sha256(
            (current_job["prev_hash"] + str(datetime.utcnow())).encode()
        ).hexdigest()
        current_job["created_at"] = datetime.utcnow()


def cumple_dificultad(hash_hex: str, dificultad: int) -> bool:
    return hash_hex.startswith("0" * dificultad)


# ---------- REGISTRO ----------
@app.post("/register")
def register_rig(mac: str, usuario_id: str, password: str, nombre: str = None, db: Session = Depends(get_db)):
    if not password:
        raise HTTPException(401, "Falta password")

    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        # Cuenta nueva: la contraseña queda fijada en el mismo instante en que se crea,
        # sin ventana de tiempo en la que otro pueda "robarla" fijando la suya primero.
        usuario = Usuario(id=usuario_id, nombre=nombre or usuario_id, oro_saldo=0, oro_historico=0, password=password)
        db.add(usuario)
        db.commit()
    elif usuario.password is None:
        # Cuenta creada antes de este arreglo (sin password todavía): se fija ahora.
        usuario.password = password
        db.commit()
    elif usuario.password != password:
        raise HTTPException(401, "Password incorrecta: esta cuenta ya tiene dueño")

    if db.get(Rig, mac):
        raise HTTPException(400, "MAC ya registrada")

    rig = Rig(mac=mac, usuario_id=usuario_id, activo=True, dias_electricidad_prepagados=1)
    db.add(rig)
    db.commit()
    return {"status": "registrado", "mac": mac}


@app.post("/rig/renombrar")
def renombrar_rig(mac: str, usuario_id: str, nuevo_nombre: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    rig = db.get(Rig, mac)
    if not rig:
        raise HTTPException(404, "Rig no encontrado")
    if rig.usuario_id != usuario_id:
        raise HTTPException(403, "Este rig no te pertenece")
    if not nuevo_nombre.strip():
        raise HTTPException(400, "Nombre inválido")
    if len(nuevo_nombre) > 30:
        raise HTTPException(400, "Nombre muy largo (máx 30 caracteres)")

    rig.nombre = nuevo_nombre.strip()
    db.commit()
    return {"status": "ok", "mac": mac, "nombre": rig.nombre}


# ---------- AGRUPACIÓN: crear un rig (contenedor de hasta 6 ESP32) ----------
@app.post("/rig/crear")
def crear_rig_grupo(usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    existentes = db.query(RigGrupo).filter_by(usuario_id=usuario_id).all()
    siguiente_id = str(max([int(r.id) for r in existentes], default=0) + 1)
    grupo = RigGrupo(id=siguiente_id, usuario_id=usuario_id, nombre=f"Rig {siguiente_id}")
    db.add(grupo)
    db.commit()
    return {"rig_id": grupo.id, "nombre": grupo.nombre}


# ---------- AGRUPACIÓN: asignar un ESP32 a un rig (máx 6 por rig) ----------
@app.post("/rig/asignar_esp32")
def asignar_esp32(mac: str, rig_id: str, usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    dispositivo = db.get(Rig, mac)
    if not dispositivo or dispositivo.usuario_id != usuario_id:
        raise HTTPException(404, "ESP32 no encontrado o no te pertenece")

    grupo = db.query(RigGrupo).filter_by(id=rig_id, usuario_id=usuario_id).first()
    if not grupo:
        raise HTTPException(404, "Rig no encontrado")

    cantidad_actual = db.query(Rig).filter_by(rig_id=rig_id, usuario_id=usuario_id).count()
    if cantidad_actual >= 6:
        raise HTTPException(400, "Ese rig ya tiene 6 ESP32 (máximo)")

    dispositivo.rig_id = rig_id
    db.commit()
    return {"status": "ok", "mac": mac, "rig_id": rig_id}


# ---------- JOB ----------
@app.get("/job")
def get_job(mac: str, db: Session = Depends(get_db)):
    rig = db.get(Rig, mac)
    if not rig:
        raise HTTPException(404, "Rig no registrado")
    if rig.dias_electricidad_prepagados <= 0:
        raise HTTPException(402, "Electricidad pendiente")

    rotar_job_si_expiro()
    return {
        "job_id": current_job["job_id"],
        "prev_hash": current_job["prev_hash"],
        "difficulty": current_job["difficulty"],
    }


# ---------- SUBMIT ----------
@app.post("/submit")
def submit_share(mac: str, job_id: str, nonce: int, hash_result: str, db: Session = Depends(get_db)):
    rig = db.get(Rig, mac)
    if not rig or rig.dias_electricidad_prepagados <= 0:
        raise HTTPException(402, "Electricidad pendiente")
    if job_id != current_job["job_id"]:
        raise HTTPException(400, "Job expirado")
    if mac in shares_por_job.get(job_id, set()):
        raise HTTPException(400, "Share ya enviado para este job")

    esperado = hashlib.sha256((current_job["prev_hash"] + str(nonce)).encode()).hexdigest()
    if esperado != hash_result or not cumple_dificultad(esperado, current_job["difficulty"]):
        raise HTTPException(400, "Hash inválido")

    shares_por_job.setdefault(job_id, set()).add(mac)

    usuario = db.get(Usuario, rig.usuario_id)

    buff = 0.0
    if rig.rig_id:
        piezas_del_rig = db.query(PiezaInstalada).filter_by(usuario_id=usuario.id, rig_id=rig.rig_id).all()
        piezas_activas = [p for p in piezas_del_rig if p.durabilidad_actual > 0]
        buff = sum(RECETAS[p.pieza_id]["buff_hashrate"] for p in piezas_activas)
        slots_llenos = {p.slot for p in piezas_activas}
        if len(slots_llenos) >= len(SLOTS_RIG):
            buff += BONUS_RIG_COMPLETO
        for p in piezas_activas:
            p.durabilidad_actual = max(0, p.durabilidad_actual - 1)

    recompensa = estado_recompensa["valor"] * (1 + buff)
    usuario.oro_saldo += recompensa
    usuario.oro_historico += recompensa

    minerales_obtenidos = []
    for mineral, data in MINERALES.items():
        if random.random() < data["prob_drop"] * 0.1:
            inv = db.query(MineralInventario).filter_by(usuario_id=usuario.id, mineral=mineral).first()
            if not inv:
                inv = MineralInventario(usuario_id=usuario.id, mineral=mineral, cantidad=0)
                db.add(inv)
            inv.cantidad += 1
            minerales_obtenidos.append(mineral)

    db.commit()
    return {"status": "ok", "oro_ganado": recompensa, "minerales": minerales_obtenidos}


# ---------- AJUSTE DE RECOMPENSA POR SHARE (cron semanal) ----------
# La dificultad NUNCA cambia (queda fija para que cada ESP32 siga tardando ~25s por share,
# sin importar cuántos usuarios haya). Lo que se ajusta es cuánto Oro vale cada share,
# para mantener estable la emisión TOTAL de la red a medida que crece la cantidad de mineros.
@app.post("/admin/ajustar_recompensa")
def ajustar_recompensa(db: Session = Depends(get_db), _admin: bool = Depends(verificar_admin)):
    shares_semana = sum(len(s) for s in shares_por_job.values())  # simplificado; en producción: log persistente por semana
    if shares_semana > 0:
        estado_recompensa["valor"] = META_ORO_SEMANAL / shares_semana
    return {"recompensa_por_share": estado_recompensa["valor"], "shares_semana": shares_semana}


# ---------- ELECTRICIDAD: descuento diario (cron cada 24h) ----------
@app.post("/admin/descontar_dia_electricidad")
def descontar_dia_electricidad(db: Session = Depends(get_db), _admin: bool = Depends(verificar_admin)):
    resultados = []
    for rig in db.query(Rig).filter_by(activo=True).all():
        if rig.dias_electricidad_prepagados > 0:
            rig.dias_electricidad_prepagados -= 1
        rig.fecha_ultimo_descuento = datetime.utcnow()
        resultados.append({"mac": rig.mac, "dias_restantes": rig.dias_electricidad_prepagados})
    db.commit()
    return resultados


# ---------- ELECTRICIDAD: solicitar paquete (flujo manual) ----------
# El usuario ve el Pay ID de Binance, transfiere manualmente, sube el comprobante,
# y la orden queda "pendiente_revision" hasta que un admin la apruebe.
BINANCE_PAY_ID = "748095851"

@app.post("/electricidad/solicitar_paquete")
def solicitar_paquete(usuario_id: str, paquete_id: str, cantidad_rigs: int, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    if paquete_id not in PAQUETES_ELECTRICIDAD:
        raise HTTPException(400, "Paquete inválido")
    paquete = PAQUETES_ELECTRICIDAD[paquete_id]

    total_esp32 = db.query(Rig).filter_by(usuario_id=usuario_id, activo=True).count()
    if total_esp32 == 0:
        raise HTTPException(400, "No tienes ESP32 activos")
    if cantidad_rigs <= 0 or cantidad_rigs > total_esp32:
        raise HTTPException(400, f"Cantidad inválida (tenés {total_esp32} ESP32 conectados)")

    costo_total_usdt = round(paquete["precio_usdt_por_esp32"] * cantidad_rigs, 2)
    orden_id = f"elec_{usuario_id}_{uuid.uuid4().hex[:10]}"

    orden = OrdenElectricidad(
        id=orden_id, usuario_id=usuario_id, paquete_id=paquete_id,
        cantidad_rigs=cantidad_rigs, dias_por_rig=paquete["dias"],
        monto_usdt=costo_total_usdt, estado="pendiente_revision",
    )
    db.add(orden)
    db.commit()

    return {
        "orden_id": orden_id,
        "binance_pay_id": BINANCE_PAY_ID,
        "monto_a_pagar_usdt": costo_total_usdt,
        "rigs_afectados": cantidad_rigs,
        "dias_por_rig": paquete["dias"],
        "siguiente_paso": "Sube el comprobante con /electricidad/subir_comprobante",
    }


# ---------- ELECTRICIDAD: subir comprobante de pago ----------
@app.post("/electricidad/subir_comprobante")
async def subir_comprobante(orden_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    orden = db.get(OrdenElectricidad, orden_id)
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    if orden.estado != "pendiente_revision":
        raise HTTPException(400, "Esta orden ya fue procesada")

    os.makedirs("comprobantes", exist_ok=True)
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    ruta = f"comprobantes/{orden_id}.{ext}"
    with open(ruta, "wb") as f:
        f.write(await file.read())

    orden.comprobante_path = ruta
    db.commit()
    return {"status": "comprobante_recibido", "orden_id": orden_id}


# ---------- ADMIN: listar órdenes pendientes de revisión ----------
@app.get("/admin/ordenes_pendientes")
def ordenes_pendientes(db: Session = Depends(get_db), _admin: bool = Depends(verificar_admin)):
    ordenes = db.query(OrdenElectricidad).filter_by(estado="pendiente_revision").order_by(OrdenElectricidad.fecha).all()
    return [
        {
            "orden_id": o.id, "usuario_id": o.usuario_id, "paquete_id": o.paquete_id,
            "cantidad_rigs": o.cantidad_rigs, "dias_por_rig": o.dias_por_rig,
            "monto_usdt": o.monto_usdt, "tiene_comprobante": bool(o.comprobante_path),
            "comprobante_path": o.comprobante_path, "fecha": o.fecha.isoformat(),
        }
        for o in ordenes
    ]


# ---------- ADMIN: ver comprobante ----------
@app.get("/admin/comprobante/{orden_id}")
def ver_comprobante(orden_id: str, x_admin_password: str = None, db: Session = Depends(get_db)):
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(401, "No autorizado")
    orden = db.get(OrdenElectricidad, orden_id)
    if not orden or not orden.comprobante_path or not os.path.exists(orden.comprobante_path):
        raise HTTPException(404, "Comprobante no encontrado")
    return FileResponse(orden.comprobante_path)


# ---------- ADMIN: aprobar orden (acredita días) ----------
@app.post("/admin/aprobar_orden")
def aprobar_orden(orden_id: str, db: Session = Depends(get_db), _admin: bool = Depends(verificar_admin)):
    orden = db.get(OrdenElectricidad, orden_id)
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    if orden.estado != "pendiente_revision":
        raise HTTPException(400, "Orden ya procesada")

    rigs = (
        db.query(Rig)
        .filter_by(usuario_id=orden.usuario_id, activo=True)
        .order_by(Rig.dias_electricidad_prepagados.asc())
        .limit(orden.cantidad_rigs)
        .all()
    )
    for rig in rigs:
        rig.dias_electricidad_prepagados += orden.dias_por_rig

    orden.estado = "aprobada"
    orden.fecha_revision = datetime.utcnow()
    db.commit()

    return {"status": "aprobada", "rigs_recargados": len(rigs), "dias_agregados_por_rig": orden.dias_por_rig}


# ---------- ADMIN: rechazar orden ----------
@app.post("/admin/rechazar_orden")
def rechazar_orden(orden_id: str, db: Session = Depends(get_db), _admin: bool = Depends(verificar_admin)):
    orden = db.get(OrdenElectricidad, orden_id)
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    if orden.estado != "pendiente_revision":
        raise HTTPException(400, "Orden ya procesada")

    orden.estado = "rechazada"
    orden.fecha_revision = datetime.utcnow()
    db.commit()
    return {"status": "rechazada"}


# ---------- CRAFTEO ----------
@app.post("/craftear")
def craftear(usuario_id: str, receta_id: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    if receta_id not in RECETAS:
        raise HTTPException(400, "Receta inválida")
    receta = RECETAS[receta_id]

    for mineral, cantidad in receta["requiere"].items():
        inv = db.query(MineralInventario).filter_by(usuario_id=usuario_id, mineral=mineral).first()
        if not inv or inv.cantidad < cantidad:
            raise HTTPException(400, f"Faltan {mineral}")

    for mineral, cantidad in receta["requiere"].items():
        inv = db.query(MineralInventario).filter_by(usuario_id=usuario_id, mineral=mineral).first()
        inv.cantidad -= cantidad

    db.add(PiezaInstalada(
        usuario_id=usuario_id, pieza_id=receta_id, slot=receta["slot"],
        rig_id=None, durabilidad_actual=receta["durabilidad_max"],
    ))
    db.commit()
    return {"status": "ok", "pieza": receta_id, "buff": receta["buff_hashrate"]}


# ---------- MERCADO ----------
@app.post("/mercado/publicar")
def publicar_orden(usuario_id: str, tipo_item: str, item_id: str, cantidad: int, precio_oro: float, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    if precio_oro <= 0 or cantidad <= 0:
        raise HTTPException(400, "Cantidad/precio inválidos")

    if tipo_item == "mineral":
        inv = db.query(MineralInventario).filter_by(usuario_id=usuario_id, mineral=item_id).first()
        if not inv or inv.cantidad < cantidad:
            raise HTTPException(400, "Inventario insuficiente")
        inv.cantidad -= cantidad  # se reserva restando ya (simplificado)

    orden = OrdenMercado(usuario_id=usuario_id, tipo_item=tipo_item, item_id=item_id,
                         cantidad=cantidad, precio_oro=precio_oro, estado="abierta")
    db.add(orden)
    db.commit()
    return {"status": "publicada", "orden_id": orden.id}


@app.post("/mercado/comprar")
def comprar_orden(usuario_id: str, orden_id: int, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    orden = db.get(OrdenMercado, orden_id)
    if not orden or orden.estado != "abierta":
        raise HTTPException(400, "Orden no disponible")
    if orden.usuario_id == usuario_id:
        raise HTTPException(400, "No puedes comprar tu propia orden")

    comprador = db.get(Usuario, usuario_id)
    vendedor = db.get(Usuario, orden.usuario_id)
    if comprador.oro_saldo < orden.precio_oro:
        raise HTTPException(400, "Oro insuficiente")

    comprador.oro_saldo -= orden.precio_oro
    vendedor.oro_saldo += orden.precio_oro

    if orden.tipo_item == "mineral":
        inv = db.query(MineralInventario).filter_by(usuario_id=usuario_id, mineral=orden.item_id).first()
        if not inv:
            inv = MineralInventario(usuario_id=usuario_id, mineral=orden.item_id, cantidad=0)
            db.add(inv)
        inv.cantidad += orden.cantidad
    elif orden.tipo_item == "pieza":
        db.add(PiezaInstalada(usuario_id=usuario_id, pieza_id=orden.item_id))

    orden.estado = "completada"
    db.commit()
    return {"status": "ok"}


@app.post("/mercado/cancelar")
def cancelar_orden(usuario_id: str, orden_id: int, db: Session = Depends(get_db)):
    orden = db.get(OrdenMercado, orden_id)
    if not orden or orden.usuario_id != usuario_id:
        raise HTTPException(403, "No autorizado")
    if orden.estado != "abierta":
        raise HTTPException(400, "No cancelable")

    if orden.tipo_item == "mineral":
        inv = db.query(MineralInventario).filter_by(usuario_id=usuario_id, mineral=orden.item_id).first()
        inv.cantidad += orden.cantidad

    orden.estado = "cancelada"
    db.commit()
    return {"status": "cancelada"}


@app.get("/mercado/ordenes")
def listar_ordenes(db: Session = Depends(get_db)):
    ordenes = db.query(OrdenMercado).filter_by(estado="abierta").order_by(OrdenMercado.fecha.desc()).all()
    return [
        {"id": o.id, "usuario_id": o.usuario_id, "tipo_item": o.tipo_item, "item_id": o.item_id,
         "cantidad": o.cantidad, "precio_oro": o.precio_oro}
        for o in ordenes
    ]


# ---------- HEARTBEAT: hashrate en vivo (sin esperar a encontrar share) ----------
heartbeats: dict[str, dict] = {}  # mac -> {hashes_por_seg, timestamp, usuario_id}

@app.post("/heartbeat")
def heartbeat(mac: str, hashes_intentados: int, segundos: float, db: Session = Depends(get_db)):
    rig = db.get(Rig, mac)
    if not rig:
        raise HTTPException(404, "Rig no registrado")

    hashes_por_seg = hashes_intentados / max(segundos, 0.1)
    heartbeats[mac] = {
        "hashes_por_seg": round(hashes_por_seg, 1),
        "timestamp": datetime.utcnow(),
        "usuario_id": rig.usuario_id,
        "nombre": rig.nombre or mac,
    }
    return {"status": "ok"}


@app.get("/stats/live")
def stats_live(usuario_id: str = None):
    ahora = datetime.utcnow()
    activos = {
        mac: h for mac, h in heartbeats.items()
        if (ahora - h["timestamp"]).total_seconds() < 30  # se considera "vivo" si reportó en los últimos 30s
        and (usuario_id is None or h["usuario_id"] == usuario_id)
    }

    total_hashes_seg = sum(h["hashes_por_seg"] for h in activos.values())
    return {
        "rigs_activos": len(activos),
        "hashrate_total": round(total_hashes_seg, 1),
        "rigs": [
            {"mac": mac, "nombre": h["nombre"], "hashes_por_seg": h["hashes_por_seg"]}
            for mac, h in activos.items()
        ],
    }


# ---------- RANKING ----------
@app.get("/ranking")
def ranking(limite: int = 100, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).order_by(Usuario.oro_historico.desc()).limit(limite).all()
    return [
        {"usuario": u.nombre, "nivel": calcular_nivel(u.oro_historico)["nombre"], "oro_historico": u.oro_historico}
        for u in usuarios
    ]


# ---------- PERFIL / INVENTARIO ----------
@app.get("/perfil/{usuario_id}")
def perfil(usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    usuario = verificar_usuario(usuario_id, password, db)
    minerales = db.query(MineralInventario).filter_by(usuario_id=usuario_id).all()
    piezas = db.query(PiezaInstalada).filter_by(usuario_id=usuario_id).all()
    dispositivos = db.query(Rig).filter_by(usuario_id=usuario_id).all()
    grupos = db.query(RigGrupo).filter_by(usuario_id=usuario_id).all()

    def esp32_dict(r):
        return {"mac": r.mac, "nombre": r.nombre or r.mac, "activo": r.activo, "dias_electricidad": r.dias_electricidad_prepagados}

    rigs_agrupados = []
    for g in grupos:
        esp32_del_grupo = [esp32_dict(r) for r in dispositivos if r.rig_id == g.id]
        rigs_agrupados.append({"rig_id": g.id, "nombre": g.nombre, "esp32": esp32_del_grupo})

    sin_asignar = [esp32_dict(r) for r in dispositivos if r.rig_id is None]

    return {
        "usuario": usuario.nombre,
        "oro_saldo": usuario.oro_saldo,
        "nivel": calcular_nivel(usuario.oro_historico)["nombre"],
        "minerales": {m.mineral: m.cantidad for m in minerales},
        "piezas": [p.pieza_id for p in piezas],
        "rigs": rigs_agrupados,
        "esp32_sin_asignar": sin_asignar,
    }


# ---------- TRANSFERENCIA DIRECTA ENTRE USUARIOS (Oro + hasta 6 ítems) ----------
class ItemTransferencia(BaseModel):
    tipo: str      # "mineral" o "pieza"
    item_id: str
    cantidad: int


class TransferenciaRequest(BaseModel):
    usuario_id: str
    password: str
    destino_usuario_id: str
    oro: float = 0
    items: List[ItemTransferencia] = []


@app.post("/transferir")
def transferir(req: TransferenciaRequest, db: Session = Depends(get_db)):
    verificar_usuario(req.usuario_id, req.password, db)

    if req.usuario_id == req.destino_usuario_id:
        raise HTTPException(400, "No podés transferirte a vos mismo")

    destino = db.get(Usuario, req.destino_usuario_id)
    if not destino:
        raise HTTPException(404, "El usuario destino no existe")

    if len(req.items) > 6:
        raise HTTPException(400, "Máximo 6 ítems por transferencia")

    origen = db.get(Usuario, req.usuario_id)

    if req.oro < 0:
        raise HTTPException(400, "Cantidad de Oro inválida")
    if req.oro > 0 and origen.oro_saldo < req.oro:
        raise HTTPException(400, "No tenés suficiente Oro")

    # Validar inventario ANTES de mover nada (para que sea todo o nada)
    for item in req.items:
        if item.cantidad <= 0:
            raise HTTPException(400, f"Cantidad inválida para {item.item_id}")
        if item.tipo == "mineral":
            inv = db.query(MineralInventario).filter_by(usuario_id=req.usuario_id, mineral=item.item_id).first()
            if not inv or inv.cantidad < item.cantidad:
                raise HTTPException(400, f"No tenés suficiente {item.item_id}")
        elif item.tipo == "pieza":
            disponibles = db.query(PiezaInstalada).filter_by(usuario_id=req.usuario_id, pieza_id=item.item_id).count()
            if disponibles < item.cantidad:
                raise HTTPException(400, f"No tenés suficientes piezas {item.item_id}")
        else:
            raise HTTPException(400, f"Tipo de ítem inválido: {item.tipo}")

    # Ejecutar la transferencia completa
    if req.oro > 0:
        origen.oro_saldo -= req.oro
        destino.oro_saldo += req.oro

    for item in req.items:
        if item.tipo == "mineral":
            inv_origen = db.query(MineralInventario).filter_by(usuario_id=req.usuario_id, mineral=item.item_id).first()
            inv_origen.cantidad -= item.cantidad

            inv_destino = db.query(MineralInventario).filter_by(usuario_id=req.destino_usuario_id, mineral=item.item_id).first()
            if not inv_destino:
                inv_destino = MineralInventario(usuario_id=req.destino_usuario_id, mineral=item.item_id, cantidad=0)
                db.add(inv_destino)
            inv_destino.cantidad += item.cantidad
        elif item.tipo == "pieza":
            piezas_a_mover = db.query(PiezaInstalada).filter_by(usuario_id=req.usuario_id, pieza_id=item.item_id).limit(item.cantidad).all()
            for p in piezas_a_mover:
                p.usuario_id = req.destino_usuario_id

    db.commit()
    return {
        "status": "ok",
        "de": req.usuario_id,
        "para": req.destino_usuario_id,
        "oro_transferido": req.oro,
        "items_transferidos": [i.dict() for i in req.items],
    }


# ---------- INVENTARIO detallado (para armar los slots de transferencia) ----------
@app.get("/inventario/{usuario_id}")
def inventario(usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    usuario = verificar_usuario(usuario_id, password, db)
    minerales = db.query(MineralInventario).filter_by(usuario_id=usuario_id).all()
    piezas = db.query(PiezaInstalada).filter_by(usuario_id=usuario_id).all()

    piezas_agrupadas = {}
    for p in piezas:
        piezas_agrupadas[p.pieza_id] = piezas_agrupadas.get(p.pieza_id, 0) + 1

    return {
        "oro_saldo": usuario.oro_saldo,
        "minerales": {m.mineral: m.cantidad for m in minerales if m.cantidad > 0},
        "piezas": piezas_agrupadas,
    }


# ---------- EQUIPO: equipar una pieza del inventario en un slot de un rig ----------
@app.post("/rig/equipar_pieza")
def equipar_pieza(pieza_id: int, rig_id: str, usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)

    pieza = db.get(PiezaInstalada, pieza_id)
    if not pieza or pieza.usuario_id != usuario_id:
        raise HTTPException(404, "Pieza no encontrada")
    if pieza.rig_id is not None:
        raise HTTPException(400, "Esa pieza ya está equipada en otro rig — desequipala primero")

    grupo = db.query(RigGrupo).filter_by(id=rig_id, usuario_id=usuario_id).first()
    if not grupo:
        raise HTTPException(404, "Rig no encontrado")

    receta = RECETAS[pieza.pieza_id]
    ya_ocupado = db.query(PiezaInstalada).filter_by(usuario_id=usuario_id, rig_id=rig_id, slot=receta["slot"]).first()
    if ya_ocupado:
        raise HTTPException(400, f"El slot '{receta['slot']}' de ese rig ya tiene una pieza — desequipala primero")

    pieza.rig_id = rig_id
    db.commit()
    return {"status": "ok", "pieza_id": pieza.id, "slot": receta["slot"], "rig_id": rig_id}


# ---------- EQUIPO: desequipar una pieza (vuelve al inventario) ----------
@app.post("/rig/desequipar_pieza")
def desequipar_pieza(pieza_id: int, usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    pieza = db.get(PiezaInstalada, pieza_id)
    if not pieza or pieza.usuario_id != usuario_id:
        raise HTTPException(404, "Pieza no encontrada")
    pieza.rig_id = None
    db.commit()
    return {"status": "ok", "pieza_id": pieza.id}


# ---------- EQUIPO: reparar durabilidad (cuesta la mitad de los minerales originales) ----------
@app.post("/rig/reparar_pieza")
def reparar_pieza(pieza_id: int, usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    pieza = db.get(PiezaInstalada, pieza_id)
    if not pieza or pieza.usuario_id != usuario_id:
        raise HTTPException(404, "Pieza no encontrada")

    receta = RECETAS[pieza.pieza_id]
    if pieza.durabilidad_actual >= receta["durabilidad_max"]:
        raise HTTPException(400, "Esa pieza ya está al 100% de durabilidad")

    costo_reparacion = {m: max(1, cantidad // 2) for m, cantidad in receta["requiere"].items()}
    for mineral, cantidad in costo_reparacion.items():
        inv = db.query(MineralInventario).filter_by(usuario_id=usuario_id, mineral=mineral).first()
        if not inv or inv.cantidad < cantidad:
            raise HTTPException(400, f"Faltan {mineral} para reparar (necesitás {cantidad})")

    for mineral, cantidad in costo_reparacion.items():
        inv = db.query(MineralInventario).filter_by(usuario_id=usuario_id, mineral=mineral).first()
        inv.cantidad -= cantidad

    pieza.durabilidad_actual = receta["durabilidad_max"]
    db.commit()
    return {"status": "ok", "pieza_id": pieza.id, "durabilidad_actual": pieza.durabilidad_actual}


# ---------- EQUIPO: ver el estado de los 9 slots de un rig ----------
# ---------- EQUIPO: piezas sin equipar (para elegir cuál poner en un rig) ----------
@app.get("/inventario_piezas/{usuario_id}")
def piezas_sueltas(usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    piezas = db.query(PiezaInstalada).filter_by(usuario_id=usuario_id, rig_id=None).all()
    return [
        {
            "id": p.id, "pieza_id": p.pieza_id, "slot": p.slot,
            "durabilidad_actual": p.durabilidad_actual,
            "durabilidad_max": RECETAS[p.pieza_id]["durabilidad_max"],
            "buff_hashrate": RECETAS[p.pieza_id]["buff_hashrate"],
        }
        for p in piezas
    ]


@app.get("/rig/{rig_id}/equipo")
def ver_equipo_rig(rig_id: str, usuario_id: str, password: str = None, db: Session = Depends(get_db)):
    verificar_usuario(usuario_id, password, db)
    piezas = db.query(PiezaInstalada).filter_by(usuario_id=usuario_id, rig_id=rig_id).all()
    por_slot = {p.slot: p for p in piezas}

    resultado = []
    for slot in SLOTS_RIG:
        p = por_slot.get(slot)
        if p:
            receta = RECETAS[p.pieza_id]
            resultado.append({
                "slot": slot, "ocupado": True, "pieza_id": p.pieza_id,
                "durabilidad_actual": p.durabilidad_actual, "durabilidad_max": receta["durabilidad_max"],
                "buff_hashrate": receta["buff_hashrate"],
            })
        else:
            resultado.append({"slot": slot, "ocupado": False})

    completo = all(r["ocupado"] and r["durabilidad_actual"] > 0 for r in resultado)
    return {"rig_id": rig_id, "slots": resultado, "rig_completo": completo, "bonus_set": BONUS_RIG_COMPLETO if completo else 0}
