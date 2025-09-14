import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class BodegaIvisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Bodega Ivis")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        self.inicializar_bd()
        
        self.mostrar_login()
        
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
        for widget in self.root.winfo_children():
            widget.destroy()
        
        login_frame = tk.Frame(self.root, bg="#34495e", padx=50, pady=50)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(login_frame, text="BODEGA IVIS", font=("Arial", 24, "bold"), 
                fg="#ecf0f1", bg="#34495e").pack(pady=20)
        
        tk.Label(login_frame, text="Sistema de Gestión", font=("Arial", 14), 
                fg="#bdc3c7", bg="#34495e").pack(pady=(0, 30))
        
        tk.Label(login_frame, text="Usuario:", font=("Arial", 12), 
                fg="#ecf0f1", bg="#34495e").pack(anchor="w")
        self.entry_usuario = tk.Entry(login_frame, font=("Arial", 12), width=25)
        self.entry_usuario.pack(pady=(5, 15))
        
        tk.Label(login_frame, text="Contraseña:", font=("Arial", 12), 
                fg="#ecf0f1", bg="#34495e").pack(anchor="w")
        self.entry_password = tk.Entry(login_frame, font=("Arial", 12), width=25, show="*")
        self.entry_password.pack(pady=(5, 25))
        
        btn_login = tk.Button(login_frame, text="Ingresar", font=("Arial", 12, "bold"),
                             bg="#27ae60", fg="black", command=self.validar_login,
                             cursor="hand2", padx=20, pady=5)
        btn_login.pack()
        
        tk.Label(login_frame, text="Usuario: admin | Contraseña: 123456", 
                font=("Arial", 10), fg="#95a5a6", bg="#34495e").pack(pady=(20, 0))
        
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
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
                self.entry_password.delete(0, tk.END)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {e}")
    
    def mostrar_menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("1000x700")
        
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True)
        
        title_frame = tk.Frame(main_frame, bg="#34495e", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="SISTEMA BODEGA IVIS", font=("Arial", 24, "bold"),
                fg="#ecf0f1", bg="#34495e").pack(expand=True)
        
        buttons_frame = tk.Frame(main_frame, bg="#2c3e50")
        buttons_frame.pack(expand=True, fill="both", padx=50, pady=30)
        
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        
        botones = [
            ("Gestión de Clientes", "#3498db", lambda: self.mostrar_crud("Clientes")),
            ("Gestión de Compras", "#e74c3c", lambda: self.mostrar_crud("Compra")),
            ("Gestión de Ventas", "#2ecc71", lambda: self.mostrar_crud("Venta")),
            ("Gestión de Trabajadores", "#f39c12", lambda: self.mostrar_crud("Trabajadores")),
            ("Reportes", "#9b59b6", self.mostrar_reportes),
            ("Info. Empresa", "#1abc9c", self.mostrar_info_empresa),
            ("Info. Equipo", "#e67e22", self.mostrar_info_equipo),
            ("Cerrar Sesión", "#95a5a6", self.mostrar_login)
        ]
        
        for i, (texto, color, comando) in enumerate(botones):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(buttons_frame, text=texto, font=("Arial", 12, "bold"),
                           bg=color, fg="black", command=comando,
                           cursor="hand2", padx=20, pady=15, width=18)
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="ew")
    
    def mostrar_crud(self, tabla):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.tabla_actual = tabla
        
        crud_frame = tk.Frame(self.root, bg="#2c3e50")
        crud_frame.pack(fill="both", expand=True)
        
        title_frame = tk.Frame(crud_frame, bg="#34495e", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text=f"GESTIÓN DE {tabla.upper()}", 
                font=("Arial", 18, "bold"), fg="#ecf0f1", bg="#34495e").pack(expand=True)
        
        action_frame = tk.Frame(crud_frame, bg="#2c3e50")
        action_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(action_frame, text="Agregar", bg="#27ae60", fg="black",
                 font=("Arial", 10, "bold"), command=self.agregar_registro,
                 cursor="hand2", padx=15).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Modificar", bg="#f39c12", fg="black",
                 font=("Arial", 10, "bold"), command=self.modificar_registro,
                 cursor="hand2", padx=15).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Eliminar", bg="#e74c3c", fg="black",
                 font=("Arial", 10, "bold"), command=self.eliminar_registro,
                 cursor="hand2", padx=15).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Actualizar Lista", bg="#3498db", fg="black",
                 font=("Arial", 10, "bold"), command=self.cargar_datos_tabla,
                 cursor="hand2", padx=15).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Volver al Menú", bg="#95a5a6", fg="black",
                 font=("Arial", 10, "bold"), command=self.mostrar_menu_principal,
                 cursor="hand2", padx=15).pack(side="right", padx=5)
        
        tree_frame = tk.Frame(crud_frame, bg="#2c3e50")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if tabla == "Clientes":
            columnas = ("DNI_Cliente", "Nombre", "Telefono", "Direccion")
        elif tabla == "Compra":
            columnas = ("Codigo_Compra", "DNI_Cliente", "Tipo_de_cafe", "Humedad", "Peso")
        elif tabla == "Venta":
            columnas = ("Codigo_Venta", "Comprador", "Venta", "Tipo_de_cafe", "Precio", "Fecha_Entrega")
        elif tabla == "Trabajadores":
            columnas = ("ID_Trabajador", "Nombres", "Apellidos", "Edad", "Sueldo", "Fecha_Contrato")
        
        self.tree = ttk.Treeview(tree_frame, columns=columnas, show="headings")
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
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
        form_window = tk.Toplevel(self.root)
        form_window.title(f"{accion} {self.tabla_actual}")
        form_window.geometry("400x500")
        form_window.configure(bg="#2c3e50")
        form_window.grab_set()
        
        tk.Label(form_window, text=f"{accion} {self.tabla_actual}", 
                font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(pady=20)
        
        fields_frame = tk.Frame(form_window, bg="#2c3e50")
        fields_frame.pack(padx=30, pady=20, fill="both", expand=True)
        
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
        
        for i, (label, campo) in enumerate(campos):
            tk.Label(fields_frame, text=label, font=("Arial", 10), 
                    fg="#ecf0f1", bg="#2c3e50").grid(row=i, column=0, sticky="w", pady=5)
            
            entry = tk.Entry(fields_frame, font=("Arial", 10), width=25)
            entry.grid(row=i, column=1, pady=5, padx=(10, 0))
            
            if valores and i < len(valores):
                entry.insert(0, str(valores[i]))
            
            self.entries[campo] = entry
        
        btn_frame = tk.Frame(form_window, bg="#2c3e50")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Guardar", bg="#27ae60", fg="black",
                 font=("Arial", 10, "bold"), command=lambda: self.guardar_registro(accion, ventana),
                 cursor="hand2", padx=20).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Cancelar", bg="#e74c3c", fg="black",
                 font=("Arial", 10, "bold"), command=form_window.destroy,
                 cursor="hand2", padx=20).pack(side="left", padx=10)
    
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
        for widget in self.root.winfo_children():
            widget.destroy()
        
        report_frame = tk.Frame(self.root, bg="#2c3e50")
        report_frame.pack(fill="both", expand=True)
        
        title_frame = tk.Frame(report_frame, bg="#34495e", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="REPORTES DEL SISTEMA", 
                font=("Arial", 18, "bold"), fg="#ecf0f1", bg="#34495e").pack(expand=True)
        
        btn_frame = tk.Frame(report_frame, bg="#2c3e50")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="Reporte de Clientes", bg="#3498db", fg="black",
                 font=("Arial", 12, "bold"), command=lambda: self.generar_reporte("Clientes"),
                 cursor="hand2", padx=20, pady=10, width=20).pack(pady=10)
        
        tk.Button(btn_frame, text="Reporte de Ventas", bg="#2ecc71", fg="black",
                 font=("Arial", 12, "bold"), command=lambda: self.generar_reporte("Venta"),
                 cursor="hand2", padx=20, pady=10, width=20).pack(pady=10)
        
        tk.Button(btn_frame, text="Reporte General", bg="#9b59b6", fg="black",
                 font=("Arial", 12, "bold"), command=self.reporte_general,
                 cursor="hand2", padx=20, pady=10, width=20).pack(pady=10)
        
        tk.Button(btn_frame, text="Volver al Menú", bg="#95a5a6", fg="black",
                 font=("Arial", 12, "bold"), command=self.mostrar_menu_principal,
                 cursor="hand2", padx=20, pady=10, width=20).pack(pady=20)
    
    def generar_reporte(self, tabla):
        report_window = tk.Toplevel(self.root)
        report_window.title(f"Reporte de {tabla}")
        report_window.geometry("800x600")
        report_window.configure(bg="#2c3e50")
        
        tk.Label(report_window, text=f"REPORTE DE {tabla.upper()}", 
                font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(pady=20)
        
        tree_frame = tk.Frame(report_window, bg="#2c3e50")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if tabla == "Clientes":
            columnas = ("DNI_Cliente", "Nombre", "Telefono", "Direccion")
        elif tabla == "Venta":
            columnas = ("Codigo_Venta", "Comprador", "Venta", "Tipo_de_cafe", "Precio", "Fecha_Entrega")
        
        tree = ttk.Treeview(tree_frame, columns=columnas, show="headings")
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        try:
            self.cursor.execute(f"SELECT * FROM {tabla}")
            registros = self.cursor.fetchall()
            
            for registro in registros:
                tree.insert("", "end", values=registro)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error generando reporte: {e}")
        
        info_frame = tk.Frame(report_window, bg="#2c3e50")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        tk.Label(info_frame, text=f"Fecha de generación: {fecha_actual}", 
                font=("Arial", 10), fg="#bdc3c7", bg="#2c3e50").pack(anchor="w")
        tk.Label(info_frame, text=f"Total de registros: {len(registros)}", 
                font=("Arial", 10), fg="#bdc3c7", bg="#2c3e50").pack(anchor="w")
        
        tk.Button(report_window, text="Preparar para Impresión", bg="#e74c3c", fg="black",
                 font=("Arial", 10, "bold"), command=lambda: self.preparar_impresion(tabla),
                 cursor="hand2", padx=20, pady=5).pack(pady=10)
    
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
            
            print_window = tk.Toplevel(self.root)
            print_window.title(f"Reporte para Impresión - {tabla}")
            print_window.geometry("600x400")
            
            text_widget = tk.Text(print_window, wrap=tk.WORD, font=("Courier", 10))
            text_widget.insert("1.0", contenido)
            text_widget.config(state=tk.DISABLED)
            
            scrollbar = ttk.Scrollbar(print_window, command=text_widget.yview)
            text_widget.config(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            messagebox.showinfo("Información", "Reporte preparado para impresión")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error preparando reporte: {e}")
    
    def reporte_general(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Reporte General del Sistema")
        report_window.geometry("600x500")
        report_window.configure(bg="#2c3e50")
        
        tk.Label(report_window, text="REPORTE GENERAL DEL SISTEMA", 
                font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(pady=20)
        
        stats_frame = tk.Frame(report_window, bg="#34495e", padx=30, pady=20)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        try:
            tablas = ["Clientes", "Compra", "Venta", "Trabajadores"]
            estadisticas = {}
            
            for tabla in tablas:
                self.cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = self.cursor.fetchone()[0]
                estadisticas[tabla] = count
            
            tk.Label(stats_frame, text="ESTADÍSTICAS DEL SISTEMA", 
                    font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=(0, 20))
            
            for tabla, count in estadisticas.items():
                tk.Label(stats_frame, text=f"Total {tabla}: {count} registros", 
                        font=("Arial", 12), fg="#bdc3c7", bg="#34495e").pack(anchor="w", pady=5)
            
            tk.Label(stats_frame, text="\nINFORMACIÓN ADICIONAL", 
                    font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=(20, 10))
            
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            tk.Label(stats_frame, text=f"Fecha de generación: {fecha_actual}", 
                    font=("Arial", 10), fg="#bdc3c7", bg="#34495e").pack(anchor="w", pady=2)
            
            total_registros = sum(estadisticas.values())
            tk.Label(stats_frame, text=f"Total de registros en el sistema: {total_registros}", 
                    font=("Arial", 10), fg="#bdc3c7", bg="#34495e").pack(anchor="w", pady=2)
            
        except sqlite3.Error as e:
            tk.Label(stats_frame, text=f"Error generando estadísticas: {e}", 
                    font=("Arial", 12), fg="#e74c3c", bg="#34495e").pack()
    
    def mostrar_info_empresa(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        info_frame = tk.Frame(self.root, bg="#2c3e50")
        info_frame.pack(fill="both", expand=True)
        
        title_frame = tk.Frame(info_frame, bg="#34495e", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="INFORMACIÓN DE LA EMPRESA", 
                font=("Arial", 20, "bold"), fg="#ecf0f1", bg="#34495e").pack(expand=True)
        
        content_frame = tk.Frame(info_frame, bg="#34495e", padx=50, pady=30)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        info_empresa = [
            ("BODEGA IVIS", "Arial", 24, "bold", "#ecf0f1"),
            ("Empresa dedicada al procesamiento y comercialización de café", "Arial", 12, "normal", "#bdc3c7"),
            ("", "", 0, "", ""),
            ("Año de Fundación: 2020", "Arial", 12, "bold", "#ecf0f1"),
            ("", "", 0, "", ""),
            ("MISIÓN:", "Arial", 14, "bold", "#ecf0f1"),
            ("Proporcionar café de la más alta calidad, apoyando a", "Arial", 10, "normal", "#bdc3c7"),
            ("los productores locales y satisfaciendo las necesidades", "Arial", 10, "normal", "#bdc3c7"),
            ("de nuestros clientes con excelencia y compromiso.", "Arial", 10, "normal", "#bdc3c7"),
            ("", "", 0, "", ""),
            ("VISIÓN:", "Arial", 14, "bold", "#ecf0f1"),
            ("Ser la empresa líder en el sector cafetero de la región,", "Arial", 10, "normal", "#bdc3c7"),
            ("reconocida por la calidad de nuestros productos y", "Arial", 10, "normal", "#bdc3c7"),
            ("nuestro compromiso con el desarrollo sostenible.", "Arial", 10, "normal", "#bdc3c7"),
            ("", "", 0, "", ""),
            ("VALORES:", "Arial", 14, "bold", "#ecf0f1"),
            ("• Calidad en todos nuestros procesos", "Arial", 10, "normal", "#bdc3c7"),
            ("• Compromiso con nuestros clientes", "Arial", 10, "normal", "#bdc3c7"),
            ("• Respeto por el medio ambiente", "Arial", 10, "normal", "#bdc3c7"),
            ("• Desarrollo de la comunidad local", "Arial", 10, "normal", "#bdc3c7"),
            ("", "", 0, "", ""),
            ("SERVICIOS:", "Arial", 14, "bold", "#ecf0f1"),
            ("• Compra y venta de café en grano", "Arial", 10, "normal", "#bdc3c7"),
            ("• Procesamiento y almacenamiento", "Arial", 10, "normal", "#bdc3c7"),
            ("• Asesoría a productores", "Arial", 10, "normal", "#bdc3c7"),
            ("• Distribución y logística", "Arial", 10, "normal", "#bdc3c7")
        ]
        
        for texto, fuente, tamaño, peso, color in info_empresa:
            if texto:
                tk.Label(content_frame, text=texto, font=(fuente, tamaño, peso),
                        fg=color, bg="#34495e").pack(anchor="w", pady=2)
            else:
                tk.Label(content_frame, text="", bg="#34495e").pack(pady=5)
        
        tk.Button(info_frame, text="Volver al Menú Principal", bg="#95a5a6", fg="black",
                 font=("Arial", 12, "bold"), command=self.mostrar_menu_principal,
                 cursor="hand2", padx=20, pady=10).pack(pady=20)
    
    def mostrar_info_equipo(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        team_frame = tk.Frame(self.root, bg="#2c3e50")
        team_frame.pack(fill="both", expand=True)
        
        title_frame = tk.Frame(team_frame, bg="#34495e", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="EQUIPO DE DESARROLLO", 
                font=("Arial", 20, "bold"), fg="#ecf0f1", bg="#34495e").pack(expand=True)
        
        content_frame = tk.Frame(team_frame, bg="#34495e", padx=50, pady=30)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(content_frame, text="INFORMACIÓN DEL EQUIPO", 
                font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=(0, 20))
        
        miembros = [
            {
                "nombre": "Juan Carlos Pérez",
                "grado": "12° Año - Informática",
                "rol": "Líder del Proyecto y Desarrollador Principal"
            },
            {
                "nombre": "María José Rodríguez",
                "grado": "12° Año - Informática", 
                "rol": "Desarrolladora de Interfaz y Base de Datos"
            },
            {
                "nombre": "Carlos Alberto Martínez",
                "grado": "12° Año - Informática",
                "rol": "Desarrollador de Reportes y Documentación"
            },
            {
                "nombre": "Ana Sofía López",
                "grado": "12° Año - Informática",
                "rol": "Diseñadora de Sistema y Testing"
            }
        ]
        
        for i, miembro in enumerate(miembros, 1):
            member_frame = tk.Frame(content_frame, bg="#2c3e50", padx=20, pady=15)
            member_frame.pack(fill="x", pady=10)
            
            tk.Label(member_frame, text=f"MIEMBRO {i}:", 
                    font=("Arial", 12, "bold"), fg="#3498db", bg="#2c3e50").pack(anchor="w")
            
            tk.Label(member_frame, text=f"Nombre: {miembro['nombre']}", 
                    font=("Arial", 11), fg="#ecf0f1", bg="#2c3e50").pack(anchor="w", pady=2)
            
            tk.Label(member_frame, text=f"Grado: {miembro['grado']}", 
                    font=("Arial", 11), fg="#bdc3c7", bg="#2c3e50").pack(anchor="w", pady=2)
            
            tk.Label(member_frame, text=f"Rol: {miembro['rol']}", 
                    font=("Arial", 11), fg="#bdc3c7", bg="#2c3e50").pack(anchor="w", pady=2)
        
        tk.Label(content_frame, text="\nINFORMACIÓN DEL PROYECTO", 
                font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=(20, 10))
        
        proyecto_info = [
            "Materia: Programación 2",
            "Profesor: Marco Tulio Madrid",
            "Institución: Instituto Marista la Inmaculada",
            "Año: 2025",
            "Tecnologías: Python, Tkinter, SQLite"
        ]
        
        for info in proyecto_info:
            tk.Label(content_frame, text=f"• {info}", 
                    font=("Arial", 10), fg="#bdc3c7", bg="#34495e").pack(anchor="w", pady=2)
        
        tk.Button(team_frame, text="Volver al Menú Principal", bg="#95a5a6", fg="black",
                 font=("Arial", 12, "bold"), command=self.mostrar_menu_principal,
                 cursor="hand2", padx=20, pady=10).pack(pady=20)
    
    def ejecutar(self):
        self.root.mainloop()
    
    def __del__(self):
        if hasattr(self, 'conexion'):
            self.conexion.close()

if __name__ == "__main__":
    app = BodegaIvisApp()
    app.ejecutar()