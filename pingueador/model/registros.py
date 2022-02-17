from .conexion_db import ConexionDB
from tkinter import messagebox

def crear_tabla():
    conexion = ConexionDB()

    query_creacion = """
    CREATE TABLE registros(
        id_registro INTEGER,
        nombre VARCHAR(100),
        direccion_ip VARCHAR(20),
        sistema_operativo VARCHAR(10),
        estado VARCHAR(6),
        PRIMARY KEY(id_registro AUTOINCREMENT)
    )
    """
    try:
        conexion.cursor.execute(query_creacion)
        conexion.cerrar_conexion()
        titulo = 'Crear Registro'
        mensaje = '¡La tabla se creo exitosamente!'
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = 'Crear Registro'
        mensaje = '¡La tabla ya existe!'
        messagebox.showwarning(titulo, mensaje)

def borrar_tabla():
    conexion = ConexionDB()

    query_eliminacion = 'DROP TABLE registros'

    try:
        conexion.cursor.execute(query_eliminacion)
        conexion.cerrar_conexion()
        titulo = 'Eliminar Registro'
        mensaje = '¡La tabla se borro exitosamente!'
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = 'Eliminar Registro'
        mensaje = '¡La tabla no existe!'
        messagebox.showwarning(titulo, mensaje)

class Registro:
    def __init__(self, nombre, direccion_ip, sistema_operativo,estado):
        self.id_registro = None
        self.nombre = nombre
        self.direccion_ip = direccion_ip
        self.sistema_operativo = sistema_operativo
        self.estado = estado

    def __str__(self):
        return f'Registro[{self.nombre}, {self.direccion_ip}, {self.sistema_operativo}, {self.estado}]'

def guardar(registro):
    conexion = ConexionDB()
    query_insertar_datos = f"""INSERT INTO registros (nombre, direccion_ip, sistema_operativo, estado) VALUES('{registro.nombre}', '{registro.direccion_ip}', '{registro.sistema_operativo}', '{registro.estado}')"""

    try:
        conexion.cursor.execute(query_insertar_datos)
        conexion.cerrar_conexion()
    except:
        titulo = 'Conexion al Registro'
        mensaje = 'La tabla registros no está creada en la base de datos'
        messagebox.showerror(titulo, mensaje)

def listar():

    conexion = ConexionDB()
    
    lista_registros = []
    query = "SELECT * FROM registros"

    try:
        conexion.cursor.execute(query)
        lista_registros = conexion.cursor.fetchall()
        conexion.cerrar_conexion()
    except:
        titulo = 'Conexion al Registro'
        mensaje = '¡Necesita crear la tabla en la base de datos!'
        messagebox.showwarning(titulo, mensaje)

    return lista_registros

def editar_base_datos(registro, id_registro):
    conexion = ConexionDB()
    query_edicion = f"""UPDATE registros
    SET direccion_ip = '{registro.direccion_ip}', nombre = '{registro.nombre}', sistema_operativo = '{registro.sistema_operativo}', estado = '{registro.estado}'
    WHERE id_registro = {id_registro}
    """

    try:
        conexion.cursor.execute(query_edicion)
        conexion.cerrar()
    
    except:
        titulo = 'Edición de Datos'
        mensaje = 'No se a podido realizar la edición de este registro'
        messagebox.showerror(titulo, mensaje)

def eliminar_base_datos(id_registro):
    conexion = ConexionDB()
    query_eliminar_registro = f"DELETE FROM registros WHERE id_registro = {id_registro}"

    try:
        conexion.cursor.execute(query_eliminar_registro)
        conexion.cerrar_conexion()
    
    except:
        titulo = 'Eliminación Datos'
        mensaje = 'No se a podido realizar la eliminacion del registro'
        messagebox.showerror(titulo, mensaje)