import hashlib, random, uuid, json, os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

from models import SessionLocal, init_db, Usuario, Rig, MineralInventario, PiezaInstalada, OrdenMercado, OrdenElectricidad
from reglas import MINERALES, RECETAS, DIFICULTAD_DISPOSITIVO, RECOMPENSA_POR_SHARE, META_ORO_SEMANAL, COSTO_DIARIO_USDT, ROTACION_JOB_SEGUNDOS, PAQUETES_ELECTRICIDAD, calcular_nivel

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "SilkAdmin41")

def verificar_admin(x_admin_password: str = Header(None)):
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(401, "No autorizado")
    return True

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
def register_rig(mac: str, usuario_id: str, nombre: str = None, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        usuario = Usuario(id=usuario_id, nombre=nombre or usuario_id, oro_saldo=0, oro_historico=0)
        db.add(usuario)

    if db.get(Rig, mac):
        raise HTTPException(400, "MAC ya registrada")

    rig = Rig(mac=mac, usuario_id=usuario_id, activo=True, dias_electricidad_prepagados=1)
    db.add(rig)
    db.commit()
    return {"status": "registrado", "mac": mac}


@app.post("/rig/renombrar")
def renombrar_rig(mac: str, usuario_id: str, nuevo_nombre: str, db: Session = Depends(get_db)):
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
    buff = sum(
        RECETAS[p.pieza_id]["buff_hashrate"]
        for p in db.query(PiezaInstalada).filter_by(usuario_id=usuario.id).all()
    )
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
def solicitar_paquete(usuario_id: str, paquete_id: str, db: Session = Depends(get_db)):
    if paquete_id not in PAQUETES_ELECTRICIDAD:
        raise HTTPException(400, "Paquete inválido")
    paquete = PAQUETES_ELECTRICIDAD[paquete_id]

    rigs = db.query(Rig).filter_by(usuario_id=usuario_id, activo=True).all()
    if not rigs:
        raise HTTPException(400, "No tienes rigs activos")

    costo_total_usdt = round(paquete["precio_usdt_por_esp32"] * len(rigs), 2)
    orden_id = f"elec_{usuario_id}_{uuid.uuid4().hex[:10]}"

    orden = OrdenElectricidad(
        id=orden_id, usuario_id=usuario_id, paquete_id=paquete_id,
        cantidad_rigs=len(rigs), dias_por_rig=paquete["dias"],
        monto_usdt=costo_total_usdt, estado="pendiente_revision",
    )
    db.add(orden)
    db.commit()

    return {
        "orden_id": orden_id,
        "binance_pay_id": BINANCE_PAY_ID,
        "monto_a_pagar_usdt": costo_total_usdt,
        "rigs_afectados": len(rigs),
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

    rigs = db.query(Rig).filter_by(usuario_id=orden.usuario_id, activo=True).all()
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
def craftear(usuario_id: str, receta_id: str, db: Session = Depends(get_db)):
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

    db.add(PiezaInstalada(usuario_id=usuario_id, pieza_id=receta_id))
    db.commit()
    return {"status": "ok", "pieza": receta_id, "buff": receta["buff_hashrate"]}


# ---------- MERCADO ----------
@app.post("/mercado/publicar")
def publicar_orden(usuario_id: str, tipo_item: str, item_id: str, cantidad: int, precio_oro: float, db: Session = Depends(get_db)):
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
def comprar_orden(usuario_id: str, orden_id: int, db: Session = Depends(get_db)):
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
def perfil(usuario_id: str, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(404, "Usuario no existe")
    minerales = db.query(MineralInventario).filter_by(usuario_id=usuario_id).all()
    piezas = db.query(PiezaInstalada).filter_by(usuario_id=usuario_id).all()
    rigs = db.query(Rig).filter_by(usuario_id=usuario_id).all()
    return {
        "usuario": usuario.nombre,
        "oro_saldo": usuario.oro_saldo,
        "nivel": calcular_nivel(usuario.oro_historico)["nombre"],
        "minerales": {m.mineral: m.cantidad for m in minerales},
        "piezas": [p.pieza_id for p in piezas],
        "rigs": [{"mac": r.mac, "nombre": r.nombre or r.mac, "activo": r.activo, "dias_electricidad": r.dias_electricidad_prepagados} for r in rigs],
    }
