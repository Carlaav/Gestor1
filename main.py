from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
import database as db
from models import ModeloCliente, ModeloCrearCliente

app = FastAPI(
    title="API del Gestor de clientes",
    description="Ofrece diferentes funciones para gestionar los clientes.")

@app.get("/")
async def index():
    content = {'mensaje': '¡Hola mundo!'}
    return JSONResponse(content=content)

print("Servidor de la API...")

@app.get("/html/")
def html():
    content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>¡Hola mundo!</title>
    </head>
    <body>
        <h1>¡Hola mundo!</h1>
    </body>
    </html>
    """
    return Response(content=content, media_type="text/html")


@app.get("/clientes/")
async def clientes():
    content = db.Clientes.lista
    content = [cliente.to_dict() for cliente in db.Clientes.lista]
    headers = {"content-type": "charset=utf-8"}
    return JSONResponse(content=content, headers=headers)


@app.get("/clientes/buscar/{dni}/")
async def clientes_buscar(dni: str):
    cliente = db.Clientes.buscar(dni=dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    headers = {"content-type": "charset=utf-8"}
    return JSONResponse(content=cliente.to_dict(), headers=headers)


@app.post("/clientes/crear/")
async def clientes_crear(datos: ModeloCrearCliente):
    cliente = db.Clientes.crear(datos.dni, datos.nombre, datos.apellido)
    if cliente:
        headers = {"content-type": "charset=utf-8"}
        return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)


@app.put("/clientes/actualizar/")
async def clientes_actualizar(datos: ModeloCliente):
    if db.Clientes.buscar(datos.dni):
        cliente = db.Clientes.modificar(datos.dni, datos.nombre, datos.apellido)
        if cliente:
            headers = {"content-type": "charset=utf-8"}
            return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)


@app.delete("/clientes/borrar/{dni}/")
async def clientes_borrar(dni: str):
    if db.Clientes.buscar(dni=dni):
        cliente = db.Clientes.borrar(dni=dni)
        headers = {"content-type": "charset=utf-8"}
        return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)
