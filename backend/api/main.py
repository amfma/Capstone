"""main.py contiene el routing y la logica de los endpoints"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import sesion, engine
from models import Usuario, Base, Producto
import crud

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = sesion()
    try:
        yield db
    finally:
        db.close()

#Endpoints de usuario
#Todos se encuentran en /api/v1/usuarios/...

@app.get('/api/v1/usuarios/{id}')
async def get_user(id: int, dbs: Session = Depends(get_db)):
    user: Usuario = crud.get_user(dbs, id)
    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return user

@app.get('/api/v1/usuarios/')
async def get_users(dbs:Session = Depends(get_db)):
    usuarios: list[Usuario] = crud.get_users(dbs)
    return usuarios

@app.post('/api/v1/usuarios/')
async def post_user(email: str, nombres:str, apellidos: str, 
                    password:str, dbs: Session= Depends(get_db)):
    return crud.create_user(db=dbs, email=email, nombres=nombres, apellidos=apellidos, password=password)

#Endpoints de producto
#Todos se encuentran en /api/v1/productos/...

@app.get('/api/v1/productos/all')
async def get_productos(dbs: Session = Depends(get_db)):
    productos: list[Producto] = crud.get_products(db=dbs)
    return productos

@app.get('/api/v1/productos/{id}')
async def get_product_by_id(id: int, dbs: Session= Depends(get_db)):
    producto: Producto = crud.get_product_id(db=dbs, producto_id=id)
    if producto is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    return producto

@app.get('/api/v1/productos/')
async def get_product_by_sku(sku: str, dbs: Session = Depends(get_db)):
    producto: Producto = crud.get_product_sku(db=dbs, sku=sku)
    if producto is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    return producto

@app.post('/api/v1/productos/')
async def post_product(sku: str, nombre: str, precio:int, 
                       descripcion:str = '', dbs: Session = Depends(get_db)):
    return crud.create_product(db=dbs, sku=sku, nombre=nombre, descripcion=descripcion, precio=precio)

@app.put('/api/v1/productos/{id}')
async def update_product_by_id(id: int, sku: str, precio: int, nombre: str, descripcion: str= '',
                      dbs: Session = Depends(get_db)):
    producto: Producto = crud.update_product(id=id, sku=sku, nombre=nombre, descripcion=descripcion, precio=precio, db=dbs)
    if producto is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    return producto

@app.put("/api/v1/productos/")
async def update_product_by_sku(sku:str, precio:int, nombre: str, descripcion: str='',
                                dbs: Session = Depends(get_db)):
    producto: Producto = crud.update_product_by_sku(sku=sku, nombre=nombre,
                                                    descripcion=descripcion, precio=precio, db=dbs)
    if producto is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    return producto

#Endpoints del pedido

@app.post('/api/v1/pedidos/')
async def post_pedido(user_id: int, dbs: Session = Depends(get_db)):
    return crud.post_pedido(user_id=user_id, db=dbs)

@app.get('/api/v1/pedidos/{pedido_id}')
async def get_pedido(pedido_id: int, dbs:Session = Depends(get_db)):
    pedido = crud.get_pedido(db=dbs, id=pedido_id)
    if pedido is None:
        raise HTTPException(404, 'Pedido no encontrado')
    return pedido

@app.get('/api/v1/pedidos/')
async def get_pedidos(dbs: Session = Depends(get_db)):
    pedidos = crud.get_pedidos(dbs)
    return pedidos

@app.post('/api/v1/detalle_pedido/')
async def annadir_producto_en_pedido(producto_id: int, pedido_id: int, dbs: Session = Depends(get_db)):
    return crud.add_product_to_pedido(db=dbs, producto_id=producto_id, pedido_id=pedido_id)

@app.delete('/api/v1/detalle_pedido/')
async def remover_producto_de_pedido(producto_id: int, pedido_id: int, dbs: Session = Depends(get_db)):
    return crud.remove_product_to_pedido(db=dbs, producto_id=producto_id, pedido_id=pedido_id)

#Endpoints de region, comuna y direccion

@app.post('/api/v1/regiones/')
async def post_region(nombre: str, dbs: Session = Depends(get_db)):
    return crud.add_region(db=dbs, nombre_region=nombre)

@app.delete('/api/v1/regiones/{id}')
async def delete_region(id: int, dbs: Session = Depends(get_db)):
    return crud.remover_region(db=dbs, id_region=id)

@app.get('/api/v1/regiones/')
async def get_regiones(dbs: Session = Depends(get_db)):
    return crud.listar_regiones(db=dbs)

@app.post('/api/v1/comunas')
async def post_comuna(nombre: str, id_region: int, dbs: Session = Depends(get_db)):
    return crud.add_comuna(db=dbs, nombre_comuna=nombre, id_region=id_region)

@app.delete('/api/v1/comunas/{id}')
async def delete_comuna(id:int, dbs: Session = Depends(get_db)):
    return crud.remover_comuna(db=dbs, id_comuna=id)

@app.get('/api/v1/comunas/')
async def get_comunas(dbs: Session = Depends(get_db)):
    return crud.listar_comunas(db=dbs)

@app.post('/api/v1/direcciones/')
async def post_direccion(id_usuario: int, id_comuna: int,
                          calle: str, numero:str, dbs: Session = Depends(get_db)):
    return crud.add_direccion(db=dbs, id_usuario=id_usuario, id_comuna=id_comuna,
                              calle=calle, numero=numero)

@app.delete('/api/v1/direcciones/{id}')
async def delete_direccion(id: int, dbs: Session = Depends(get_db)):
    return crud.remover_direccion(db=dbs,id_direccion=id)

@app.get('/api/v1/direcciones/')
async def get_direcciones(dbs: Session = Depends(get_db)):
    return crud.listar_direcciones(db=dbs)

@app.get('/api/v1/direcciones/{id_usuario}')
async def get_direcciones_por_usuario(id_usuario: int, dbs: Session = Depends(get_db)):
    return crud.listar_direcciones_por_usuario(db=dbs, id_usuario=id_usuario)

#Endpoints de sucursal
@app.post('/api/v1/sucursales/')
async def post_sucursal(id_comuna: int, direccion: str, nombre: str, longitude: float,
                        latitude: float, telefono: str, dbs: Session = Depends(get_db)):
    return crud.add_sucursal(db=dbs, id_comuna=id_comuna, direccion=direccion, nombre=nombre,
                             latitude=latitude, longitude=longitude, telefono=telefono)

@app.delete('/api/v1/sucursales/{id}')
async def delete_sucursal(id: int, dbs: Session = Depends(get_db)):
    return crud.remover_sucursal(db=dbs, id_sucursal=id)

@app.get('/api/v1/sucursales/')
async def get_sucursales(dbs: Session = Depends(get_db)):
    return crud.listar_sucursales(db=dbs)

#Endpoints asociados al inventario
@app.post('/api/v1/inventario/')
async def post_inventario(sucursal_id: int, producto_id: int,
                           cantidad: int, dbs: Session = Depends(get_db)):
    return crud.annadir_inventario(db=dbs, sucursal_id=sucursal_id, producto_id=producto_id, cantidad=cantidad)

@app.delete('/api/v1/inventario/')
async def delete_inventario(sucursal_id: int, producto_id: int, dbs: Session = Depends(get_db)):
    return crud.remover_inventario(db=dbs, sucursal_id=sucursal_id, producto_id=producto_id)

@app.get('/api/v1/inventario/')
async def get_inventario(dbs: Session = Depends(get_db)):
    return crud.listar_inventario(db=dbs)

@app.get('/api/v1/inventario/{sucursal_id}')
async def get_inventario_sucursal(sucursal_id: int, dbs: Session = Depends(get_db)):
    return crud.listar_inventario_sucursal(db=dbs, sucursal_id=sucursal_id)

#Endpoints asociados al medio de pago y el pago
@app.post('/api/v1/medios_de_pago/')
async def post_medio_de_pago(nombre: str, dbs: Session = Depends(get_db)):
    return crud.add_medio_pago(nombre=nombre, db=dbs)

@app.delete('/api/v1/medios_de_pago/{id}')
async def delete_medio_de_pago(id: int, dbs: Session = Depends(get_db)):
    return crud.remover_medio_pago(id=id, db=dbs)

@app.get('/api/v1/medios_de_pago')
async def get_medios_de_pago(dbs: Session = Depends(get_db)):
    return crud.listar_medios(db=dbs)

@app.post('/api/v1/pagos/')
async def post_pago(id_pedido: int, id_medio: int, total: int,
                              dbs: Session = Depends(get_db)):
    return crud.crear_pago(db=dbs, id_medio=id_medio, id_pedido=id_pedido, total=total)

@app.delete('/api/v1/pagos/{id}')
async def delete_pago(id: int, dbs: Session = Depends(get_db)):
    return crud.remover_pago(db=dbs, id=id)

@app.get('/api/v1/pagos/')
async def get_pagos(dbs: Session = Depends(get_db)):
    return crud.listar_pagos(db=dbs)

#Endpoints asociados a los faqs

@app.post('/api/v1/categoriaFAQ/')
async def post_categoria_faq(nombre:str, dbs: Session = Depends(get_db)):
    return crud.crear_categoria_faq(db=dbs, nombre=nombre)

@app.delete('/api/v1/categoriaFAQ/{id}')
async def delete_categoria_faq(id:int, dbs: Session=Depends(get_db)):
    return crud.remover_categoria_faq(db=dbs, id=id)

@app.get('/api/v1/categoriaFAQ/')
async def listar_categorias_faq(dbs: Session = Depends(get_db)):
    return crud.listar_categorias(db=dbs)

@app.post('/api/v1/FAQ/')
async def post_faq(categoria_id:int, pregunta:str, resumen:str,
                    respuesta:str, dbs:Session = Depends(get_db)):
    return crud.crear_faq(db=dbs, categoria_id=categoria_id, pregunta=pregunta,
                          resumen=resumen, respuesta=respuesta)

@app.delete('/api/v1/FAQ/{id}')
async def delete_faq(id: int, dbs: Session = Depends(get_db)):
    return crud.remover_faq(db=dbs, id=id)

@app.get('/api/v1/FAQ/')
async def get_faq(dbs: Session = Depends(get_db)):
    return crud.listar_faq(db=dbs)