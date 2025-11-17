import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from calculadora import Calculadora

class InterfazCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Profesional")
        
        # NUEVO: Configuración de tamaño mínimo y adaptable
        self.root.minsize(350, 550)
        
        # Detectar tamaño de pantalla y ajustar ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular tamaño apropiado (30% del ancho, 70% del alto, máximo 500x800)
        window_width = min(int(screen_width * 0.3), 500)
        window_height = min(int(screen_height * 0.7), 800)
        
        # Centrar ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#1e1e2e")
        
        # NUEVO: Límite de caracteres
        self.MAX_CARACTERES = 15
        
        # Instancia de la calculadora
        self.calc = Calculadora()
        
        # Variables para la pantalla
        self.pantalla_texto = ""
        self.operacion_actual = None
        self.primer_numero = None
        self.resetear_pantalla = False
        
        # NUEVO: Vincular evento de redimensionamiento
        self.root.bind('<Configure>', self.on_resize)
        
        # Crear widgets
        self.crear_widgets()
        
        # NUEVO: Atajos de teclado
        self.configurar_teclado()
    
    def crear_widgets(self):
        # Frame principal con padding proporcional
        self.main_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== PANTALLA PRINCIPAL =====
        pantalla_frame = tk.Frame(self.main_frame, bg="#2d2d44", bd=2, relief=tk.RIDGE)
        pantalla_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Pantalla de operación (pequeña, arriba)
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
        
        # Pantalla principal (grande) - NUEVO: Tamaño de fuente adaptable
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
        
        # NUEVO: Label para mostrar límite de caracteres
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
        
        # ===== BOTONES =====
        self.botones_frame = tk.Frame(self.main_frame, bg="#1e1e2e")
        self.botones_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Configurar el grid con peso proporcional
        for i in range(5):
            self.botones_frame.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4):
            self.botones_frame.grid_columnconfigure(i, weight=1, uniform="col")
        
        # Definir botones
        botones = [
            # Fila 0
            ("C", 0, 0, 1, "#ef4444", "#ffffff", self.limpiar),
            ("⌫", 0, 1, 1, "#f59e0b", "#ffffff", self.borrar),
            ("%", 0, 2, 1, "#6366f1", "#ffffff", lambda: self.agregar_operador("%")),
            ("÷", 0, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("÷")),
            
            # Fila 1
            ("7", 1, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("7")),
            ("8", 1, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("8")),
            ("9", 1, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("9")),
            ("×", 1, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("×")),
            
            # Fila 2
            ("4", 2, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("4")),
            ("5", 2, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("5")),
            ("6", 2, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("6")),
            ("-", 2, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("-")),
            
            # Fila 3
            ("1", 3, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("1")),
            ("2", 3, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("2")),
            ("3", 3, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("3")),
            ("+", 3, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("+")),
            
            # Fila 4
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
            
            # Efectos hover
            btn.bind("<Enter>", lambda e, b=btn, c=bg: b.configure(bg=self.color_hover(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))
            
            self.botones[texto] = btn
        
        # ===== HISTORIAL =====
        historial_label = tk.Label(
            self.main_frame,
            text="📋 Historial",
            font=("Segoe UI", 11, "bold"),
            bg="#1e1e2e",
            fg="#ffffff"
        )
        historial_label.pack(pady=(5, 5))
        
        # Frame para el historial con scrollbar
        historial_frame = tk.Frame(self.main_frame, bg="#2d2d44", bd=2, relief=tk.RIDGE)
        historial_frame.pack(fill=tk.BOTH, expand=True)
        
        self.texto_historial = scrolledtext.ScrolledText(
            historial_frame,
            font=("Consolas", 9),
            bg="#2d2d44",
            fg="#e5e7eb",
            wrap=tk.WORD,
            bd=0,
            insertbackground="#6366f1"
        )
        self.texto_historial.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.texto_historial.config(state=tk.DISABLED)
        
        # Botón limpiar historial
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
    
    def on_resize(self, event):
        """NUEVO: Ajustar tamaños de fuente según el tamaño de la ventana"""
        if event.widget == self.root:
            width = self.root.winfo_width()
            
            # Ajustar tamaño de fuente de la pantalla principal
            if width < 350:
                font_size = 24
                btn_font = 12
            elif width < 400:
                font_size = 28
                btn_font = 14
            elif width < 450:
                font_size = 32
                btn_font = 16
            else:
                font_size = 36
                btn_font = 18
            
            self.pantalla.config(font=("Segoe UI", font_size, "bold"))
            
            # Ajustar tamaño de botones
            for btn in self.botones.values():
                btn.config(font=("Segoe UI", btn_font, "bold"))
    
    def configurar_teclado(self):
        """NUEVO: Configurar atajos de teclado"""
        self.root.bind('<Return>', lambda e: self.calcular())
        self.root.bind('<KP_Enter>', lambda e: self.calcular())
        self.root.bind('<Escape>', lambda e: self.limpiar())
        self.root.bind('<BackSpace>', lambda e: self.borrar())
        
        # Números
        for i in range(10):
            self.root.bind(str(i), lambda e, n=str(i): self.agregar_numero(n))
            self.root.bind(f'<KP_{i}>', lambda e, n=str(i): self.agregar_numero(n))
        
        # Operadores
        self.root.bind('+', lambda e: self.operacion('+'))
        self.root.bind('-', lambda e: self.operacion('-'))
        self.root.bind('*', lambda e: self.operacion('×'))
        self.root.bind('/', lambda e: self.operacion('÷'))
        self.root.bind('.', lambda e: self.agregar_numero('.'))
        self.root.bind('<KP_Decimal>', lambda e: self.agregar_numero('.'))
    
    def color_hover(self, color):
        """Genera un color más claro para el efecto hover"""
        colores = {
            "#ef4444": "#dc2626",
            "#f59e0b": "#d97706",
            "#6366f1": "#4f46e5",
            "#10b981": "#059669",
            "#374151": "#4b5563"
        }
        return colores.get(color, color)
    
    def agregar_numero(self, numero):
        if self.resetear_pantalla:
            self.pantalla_texto = ""
            self.resetear_pantalla = False
        
        # NUEVO: Verificar límite de caracteres
        if len(self.pantalla_texto) >= self.MAX_CARACTERES:
            self.mostrar_advertencia_limite()
            return
        
        if numero == "." and "." in self.pantalla_texto:
            return
        
        # NUEVO: No permitir múltiples ceros al inicio
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
        
        # NUEVO: Eliminar operadores finales antes de procesar
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
            
            # Formatear resultado
            if isinstance(resultado, float):
                if resultado.is_integer():
                    resultado = int(resultado)
                else:
                    resultado = round(resultado, 10)
            
            # NUEVO: Verificar si el resultado excede el límite
            resultado_str = str(resultado)
            if len(resultado_str) > self.MAX_CARACTERES:
                # Usar notación científica si es muy largo
                resultado_str = f"{resultado:.4e}"
            
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
        """NUEVO: Formatear número para visualización"""
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
        """NUEVO: Actualizar contador de caracteres"""
        longitud = len(self.pantalla_texto)
        color = "#6b7280" if longitud < self.MAX_CARACTERES else "#ef4444"
        self.label_limite.config(
            text=f"{longitud}/{self.MAX_CARACTERES}",
            fg=color
        )
    
    def mostrar_advertencia_limite(self):
        """NUEVO: Mostrar advertencia visual cuando se alcanza el límite"""
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
    root = tk.Tk()
    app = InterfazCalculadora(root)
    root.mainloop()