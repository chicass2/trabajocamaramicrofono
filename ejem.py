import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class BodegaIvisApp:
    def __init__(self):
        self.ven = tk.Tk()
        self.ven.title("Sistema Bodega Ivis")
        self.ven.geometry("800x600")
        self.ven.configure(bg="#2c3e50")
        
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
        for widget in self.ven.winfo_children():
            widget.destroy()
        
        login_frame = tk.Frame(self.ven, bg="#34495e", width=400, height=350)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        titulo = tk.Label(login_frame, text="BODEGA IVIS", font=("Arial", 24, "bold"), 
                         fg="#ecf0f1", bg="#34495e")
        titulo.place(x=200, y=50, anchor="center")
        
        subtitulo = tk.Label(login_frame, text="Sistema de Gestión", font=("Arial", 14), 
                            fg="#bdc3c7", bg="#34495e")
        subtitulo.place(x=200, y=85, anchor="center")
        
        lbl_usuario = tk.Label(login_frame, text="Usuario:", font=("Arial", 12), 
                              fg="#ecf0f1", bg="#34495e")
        lbl_usuario.place(x=50, y=130)
        
        self.entry_usuario = tk.Entry(login_frame, font=("Arial", 12), width=25)
        self.entry_usuario.place(x=50, y=155)
        
        lbl_password = tk.Label(login_frame, text="Contraseña:", font=("Arial", 12), 
                               fg="#ecf0f1", bg="#34495e")
        lbl_password.place(x=50, y=190)
        
        self.entry_password = tk.Entry(login_frame, font=("Arial", 12), width=25, show="*")
        self.entry_password.place(x=50, y=215)
        
        btn_login = tk.Button(login_frame, text="Ingresar", font=("Arial", 12, "bold"),
                             bg="#27ae60", fg="black", command=self.validar_login,
                             cursor="hand2", width=15)
        btn_login.place(x=200, y=260, anchor="center")
        
        info_login = tk.Label(login_frame, text="Usuario: admin | Contraseña: 123456", 
                             font=("Arial", 10), fg="#95a5a6", bg="#34495e")
        info_login.place(x=200, y=300, anchor="center")
        
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
        for widget in self.ven.winfo_children():
            widget.destroy()
        
        self.ven.geometry("1000x700")
        
        title_frame = tk.Frame(self.ven, bg="#34495e", width=1000, height=80)
        title_frame.place(x=0, y=0)
        
        titulo_menu = tk.Label(title_frame, text="SISTEMA BODEGA IVIS", font=("Arial", 24, "bold"),
                              fg="#ecf0f1", bg="#34495e")
        titulo_menu.place(x=500, y=40, anchor="center")
        
        # Botones del menú principal usando .place()
        btn_clientes = tk.Button(self.ven, text="Gestión de Clientes", font=("Arial", 12, "bold"),
                                bg="#3498db", fg="black", command=lambda: self.mostrar_crud("Clientes"),
                                cursor="hand2", width=18, height=2)
        btn_clientes.place(x=150, y=150)
        
        btn_compras = tk.Button(self.ven, text="Gestión de Compras", font=("Arial", 12, "bold"),
                               bg="#e74c3c", fg="black", command=lambda: self.mostrar_crud("Compra"),
                               cursor="hand2", width=18, height=2)
        btn_compras.place(x=400, y=150)
        
        btn_ventas = tk.Button(self.ven, text="Gestión de Ventas", font=("Arial", 12, "bold"),
                              bg="#2ecc71", fg="black", command=lambda: self.mostrar_crud("Venta"),
                              cursor="hand2", width=18, height=2)
        btn_ventas.place(x=650, y=150)
        
        btn_trabajadores = tk.Button(self.ven, text="Gestión de Trabajadores", font=("Arial", 12, "bold"),
                                    bg="#f39c12", fg="black", command=lambda: self.mostrar_crud("Trabajadores"),
                                    cursor="hand2", width=18, height=2)
        btn_trabajadores.place(x=150, y=250)
        
        btn_reportes = tk.Button(self.ven, text="Reportes", font=("Arial", 12, "bold"),
                                bg="#9b59b6", fg="black", command=self.mostrar_reportes,
                                cursor="hand2", width=18, height=2)
        btn_reportes.place(x=400, y=250)
        
        btn_info_empresa = tk.Button(self.ven, text="Info. Empresa", font=("Arial", 12, "bold"),
                                    bg="#1abc9c", fg="black", command=self.mostrar_info_empresa,
                                    cursor="hand2", width=18, height=2)
        btn_info_empresa.place(x=650, y=250)
        
        btn_info_equipo = tk.Button(self.ven, text="Info. Equipo", font=("Arial", 12, "bold"),
                                   bg="#e67e22", fg="black", command=self.mostrar_info_equipo,
                                   cursor="hand2", width=18, height=2)
        btn_info_equipo.place(x=275, y=350)
        
        btn_cerrar_sesion = tk.Button(self.ven, text="Cerrar Sesión", font=("Arial", 12, "bold"),
                                     bg="#95a5a6", fg="black", command=self.mostrar_login,
                                     cursor="hand2", width=18, height=2)
        btn_cerrar_sesion.place(x=525, y=350)
    
    def mostrar_crud(self, tabla):
        for widget in self.ven.winfo_children():
            widget.destroy()
        
        self.tabla_actual = tabla
        
        title_frame = tk.Frame(self.ven, bg="#34495e", width=1000, height=60)
        title_frame.place(x=0, y=0)
        
        titulo_crud = tk.Label(title_frame, text=f"GESTIÓN DE {tabla.upper()}", 
                              font=("Arial", 18, "bold"), fg="#ecf0f1", bg="#34495e")
        titulo_crud.place(x=500, y=30, anchor="center")
        
        # Botones de acción usando .place()
        btn_agregar = tk.Button(self.ven, text="Agregar", bg="#27ae60", fg="black",
                               font=("Arial", 10, "bold"), command=self.agregar_registro,
                               cursor="hand2", width=12)
        btn_agregar.place(x=50, y=80)
        
        btn_modificar = tk.Button(self.ven, text="Modificar", bg="#f39c12", fg="black",
                                 font=("Arial", 10, "bold"), command=self.modificar_registro,
                                 cursor="hand2", width=12)
        btn_modificar.place(x=170, y=80)
        
        btn_eliminar = tk.Button(self.ven, text="Eliminar", bg="#e74c3c", fg="black",
                                font=("Arial", 10, "bold"), command=self.eliminar_registro,
                                cursor="hand2", width=12)
        btn_eliminar.place(x=290, y=80)
        
        btn_actualizar = tk.Button(self.ven, text="Actualizar Lista", bg="#3498db", fg="black",
                                  font=("Arial", 10, "bold"), command=self.cargar_datos_tabla,
                                  cursor="hand2", width=12)
        btn_actualizar.place(x=410, y=80)
        
        btn_volver = tk.Button(self.ven, text="Volver al Menú", bg="#95a5a6", fg="black",
                              font=("Arial", 10, "bold"), command=self.mostrar_menu_principal,
                              cursor="hand2", width=12)
        btn_volver.place(x=800, y=80)
        
        # Frame para la tabla
        tree_frame = tk.Frame(self.ven, bg="#2c3e50")
        tree_frame.place(x=20, y=120, width=960, height=520)
        
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
        
        self.tree.place(x=0, y=0, width=920, height=480)
        v_scrollbar.place(x=920, y=0, height=480)
        h_scrollbar.place(x=0, y=480, width=920)
        
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
        self.ven2 = tk.Toplevel(self.ven)
        self.ven2.title(f"{accion} {self.tabla_actual}")
        self.ven2.geometry("400x500")
        self.ven2.configure(bg="#2c3e50")
        self.ven2.grab_set()
        
        titulo_form = tk.Label(self.ven2, text=f"{accion} {self.tabla_actual}", 
                              font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
        titulo_form.place(x=200, y=30, anchor="center")
        
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
        
        y_pos = 80
        for i, (label, campo) in enumerate(campos):
            lbl = tk.Label(self.ven2, text=label, font=("Arial", 10), 
                          fg="#ecf0f1", bg="#2c3e50")
            lbl.place(x=50, y=y_pos)
            
            entry = tk.Entry(self.ven2, font=("Arial", 10), width=25)
            entry.place(x=180, y=y_pos)
            
            if valores and i < len(valores):
                entry.insert(0, str(valores[i]))
            
            self.entries[campo] = entry
            y_pos += 40
        
        btn_guardar = tk.Button(self.ven2, text="Guardar", bg="#27ae60", fg="black",
                               font=("Arial", 10, "bold"), command=lambda: self.guardar_registro(accion, self.ven2),
                               cursor="hand2", width=12)
        btn_guardar.place(x=120, y=400)
        
        btn_cancelar = tk.Button(self.ven2, text="Cancelar", bg="#e74c3c", fg="black",
                                font=("Arial", 10, "bold"), command=self.ven2.destroy,
                                cursor="hand2", width=12)
        btn_cancelar.place(x=240, y=400)
    
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
        for widget in self.ven.winfo_children():
            widget.destroy()
        
        title_frame = tk.Frame(self.ven, bg="#34495e", width=1000, height=60)
        title_frame.place(x=0, y=0)
        
        titulo_reportes = tk.Label(title_frame, text="REPORTES DEL SISTEMA", 
                                  font=("Arial", 18, "bold"), fg="#ecf0f1", bg="#34495e")
        titulo_reportes.place(x=500, y=30, anchor="center")
        
        btn_rep_clientes = tk.Button(self.ven, text="Reporte de Clientes", bg="#3498db", fg="black",
                                    font=("Arial", 12, "bold"), command=lambda: self.generar_reporte("Clientes"),
                                    cursor="hand2", width=20, height=2)
        btn_rep_clientes.place(x=400, y=150, anchor="center")
        
        btn_rep_ventas = tk.Button(self.ven, text="Reporte de Ventas", bg="#2ecc71", fg="black",
                                  font=("Arial", 12, "bold"), command=lambda: self.generar_reporte("Venta"),
                                  cursor="hand2", width=20, height=2)
        btn_rep_ventas.place(x=400, y=220, anchor="center")
        
        btn_rep_general = tk.Button(self.ven, text="Reporte General", bg="#9b59b6", fg="black",
                                   font=("Arial", 12, "bold"), command=self.reporte_general,
                                   cursor="hand2", width=20, height=2)
        btn_rep_general.place(x=400, y=290, anchor="center")
        
        btn_volver_reportes = tk.Button(self.ven, text="Volver al Menú", bg="#95a5a6", fg="black",
                                       font=("Arial", 12, "bold"), command=self.mostrar_menu_principal,
                                       cursor="hand2", width=20, height=2)
        btn_volver_reportes.place(x=400, y=380, anchor="center")
    
    def generar_reporte(self, tabla):
        self.ven3 = tk.Toplevel(self.ven)
        self.ven3.title(f"Reporte de {tabla}")
        self.ven3.geometry("800x600")
        self.ven3.configure(bg="#2c3e50")
        
        titulo_reporte = tk.Label(self.ven3, text=f"REPORTE DE {tabla.upper()}", 
                                 font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
        titulo_reporte.place(x=400, y=30, anchor="center")
        
        tree_frame = tk.Frame(self.ven3, bg="#2c3e50")
        tree_frame.place(x=20, y=70, width=760, height=450)
        
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
        
        tree.place(x=0, y=0, width=720, height=450)
        scrollbar.place(x=720, y=0, height=450)
        
        try:
            self.cursor.execute(f"SELECT * FROM {tabla}")
            registros = self.cursor.fetchall()
            
            for registro in registros:
                tree.insert("", "end", values=registro)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error generando reporte: {e}")
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        lbl_fecha = tk.Label(self.ven3, text=f"Fecha de generación: {fecha_actual}", 
                            font=("Arial", 10), fg="#bdc3c7", bg="#2c3e50")
        lbl_fecha.place(x=20, y=530)
        
        lbl_total = tk.Label(self.ven3, text=f"Total de registros: {len(registros)}", 
                            font=("Arial", 10), fg="#bdc3c7", bg="#2c3e50")
        lbl_total.place(x=20, y=550)
        
        btn_imprimir = tk.Button(self.ven3, text="Preparar para Impresión", bg="#e74c3c", fg="black",
                                font=("Arial", 10, "bold"), command=lambda: self.preparar_impresion(tabla),
                                cursor="hand2", width=20)
        btn_imprimir.place(x=400, y=570, anchor="center")
    
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
            
            self.ven4 = tk.Toplevel(self.ven)
            self.ven4.title(f"Reporte para Impresión - {tabla}")
            self.ven4.geometry("600x400")
            
            text_widget = tk.Text(self.ven4, wrap=tk.WORD, font=("Courier", 10))
            text_widget.insert("1.0", contenido)
            text_widget.config(state=tk.DISABLED)
            
            scrollbar = ttk.Scrollbar(self.ven4, command=text_widget.yview)
            text_widget.config(yscrollcommand=scrollbar.set)
            
            text_widget.place(x=0, y=0, width=570, height=400)
            scrollbar.place(x=570, y=0, height=400)
            
            messagebox.showinfo("Información", "Reporte preparado para impresión")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error preparando reporte: {e}")
    
    def reporte_general(self):
        self.ven5 = tk.Toplevel(self.ven)
        self.ven5.title("Reporte General del Sistema")
        self.ven5.geometry("600x500")
        self.ven5.configure(bg="#2c3e50")
        
        titulo_general = tk.Label(self.ven5, text="REPORTE GENERAL DEL SISTEMA", 
                                 font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
        titulo_general.place(x=300, y=30, anchor="center")
        
        stats_frame = tk.Frame(self.ven5, bg="#34495e", width=540, height=350)
        stats_frame.place(x=30, y=70)
        
        try:
            tablas = ["Clientes", "Compra", "Venta", "Trabajadores"]
            estadisticas = {}
            
            for tabla in tablas:
                self.cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = self.cursor.fetchone()[0]
                estadisticas[tabla] = count
            
            lbl_estadisticas = tk.Label(stats_frame, text="ESTADÍSTICAS DEL SISTEMA", 
                                       font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#34495e")
            lbl_estadisticas.place(x=270, y=30, anchor="center")
            
            y_pos = 80
            for tabla, count in estadisticas.items():
                lbl_stat = tk.Label(stats_frame, text=f"Total {tabla}: {count} registros", 
                                   font=("Arial", 12), fg="#bdc3c7", bg="#34495e")
                lbl_stat.place(x=30, y=y_pos)
                y_pos += 30
            
            lbl_info_adicional = tk.Label(stats_frame, text="INFORMACIÓN ADICIONAL", 
                                         font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#34495e")
            lbl_info_adicional.place(x=30, y=y_pos + 20)
            
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            lbl_fecha_reporte = tk.Label(stats_frame, text=f"Fecha de generación: {fecha_actual}", 
                                        font=("Arial", 10), fg="#bdc3c7", bg="#34495e")
            lbl_fecha_reporte.place(x=30, y=y_pos + 50)
            
            total_registros = sum(estadisticas.values())
            lbl_total_reg = tk.Label(stats_frame, text=f"Total de registros en el sistema: {total_registros}", 
                                    font=("Arial", 10), fg="#bdc3c7", bg="#34495e")
            lbl_total_reg.place(x=30, y=y_pos + 80)
            
        except sqlite3.Error as e:
            lbl_error = tk.Label(stats_frame, text=f"Error generando estadísticas: {e}", 
                                font=("Arial", 12), fg="#e74c3c", bg="#34495e")
            lbl_error.place(x=30, y=80)
        
        btn_volver_reporte = tk.Button(self.ven5, text="Volver al Menú", bg="#95a5a6", fg="black",
                                     font=("Arial", 12, "bold"), command=self.ven5.destroy,
                                     cursor="hand2", width=15)
        btn_volver_reporte.place(x=300, y=440, anchor="center")
    
    def mostrar_info_empresa(self):
        for widget in self.ven.winfo_children():
            widget.destroy()
        
        title_frame = tk.Frame(self.ven, bg="#34495e", width=1000, height=80)
        title_frame.place(x=0, y=0)
        
        titulo_empresa = tk.Label(title_frame, text="INFORMACIÓN DE LA EMPRESA", 
                                font=("Arial", 20, "bold"), fg="#ecf0f1", bg="#34495e")
        titulo_empresa.place(x=500, y=40, anchor="center")
        
        content_frame = tk.Frame(self.ven, bg="#34495e", width=940, height=500)
        content_frame.place(x=30, y=100)
        
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
        
        y_pos = 20
        for texto, fuente, tamaño, peso, color in info_empresa:
            if texto:
                lbl = tk.Label(content_frame, text=texto, font=(fuente, tamaño, peso),
                              fg=color, bg="#34495e")
                lbl.place(x=20, y=y_pos)
                y_pos += 25 if tamaño < 14 else 30
            else:
                y_pos += 15
        
        btn_volver_empresa = tk.Button(self.ven, text="Volver al Menú Principal", bg="#95a5a6", fg="black",
                                     font=("Arial", 12, "bold"), command=self.mostrar_menu_principal,
                                     cursor="hand2", width=20, height=2)
        btn_volver_empresa.place(x=500, y=620, anchor="center")
    
    def mostrar_info_equipo(self):
        for widget in self.ven.winfo_children():
            widget.destroy()
        
        title_frame = tk.Frame(self.ven, bg="#34495e", width=1000, height=80)
        title_frame.place(x=0, y=0)
        
        titulo_equipo = tk.Label(title_frame, text="EQUIPO DE DESARROLLO", 
                               font=("Arial", 20, "bold"), fg="#ecf0f1", bg="#34495e")
        titulo_equipo.place(x=500, y=40, anchor="center")
        
        content_frame = tk.Frame(self.ven, bg="#34495e", width=940, height=500)
        content_frame.place(x=30, y=100)
        
        lbl_info_equipo = tk.Label(content_frame, text="INFORMACIÓN DEL EQUIPO", 
                                 font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#34495e")
        lbl_info_equipo.place(x=470, y=20, anchor="center")
        
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
        
        y_pos = 60
        for i, miembro in enumerate(miembros, 1):
            member_frame = tk.Frame(content_frame, bg="#2c3e50", width=880, height=100)
            member_frame.place(x=30, y=y_pos)
            
            lbl_miembro = tk.Label(member_frame, text=f"MIEMBRO {i}:", 
                                  font=("Arial", 12, "bold"), fg="#3498db", bg="#2c3e50")
            lbl_miembro.place(x=20, y=10)
            
            lbl_nombre = tk.Label(member_frame, text=f"Nombre: {miembro['nombre']}", 
                                 font=("Arial", 11), fg="#ecf0f1", bg="#2c3e50")
            lbl_nombre.place(x=20, y=40)
            
            lbl_grado = tk.Label(member_frame, text=f"Grado: {miembro['grado']}", 
                                font=("Arial", 11), fg="#bdc3c7", bg="#2c3e50")
            lbl_grado.place(x=20, y=65)
            
            lbl_rol = tk.Label(member_frame, text=f"Rol: {miembro['rol']}", 
                              font=("Arial", 11), fg="#bdc3c7", bg="#2c3e50")
            lbl_rol.place(x=20, y=90)
            
            y_pos += 120
        
        lbl_info_proyecto = tk.Label(content_frame, text="INFORMACIÓN DEL PROYECTO", 
                                    font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#34495e")
        lbl_info_proyecto.place(x=30, y=y_pos + 20)
        
        proyecto_info = [
            "Materia: Programación 2",
            "Profesor: Marco Tulio Madrid",
            "Institución: Instituto Marista la Inmaculada",
            "Año: 2025",
            "Tecnologías: Python, Tkinter, SQLite"
        ]
        
        y_pos += 60
        for info in proyecto_info:
            lbl_info = tk.Label(content_frame, text=f"• {info}", 
                              font=("Arial", 10), fg="#bdc3c7", bg="#34495e")
            lbl_info.place(x=50, y=y_pos)
            y_pos += 25
        
        btn_volver_equipo = tk.Button(self.ven, text="Volver al Menú Principal", bg="#95a5a6", fg="black",
                                    font=("Arial", 12, "bold"), command=self.mostrar_menu_principal,
                                    cursor="hand2", width=20, height=2)
        btn_volver_equipo.place(x=500, y=620, anchor="center")
    
    def ejecutar(self):
        self.ven.mainloop()
    
    def __del__(self):
        if hasattr(self, 'conexion'):
            self.conexion.close()

if __name__ == "__main__": 
    app = BodegaIvisApp()
    app.ejecutar()
        