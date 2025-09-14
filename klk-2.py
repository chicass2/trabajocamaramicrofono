from tkinter import Tk, Frame, Label, Entry, Button, Text, Toplevel, messagebox, WORD, DISABLED, END, Canvas
from tkinter import ttk
import sqlite3
from datetime import datetime

class BodegaIvisApp:
    def __init__(self):
        self.ven = Tk()
        self.ven.title("Sistema Bodega Ivis")
        self.ven.geometry("800x600")
        self.ven.configure(bg="#ca9e7a")
        self.inicializar_bd()
        self.ven.withdraw()
        self.mostrar_login()
    
    def centrar_ventana(self, ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana.resizable(False, False)  # Deshabilitar redimensionamiento
    
    def inicializar_bd(self):
        self.conexion = sqlite3.connect("bod_ivis.db")
        self.cursor = self.conexion.cursor()
        
        try:
            self.conexion.execute("""CREATE TABLE IF NOT EXISTS Usuarios(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT UNIQUE,
                                password TEXT)""")
            
            self.cursor.execute("SELECT * FROM Usuarios WHERE usuario='admin'")
            if not self.cursor.fetchone():
                self.cursor.execute("INSERT INTO Usuarios (usuario, password) VALUES ('admin', '123456')")
                self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error creando tabla usuarios: {e}")
        
        try:
            self.conexion.execute("""CREATE TABLE IF NOT EXISTS Clientes(
                            DNI_Cliente INTEGER PRIMARY KEY,
                            Nombre TEXT,
                            Telefono TEXT,
                            Direccion TEXT)""")
            
            self.conexion.execute("""CREATE TABLE IF NOT EXISTS Compra(
                            Codigo_Compra INTEGER PRIMARY KEY,
                            DNI_Cliente INTEGER,
                            Tipo_de_cafe TEXT,
                            Humedad REAL,
                            Peso INTEGER)""")
            
            self.conexion.execute("""CREATE TABLE IF NOT EXISTS Venta(
                            Codigo_Venta INTEGER PRIMARY KEY,
                            Comprador TEXT,
                            Venta TEXT,
                            Tipo_de_cafe TEXT,
                            Precio INTEGER,
                            Fecha_Entrega TEXT)""")
            
            self.conexion.execute("""CREATE TABLE IF NOT EXISTS Trabajadores(
                            ID_Trabajador INTEGER PRIMARY KEY,
                            Nombres TEXT,
                            Apellidos TEXT,
                            Edad INTEGER,
                            Sueldo INTEGER,
                            Fecha_Contrato TEXT)""")
            
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error creando tablas: {e}")
    
    def mostrar_login(self):
        self.login_win = Toplevel(self.ven)
        self.login_win.title("Inicio de Sesión")
        self.login_win.geometry("400x350")
        self.centrar_ventana(self.login_win, 400, 350)
        self.login_win.configure(bg="#87644b")
        self.login_win.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        self.login_win.grab_set()
        
        # Frame principal para mejor organización
        main_frame = Frame(self.login_win, bg="#87644b")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.titulo = Label(main_frame, text="BODEGA IVIS", font=("Arial", 24, "bold"), 
                         fg="#ca9e7a", bg="#87644b")
        self.titulo.pack(pady=(10, 5))
        
        self.subtitulo = Label(main_frame, text="Sistema de Gestión", font=("Arial", 14), 
                            fg="#e2d5c8", bg="#87644b")
        self.subtitulo.pack(pady=(0, 20))
        
        # Frame para campos de entrada
        input_frame = Frame(main_frame, bg="#87644b")
        input_frame.pack(pady=10)
        
        self.lbl_usuario = Label(input_frame, text="Usuario:", font=("Arial", 12), 
                              fg="#ffffff", bg="#87644b")
        self.lbl_usuario.grid(row=0, column=0, sticky="w", pady=5)
        
        self.entry_usuario = Entry(input_frame, font=("Arial", 12), width=25, bg="#e2d5c8")
        self.entry_usuario.grid(row=1, column=0, pady=5)
        
        self.lbl_password = Label(input_frame, text="Contraseña:", font=("Arial", 12), 
                               fg="#ffffff", bg="#87644b")
        self.lbl_password.grid(row=2, column=0, sticky="w", pady=5)
        
        self.entry_password = Entry(input_frame, font=("Arial", 12), width=25, show="*", bg="#e2d5c8")
        self.entry_password.grid(row=3, column=0, pady=5)
        
        # Frame para botones
        button_frame = Frame(main_frame, bg="#87644b")
        button_frame.pack(pady=20)
        
        self.btn_login = Button(button_frame, text="Ingresar", font=("Arial", 12, "bold"),
                             bg="#837469", fg="#ffffff", command=self.validar_login,
                             cursor="hand2", width=15)
        self.btn_login.pack(pady=5)
        
        self.info_login = Label(main_frame, text="Usuario: admin | Contraseña: 123456", 
                             font=("Arial", 10), fg="#e2d5c8", bg="#87644b")
        self.info_login.pack(pady=10)
        
        self.entry_usuario.focus()
        self.entry_password.bind('<Return>', lambda e: self.validar_login())
    
    def validar_login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        try:
            self.cursor.execute("SELECT * FROM Usuarios WHERE usuario=? AND password=?", 
                              (usuario, password))
            if self.cursor.fetchone():
                self.login_win.destroy()
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
                self.entry_password.delete(0, END)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {e}")
    
    def mostrar_menu_principal(self):
        self.menu_win = Toplevel(self.ven)
        self.menu_win.title("Menú Principal")
        self.menu_win.geometry("1000x700")
        self.centrar_ventana(self.menu_win, 1000, 700)
        self.menu_win.configure(bg="#ca9e7a")
        self.menu_win.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        # Frame de título
        self.title_frame = Frame(self.menu_win, bg="#87644b", width=1000, height=80)
        self.title_frame.pack()
        
        self.titulo_menu = Label(self.title_frame, text="SISTEMA BODEGA IVIS", font=("Arial", 24, "bold"),
                              fg="#ffffff", bg="#87644b")
        self.titulo_menu.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame principal para botones
        main_frame = Frame(self.menu_win, bg="#ca9e7a")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Primera fila de botones
        row1_frame = Frame(main_frame, bg="#ca9e7a")
        row1_frame.pack(pady=20)
        
        self.btn_clientes = Button(row1_frame, text="Gestión de Clientes", font=("Arial", 12, "bold"),
                                bg="#837469", fg="#ffffff", command=lambda: self.mostrar_crud("Clientes"),
                                cursor="hand2", width=18, height=2)
        self.btn_clientes.grid(row=0, column=0, padx=20)
        
        self.btn_compras = Button(row1_frame, text="Gestión de Compras", font=("Arial", 12, "bold"),
                               bg="#87644b", fg="#ffffff", command=lambda: self.mostrar_crud("Compra"),
                               cursor="hand2", width=18, height=2)
        self.btn_compras.grid(row=0, column=1, padx=20)
        
        self.btn_ventas = Button(row1_frame, text="Gestión de Ventas", font=("Arial", 12, "bold"),
                              bg="#110705", fg="#ffffff", command=lambda: self.mostrar_crud("Venta"),
                              cursor="hand2", width=18, height=2)
        self.btn_ventas.grid(row=0, column=2, padx=20)
        
        # Segunda fila de botones
        row2_frame = Frame(main_frame, bg="#ca9e7a")
        row2_frame.pack(pady=20)
        
        self.btn_trabajadores = Button(row2_frame, text="Gestión de Trabajadores", font=("Arial", 12, "bold"),
                                    bg="#837469", fg="#ffffff", command=lambda: self.mostrar_crud("Trabajadores"),
                                    cursor="hand2", width=18, height=2)
        self.btn_trabajadores.grid(row=0, column=0, padx=20)
        
        self.btn_reportes = Button(row2_frame, text="Reportes", font=("Arial", 12, "bold"),
                                bg="#87644b", fg="#ffffff", command=self.mostrar_reportes,
                                cursor="hand2", width=18, height=2)
        self.btn_reportes.grid(row=0, column=1, padx=20)
        
        self.btn_info_empresa = Button(row2_frame, text="Info. Empresa", font=("Arial", 12, "bold"),
                                    bg="#110705", fg="#ffffff", command=self.mostrar_info_empresa,
                                    cursor="hand2", width=18, height=2)
        self.btn_info_empresa.grid(row=0, column=2, padx=20)
        
        # Tercera fila de botones
        row3_frame = Frame(main_frame, bg="#ca9e7a")
        row3_frame.pack(pady=20)
        
        self.btn_info_equipo = Button(row3_frame, text="Info. Equipo", font=("Arial", 12, "bold"),
                                   bg="#87644b", fg="#ffffff", command=self.mostrar_info_equipo,
                                   cursor="hand2", width=18, height=2)
        self.btn_info_equipo.grid(row=0, column=0, padx=20)
        
        self.btn_cerrar_sesion = Button(row3_frame, text="Cerrar Sesión", font=("Arial", 12, "bold"),
                                     bg="#837469", fg="#ffffff", command=self.cerrar_sesion,
                                     cursor="hand2", width=18, height=2)
        self.btn_cerrar_sesion.grid(row=0, column=1, padx=20)
    
    def cerrar_sesion(self):
        self.menu_win.destroy()
        self.mostrar_login()
    
    def mostrar_crud(self, tabla):
        self.crud_win = Toplevel(self.menu_win)
        self.crud_win.title(f"Gestión de {tabla}")
        self.crud_win.geometry("1000x700")
        self.centrar_ventana(self.crud_win, 1000, 700)
        self.crud_win.configure(bg="#ca9e7a")
        self.crud_win.grab_set()
        
        self.tabla_actual = tabla
        
        # Frame de título
        self.title_frame = Frame(self.crud_win, bg="#87644b", width=1000, height=60)
        self.title_frame.pack()
        
        self.titulo_crud = Label(self.title_frame, text=f"GESTIÓN DE {tabla.upper()}", 
                              font=("Arial", 18, "bold"), fg="#ffffff", bg="#87644b")
        self.titulo_crud.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame principal para botones y tabla
        main_frame = Frame(self.crud_win, bg="#ca9e7a")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Frame para botones de acción
        button_frame = Frame(main_frame, bg="#ca9e7a")
        button_frame.pack(pady=10)
        
        self.btn_agregar = Button(button_frame, text="Agregar", bg="#837469", fg="#ffffff",
                               font=("Arial", 10, "bold"), command=self.agregar_registro,
                               cursor="hand2", width=12)
        self.btn_agregar.grid(row=0, column=0, padx=5)
        
        self.btn_modificar = Button(button_frame, text="Modificar", bg="#87644b", fg="#ffffff",
                                 font=("Arial", 10, "bold"), command=self.modificar_registro,
                                 cursor="hand2", width=12)
        self.btn_modificar.grid(row=0, column=1, padx=5)
        
        self.btn_eliminar = Button(button_frame, text="Eliminar", bg="#110705", fg="#ffffff",
                                font=("Arial", 10, "bold"), command=self.eliminar_registro,
                                cursor="hand2", width=12)
        self.btn_eliminar.grid(row=0, column=2, padx=5)
        
        self.btn_actualizar = Button(button_frame, text="Actualizar Lista", bg="#837469", fg="#ffffff",
                                  font=("Arial", 10, "bold"), command=self.cargar_datos_tabla,
                                  cursor="hand2", width=12)
        self.btn_actualizar.grid(row=0, column=3, padx=5)
        
        self.btn_volver = Button(button_frame, text="Volver al Menú", bg="#87644b", fg="#ffffff",
                              font=("Arial", 10, "bold"), command=self.crud_win.destroy,
                              cursor="hand2", width=12)
        self.btn_volver.grid(row=0, column=4, padx=5)
        
        # Frame para la tabla
        self.tree_frame = Frame(main_frame, bg="#ca9e7a")
        self.tree_frame.pack(expand=True, fill="both", pady=10)
        
        if tabla == "Clientes":
            columnas = ("DNI_Cliente", "Nombre", "Telefono", "Direccion")
        elif tabla == "Compra":
            columnas = ("Codigo_Compra", "DNI_Cliente", "Tipo_de_cafe", "Humedad", "Peso")
        elif tabla == "Venta":
            columnas = ("Codigo_Venta", "Comprador", "Venta", "Tipo_de_cafe", "Precio", "Fecha_Entrega")
        elif tabla == "Trabajadores":
            columnas = ("ID_Trabajador", "Nombres", "Apellidos", "Edad", "Sueldo", "Fecha_Contrato")
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columnas, show="headings", style="Custom.Treeview")
        
        # Configurar estilo para el Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#e2d5c8", fieldbackground="#e2d5c8", foreground="#110705")
        style.configure("Custom.Treeview.Heading", background="#87644b", foreground="#ffffff", font=('Arial', 10, 'bold'))
        style.map("Custom.Treeview", background=[('selected', '#837469')])
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        
        self.v_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.h_scrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        self.tree.pack(side="left", expand=True, fill="both")
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        
        self.cargar_datos_tabla()
    
    def cargar_datos_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            self.cursor.execute(f"SELECT * FROM {self.tabla_actual}")
            registros = self.cursor.fetchall()
            
            for registro in registros:
                self.tree.insert("", "end", values=registro)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error cargando datos: {e}")
    
    def agregar_registro(self):
        self.ventana_formulario("Agregar")
    
    def modificar_registro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un registro para modificar")
            return
        
        valores = self.tree.item(seleccion[0])['values']
        self.ventana_formulario("Modificar", valores)
    
    def eliminar_registro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
            try:
                valores = self.tree.item(seleccion[0])['values']
                id_campo = self.obtener_campo_id()
                
                self.cursor.execute(f"DELETE FROM {self.tabla_actual} WHERE {id_campo}=?", (valores[0],))
                self.conexion.commit()
                
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.cargar_datos_tabla()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error eliminando registro: {e}")
    
    def obtener_campo_id(self):
        campos_id = {
            "Clientes": "DNI_Cliente",
            "Compra": "Codigo_Compra",
            "Venta": "Codigo_Venta",
            "Trabajadores": "ID_Trabajador"
        }
        return campos_id.get(self.tabla_actual, "id")
    
    def ventana_formulario(self, accion, valores=None):
        self.form_win = Toplevel(self.crud_win)
        self.form_win.title(f"{accion} {self.tabla_actual}")
        self.form_win.geometry("400x500")
        self.centrar_ventana(self.form_win, 400, 500)
        self.form_win.configure(bg="#ca9e7a")
        self.form_win.grab_set()
        
        main_frame = Frame(self.form_win, bg="#ca9e7a")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.titulo_form = Label(main_frame, text=f"{accion} {self.tabla_actual}", 
                              font=("Arial", 16, "bold"), fg="#110705", bg="#ca9e7a")
        self.titulo_form.pack(pady=10)
        
        self.entries = {}
        
        if self.tabla_actual == "Clientes":
            campos = [("DNI Cliente:", "DNI_Cliente"), ("Nombre:", "Nombre"), 
                     ("Teléfono:", "Telefono"), ("Dirección:", "Direccion")]
        elif self.tabla_actual == "Compra":
            campos = [("Código Compra:", "Codigo_Compra"), ("DNI Cliente:", "DNI_Cliente"),
                     ("Tipo de Café:", "Tipo_de_cafe"), ("Humedad:", "Humedad"), ("Peso:", "Peso")]
        elif self.tabla_actual == "Venta":
            campos = [("Código Venta:", "Codigo_Venta"), ("Comprador:", "Comprador"),
                     ("Venta:", "Venta"), ("Tipo de Café:", "Tipo_de_cafe"), 
                     ("Precio:", "Precio"), ("Fecha Entrega:", "Fecha_Entrega")]
        elif self.tabla_actual == "Trabajadores":
            campos = [("ID Trabajador:", "ID_Trabajador"), ("Nombres:", "Nombres"),
                     ("Apellidos:", "Apellidos"), ("Edad:", "Edad"), 
                     ("Sueldo:", "Sueldo"), ("Fecha Contrato:", "Fecha_Contrato")]
        
        input_frame = Frame(main_frame, bg="#ca9e7a")
        input_frame.pack(pady=10)
        
        for i, (label, campo) in enumerate(campos):
            lbl = Label(input_frame, text=label, font=("Arial", 10), 
                      fg="#110705", bg="#ca9e7a", width=15, anchor="e")
            lbl.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            
            entry = Entry(input_frame, font=("Arial", 10), width=25, bg="#e2d5c8")
            entry.grid(row=i, column=1, pady=5)
            
            if valores and i < len(valores):
                entry.insert(0, str(valores[i]))
            
            self.entries[campo] = entry
        
        button_frame = Frame(main_frame, bg="#ca9e7a")
        button_frame.pack(pady=20)
        
        self.btn_guardar = Button(button_frame, text="Guardar", bg="#837469", fg="#ffffff",
                               font=("Arial", 10, "bold"), command=lambda: self.guardar_registro(accion, self.form_win),
                               cursor="hand2", width=12)
        self.btn_guardar.grid(row=0, column=0, padx=10)
        
        self.btn_cancelar = Button(button_frame, text="Cancelar", bg="#87644b", fg="#ffffff",
                                font=("Arial", 10, "bold"), command=self.form_win.destroy,
                                cursor="hand2", width=12)
        self.btn_cancelar.grid(row=0, column=1, padx=10)
    
    def guardar_registro(self, accion, ventana):
        valores = {}
        for campo, entry in self.entries.items():
            valor = entry.get().strip()
            if not valor:
                messagebox.showerror("Error", f"El campo {campo} es obligatorio")
                return
            valores[campo] = valor
        
        try:
            if accion == "Agregar":
                campos = list(valores.keys())
                placeholders = ", ".join(["?" for _ in campos])
                query = f"INSERT INTO {self.tabla_actual} ({', '.join(campos)}) VALUES ({placeholders})"
                self.cursor.execute(query, list(valores.values()))
            else:
                id_campo = self.obtener_campo_id()
                id_valor = valores[id_campo]
                
                campos_update = [f"{campo}=?" for campo in valores.keys() if campo != id_campo]
                valores_update = [valor for campo, valor in valores.items() if campo != id_campo]
                valores_update.append(id_valor)
                
                query = f"UPDATE {self.tabla_actual} SET {', '.join(campos_update)} WHERE {id_campo}=?"
                self.cursor.execute(query, valores_update)
            
            self.conexion.commit()
            messagebox.showinfo("Éxito", f"Registro {accion.lower()} correctamente")
            ventana.destroy()
            self.cargar_datos_tabla()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error guardando registro: {e}")
    
    def mostrar_reportes(self):
        self.reportes_win = Toplevel(self.menu_win)
        self.reportes_win.title("Reportes del Sistema")
        self.reportes_win.geometry("1000x500")
        self.centrar_ventana(self.reportes_win, 1000, 500)
        self.reportes_win.configure(bg="#ca9e7a")
        self.reportes_win.grab_set()
        
        # Frame de título
        self.title_frame = Frame(self.reportes_win, bg="#87644b", width=1000, height=60)
        self.title_frame.pack()
        
        self.titulo_reportes = Label(self.title_frame, text="REPORTES DEL SISTEMA", 
                                  font=("Arial", 18, "bold"), fg="#ffffff", bg="#87644b")
        self.titulo_reportes.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame principal para botones
        main_frame = Frame(self.reportes_win, bg="#ca9e7a")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        self.btn_rep_clientes = Button(main_frame, text="Reporte de Clientes", bg="#837469", fg="#ffffff",
                                    font=("Arial", 12, "bold"), command=lambda: self.generar_reporte("Clientes"),
                                    cursor="hand2", width=20, height=2)
        self.btn_rep_clientes.place(relx=0.5, rely=0.3, anchor="center")
        
        self.btn_rep_ventas = Button(main_frame, text="Reporte de Ventas", bg="#87644b", fg="#ffffff",
                                  font=("Arial", 12, "bold"), command=lambda: self.generar_reporte("Venta"),
                                  cursor="hand2", width=20, height=2)
        self.btn_rep_ventas.place(relx=0.5, rely=0.45, anchor="center")
        
        self.btn_rep_general = Button(main_frame, text="Reporte General", bg="#110705", fg="#ffffff",
                                   font=("Arial", 12, "bold"), command=self.reporte_general,
                                   cursor="hand2", width=20, height=2)
        self.btn_rep_general.place(relx=0.5, rely=0.6, anchor="center")
        
        self.btn_volver_reportes = Button(main_frame, text="Volver al Menú", bg="#837469", fg="#ffffff",
                                       font=("Arial", 12, "bold"), command=self.reportes_win.destroy,
                                       cursor="hand2", width=20, height=2)
        self.btn_volver_reportes.place(relx=0.5, rely=0.75, anchor="center")
    
    def generar_reporte(self, tabla):
        self.reporte_win = Toplevel(self.reportes_win)
        self.reporte_win.title(f"Reporte de {tabla}")
        self.reporte_win.geometry("800x600")
        self.centrar_ventana(self.reporte_win, 800, 600)
        self.reporte_win.configure(bg="#ca9e7a")
        self.reporte_win.grab_set()
        
        main_frame = Frame(self.reporte_win, bg="#ca9e7a")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.titulo_reporte = Label(main_frame, text=f"REPORTE DE {tabla.upper()}", 
                                 font=("Arial", 16, "bold"), fg="#110705", bg="#ca9e7a")
        self.titulo_reporte.pack(pady=10)
        
        self.tree_frame = Frame(main_frame, bg="#ca9e7a")
        self.tree_frame.pack(expand=True, fill="both", pady=10)
        
        if tabla == "Clientes":
            columnas = ("DNI_Cliente", "Nombre", "Telefono", "Direccion")
        elif tabla == "Venta":
            columnas = ("Codigo_Venta", "Comprador", "Venta", "Tipo_de_cafe", "Precio", "Fecha_Entrega")
        
        tree = ttk.Treeview(self.tree_frame, columns=columnas, show="headings", style="Report.Treeview")
        
        # Configurar estilo para el Treeview de reportes
        style = ttk.Style()
        style.configure("Report.Treeview", background="#e2d5c8", fieldbackground="#e2d5c8", foreground="#110705")
        style.configure("Report.Treeview.Heading", background="#87644b", foreground="#ffffff", font=('Arial', 10, 'bold'))
        style.map("Report.Treeview", background=[('selected', '#837469')])
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")
        
        try:
            self.cursor.execute(f"SELECT * FROM {tabla}")
            registros = self.cursor.fetchall()
            
            for registro in registros:
                tree.insert("", "end", values=registro)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error generando reporte: {e}")
        
        info_frame = Frame(main_frame, bg="#ca9e7a")
        info_frame.pack(fill="x", pady=10)
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.lbl_fecha = Label(info_frame, text=f"Fecha de generación: {fecha_actual}", 
                            font=("Arial", 10), fg="#110705", bg="#ca9e7a")
        self.lbl_fecha.pack(side="left", padx=10)
        
        self.lbl_total = Label(info_frame, text=f"Total de registros: {len(registros)}", 
                            font=("Arial", 10), fg="#110705", bg="#ca9e7a")
        self.lbl_total.pack(side="left", padx=10)
        
        button_frame = Frame(main_frame, bg="#ca9e7a")
        button_frame.pack(pady=10)
        
        self.btn_imprimir = Button(button_frame, text="Preparar para Impresión", bg="#87644b", fg="#ffffff",
                                font=("Arial", 10, "bold"), command=lambda: self.preparar_impresion(tabla),
                                cursor="hand2", width=20)
        self.btn_imprimir.pack()
    
    def preparar_impresion(self, tabla):
        try:
            self.cursor.execute(f"SELECT * FROM {tabla}")
            registros = self.cursor.fetchall()
            
            contenido = f"""
BODEGA IVIS - REPORTE DE {tabla.upper()}
{'='*50}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Total de registros: {len(registros)}

"""
            
            for i, registro in enumerate(registros, 1):
                contenido += f"Registro {i}: {registro}\n"
            
            contenido += f"\n{'='*50}\nFin del reporte"
            
            self.impresion_win = Toplevel(self.reporte_win)
            self.impresion_win.title(f"Reporte para Impresión - {tabla}")
            self.impresion_win.geometry("600x400")
            self.centrar_ventana(self.impresion_win, 600, 400)
            self.impresion_win.configure(bg="#ca9e7a")
            
            self.text_widget = Text(self.impresion_win, wrap=WORD, font=("Courier", 10), bg="#e2d5c8", fg="#110705")
            self.text_widget.insert("1.0", contenido)
            self.text_widget.config(state=DISABLED)
            
            self.scrollbar = ttk.Scrollbar(self.impresion_win, command=self.text_widget.yview)
            self.text_widget.config(yscrollcommand=self.scrollbar.set)
            
            self.text_widget.pack(side="left", expand=True, fill="both")
            self.scrollbar.pack(side="right", fill="y")
            
            messagebox.showinfo("Información", "Reporte preparado para impresión")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error preparando reporte: {e}")
    
    def reporte_general(self):
        self.rep_general_win = Toplevel(self.reportes_win)
        self.rep_general_win.title("Reporte General del Sistema")
        self.rep_general_win.geometry("600x500")
        self.centrar_ventana(self.rep_general_win, 600, 500)
        self.rep_general_win.configure(bg="#ca9e7a")
        self.rep_general_win.grab_set()
        
        main_frame = Frame(self.rep_general_win, bg="#ca9e7a")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.titulo_general = Label(main_frame, text="REPORTE GENERAL DEL SISTEMA", 
                                 font=("Arial", 16, "bold"), fg="#110705", bg="#ca9e7a")
        self.titulo_general.pack(pady=10)
        
        self.stats_frame = Frame(main_frame, bg="#87644b", width=540, height=350)
        self.stats_frame.pack(pady=10)
        
        try:
            tablas = ["Clientes", "Compra", "Venta", "Trabajadores"]
            estadisticas = {}
            
            for tabla in tablas:
                self.cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = self.cursor.fetchone()[0]
                estadisticas[tabla] = count
            
            self.lbl_estadisticas = Label(self.stats_frame, text="ESTADÍSTICAS DEL SISTEMA", 
                                       font=("Arial", 14, "bold"), fg="#ffffff", bg="#87644b")
            self.lbl_estadisticas.place(relx=0.5, y=30, anchor="center")
            
            y_pos = 80
            for tabla, count in estadisticas.items():
                lbl_stat = Label(self.stats_frame, text=f"Total {tabla}: {count} registros", 
                                   font=("Arial", 12), fg="#e2d5c8", bg="#87644b")
                lbl_stat.place(x=30, y=y_pos)
                y_pos += 30
            
            self.lbl_info_adicional = Label(self.stats_frame, text="INFORMACIÓN ADICIONAL", 
                                         font=("Arial", 14, "bold"), fg="#ffffff", bg="#87644b")
            self.lbl_info_adicional.place(x=30, y=y_pos + 20)
            
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.lbl_fecha_reporte = Label(self.stats_frame, text=f"Fecha de generación: {fecha_actual}", 
                                        font=("Arial", 10), fg="#e2d5c8", bg="#87644b")
            self.lbl_fecha_reporte.place(x=30, y=y_pos + 50)
            
            total_registros = sum(estadisticas.values())
            self.lbl_total_reg = Label(self.stats_frame, text=f"Total de registros en el sistema: {total_registros}", 
                                    font=("Arial", 10), fg="#e2d5c8", bg="#87644b")
            self.lbl_total_reg.place(x=30, y=y_pos + 80)
            
        except sqlite3.Error as e:
            self.lbl_error = Label(self.stats_frame, text=f"Error generando estadísticas: {e}", 
                                font=("Arial", 12), fg="#e74c3c", bg="#87644b")
            self.lbl_error.place(x=30, y=80)
        
        button_frame = Frame(main_frame, bg="#ca9e7a")
        button_frame.pack(pady=10)
        
        self.btn_volver_reporte = Button(button_frame, text="Volver", bg="#837469", fg="#ffffff",
                                     font=("Arial", 12, "bold"), command=self.rep_general_win.destroy,
                                     cursor="hand2", width=15)
        self.btn_volver_reporte.pack()
    
    def mostrar_info_empresa(self):
        self.info_empresa_win = Toplevel(self.menu_win)
        self.info_empresa_win.title("Información de la Empresa")
        self.info_empresa_win.geometry("1000x700")
        self.centrar_ventana(self.info_empresa_win, 1000, 700)
        self.info_empresa_win.configure(bg="#ca9e7a")
        self.info_empresa_win.grab_set()
        
        # Frame de título
        self.title_frame = Frame(self.info_empresa_win, bg="#87644b", width=1000, height=80)
        self.title_frame.pack()
        
        self.titulo_empresa = Label(self.title_frame, text="INFORMACIÓN DE LA EMPRESA", 
                                font=("Arial", 20, "bold"), fg="#ffffff", bg="#87644b")
        self.titulo_empresa.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame principal con scroll
        self.container = Frame(self.info_empresa_win, bg="#ca9e7a")
        self.container.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.canvas = Canvas(self.container, bg="#ca9e7a", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#87644b")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Contenido dentro del frame con scroll
        self.content_frame = Frame(self.scrollable_frame, bg="#87644b", width=940)
        self.content_frame.pack(padx=20, pady=20)
        
        info_empresa = [
            ("BODEGA IVIS", "Arial", 22, "bold", "#ffffff"),
            ("Empresa dedicada al procesamiento y comercialización de café", "Arial", 12, "normal", "#e2d5c8"),
            ("", "", 0, "", ""),
            ("Año de Fundación: 2020", "Arial", 12, "bold", "#ffffff"),
            ("", "", 0, "", ""),
            ("MISIÓN:", "Arial", 14, "bold", "#ffffff"),
            ("Proporcionar café de la más alta calidad, apoyando a", "Arial", 10, "normal", "#e2d5c8"),
            ("los productores locales y satisfaciendo las necesidades", "Arial", 10, "normal", "#e2d5c8"),
            ("de nuestros clientes con excelencia y compromiso.", "Arial", 10, "normal", "#e2d5c8"),
            ("", "", 0, "", ""),
            ("VISIÓN:", "Arial", 14, "bold", "#ffffff"),
            ("Ser la empresa líder en el sector cafetero de la región,", "Arial", 10, "normal", "#e2d5c8"),
            ("reconocida por la calidad de nuestros productos y", "Arial", 10, "normal", "#e2d5c8"),
            ("nuestro compromiso con el desarrollo sostenible.", "Arial", 10, "normal", "#e2d5c8"),
            ("", "", 0, "", ""),
            ("VALORES:", "Arial", 14, "bold", "#ffffff"),
            ("• Calidad en todos nuestros procesos", "Arial", 10, "normal", "#e2d5c8"),
            ("• Compromiso con nuestros clientes", "Arial", 10, "normal", "#e2d5c8"),
            ("• Respeto por el medio ambiente", "Arial", 10, "normal", "#e2d5c8"),
            ("• Desarrollo de la comunidad local", "Arial", 10, "normal", "#e2d5c8"),
            ("", "", 0, "", ""),
            ("SERVICIOS:", "Arial", 14, "bold", "#ffffff"),
            ("• Compra y venta de café en grano", "Arial", 10, "normal", "#e2d5c8"),
            ("• Procesamiento y almacenamiento", "Arial", 10, "normal", "#e2d5c8"),
            ("• Asesoría a productores", "Arial", 10, "normal", "#e2d5c8"),
            ("• Distribución y logística", "Arial", 10, "normal", "#e2d5c8")
        ]
        
        y_pos = 20
        for texto, fuente, tamaño, peso, color in info_empresa:
            if texto:
                lbl = Label(self.content_frame, text=texto, font=(fuente, tamaño, peso),
                              fg=color, bg="#87644b", anchor="w", justify="left")
                lbl.pack(anchor="w", padx=20, pady=(5 if tamaño < 14 else 10))
            else:
                y_pos += 15
        
        # Botón de volver (fuera del frame con scroll)
        button_frame = Frame(self.info_empresa_win, bg="#ca9e7a")
        button_frame.pack(pady=10)
        
        self.btn_volver_empresa = Button(button_frame, text="Volver al Menú", bg="#837469", fg="#ffffff",
                                     font=("Arial", 12, "bold"), command=self.info_empresa_win.destroy,
                                     cursor="hand2", width=20, height=2)
        self.btn_volver_empresa.pack()
    
    def mostrar_info_equipo(self):
        self.info_equipo_win = Toplevel(self.menu_win)
        self.info_equipo_win.title("Información del Equipo")
        self.info_equipo_win.geometry("1000x800")
        self.centrar_ventana(self.info_equipo_win, 1000, 800)
        self.info_equipo_win.configure(bg="#ca9e7a")
        self.info_equipo_win.grab_set()
        
        # Frame de título
        self.title_frame = Frame(self.info_equipo_win, bg="#87644b", width=1000, height=80)
        self.title_frame.pack()
        
        self.titulo_equipo = Label(self.title_frame, text="EQUIPO DE DESARROLLO", 
                               font=("Arial", 20, "bold"), fg="#ffffff", bg="#87644b")
        self.titulo_equipo.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame principal con scroll
        self.container = Frame(self.info_equipo_win, bg="#ca9e7a")
        self.container.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.canvas = Canvas(self.container, bg="#ca9e7a", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#ca9e7a")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Contenido dentro del frame con scroll
        self.content_frame = Frame(self.scrollable_frame, bg="#87644b", width=940)
        self.content_frame.pack(padx=20, pady=20)
        
        self.lbl_info_equipo = Label(self.content_frame, text="INFORMACIÓN DEL EQUIPO", 
                                 font=("Arial", 16, "bold"), fg="#ffffff", bg="#87644b")
        self.lbl_info_equipo.pack(pady=20)
        
        miembros = [
            {
                "nombre": "Ivis Maradiaga",
                "grado": "12° Año - Informática",
                "rol": "Líder del Proyecto"
            },
            {
                "nombre": "Jafet Rojas",
                "grado": "12° Año - Informática", 
                "rol": "Desarrollador de la Base de Datos"
            },
            {
                "nombre": "Jahir Chicas",
                "grado": "12° Año - Informática",
                "rol": "Desarrollador de Reportes"
            },
            {
                "nombre": "Pedro Bonilla",
                "grado": "12° Año - Informática",
                "rol": "Diseñadora de Sistema"
            },
            {
                "nombre": "Kevin Gomez",
                "grado": "12° Año - Informática",
                "rol": "Desarrollador de Registro"
            },
            {
                "nombre": "Jose Padilla",
                "grado": "12° Año - Informática",
                "rol": "Desarrollador de Documentación"
            }
        ]
        
        for i, miembro in enumerate(miembros, 1):
            self.member_frame = Frame(self.content_frame, bg="#837469", width=880)
            self.member_frame.pack(pady=10, padx=30, fill="x")
            
            self.lbl_miembro = Label(self.member_frame, text=f"MIEMBRO {i}:", 
                                  font=("Arial", 12, "bold"), fg="#110705", bg="#837469")
            self.lbl_miembro.pack(anchor="w", padx=10, pady=(10, 5))
            
            self.lbl_nombre = Label(self.member_frame, text=f"Nombre: {miembro['nombre']}", 
                                 font=("Arial", 11), fg="#ffffff", bg="#837469")
            self.lbl_nombre.pack(anchor="w", padx=10, pady=5)
            
            self.lbl_grado = Label(self.member_frame, text=f"Grado: {miembro['grado']}", 
                                font=("Arial", 11), fg="#e2d5c8", bg="#837469")
            self.lbl_grado.pack(anchor="w", padx=10, pady=5)
            
            self.lbl_rol = Label(self.member_frame, text=f"Rol: {miembro['rol']}", 
                              font=("Arial", 11), fg="#e2d5c8", bg="#837469")
            self.lbl_rol.pack(anchor="w", padx=10, pady=(5, 10))
        
        self.lbl_info_proyecto = Label(self.content_frame, text="INFORMACIÓN DEL PROYECTO", 
                                    font=("Arial", 14, "bold"), fg="#ffffff", bg="#87644b")
        self.lbl_info_proyecto.pack(pady=(30, 10))
        
        proyecto_info = [
            "Materia: Programación 2",
            "Profesor: Marco Tulio Madrid",
            "Institución: Instituto Marista la Inmaculada",
            "Año: 2025",
            "Tecnologías: Python, Tkinter, SQLite"
        ]
        
        for info in proyecto_info:
            self.lbl_info = Label(self.content_frame, text=f"• {info}", 
                              font=("Arial", 10), fg="#e2d5c8", bg="#87644b")
            self.lbl_info.pack(anchor="w", padx=30, pady=5)
        
        # Botón de volver (fuera del frame con scroll)
        button_frame = Frame(self.info_equipo_win, bg="#ca9e7a")
        button_frame.pack(pady=10)
        
        self.btn_volver_equipo = Button(button_frame, text="Volver al Menú", bg="#837469", fg="#ffffff",
                                    font=("Arial", 12, "bold"), command=self.info_equipo_win.destroy,
                                    cursor="hand2", width=20, height=2)
        self.btn_volver_equipo.pack()
    
    def cerrar_aplicacion(self):
        if hasattr(self, 'conexion'):
            self.conexion.close()
        self.ven.destroy()
    
    def ejecutar(self):
        self.ven.mainloop()

if __name__ == "__main__": 
    app = BodegaIvisApp()
    app.ejecutar()
