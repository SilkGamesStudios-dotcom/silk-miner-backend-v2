from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# En Render, DATABASE_URL viene seteada apuntando a Postgres (postgres://... o postgresql://...).
# Local/dev sin esa variable, sigue usando SQLite como hasta ahora.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./miner.db")
if DATABASE_URL.startswith("postgres://"):
    # SQLAlchemy moderno exige el prefijo "postgresql://", Render todavía entrega el viejo "postgres://"
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(String, primary_key=True)
    nombre = Column(String, unique=True)
    password = Column(String, nullable=True)
    wallet = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)
    oro_saldo = Column(Float, default=0)
    oro_historico = Column(Float, default=0)
    tickets_saldo = Column(Float, default=0)  # moneda de logro de los mini-juegos, canjeable en la tienda o tradeable en el mercado
    shares_hoy = Column(Integer, default=0)             # se resetea solo cuando cambia fecha_actividad
    fecha_actividad = Column(String, nullable=True)      # "YYYY-MM-DD" del último share minado
    misiones_reclamadas_hoy = Column(String, default="")  # ids de misión ya cobrados hoy, separados por coma

    # ---- Cupón de subsidio (fidelización, ver reglas.CUPON_SUBSIDIO_*) ----
    cupon_activo = Column(Boolean, default=False)
    cupon_usado = Column(Boolean, default=True)  # True por default para que un usuario nuevo no "tenga" cupón
    cupon_porcentaje = Column(Integer, default=0)
    cupon_motivo = Column(String, nullable=True)
    cupon_generado_en = Column(DateTime, nullable=True)
    cupon_expira_en = Column(DateTime, nullable=True)

    # ---- Tope semanal de electricidad canjeada con tickets (regla de oro, ver reglas.py) ----
    electricidad_tickets_semana_inicio = Column(DateTime, nullable=True)
    electricidad_tickets_dias_semana = Column(Integer, default=0)  # días de electricidad ya canjeados con tickets esta semana

    # ---- Racha de login diario (recompensa por entrar seguido, ver reglas.RECOMPENSAS_RACHA) ----
    racha_dia_actual = Column(Integer, default=1)          # próximo día de racha a reclamar (1-7)
    racha_ultimo_reclamo = Column(String, nullable=True)    # "YYYY-MM-DD" del último reclamo (evita reclamar 2 veces el mismo día)


class RigGrupo(Base):
    __tablename__ = "rig_grupos"
    id = Column(String, primary_key=True)  # ej: "1", "2" (por usuario)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    nombre = Column(String, nullable=True)
    vip_hasta = Column(DateTime, nullable=True)  # si es futuro respecto a ahora, el rig tiene VIP activo


class Rig(Base):
    __tablename__ = "rigs"
    mac = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    rig_id = Column(String, nullable=True)  # a qué RigGrupo pertenece (null = sin asignar)
    nombre = Column(String, nullable=True)  # nombre personalizado, ej. "Rig Hércules"
    activo = Column(Boolean, default=True)
    dias_electricidad_prepagados = Column(Integer, default=1)  # 1 día gratis al registrar
    fecha_ultimo_descuento = Column(DateTime, default=datetime.utcnow)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    experiencia = Column(Float, default=0)  # XP propia del dispositivo (ESP32 o celular)


class MineralInventario(Base):
    __tablename__ = "minerales_inventario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    mineral = Column(String)
    cantidad = Column(Integer, default=0)


class PiezaInstalada(Base):
    __tablename__ = "piezas_instaladas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    pieza_id = Column(String)
    slot = Column(String, nullable=True)          # cpu, refrigeracion, fuente_poder, etc.
    rig_id = Column(String, nullable=True)         # a qué RigGrupo está equipada (null = en inventario, sin equipar)
    durabilidad_actual = Column(Integer, default=0)
    fecha = Column(DateTime, default=datetime.utcnow)


class CertificadoInstalado(Base):
    __tablename__ = "certificados_instalados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    certificado_id = Column(String)             # ej: "certificado_bronce"
    origen_mac = Column(String, nullable=True)   # qué dispositivo lo generó (evita otorgarlo 2 veces al mismo)
    rig_id = Column(String, nullable=True)       # a qué RigGrupo está equipado (null = en inventario, sin equipar)
    fecha = Column(DateTime, default=datetime.utcnow)


class LogroObtenido(Base):
    __tablename__ = "logros_obtenidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    logro_id = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)


class AnuncioGlobal(Base):
    __tablename__ = "anuncios_globales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)


class MensajePrivado(Base):
    __tablename__ = "mensajes_privados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    de_usuario_id = Column(String, ForeignKey("usuarios.id"))
    para_usuario_id = Column(String, ForeignKey("usuarios.id"))
    texto = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)
    leido = Column(Boolean, default=False)


class MensajeGlobal(Base):
    __tablename__ = "mensajes_globales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    texto = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)


class EventoActivo(Base):
    __tablename__ = "evento_activo"
    id = Column(Integer, primary_key=True)  # siempre una sola fila, id=1
    nombre = Column(String, nullable=True)
    buff_drop_extra = Column(Float, default=0)
    activo_hasta = Column(DateTime, nullable=True)


class OrdenElectricidad(Base):
    __tablename__ = "ordenes_electricidad"
    id = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    paquete_id = Column(String)
    cantidad_rigs = Column(Integer)
    dias_por_rig = Column(Integer)
    monto_usdt = Column(Float)
    comprobante_path = Column(String, nullable=True)
    estado = Column(String, default="pendiente_revision")  # pendiente_revision / aprobada / rechazada
    cupon_aplicado = Column(Boolean, default=False)  # True si esta orden ya usó el cupón de subsidio
    fecha = Column(DateTime, default=datetime.utcnow)
    fecha_revision = Column(DateTime, nullable=True)


