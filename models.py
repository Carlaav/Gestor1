from pydantic import BaseModel, constr, ValidationError, validator
import helpers
import database as db

class ModeloCliente(BaseModel):
    dni: constr(min_length=3, max_length=3)
    nombre: constr(min_length=2, max_length=30)
    apellido: constr(min_length=2, max_length=30)


class ModeloCrearCliente(ModeloCliente):
    @validator("dni")
    def validar_dni(cls, dni):
        if not helpers.dni_valido(dni, db.Clientes.lista):
            raise ValueError("Cliente ya existente o DNI incorrecto")
        return dni
