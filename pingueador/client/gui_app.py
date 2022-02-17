#================IMPORTS================#
import tkinter as tk
from tkinter import ttk, messagebox
from model.registros import crear_tabla, borrar_tabla
from model.registros import Registro, guardar, listar, editar_base_datos, eliminar_base_datos

#================MENUS================#
def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width=300, height=300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)

    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)

    menu_inicio.add_command(label='Crear Registro en DB', command=crear_tabla)
    menu_inicio.add_command(label='Eliminar Registro en DB', command=borrar_tabla)
    menu_inicio.add_command(label='Salir', command=root.destroy)

    barra_menu.add_cascade(label='Resumen', menu=menu_inicio)
    barra_menu.add_cascade(label='Configuración', menu=menu_inicio)
    barra_menu.add_cascade(label='Ayuda', menu=menu_inicio)

#================FRAME================#
class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=700, height=400)
        self.root = root
        self.pack()
        self.id_registro = None

        self.opciones_reconocimiento()
        self.desabilitar_campos()
        self.tabla_registro()

    #================FUNCIONES================#
    def opciones_reconocimiento(self):
        #================LABELS================#
        self.label_ip = tk.Label(self, text="Dirección IP:")
        self.label_ip.config(font= ('consolas', 12, 'bold'))
        self.label_ip.grid(row=0, column=0, padx=10, pady=10)

        self.label_nombre = tk.Label(self, text="Nombre:")
        self.label_nombre.config(font= ('consolas', 12, 'bold'))
        self.label_nombre.grid(row=1, column=0, padx=10, pady=10)

        self.label_selectores = tk.Label(self, text="Indique su Sistema Operativo:")
        self.label_selectores.config(font= ('consolas', 12, 'bold'))
        self.label_selectores.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        #================ENTRYS================#
        self.mi_ip = tk.StringVar()
        self.entry_ip = tk.Entry(self, textvariable=self.mi_ip)
        self.entry_ip.config(width=50, font=('consolas', 12, 'bold'))
        self.entry_ip.grid(row=0, column=1, padx=10, pady=10, columnspan=3)

        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=50, font=('consolas', 12, 'bold'))
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        #================SELECTORES================#
        self.opcion_so = tk.IntVar()

        self.selector_1 = tk.Radiobutton(self, text="Windows", variable=self.opcion_so, value=1, command="")
        self.selector_1.config(width=35, font=('consolas', 12, 'bold'), indicatoron=False, cursor='hand2', fg='#DAD5D6', bg='#158645', activebackground='#35BD6F', selectcolor='#35BD6F')
        self.selector_1.grid(row=3, column=0, padx=10, pady=10, columnspan=4)

        self.selector_2 = tk.Radiobutton(self, text="Linux", variable=self.opcion_so, value=2, command="")
        self.selector_2.config(width=35, font=('consolas', 12, 'bold'), indicatoron=False, cursor='hand2', fg='#DAD5D6', bg='#158645', activebackground='#35BD6F', selectcolor='#35BD6F')
        self.selector_2.grid(row=4, column=0, padx=10, pady=10, columnspan=4)

        #================BOTONES PRINCIPAL================#
        self.boton_nuevo = tk.Button(self, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=30, font=('consolas', 12, 'bold'), fg='#DAD5D6', bg='#1658A2', cursor='hand2', activebackground='#3586DF')
        self.boton_nuevo.grid(row=5, column=0, padx=10, pady=10)

        self.boton_comenzar = tk.Button(self, text="Comenzar", command=self.comenzar)
        self.boton_comenzar.config(width=40, font=('consolas', 12, 'bold'), fg='#DAD5D6', bg='#158645', cursor='hand2', activebackground='#35BD6F')
        self.boton_comenzar.grid(row=5, column=1, pady=10)

        self.boton_cancelar = tk.Button(self, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(width=30, font=('consolas', 12, 'bold'), fg='#DAD5D6', bg='#BB152E', cursor='hand2', activebackground='#E15370')
        self.boton_cancelar.grid(row=5, column=2, padx=10, pady=10)

    def habilitar_campos(self):
        self.entry_ip.config(state='normal')
        self.entry_nombre.config(state='normal')

        self.boton_comenzar.config(state='normal')
        self.boton_cancelar.config(state='normal')

        self.selector_1.config(state='normal')
        self.selector_2.config(state='normal')

    def desabilitar_campos(self):
        #Se envia un string vacio, para limpiar el campo
        self.id_registro = None
        self.mi_ip.set('')
        self.mi_nombre.set('')

        self.entry_ip.config(state='disabled')
        self.entry_nombre.config(state='disabled')
        
        self.boton_comenzar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')

        self.selector_1.config(state='disabled')
        self.selector_2.config(state='disabled')

        #Se envia un vacio, resetear y no guarde la anterior seleccion
        self.opcion_so.set(None)
    
    def comenzar(self):

        #Ejecucion del ping
        import subprocess
        valor = self.opcion_so.get()
        windows = 1

        #================WINDOWS================#
        if valor == windows:
            
            try:
            
                p = subprocess.Popen(f"C:/Windows/System32/ping {self.mi_ip.get()}", shell=True, stdout=subprocess.PIPE)
                (cadena, error) = p.communicate()
                cadena_origin = cadena.split()
                TTL = b'TTL'
                cadena_ttl = cadena_origin[14][0:-3]

                if cadena_ttl == TTL:
                    get_ttl = int(cadena_origin[14][4:])
                    if get_ttl > 64 and get_ttl <= 128:
                        self.sistema_operativo = "Windows"

                    elif get_ttl <= 64:
                        self.sistema_operativo = "Linux"
                    
                    else:
                        self.sistema_operativo = "Desconocido"
                    
                    self.estado = "Ok"

                    registro = Registro(
                        self.mi_ip.get(),
                        self.mi_nombre.get(),
                        self.sistema_operativo,
                        self.estado
                    )
                    if self.id_registro == None:
                        guardar(registro)
                    else:
                        editar_base_datos(registro, self.id_registro)
                    self.tabla_registro()

                    titulo = "Pingueador"
                    mensaje = "¡El programa a fallado exitosamente!"
                    messagebox.showinfo(titulo, mensaje)
                    self.desabilitar_campos()

                else:
                    self.estado = "Failed"
                    self.sistema_operativo = "Desconocido"
                    registro = Registro(
                        self.mi_ip.get(),
                        self.mi_nombre.get(),
                        self.sistema_operativo,
                        self.estado
                    )
                    guardar(registro)
                    self.tabla_registro()

                    titulo = "Error Ping"
                    mensaje = "¡La dirección IP indicada es inalcanzable!"
                    messagebox.showerror(titulo, mensaje)
                    self.desabilitar_campos()

            except:
                self.mi_ip.set('')
                self.mi_nombre.set('')
                self.opcion_so.set(None)
                titulo = "Pingueador"
                mensaje = "¡Por favor seleccione correctamente su Sistema Operativo!"
                messagebox.showerror(titulo, mensaje)

        #================LINUX================#
        else:

            try:

                p = subprocess.Popen(f"/usr/bin/ping {self.mi_ip.get()}", shell=True, stderr=subprocess.PIPE)
                (cadena, error) = p.communicate()
                cadena_origin = cadena.split()
                TTL = b'ttl'
                cadena_ttl = cadena_origin[12][0:-3]

            except:

                self.mi_ip.set('')
                self.mi_nombre.set('')
                self.opcion_so.set(None)
                titulo = "Pingueador"
                mensaje = "¡Por favor seleccione correctamente su Sistema Operativo!"
                messagebox.showerror(titulo, mensaje)

                if cadena_ttl == TTL:
                    get_ttl = int(cadena_origin[12][4:])
                    if get_ttl > 64 and get_ttl <= 128:
                        self.sistema_operativo = "Windows"
                    
                    if get_ttl <= 64:
                        self.sistema_operativo = "Linux"
                    
                    else:
                        self.sistema_operativo = "Desconocido"
                    
                    self.estado = "Ok"

                    registro = Registro(
                        self.mi_ip.get(),
                        self.mi_nombre.get(),
                        self.sistema_operativo,
                        self.estado
                    )
                    if self.id_registro == None:
                        guardar(registro)
                    else:
                        editar_base_datos(registro, self.id_registro)
                    self.tabla_registro()

                    titulo = "Pingueador"
                    mensaje = "¡El programa a fallado exitosamente!"
                    messagebox.showinfo(titulo, mensaje)
                    self.desabilitar_campos()

                else:
                    self.estado = "Failed"
                    self.sistema_operativo = "Desconocido"
                    registro = Registro(
                        self.mi_ip.get(),
                        self.mi_nombre.get(),
                        self.sistema_operativo,
                        self.estado
                    )
                    guardar(registro)
                    self.tabla_registro()
                    
                    titulo = "Error Ping"
                    mensaje = "¡La dirección IP indicada es inalcanzable!"
                    messagebox.showerror(titulo, mensaje)
                    self.desabilitar_campos()

    #================TABLA================#
    def tabla_registro(self):

        #Recuperar lista de los registros
        self.lista_registros = listar()
        self.lista_registros.reverse()

        #================DISEÑO TABLA================#
        self.tabla = ttk.Treeview(self, columns=('Nombre', 'IP', 'Sistema Operativo', 'Estado'))
        self.tabla.grid(row=6, column=0, columnspan=5, sticky='nse')

        #Scrollbar
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=6, column=5, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll)

        self.tabla.column('#0', anchor=tk.CENTER)
        self.tabla.heading('#0', text='ID')

        self.tabla.column('#1', anchor=tk.CENTER)
        self.tabla.heading('#1', text='Nombre')

        self.tabla.column('#2', anchor=tk.CENTER)
        self.tabla.heading('#2', text='IP')

        self.tabla.column('#3', anchor=tk.CENTER)
        self.tabla.heading('#3', text='Sistema Operativo de la IP')

        self.tabla.column('#4', anchor=tk.CENTER)
        self.tabla.heading('#4', text='Estado')

        #================INSERTAR DATOS TABLA================#
        for r in self.lista_registros:
            
            self.tabla.insert('', tk.END, text=r[0], values=(r[2], r[1], r[3], r[4]))

        #================BOTONES TABLA================#
        self.boton_editar = tk.Button(self, text="Editar", command=self.editar_datos)
        self.boton_editar.config(width=22, font=('consolas', 12, 'bold'), fg='#DAD5D6', bg='#1658A2', cursor='hand2', activebackground='#3586DF')
        self.boton_editar.grid(row=7, column=0, padx=10, pady=10, columnspan=2)

        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_datos)
        self.boton_eliminar.config(width=22, font=('consolas', 12, 'bold'), fg='#DAD5D6', bg='#BB152E', cursor='hand2', activebackground='#E15370')
        self.boton_eliminar.grid(row=7, column=1, padx=10, pady=10, columnspan=2)


    #================FUNCION EDITAR================#
    def editar_datos(self):
        try:
            self.id_registro = self.tabla.item(self.tabla.selection())['text']
            self.direccion_ip = self.tabla.item(self.tabla.selection())['values'][1]
            self.nombre = self.tabla.item(self.tabla.selection())['values'][0]

            self.habilitar_campos()

            self.entry_ip.insert(0, self.direccion_ip)
            self.entry_nombre.insert(0, self.nombre)

        except:
            titulo = 'Edicion de Datos'
            mensaje = 'No se ha seleccionado ningun registro'
            messagebox.showerror(titulo, mensaje)

    #================FUNCION ELIMINAR================#
    def eliminar_datos(self):
        try:
            self.id_registro = self.tabla.item(self.tabla.selection())['text']
            eliminar_base_datos(self.id_registro)
            self.tabla_registro()

        except:
            titulo = 'Eliminación de Datos'
            mensaje = 'No se ha seleccionado ningun registro'
            messagebox.showerror(titulo, mensaje)