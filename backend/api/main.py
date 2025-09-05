"""main.py contiene el routing y la logica de los endpoints"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import sesion, engine
from models import FAQ, CategoriaFAQ, Comuna, Cupon, DetallePedido, Direccion, EstadoTicket, InventarioSucursal, MedioPago, Oferta, Pago, Pedido, Region, Sucursal, Ticket, Usuario, Base, Producto
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import crud
import schema

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

admin = Admin(flask_app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Usuario, sesion()))
admin.add_view(ModelView(Producto, sesion()))
admin.add_view(ModelView(Comuna,sesion()))
admin.add_view(ModelView(Region,sesion()))
admin.add_view(ModelView(Direccion,sesion()))
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
    usuarios: list[Usuario] = crud.get_users(dbs)
    return usuarios

@app.post('/api/v1/usuarios/')
async def post_user(user: schema.UserCreate, dbs: Session= Depends(get_db)):
    return crud.create_user(db=dbs, email=user.email, nombres=user.nombres, apellidos=user.apellidos, password=user.password)

@app.post('/api/v1/login/')
async def login(user: schema.UserLogin, dbs: Session = Depends(get_db))->bool:
    return crud.login_user(db=dbs, email=user.email, password=user.password)

##MIDDLEWARE PARA IMPLEMENTAR FLASK

app.mount('/admin', WSGIMiddleware(flask_app))