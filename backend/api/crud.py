""""crud.py contiene la logica de las operaciones CRUD del backend, para cada uno de los modelos."""
from sqlalchemy.orm import Session
from models import FAQ, CategoriaFAQ, Comuna, Direccion, InventarioSucursal, MedioPago, Pago, Region, Sucursal, Usuario, Producto, Pedido, DetallePedido
from datetime import date

#Funciones de usuario
def get_user(db, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_users(db:Session):
    return db.query(Usuario).all()

def create_user(db:Session, email: str, nombres: str, apellidos: str, password:str):
    usuario = Usuario(email=email, nombres=nombres, apellidos=apellidos)
    usuario.set_password(password)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def login_user(db:Session, email:str, password: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    return usuario.check_password(password)

#Funciones de Producto
def get_product_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

def get_product_sku(db: Session, sku: str):
    return db.query(Producto).filter(Producto.sku == sku).first()

def get_products(db: Session):
    return db.query(Producto).all()

def create_product(db:Session, sku: str, nombre:str, descripcion: str,
                   precio: int):
    producto = Producto(sku=sku, nombre=nombre, descripcion=descripcion, precio=precio)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

def update_product(db: Session, id: int, nombre: str, descripcion: str,
                   precio: int, sku: str):
    producto = db.query(Producto).filter(Producto.id==id).first()
    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.sku = sku
    producto.precio = precio
    producto.ultima_modificacion = date.today()
    db.commit()
    db.refresh(producto)
    return producto

def update_product_by_sku(db: Session, nombre: str, sku: str, descripcion: str, precio: int):
    producto = db.query(Producto).filter(Producto.sku == sku).first()
    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.precio = precio
    producto.ultima_modificacion = date.today()
    db.commit()
    db.refresh(producto)
    return producto

#Funciones de Pedido

def post_pedido(db: Session, user_id: int):
    pedido = Pedido(id_usuario = user_id)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido

def get_pedidos(db: Session):
    return db.query(Pedido).all()

def get_pedido(db: Session, id: int):
    pedido = db.query(Pedido).filter(Pedido.id==id).first()
    return pedido

#Funciones de detalle del pedido

def add_product_to_pedido(db: Session, producto_id: int, pedido_id: int):
    producto_pedido = DetallePedido(pedido_id=pedido_id, producto_id=producto_id)
    db.add(producto_pedido)
    db.commit()
    db.refresh(producto_pedido)
    return producto_pedido

def remove_product_to_pedido(db: Session, producto_id: int, pedido_id: int):
    producto_pedido = db.query(DetallePedido).filter(pedido_id==pedido_id, producto_id==producto_id).first()
    if producto_pedido is None:
        return {'Error: No encontrado'}
    db.delete(producto_pedido)
    db.commit()
    return {'Producto eliminado'}

#Funciones de Region

def add_region(db: Session, nombre_region: str):
    region = Region(nombre=nombre_region)
    db.add(region)
    db.commit()
    db.refresh(region)
    return region

def remover_region(db: Session, id_region: str):
    region = db.query(Region).filter(Region.id == id_region).first()
    if region is None:
        return {'Error: No encontrado'}
    db.delete(region)
    db.commit()
    return {'Region eliminada'}

def listar_regiones(db: Session):
    return db.query(Region).all()

#Funciones de comuna

def add_comuna(db: Session, nombre_comuna: str, id_region: int):
    comuna = Comuna(nombre=nombre_comuna, id_region=id_region)
    db.add(comuna)
    db.commit()
    db.refresh(comuna)
    return comuna

def remover_comuna(db: Session, id_comuna: int):
    comuna = db.query(Comuna).filter(Comuna.id ==id_comuna).first()
    if comuna is None:
        return {'Error: No encontrado'}
    db.delete(comuna)
    db.commit()
    return {'Comuna eliminada'}

def listar_comunas(db: Session):
    return db.query(Comuna).all()

#Funciones de direccion

def add_direccion(db: Session, id_usuario: int, id_comuna: int, calle: str,
                  numero: str):
    direccion = Direccion(id_comuna=id_comuna, id_usuario=id_usuario,
                          calle=calle, numero=numero)
    db.add(direccion)
    db.commit()
    db.refresh(direccion)
    return direccion

def remover_direccion(db: Session, id_direccion: int):
    direccion = db.query(Direccion).filter(Direccion.id == id_direccion).first()
    if direccion is None:
        return {'Error: No encontrado'}
    db.delete(direccion)
    db.commit()
    return {'Comuna eliminada'}

def editar_direccion(db:Session, id_direccion:int, id_comuna: int, calle: str,
                     numero: str, comentario: str = ''):
    #Enfoque actual es añadir, eliminar, listar
    pass

def listar_direcciones(db:Session):
    return db.query(Direccion).all()

def listar_direcciones_por_usuario(db: Session, id_usuario: int):
    return db.query(Direccion).filter(Direccion.id_usuario == id_usuario).all()

#Funciones de Sucursal

def add_sucursal(db: Session, id_comuna: int, direccion: str, nombre: str,
                 longitude: float, latitude: float, telefono: str):
    sucursal = Sucursal(id_comuna=id_comuna, direccion=direccion,
                        nombre=nombre, longitude=longitude, latitude=latitude,
                        telefono=telefono)
    db.add(sucursal)
    db.commit()
    db.refresh(sucursal)
    return sucursal

def remover_sucursal(db: Session, id_sucursal: int):
    sucursal = db.query(Sucursal).filter(Sucursal.id == id_sucursal).first()
    if sucursal is None:
        return {'Error: No encontrado'}
    db.delete(sucursal)
    db.commit()
    return {'Eliminado'}

def editar_sucursal(db: Session, id_sucursal: int, direccion: str, nombre: str,
                    latitude: float, longitude: float, telefono: str):
    pass

def listar_sucursales(db: Session):
    return db.query(Sucursal).all()

#Funciones de inventario

def annadir_inventario(db: Session, sucursal_id: int, producto_id: int, 
                       cantidad: int):
    inventario = InventarioSucursal(sucursal_id=sucursal_id, producto_id=producto_id, cantidad=cantidad)
    db.add(inventario)
    db.commit()
    db.refresh(inventario)
    return inventario

def remover_inventario(db: Session, sucursal_id: int, producto_id: int):
    inventario = db.query(InventarioSucursal).filter(InventarioSucursal.sucursal_id == sucursal_id, 
                                                     InventarioSucursal.producto_id==producto_id).first()
    if inventario is None:
        return {'Error: No encontrado'}
    db.delete(inventario)
    db.commit()
    return {'Eliminado'}

def editar_inventario(db: Session, id_sucursal: int, id_producto: int, cantidad: int):
    pass

def listar_inventario(db: Session):
    return db.query(InventarioSucursal).all()

def listar_inventario_sucursal(db: Session, sucursal_id: int):
    return db.query(InventarioSucursal).filter(InventarioSucursal.sucursal_id == sucursal_id).all()

#Funciones del medio de pago

def add_medio_pago(db: Session, nombre: str):
    medio = MedioPago(nombre=nombre)
    db.add(medio)
    db.commit()
    db.refresh(medio)
    return medio

def remover_medio_pago(db:Session, id: int):
    medio = db.query(MedioPago).filter(MedioPago.id==id).first()
    if medio is None:
        return {'Error: No encontrado'}
    db.delete(medio)
    db.commit()
    return {'Eliminado'}

def listar_medios(db:Session):
    return db.query(MedioPago).all()

#Funciones del Pago

def crear_pago(db:Session, id_pedido: int, id_medio: int, total:int):
    pago = Pago(id_pedido = id_pedido, id_medio = id_medio, total=total)
    db.add(pago)
    db.commit()
    db.refresh(pago)
    return pago

def remover_pago(db: Session, id: int):
    pago = db.query(Pago).filter(Pago.id==id).first()
    if pago is None:
        return {'No encontrado'}
    db.delete(pago)
    db.commit()
    return {'Eliminado'}

def listar_pagos(db:Session):
    return db.query(Pago).all()

#Funciones asociadas a los FAQ

def crear_categoria_faq(db: Session, nombre: str):
    categoria = CategoriaFAQ(nombre = nombre)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

def remover_categoria_faq(db: Session, id: int):
    categoria = db.query(CategoriaFAQ).filter(CategoriaFAQ.id==id).first()
    if categoria is None:
        return {'No encontrado'}
    db.delete(categoria)
    db.commit()
    return {'Eliminado'}

def listar_categorias(db: Session):
    return db.query(CategoriaFAQ).all()

def crear_faq(db: Session, categoria_id:int, pregunta: str,
               resumen: str, respuesta:str):
    faq = FAQ(categoria_id=categoria_id, pregunta=pregunta, 
              resumen=resumen, respuesta=respuesta)
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq

def listar_faq(db:Session):
    return db.query(FAQ).all()

def remover_faq(db:Session, id: int):
    faq = db.query(FAQ).filter(FAQ.id==id).first()
    if faq is None:
        return {'No encontrado'}
    db.delete(faq)
    db.commit()
    return {'Eliminado'}