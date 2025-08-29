"""db.py contiene todos los elementos relacionados a la configuración de la base de datos.
Por defecto incluira un db sqlite para facilitar el prototipado"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#Para efectos de prototipado la conexion sera a un archivo sqlite
DB_URI = "sqlite:///aurora.db"

#Con estos elementos configuramos la conexion a la DB.
#Por seguridad hacemos que todo commit deba ser declarado
engine = create_engine(DB_URI)
sesion = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()