class OrdenVip(Base):
    __tablename__ = "ordenes_vip"
    id = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    rig_id = Column(String)  # RigGrupo.id al que se le aplica el VIP
    dias = Column(Integer)
    monto_usdt = Column(Float)
    comprobante_path = Column(String, nullable=True)
    estado = Column(String, default="pendiente_revision")  # pendiente_revision / aprobada / rechazada
    fecha = Column(DateTime, default=datetime.utcnow)
    fecha_revision = Column(DateTime, nullable=True)


class OrdenRig(Base):
    """Orden de pago en USDT para abrir un rig nuevo (2do en adelante — el 1ro es gratis).
    Mismo patrón manual que OrdenElectricidad: se genera la orden, el usuario transfiere y sube
    comprobante, un admin la aprueba y recién ahí se crea el RigGrupo de verdad."""
    __tablename__ = "ordenes_rig"
    id = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    numero_rig = Column(Integer)          # qué número de rig es (2, 3, 4...)
    mac_pendiente = Column(String, nullable=True)  # ESP32 que se le va a asignar al aprobarse (opcional)
    monto_usdt = Column(Float)
    comprobante_path = Column(String, nullable=True)
    estado = Column(String, default="pendiente_revision")  # pendiente_revision / aprobada / rechazada
    cupon_aplicado = Column(Boolean, default=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    fecha_revision = Column(DateTime, nullable=True)


class PartidaMinijuego(Base):
    """Registro de cada partida terminada de un mini-juego (Tetris, etc.) — sirve
    para el límite diario anti-farmeo y para auditar oro/tickets entregados."""
    __tablename__ = "partidas_minijuego"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    juego = Column(String)                       # "tetris", "asteroides", etc.
    nivel_alcanzado = Column(Integer, default=0)
    duracion_segundos = Column(Integer, default=0)
    oro_ganado = Column(Float, default=0)
    tickets_ganados = Column(Integer, default=0)
    fecha = Column(DateTime, default=datetime.utcnow)


class OfertaCompletada(Base):
    """Registro de cada postback de CPX Research procesado (anti-duplicados + soporte de reversión por fraude)."""
    __tablename__ = "ofertas_completadas"
    trans_id = Column(String, primary_key=True)   # trans_id que manda CPX, único por oferta completada
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    offer_id = Column(String, nullable=True)
    monto_usdt = Column(Float, default=0)
    rigs_recargados = Column(String, default="")   # macs de los ESP32 que recibieron los días, separados por coma (para poder revertir)
    dias_por_rig = Column(Integer, default=0)
    estado = Column(String, default="acreditada")   # acreditada / revertida
    fecha = Column(DateTime, default=datetime.utcnow)
    fecha_reversion = Column(DateTime, nullable=True)


class OrdenMercado(Base):
    __tablename__ = "ordenes_mercado"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String)
    tipo_item = Column(String)
    item_id = Column(String)
    cantidad = Column(Integer)
    precio_oro = Column(Float)
    estado = Column(String, default="abierta")
    fecha = Column(DateTime, default=datetime.utcnow)


def _migrar_columnas_nuevas():
    """Si la base ya existía de antes (deploy previo persistido), le agrega las
    columnas nuevas sin borrar nada. Si la base es nueva, create_all ya las trae
    bien puestas y esto no encuentra nada para hacer.

    Usa el inspector de SQLAlchemy en vez de "PRAGMA table_info" (SQLite-only) para
    que la migración funcione igual en Postgres (Render) que en SQLite (local/dev)."""
    columnas_nuevas = {
        "rigs": [("experiencia", "FLOAT DEFAULT 0")],
        "rig_grupos": [("vip_hasta", "TIMESTAMP")],
        "usuarios": [
            ("shares_hoy", "INTEGER DEFAULT 0"),
            ("fecha_actividad", "VARCHAR"),
            ("misiones_reclamadas_hoy", "VARCHAR DEFAULT ''"),
            ("whatsapp", "VARCHAR"),
            ("tickets_saldo", "FLOAT DEFAULT 0"),
            ("cupon_activo", "BOOLEAN DEFAULT FALSE"),
            ("cupon_usado", "BOOLEAN DEFAULT TRUE"),
            ("cupon_porcentaje", "INTEGER DEFAULT 0"),
            ("cupon_motivo", "VARCHAR"),
            ("cupon_generado_en", "TIMESTAMP"),
            ("cupon_expira_en", "TIMESTAMP"),
            ("electricidad_tickets_semana_inicio", "TIMESTAMP"),
            ("electricidad_tickets_dias_semana", "INTEGER DEFAULT 0"),
            ("racha_dia_actual", "INTEGER DEFAULT 1"),
            ("racha_ultimo_reclamo", "VARCHAR"),
        ],
        "ordenes_electricidad": [("cupon_aplicado", "BOOLEAN DEFAULT FALSE")],
    }
    inspector = inspect(engine)
    tablas_existentes = set(inspector.get_table_names())

    with engine.connect() as conn:
        for tabla, columnas in columnas_nuevas.items():
            if tabla not in tablas_existentes:
                continue  # tabla nueva (ej. ordenes_rig): ya la crea create_all(), nada que migrar
            existentes = {col["name"] for col in inspector.get_columns(tabla)}
            for nombre, tipo_sql in columnas:
                if nombre not in existentes:
                    conn.exec_driver_sql(f"ALTER TABLE {tabla} ADD COLUMN {nombre} {tipo_sql}")
                    print(f"[migracion] agregada columna {tabla}.{nombre}")
        conn.commit()

def init_db():
    Base.metadata.create_all(bind=engine)
    _migrar_columnas_nuevas()
