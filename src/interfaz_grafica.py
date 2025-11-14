import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from calculadora import Calculadora

class InterfazCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Profesional")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        
        # Instancia de la calculadora
        self.calc = Calculadora()
        
        # Variables para la pantalla
        self.pantalla_texto = ""
        self.operacion_actual = None
        self.primer_numero = None
        self.resetear_pantalla = False
        
        # Crear widgets
        self.crear_widgets()
    
    def crear_widgets(self):
        # Frame principal con padding
        main_frame = tk.Frame(self.root, bg="#1e1e2e", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== PANTALLA PRINCIPAL =====
        pantalla_frame = tk.Frame(main_frame, bg="#2d2d44", bd=2, relief=tk.RIDGE)
        pantalla_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Pantalla de operación (pequeña, arriba)
        self.pantalla_operacion = tk.Label(
            pantalla_frame,
            text="",
            font=("Segoe UI", 12),
            bg="#2d2d44",
            fg="#9ca3af",
            anchor=tk.E,
            padx=15,
            pady=5
        )
        self.pantalla_operacion.pack(fill=tk.X)
        
        # Pantalla principal (grande)
        self.pantalla = tk.Label(
            pantalla_frame,
            text="0",
            font=("Segoe UI", 36, "bold"),
            bg="#2d2d44",
            fg="#ffffff",
            anchor=tk.E,
            padx=15,
            pady=15
        )
        self.pantalla.pack(fill=tk.X)
        
        # ===== BOTONES =====
        botones_frame = tk.Frame(main_frame, bg="#1e1e2e")
        botones_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Configurar el grid
        for i in range(5):
            botones_frame.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4):
            botones_frame.grid_columnconfigure(i, weight=1, uniform="col")
        
        # Definir botones: (texto, fila, columna, colspan, color_fondo, color_texto, comando)
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
        
        for texto, fila, col, colspan, bg, fg, cmd in botones:
            btn = tk.Button(
                botones_frame,
                text=texto,
                font=("Segoe UI", 18, "bold"),
                bg=bg,
                fg=fg,
                activebackground=self.color_hover(bg),
                activeforeground=fg,
                bd=0,
                cursor="hand2",
                command=cmd
            )
            btn.grid(row=fila, column=col, columnspan=colspan, 
                    sticky="nsew", padx=3, pady=3)
            
            # Efectos hover
            btn.bind("<Enter>", lambda e, b=btn, c=bg: b.configure(bg=self.color_hover(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))
        
        # ===== HISTORIAL =====
        historial_label = tk.Label(
            main_frame,
            text="📋 Historial",
            font=("Segoe UI", 12, "bold"),
            bg="#1e1e2e",
            fg="#ffffff"
        )
        historial_label.pack(pady=(5, 5))
        
        # Frame para el historial con scrollbar
        historial_frame = tk.Frame(main_frame, bg="#2d2d44", bd=2, relief=tk.RIDGE)
        historial_frame.pack(fill=tk.BOTH, expand=True)
        
        self.texto_historial = scrolledtext.ScrolledText(
            historial_frame,
            width=40,
            height=8,
            font=("Consolas", 10),
            bg="#2d2d44",
            fg="#e5e7eb",
            wrap=tk.WORD,
            bd=0,
            insertbackground="#6366f1"
        )
        self.texto_historial.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.texto_historial.config(state=tk.DISABLED)
        
        # Botón limpiar historial
        btn_limpiar_hist = tk.Button(
            main_frame,
            text="🗑️ Limpiar Historial",
            font=("Segoe UI", 10, "bold"),
            bg="#dc2626",
            fg="#ffffff",
            activebackground="#b91c1c",
            bd=0,
            cursor="hand2",
            command=self.limpiar_historial,
            pady=8
        )
        btn_limpiar_hist.pack(fill=tk.X, pady=(5, 0))
    
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
        
        if numero == "." and "." in self.pantalla_texto:
            return
        
        self.pantalla_texto += numero
        self.actualizar_pantalla()
    
    def agregar_operador(self, operador):
        if self.pantalla_texto and self.pantalla_texto[-1] not in ["+", "-", "×", "÷", "%"]:
            self.pantalla_texto += operador
            self.actualizar_pantalla()
    
    def operacion(self, op):
        if self.pantalla_texto == "":
            return
        
        if self.operacion_actual is not None:
            self.calcular()
        
        self.primer_numero = float(self.pantalla_texto)
        self.operacion_actual = op
        self.pantalla_operacion.config(text=f"{self.pantalla_texto} {op}")
        self.resetear_pantalla = True
    
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
                    resultado = round(resultado, 8)
            
            self.pantalla_operacion.config(
                text=f"{self.primer_numero} {self.operacion_actual} {segundo_numero} ="
            )
            self.pantalla_texto = str(resultado)
            self.actualizar_pantalla()
            self.actualizar_historial()
            
            self.operacion_actual = None
            self.primer_numero = None
            self.resetear_pantalla = True
            
        except ValueError:
            messagebox.showerror("Error", "Operación inválida")
            self.limpiar()
    
    def limpiar(self):
        self.pantalla_texto = ""
        self.operacion_actual = None
        self.primer_numero = None
        self.resetear_pantalla = False
        self.pantalla.config(text="0")
        self.pantalla_operacion.config(text="")
    
    def borrar(self):
        if self.pantalla_texto:
            self.pantalla_texto = self.pantalla_texto[:-1]
            self.actualizar_pantalla()
    
    def actualizar_pantalla(self):
        texto = self.pantalla_texto if self.pantalla_texto else "0"
        self.pantalla.config(text=texto)
    
    def actualizar_historial(self):
        self.texto_historial.config(state=tk.NORMAL)
        self.texto_historial.delete(1.0, tk.END)
        
        historial = self.calc.obtener_historial()
        for i, operacion in enumerate(historial, 1):
            self.texto_historial.insert(tk.END, f"{i}. {operacion}\n")
        
        self.texto_historial.config(state=tk.DISABLED)
        self.texto_historial.see(tk.END)
    
    def limpiar_historial(self):
        respuesta = messagebox.askyesno(
            "Confirmar", 
            "¿Deseas limpiar todo el historial?"
        )
        if respuesta:
            self.calc.historial.clear()
            self.actualizar_historial()

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCalculadora(root)
    root.mainloop()