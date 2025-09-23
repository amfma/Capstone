'''
Documento con la logica asociada al proceso de ventas.
Idea basica:
Recibes via API:
    Una coleccion (lista) de productos.
    Un usuario
    Un subtotal
    Uno o más cupones
    Una o más ofertas

Dado esto, se realiza la siguiente acción:
    Se verifica que todos los productos existan al momento de la compra.
    Si existen, se genera un pedido con el id de usuario.
    Se añade al DetallePedido la lista completa de productos.
    Se restan del stock existente en web (u otros) los productos.
    Se calcula el subtotal.
    (Implementar en siguiente version: Calculo de los cupones y ofertas)
    Se obtiene el total.
    Dado todo esto, se genera una orden de transaccion para transbank

Presuncion:
    Las ventas en linea solo procesan stock de la sucursal virtual
'''

from schema import InputVenta, ProductoVenta
from sqlalchemy.orm import Session
import models

ejemplo = InputVenta(user_id=1, subtotal=100, productos=[ProductoVenta(id=1, cantidad=3),
                                                         ProductoVenta(id=2, cantidad=1),
                                                         ProductoVenta(id=4, cantidad=2)])


def procesar_venta(venta: InputVenta, db: Session):
    total = 0
    productos_buscados = db.query(models.InventarioSucursal).filter(models.InventarioSucursal.producto_id.in_([p.id for p in venta.productos]))
    for producto in venta.productos:
        print(producto)

