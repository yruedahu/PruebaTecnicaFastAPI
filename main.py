from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()
engine = create_engine('mysql+pymysql://root:root@localhost:3306/Personajes')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Personaje (Base):
    _tablename_ = 'Personajes'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    descripcion = Column(String(100), index=True)

Base.metadata.create_all(bind=engine)
# Obtener todos los personajes
@app.get("/personajes")
def obtener_todos():
    sesion = Session()
    try:
        personas = sesion.query(Personaje).all()
        return {"personajes": [persona.json() for persona in personas]}
    finally:
        sesion.close()


# Crear un nuevo personaje
@app.post("/personajes", status_code=201)
def crear_nuevo_personaje(personaje: Personaje):
    """Agrega un nuevo personaje a la base de datos."""
    sesion = Session()
    try:
        sesion.add(personaje)
        sesion.commit()
        return personaje.json()
    except Exception as e:
        return {"error": str(e)}
    finally:
        sesion.close()

# Obtener por ID
@app.get("/personajes/{id}")
def obtener_por_id(id: int):
    """Obtiene el detalle de un personaje por su ID."""
    sesion = Session() 
    try:
        persona = sesion.query(Personaje).filter(Personaje.id == id).first()
        if persona is None:
            raise HTTPException(status_code=404, detail="Personaje no encontrado")
        else:
            return persona.json()
    except Exception as e:
        return {"error": str(e)}
