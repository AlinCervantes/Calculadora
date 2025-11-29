import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from calculadora import Calculadora
import math

class InterfazCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica Profesional")
        
        # Configuración de tamaño
        self.root.minsize(400, 600)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = min(int(screen_width * 0.35), 550)
        window_height = min(int(screen_height * 0.75), 850)
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#1e1e2e")
        
        self.MAX_CARACTERES = 15
        
        # Instancia de la calculadora
        self.calc = Calculadora()
        
        # Variables para la pantalla
        self.pantalla_texto = ""
        self.operacion_actual = None
        self.primer_numero = None
        self.resetear_pantalla = False
        
        self.root.bind('<Configure>', self.on_resize)
        
        self.crear_widgets()
        self.configurar_teclado()
    
    def crear_widgets(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== PANTALLA =====
        pantalla_frame = tk.Frame(self.main_frame, bg="#2d2d44", bd=2, relief=tk.RIDGE)
        pantalla_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.pantalla_operacion = tk.Label(
            pantalla_frame,
            text="",
            font=("Segoe UI", 11),
            bg="#2d2d44",
            fg="#9ca3af",
            anchor=tk.E,
            padx=10,
            pady=3
        )
        self.pantalla_operacion.pack(fill=tk.X)
        
        self.pantalla = tk.Label(
            pantalla_frame,
            text="0",
            font=("Segoe UI", 32, "bold"),
            bg="#2d2d44",
            fg="#ffffff",
            anchor=tk.E,
            padx=10,
            pady=10
        )
        self.pantalla.pack(fill=tk.X)
        
        self.label_limite = tk.Label(
            pantalla_frame,
            text=f"0/{self.MAX_CARACTERES}",
            font=("Segoe UI", 8),
            bg="#2d2d44",
            fg="#6b7280",
            anchor=tk.E,
            padx=10,
            pady=2
        )
        self.label_limite.pack(fill=tk.X)
        
        # ===== PESTAÑAS =====
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Estilo para pestañas
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background="#1e1e2e", borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background="#374151", 
                       foreground="#ffffff",
                       padding=[20, 10],
                       font=("Segoe UI", 10, "bold"))
        style.map('TNotebook.Tab',
                 background=[('selected', "#6366f1")],
                 foreground=[('selected', "#ffffff")])
        
        # Pestaña Básica
        self.tab_basica = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.tab_basica, text="Básica")
        self.crear_botones_basicos()
        
        # Pestaña Científica
        self.tab_cientifica = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.tab_cientifica, text="Científica")
        self.crear_botones_cientificos()
        
        # ===== HISTORIAL =====
        historial_label = tk.Label(
            self.main_frame,
            text="📋 Historial",
            font=("Segoe UI", 11, "bold"),
            bg="#1e1e2e",
            fg="#ffffff"
        )
        historial_label.pack(pady=(5, 5))
        
        historial_frame = tk.Frame(self.main_frame, bg="#2d2d44", bd=2, relief=tk.RIDGE)
        historial_frame.pack(fill=tk.BOTH, expand=True)
        
        self.texto_historial = scrolledtext.ScrolledText(
            historial_frame,
            font=("Consolas", 9),
            bg="#2d2d44",
            fg="#e5e7eb",
            wrap=tk.WORD,
            bd=0,
            insertbackground="#6366f1",
            height=6
        )
        self.texto_historial.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.texto_historial.config(state=tk.DISABLED)
        
        self.btn_limpiar_hist = tk.Button(
            self.main_frame,
            text="🗑️ Limpiar Historial",
            font=("Segoe UI", 9, "bold"),
            bg="#dc2626",
            fg="#ffffff",
            activebackground="#b91c1c",
            bd=0,
            cursor="hand2",
            command=self.limpiar_historial,
            pady=6
        )
        self.btn_limpiar_hist.pack(fill=tk.X, pady=(5, 0))
    
    def crear_botones_basicos(self):
        self.botones_frame = tk.Frame(self.tab_basica, bg="#1e1e2e")
        self.botones_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for i in range(5):
            self.botones_frame.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4):
            self.botones_frame.grid_columnconfigure(i, weight=1, uniform="col")
        
        botones = [
            ("C", 0, 0, 1, "#ef4444", "#ffffff", self.limpiar),
            ("⌫", 0, 1, 1, "#f59e0b", "#ffffff", self.borrar),
            ("%", 0, 2, 1, "#6366f1", "#ffffff", lambda: self.agregar_operador("%")),
            ("÷", 0, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("÷")),
            
            ("7", 1, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("7")),
            ("8", 1, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("8")),
            ("9", 1, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("9")),
            ("×", 1, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("×")),
            
            ("4", 2, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("4")),
            ("5", 2, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("5")),
            ("6", 2, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("6")),
            ("-", 2, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("-")),
            
            ("1", 3, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("1")),
            ("2", 3, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("2")),
            ("3", 3, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("3")),
            ("+", 3, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("+")),
            
            ("0", 4, 0, 2, "#374151", "#ffffff", lambda: self.agregar_numero("0")),
            (".", 4, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero(".")),
            ("=", 4, 3, 1, "#10b981", "#ffffff", self.calcular),
        ]
        
        self.botones = {}
        for texto, fila, col, colspan, bg, fg, cmd in botones:
            btn = tk.Button(
                self.botones_frame,
                text=texto,
                font=("Segoe UI", 16, "bold"),
                bg=bg,
                fg=fg,
                activebackground=self.color_hover(bg),
                activeforeground=fg,
                bd=0,
                cursor="hand2",
                command=cmd
            )
            btn.grid(row=fila, column=col, columnspan=colspan, 
                    sticky="nsew", padx=2, pady=2)
            
            btn.bind("<Enter>", lambda e, b=btn, c=bg: b.configure(bg=self.color_hover(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))
            
            self.botones[texto] = btn
    
    def crear_botones_cientificos(self):
        self.cientificos_frame = tk.Frame(self.tab_cientifica, bg="#1e1e2e")
        self.cientificos_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for i in range(8):
            self.cientificos_frame.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4):
            self.cientificos_frame.grid_columnconfigure(i, weight=1, uniform="col")
        
        botones_cient = [
            # Fila 0 - Trigonométricas
            ("sin", 0, 0, 1, "#8b5cf6", "#ffffff", lambda: self.funcion_cientifica("sin")),
            ("cos", 0, 1, 1, "#8b5cf6", "#ffffff", lambda: self.funcion_cientifica("cos")),
            ("tan", 0, 2, 1, "#8b5cf6", "#ffffff", lambda: self.funcion_cientifica("tan")),
            ("π", 0, 3, 1, "#ec4899", "#ffffff", self.insertar_pi),
            
            # Fila 1 - Inversas trigonométricas
            ("asin", 1, 0, 1, "#8b5cf6", "#ffffff", lambda: self.funcion_cientifica("asin")),
            ("acos", 1, 1, 1, "#8b5cf6", "#ffffff", lambda: self.funcion_cientifica("acos")),
            ("atan", 1, 2, 1, "#8b5cf6", "#ffffff", lambda: self.funcion_cientifica("atan")),
            ("1/x", 1, 3, 1, "#ec4899", "#ffffff", lambda: self.funcion_cientifica("inv")),
            
            # Fila 2 - Potencias y raíces
            ("x²", 2, 0, 1, "#10b981", "#ffffff", lambda: self.potencia(2)),
            ("xⁿ", 2, 1, 1, "#10b981", "#ffffff", self.potencia_n),
            ("√", 2, 2, 1, "#10b981", "#ffffff", lambda: self.funcion_cientifica("sqrt")),
            ("ⁿ√", 2, 3, 1, "#10b981", "#ffffff", self.raiz_n),
            
            # Fila 3 - Logaritmos y exponencial
            ("ln", 3, 0, 1, "#f59e0b", "#ffffff", lambda: self.funcion_cientifica("ln")),
            ("eˣ", 3, 1, 1, "#f59e0b", "#ffffff", lambda: self.funcion_cientifica("exp")),
            ("C", 3, 2, 1, "#ef4444", "#ffffff", self.limpiar),
            ("⌫", 3, 3, 1, "#f59e0b", "#ffffff", self.borrar),
            
            # Fila 4 - Números
            ("7", 4, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("7")),
            ("8", 4, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("8")),
            ("9", 4, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("9")),
            ("÷", 4, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("÷")),
            
            # Fila 5 - Más números
            ("4", 5, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("4")),
            ("5", 5, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("5")),
            ("6", 5, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("6")),
            ("×", 5, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("×")),
            
            # Fila 6 - Más números
            ("1", 6, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("1")),
            ("2", 6, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("2")),
            ("3", 6, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("3")),
            ("-", 6, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("-")),
            
            # Fila 7 - Última fila
            ("0", 7, 0, 2, "#374151", "#ffffff", lambda: self.agregar_numero("0")),
            (".", 7, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero(".")),
            ("+", 7, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("+")),
        ]
        
        for texto, fila, col, colspan, bg, fg, cmd in botones_cient:
            btn = tk.Button(
                self.cientificos_frame,
                text=texto,
                font=("Segoe UI", 12, "bold"),
                bg=bg,
                fg=fg,
                activebackground=self.color_hover(bg),
                activeforeground=fg,
                bd=0,
                cursor="hand2",
                command=cmd
            )
            btn.grid(row=fila, column=col, columnspan=colspan, 
                    sticky="nsew", padx=2, pady=2)
            
            btn.bind("<Enter>", lambda e, b=btn, c=bg: b.configure(bg=self.color_hover(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))
    
    def funcion_cientifica(self, funcion):
        if not self.pantalla_texto or self.pantalla_texto == "0":
            return
        
        try:
            valor = float(self.pantalla_texto)
            
            if funcion == "sin":
                resultado = self.calc.seno(valor)
            elif funcion == "cos":
                resultado = self.calc.coseno(valor)
            elif funcion == "tan":
                resultado = self.calc.tangente(valor)
            elif funcion == "asin":
                resultado = self.calc.arcoseno(valor)
            elif funcion == "acos":
                resultado = self.calc.arcocoseno(valor)
            elif funcion == "atan":
                resultado = self.calc.arcotangente(valor)
            elif funcion == "sqrt":
                resultado = self.calc.raiz_cuadrada(valor)
            elif funcion == "ln":
                resultado = self.calc.log_natural(valor)
            elif funcion == "exp":
                resultado = self.calc.exponencial(valor)
            elif funcion == "inv":
                resultado = self.calc.inverso(valor)
            
            if isinstance(resultado, str):
                messagebox.showerror("Error", resultado)
                return
            
            self.pantalla_operacion.config(text=f"{funcion}({self.formatear_numero(str(valor))})")
            self.pantalla_texto = self.formatear_resultado(resultado)
            self.actualizar_pantalla()
            self.actualizar_historial()
            self.resetear_pantalla = True
            
        except ValueError:
            messagebox.showerror("Error", "Valor inválido")
    
    def potencia(self, exp):
        if not self.pantalla_texto or self.pantalla_texto == "0":
            return
        
        try:
            base = float(self.pantalla_texto)
            resultado = self.calc.potencia(base, exp)
            
            self.pantalla_operacion.config(text=f"{self.formatear_numero(str(base))}^{exp}")
            self.pantalla_texto = self.formatear_resultado(resultado)
            self.actualizar_pantalla()
            self.actualizar_historial()
            self.resetear_pantalla = True
        except:
            messagebox.showerror("Error", "Operación inválida")
    
    def potencia_n(self):
        exp = tk.simpledialog.askfloat("Potencia", "Ingrese el exponente:", parent=self.root)
        if exp is not None:
            self.potencia(exp)
    
    def raiz_n(self):
        n = tk.simpledialog.askfloat("Raíz enésima", "Ingrese el índice de la raíz:", parent=self.root)
        if n is not None and n != 0:
            try:
                valor = float(self.pantalla_texto)
                resultado = self.calc.raiz_enesima(valor, n)
                
                if isinstance(resultado, str):
                    messagebox.showerror("Error", resultado)
                    return
                
                self.pantalla_operacion.config(text=f"raíz({valor}, {n})")
                self.pantalla_texto = self.formatear_resultado(resultado)
                self.actualizar_pantalla()
                self.actualizar_historial()
                self.resetear_pantalla = True
            except:
                messagebox.showerror("Error", "Operación inválida")
    
    def insertar_pi(self):
        if self.resetear_pantalla:
            self.pantalla_texto = ""
            self.resetear_pantalla = False
        
        pi_value = str(self.calc.pi())
        if len(self.pantalla_texto + pi_value) <= self.MAX_CARACTERES:
            self.pantalla_texto += pi_value
            self.actualizar_pantalla()
            self.actualizar_contador_caracteres()
    
    def formatear_resultado(self, resultado):
        if isinstance(resultado, float):
            if resultado.is_integer():
                resultado = int(resultado)
            else:
                resultado = round(resultado, 10)
        
        resultado_str = str(resultado)
        if len(resultado_str) > self.MAX_CARACTERES:
            resultado_str = f"{resultado:.4e}"
        
        return resultado_str
    
    def on_resize(self, event):
        if event.widget == self.root:
            width = self.root.winfo_width()
            
            if width < 400:
                font_size = 24
            elif width < 450:
                font_size = 28
            elif width < 500:
                font_size = 32
            else:
                font_size = 36
            
            self.pantalla.config(font=("Segoe UI", font_size, "bold"))
    
    def configurar_teclado(self):
        self.root.bind('<Return>', lambda e: self.calcular())
        self.root.bind('<KP_Enter>', lambda e: self.calcular())
        self.root.bind('<Escape>', lambda e: self.limpiar())
        self.root.bind('<BackSpace>', lambda e: self.borrar())
        
        for i in range(10):
            self.root.bind(str(i), lambda e, n=str(i): self.agregar_numero(n))
            self.root.bind(f'<KP_{i}>', lambda e, n=str(i): self.agregar_numero(n))
        
        self.root.bind('+', lambda e: self.operacion('+'))
        self.root.bind('-', lambda e: self.operacion('-'))
        self.root.bind('*', lambda e: self.operacion('×'))
        self.root.bind('/', lambda e: self.operacion('÷'))
        self.root.bind('.', lambda e: self.agregar_numero('.'))
        self.root.bind('<KP_Decimal>', lambda e: self.agregar_numero('.'))
    
    def color_hover(self, color):
        colores = {
            "#ef4444": "#dc2626",
            "#f59e0b": "#d97706",
            "#6366f1": "#4f46e5",
            "#10b981": "#059669",
            "#374151": "#4b5563",
            "#8b5cf6": "#7c3aed",
            "#ec4899": "#db2777"
        }
        return colores.get(color, color)
    
    def agregar_numero(self, numero):
        if self.resetear_pantalla:
            self.pantalla_texto = ""
            self.resetear_pantalla = False
        
        if len(self.pantalla_texto) >= self.MAX_CARACTERES:
            self.mostrar_advertencia_limite()
            return
        
        if numero == "." and "." in self.pantalla_texto:
            return
        
        if numero == "0" and self.pantalla_texto == "0":
            return
        
        if self.pantalla_texto == "0" and numero != ".":
            self.pantalla_texto = numero
        else:
            self.pantalla_texto += numero
        
        self.actualizar_pantalla()
        self.actualizar_contador_caracteres()
    
    def agregar_operador(self, operador):
        if self.pantalla_texto and self.pantalla_texto[-1] not in ["+", "-", "×", "÷", "%"]:
            self.pantalla_texto += operador
            self.actualizar_pantalla()
    
    def operacion(self, op):
        if self.pantalla_texto == "" or self.pantalla_texto == "0":
            return
        
        while self.pantalla_texto and self.pantalla_texto[-1] in ["+", "-", "×", "÷", "%", "."]:
            self.pantalla_texto = self.pantalla_texto[:-1]
        
        if not self.pantalla_texto:
            return
        
        if self.operacion_actual is not None:
            self.calcular()
        
        try:
            self.primer_numero = float(self.pantalla_texto)
            self.operacion_actual = op
            self.pantalla_operacion.config(text=f"{self.formatear_numero(self.pantalla_texto)} {op}")
            self.resetear_pantalla = True
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            self.limpiar()
    
    def calcular(self):
        if self.operacion_actual is None or self.pantalla_texto == "":
            return
        
        try:
            segundo_numero = float(self.pantalla_texto)
            
            if self.operacion_actual == "+":
                resultado = self.calc.sumar(self.primer_numero, segundo_numero)
            elif self.operacion_actual == "-":
                resultado = self.calc.restar(self.primer_numero, segundo_numero)
            elif self.operacion_actual == "×":
                resultado = self.calc.multiplicar(self.primer_numero, segundo_numero)
            elif self.operacion_actual == "÷":
                resultado = self.calc.dividir(self.primer_numero, segundo_numero)
                if isinstance(resultado, str):
                    messagebox.showerror("Error", resultado)
                    self.limpiar()
                    return
            
            resultado_str = self.formatear_resultado(resultado)
            
            self.pantalla_operacion.config(
                text=f"{self.formatear_numero(str(self.primer_numero))} {self.operacion_actual} {self.formatear_numero(str(segundo_numero))} ="
            )
            self.pantalla_texto = resultado_str
            self.actualizar_pantalla()
            self.actualizar_historial()
            
            self.operacion_actual = None
            self.primer_numero = None
            self.resetear_pantalla = True
            
        except ValueError:
            messagebox.showerror("Error", "Operación inválida")
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            self.limpiar()
    
    def formatear_numero(self, numero):
        try:
            num = float(numero)
            if num.is_integer():
                return str(int(num))
            return numero
        except:
            return numero
    
    def limpiar(self):
        self.pantalla_texto = ""
        self.operacion_actual = None
        self.primer_numero = None
        self.resetear_pantalla = False
        self.pantalla.config(text="0")
        self.pantalla_operacion.config(text="")
        self.actualizar_contador_caracteres()
    
    def borrar(self):
        if self.pantalla_texto:
            self.pantalla_texto = self.pantalla_texto[:-1]
            self.actualizar_pantalla()
            self.actualizar_contador_caracteres()
    
    def actualizar_pantalla(self):
        texto = self.pantalla_texto if self.pantalla_texto else "0"
        self.pantalla.config(text=texto)
    
    def actualizar_contador_caracteres(self):
        longitud = len(self.pantalla_texto)
        color = "#6b7280" if longitud < self.MAX_CARACTERES else "#ef4444"
        self.label_limite.config(
            text=f"{longitud}/{self.MAX_CARACTERES}",
            fg=color
        )
    
    def mostrar_advertencia_limite(self):
        self.pantalla.config(bg="#7f1d1d")
        self.root.after(200, lambda: self.pantalla.config(bg="#2d2d44"))
    
    def actualizar_historial(self):
        self.texto_historial.config(state=tk.NORMAL)
        self.texto_historial.delete(1.0, tk.END)
        
        historial = self.calc.obtener_historial()
        if not historial:
            self.texto_historial.insert(tk.END, "Sin operaciones aún...\n")
        else:
            for i, operacion in enumerate(historial, 1):
                self.texto_historial.insert(tk.END, f"{i}. {operacion}\n")
        
        self.texto_historial.config(state=tk.DISABLED)
        self.texto_historial.see(tk.END)
    
    def limpiar_historial(self):
        if not self.calc.historial:
            messagebox.showinfo("Información", "El historial ya está vacío")
            return
            
        respuesta = messagebox.askyesno(
            "Confirmar", 
            "¿Deseas limpiar todo el historial?"
        )
        if respuesta:
            self.calc.historial.clear()
            self.actualizar_historial()
            messagebox.showinfo("Éxito", "Historial limpiado correctamente")

# Ejecutar la aplicación
if __name__ == "__main__":
    import tkinter.simpledialog
    root = tk.Tk()
    app = InterfazCalculadora(root)
    root.mainloop()

    