"""main.py contiene el routing y la logica de los endpoints"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import sesion, engine
from models import FAQ, CategoriaFAQ, Comuna, Cupon, DetallePedido, Direccion, EstadoTicket, InventarioSucursal, MedioPago, Oferta, Pago, Pedido, Region, Sucursal, Ticket, Usuario, Base, Producto, Rol
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import crud
import schema
import fadmin_models
import models

Base.metadata.create_all(bind=engine)

def get_db():
    db = sesion()
    try:
        yield db
    finally:
        db.close()

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aurora.db'
flask_app.secret_key = 'super secret key'
fdb = SQLAlchemy(flask_app)

admin = Admin(flask_app, name='TiendaAurora', template_mode='bootstrap3')
admin.add_view(ModelView(Usuario, sesion()))
admin.add_view(ModelView(Producto, sesion()))
admin.add_view(fadmin_models.ComunaAdmin(Comuna,sesion()))
admin.add_view(ModelView(Region,sesion()))
admin.add_view(fadmin_models.DireccionAdmin(Direccion,sesion()))
admin.add_view(ModelView(Pedido, sesion()))
admin.add_view(ModelView(MedioPago,sesion()))
admin.add_view(ModelView(Pago,sesion()))
admin.add_view(ModelView(Sucursal,sesion()))
admin.add_view(ModelView(Ticket,sesion()))
admin.add_view(ModelView(EstadoTicket,sesion()))
admin.add_view(ModelView(CategoriaFAQ,sesion()))
admin.add_view(ModelView(FAQ,sesion()))
admin.add_view(ModelView(Cupon,sesion()))
admin.add_view(ModelView(Oferta,sesion()))
admin.add_view(ModelView(DetallePedido,sesion()))
admin.add_view(ModelView(InventarioSucursal,sesion()))
admin.add_view(ModelView(Rol, sesion()))

@flask_app.route('/')
def flask_main():
    return 'hello world'

app = FastAPI()

#configuracion de CORS

app.add_middleware(CORSMiddleware, 
                   allow_origins=['*'], 
                   allow_credentials=True, 
                   allow_methods=["*"],
                   allow_headers=["*"],)

#Endpoints de usuario
#Todos se encuentran en /api/v1/usuarios/...

@app.get('/api/v1/usuarios/{id}')
async def get_user(id: int, dbs:SQLAlchemy = Depends(get_db)):
    user: Usuario = crud.get_user(dbs, id)
    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return user

@app.get('/api/v1/usuarios/')
async def get_users(dbs:Session = Depends(get_db)):
    '''Recupera la lista completa de usuarios
    ADVERTENCIA: Temporalmente devuelve tambien el hash del password, quedando este visible
    To-do: Crear la clase usuario de respuesta y serializarla en la lista.
    '''
    usuarios: list[Usuario] = crud.get_users(dbs)
    return usuarios

@app.post('/api/v1/usuarios/')
async def post_user(user: schema.UserCreate, dbs: Session= Depends(get_db))->schema.NewUser:
    '''
    Dada un diccionario json con los siguientes parametros:
    {
    email,
    nombres,
    apellidos,
    password,
    }
    Intenta crear el usuario en la base de datos y retornar la informacion del usuario
    ADVERTENCIA: Muestra el hash del password ingresado
    TO-DO: Crear clase de pydantic de respuesta. Añadir excepcion en caso de no lograr crear usuario.
    '''
    try:
       user = crud.create_user(db=dbs, email=user.email, nombres=user.nombres, apellidos=user.apellidos, password=user.password)
       return schema.NewUser(status=True, mensaje='Usuario creado')
    except:  # noqa: E722
        return schema.NewUser(status=False, mensaje='No se pudo crear el usuario')


@app.post('/api/v1/login/')
async def login(user: schema.UserLogin, dbs: Session = Depends(get_db))->schema.UserLoginData:
    '''
    Dado un diccionario json con los siguientes datos:
    {
    email,
    password,
    }

    Responde con un diccionario con los datos
    {
    id,
    token,
    mensaje
    }
    Verifica si el usuario existe en la base de datos y si su password corresponde.

    Si el usuario no existe o el password no corresponde, responde con id 0, sin token y un mensaje de Usuario o Contraseña Invalido.
    De otro modo devuelve el id del usuario y token, para ser almacenados en el storage local.
    '''
    try:
        if crud.login_user(db=dbs, email=user.email, password=user.password):
            usuario = crud.return_login_info(db=dbs, email=user.email)
            if usuario:
                return schema.UserLoginData(id=usuario.id, token='EsteEsUnTokenValido')
            else:
                return schema.UserLoginData(id=0, mensaje='Usuario o contraseña invalido')
    except:  # noqa: E722
        return schema.UserLoginData(id=0, mensaje='Usuario o contraseña invalido')
    
@app.post('/api/test/venta')
async def procesar_venta(venta: schema.InputVenta, dbs: Session = Depends(get_db)):
    cantidades = [p.cantidad for p in venta.productos]
    identificadores = [p.id for p in venta.productos]
    productos_buscados = dbs.query(models.InventarioSucursal, models.Producto).filter(
        models.Producto.id.in_(identificadores)).filter(
            models.InventarioSucursal.producto_id == models.Producto.id
        ).filter(
            models.InventarioSucursal.sucursal_id == 1
        ).all()
    pedido = models.Pedido(id_usuario = venta.user_id, subtotal=0, total=0)
    dbs.add(pedido)
    dbs.commit()
    dbs.refresh(pedido)

    for producto in productos_buscados:
        p = schema.Producto(id=producto[1].id, 
                            cantidad=producto[0].cantidad, 
                            precio=producto[1].precio)
        if p.cantidad < cantidades[identificadores.index(p.id)]:
            return False
        o = dbs.query(models.InventarioSucursal).filter(
            models.InventarioSucursal.producto_id == p.id).filter(
                models.InventarioSucursal.sucursal_id == 1
            ).first()
        o.cantidad -= p.cantidad
        pedido.total += p.precio * p.cantidad
        dbs.add(models.DetallePedido(pedido_id=pedido.id, producto_id=p.id))
        dbs.commit()
        dbs.refresh(pedido)

    return {'pedido': pedido}

##MIDDLEWARE PARA IMPLEMENTAR FLASK

app.mount('/admin', WSGIMiddleware(flask_app))