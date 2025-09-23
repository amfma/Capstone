from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    nombres: str
    apellidos: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginData(BaseModel):
    id: int
    token: str | None = None
    mensaje: str | None = None

class NewUser(BaseModel):
    status: bool
    mensaje: str

class ProductoVenta(BaseModel):
    id: int
    cantidad: int

class Producto(ProductoVenta):
    precio: int

class InputVenta(BaseModel):
    user_id: int
    subtotal: int
    productos: list[ProductoVenta]