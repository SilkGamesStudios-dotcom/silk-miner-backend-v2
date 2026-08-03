from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///./miner.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(String, primary_key=True)
    nombre = Column(String, unique=True)
    password = Column(String, nullable=True)
    wallet = Column(String, nullable=True)
    oro_saldo = Column(Float, default=0)
    oro_historico = Column(Float, default=0)


class RigGrupo(Base):
    __tablename__ = "rig_grupos"
    id = Column(String, primary_key=True)  # ej: "1", "2" (por usuario)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    nombre = Column(String, nullable=True)


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
    fecha = Column(DateTime, default=datetime.utcnow)


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
    fecha = Column(DateTime, default=datetime.utcnow)
    fecha_revision = Column(DateTime, nullable=True)


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


def init_db():
    Base.metadata.create_all(bind=engine)
