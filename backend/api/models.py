""""models.py incluye toda la información respecto a los modelos relacionales de la base de datos"""
from db import Base
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Numeric, Time, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(Base):
    __tablename__ = 'Usuario'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    password = Column(String(256), nullable=False)

    #relaciones
    pedidos = relationship("Pedido")
    direcciones = relationship('Direccion')
    tickets = relationship('Ticket')

    #metodos de verificacion

    def set_password(self, pas):
        self.password = generate_password_hash(pas)
    
    def check_password(self, pas):
        return check_password_hash(self.password, pas)

class Direccion(Base):
    __tablename__ = 'Direccion'
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('Usuario.id'))
    id_comuna = Column(Integer, ForeignKey('Comuna.id'))
    calle = Column(String(100), nullable=False)
    numero = Column(String(50), nullable=False)
    comentario = Column(Text, nullable=True, default='')
    
    #Relaciones
    pedidos = relationship("Pedido")

class Comuna(Base):
    __tablename__ = 'Comuna'
    id = Column(Integer, primary_key=True, index=True)
    id_region = Column(Integer, ForeignKey('Region.id'))
    nombre = Column(String(100), nullable=False)

    #relaciones
    direcciones = relationship('Direccion')
    sucursales = relationship('Sucursal')

class Region(Base):
    __tablename__ = 'Region'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)

    #relaciones
    comunas = relationship('Comuna')

class Producto(Base):
    __tablename__ = 'Producto'
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(12), nullable=False, index=True, unique=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Integer, nullable=False, default=0)
    added = Column(Date, nullable=False, default=date.today())
    ultima_modificacion = Column(Date, nullable=False, default=date.today())

    #Relaciones
    pedidos = relationship('DetallePedido',
                           back_populates='producto')
    sucursales = relationship('InventarioSucursal', back_populates='producto')

class Pedido(Base):
    __tablename__ = 'Pedido'
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('Usuario.id'))
    id_direccion = Column(Integer, ForeignKey('Direccion.id'), nullable=True)
    subtotal = Column(Integer, nullable=True, default=0)
    total = Column(Integer, nullable=True, default=0)

    #relaciones
    productos = relationship('DetallePedido',
                             back_populates='pedido')
    pagos = relationship('Pago')
    
class MedioPago(Base):
    __tablename__ = 'MedioPago'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True, default='')

    #relaciones
    pagos = relationship('Pago')

class Pago(Base):
    __tablename__ = 'Pago'
    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(ForeignKey('Pedido.id'))
    id_medio = Column(ForeignKey('MedioPago.id'))
    total = Column(Integer, nullable=False, default=0)

class Sucursal(Base):
    __tablename__ = 'Sucursal'
    id = Column(Integer, primary_key=True, index=True)
    id_comuna = Column(Integer, ForeignKey('Comuna.id'))
    direccion = Column(String(100), nullable=False)
    nombre = Column(String(100), nullable=False)
    latitude = Column(Numeric(precision=8, scale=6), nullable=False, default=0)
    longitude = Column(Numeric(precision=9, scale=6), nullable=False, default=0)
    telefono = Column(String(12), nullable=False)

    #Relaciones
    productos = relationship('InventarioSucursal', back_populates='sucursal')

class Ticket(Base):
    __tablename__ = 'Ticket'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    id_estado = Column(Integer, ForeignKey('EstadoTicket.id'))
    id_usuario = Column(Integer, ForeignKey('Usuario.id'))
    fecha_ingreso = Column(Date, nullable=False, default=date.today())
    resumen = Column(String(100), nullable=False)
    texto = Column(Text, nullable=False)
    ultima_modificacion = Column(Time, nullable=False, default=datetime.now())

class EstadoTicket(Base):
    __tablename__ = 'EstadoTicket'
    id = Column(Integer, primary_key=True, nullable=False)
    estado = Column(String(50), index=True, unique=True, nullable=False)
    descripcion = Column(Text, nullable=True, default='')

    #Relaciones
    tickets = relationship('Ticket')

class CategoriaFAQ(Base):
    __tablename__ = 'CategoriaFAQ'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)

    #Relaciones
    preguntas = relationship('FAQ')

class FAQ(Base):
    __tablename__ = 'FAQ'
    id = Column(Integer, primary_key=True, index=True)
    categoria_id = Column(Integer, ForeignKey('CategoriaFAQ.id'), nullable=False)
    pregunta = Column(String(100), nullable=False)
    resumen = Column(String(100), nullable=False)
    respuesta = Column(Text, nullable=False)

class Cupon(Base):
    __tablename__ = 'Cupon'
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(12), nullable=False)
    procentaje = Column(Integer, nullable=True)
    valor = Column(Integer, nullable=True)
    compra_minima = Column(Integer, nullable=True)
    usos_maximos = Column(Integer, nullable=False, default=0)
    usos_hechos = Column(Integer, nullable=False, default=0)
    vigente = Column(Boolean, nullable=False, default=True)

class Oferta(Base):
    __tablename__ = 'Oferta'
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=False)
    porcentaje = Column(Integer, nullable=True)
    valor = Column(Integer, nullable=True)
    fecha_inicio = Column(Date, nullable=False, default=date.today())
    fecha_fin = Column(Date, nullable=False, default=date.today())

#Tablas de asociacion

class DetallePedido(Base):
    __tablename__ = 'DetallePedido'
    pedido_id = Column(ForeignKey('Pedido.id'), primary_key=True)
    producto_id = Column(ForeignKey('Producto.id'), primary_key=True)

    #relaciones
    pedido = relationship('Pedido', back_populates='productos')
    producto = relationship('Producto', back_populates='pedidos')

class InventarioSucursal(Base):
    __tablename__ = 'InventarioSucursal'
    sucursal_id = Column(ForeignKey('Sucursal.id'), primary_key=True)
    producto_id = Column(ForeignKey('Producto.id'), primary_key=True)
    cantidad = Column(Integer, nullable=False, default=0)
    ultima_modificacion = Column(DateTime, nullable=False, default=datetime.now())

    #Relaciones
    sucursal = relationship('Sucursal', back_populates='productos')
    producto = relationship('Producto', back_populates='sucursales')
    