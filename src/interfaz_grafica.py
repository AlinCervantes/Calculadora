import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from calculadora import Calculadora

class InterfazCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Profesional")
        
        # Configuración general
        self.root.minsize(350, 550)
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = min(int(screen_w * 0.3), 500)
        win_h = min(int(screen_h * 0.7), 800)
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.root.configure(bg="#1e1e2e")

        self.MAX_CARACTERES = 15

        # Instancia de calculadora
        self.calc = Calculadora()

        # Variables internas
        self.pantalla_texto = ""
        self.operacion_actual = None
        self.primer_numero = None
        self.resetear_pantalla = False

        self.root.bind("<Configure>", self.on_resize)

        self.crear_widgets()
        self.configurar_teclado()

    # ======================================================
    # CREACIÓN DE WIDGETS
    # ======================================================
    def crear_widgets(self):
        self.main_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pantalla
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

        # ===================== BOTONES ======================
        self.botones_frame = tk.Frame(self.main_frame, bg="#1e1e2e")
        self.botones_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        for i in range(7):  # ahora hay más filas
            self.botones_frame.grid_rowconfigure(i, weight=1)

        for i in range(4):
            self.botones_frame.grid_columnconfigure(i, weight=1)

        # ------------------ BOTONES -------------------------
        botones = [
            # FILA 0 (limpieza)
            ("C", 0, 0, 1, "#ef4444", "#ffffff", self.limpiar),
            ("⌫", 0, 1, 1, "#f59e0b", "#ffffff", self.borrar),
            ("%", 0, 2, 1, "#6366f1", "#ffffff", lambda: self.agregar_operador("%")),
            ("÷", 0, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("÷")),

            # FILA 1 — FUNCIONES CIENTÍFICAS NUEVAS
            ("sin", 1, 0, 1, "#4b5563", "#ffffff", lambda: self.funcion_cientifica("sin")),
            ("cos", 1, 1, 1, "#4b5563", "#ffffff", lambda: self.funcion_cientifica("cos")),
            ("tan", 1, 2, 1, "#4b5563", "#ffffff", lambda: self.funcion_cientifica("tan")),
            ("√",   1, 3, 1, "#4b5563", "#ffffff", lambda: self.funcion_cientifica("sqrt")),

            # FILA 2 — FUNCIONES CIENTÍFICAS NUEVAS
            ("ln",  2, 0, 1, "#4b5563", "#ffffff", lambda: self.funcion_cientifica("ln")),
            ("exp", 2, 1, 1, "#4b5563", "#ffffff", lambda: self.funcion_cientifica("exp")),
            ("x^y", 2, 2, 1, "#4b5563", "#ffffff", lambda: self.funcion_cientifica("pow")),
            ("π",   2, 3, 1, "#4b5563", "#ffffff", self.insertar_pi),

            # FILA 3
            ("7", 3, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("7")),
            ("8", 3, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("8")),
            ("9", 3, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("9")),
            ("×", 3, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("×")),

            # FILA 4
            ("4", 4, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("4")),
            ("5", 4, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("5")),
            ("6", 4, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("6")),
            ("-", 4, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("-")),

            # FILA 5
            ("1", 5, 0, 1, "#374151", "#ffffff", lambda: self.agregar_numero("1")),
            ("2", 5, 1, 1, "#374151", "#ffffff", lambda: self.agregar_numero("2")),
            ("3", 5, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero("3")),
            ("+", 5, 3, 1, "#6366f1", "#ffffff", lambda: self.operacion("+")),

            # FILA 6
            ("0", 6, 0, 2, "#374151", "#ffffff", lambda: self.agregar_numero("0")),
            (".", 6, 2, 1, "#374151", "#ffffff", lambda: self.agregar_numero(".")),
            ("=", 6, 3, 1, "#10b981", "#ffffff", self.calcular),
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
                command=cmd,
            )
            btn.grid(row=fila, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

            btn.bind("<Enter>", lambda e, b=btn, c=bg: b.configure(bg=self.color_hover(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))

            self.botones[texto] = btn

        # ===================== HISTORIAL =====================
        historial_label = tk.Label(
            self.main_frame,
            text="📋 Historial",
            font=("Segoe UI", 11, "bold"),
            bg="#1e1e2e",
            fg="#ffffff",
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
            pady=6,
        )
        self.btn_limpiar_hist.pack(fill=tk.X, pady=(5, 0))

    # ======================================================
    # MÉTODOS CIENTÍFICOS
    # ======================================================
    def funcion_cientifica(self, tipo):
        try:
            if self.pantalla_texto == "":
                return

            numero = float(self.pantalla_texto)

            if tipo == "sin":
                resultado = self.calc.seno(numero)

            elif tipo == "cos":
                resultado = self.calc.coseno(numero)

            elif tipo == "tan":
                resultado = self.calc.tangente(numero)

            elif tipo == "sqrt":
                resultado = self.calc.raiz_cuadrada(numero)

            elif tipo == "ln":
                resultado = self.calc.log_natural(numero)

            elif tipo == "exp":
                resultado = self.calc.exponencial(numero)

            elif tipo == "pow":
                self.primer_numero = numero
                self.operacion_actual = "^"
                self.pantalla_operacion.config(text=f"{numero} ^")
                self.resetear_pantalla = True
                return

            self.pantalla_texto = str(resultado)
            self.actualizar_pantalla()
            self.actualizar_historial()
            self.resetear_pantalla = True

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insertar_pi(self):
        self.pantalla_texto = str(self.calc.pi())
        self.actualizar_pantalla()

    # ======================================================
    # OPERACIONES GENERALES
    # ======================================================
    def on_resize(self, event):
        if event.widget == self.root:
            width = self.root.winfo_width()
            if width < 350:
                fsize = 24
                bsize = 12
            elif width < 400:
                fsize = 28
                bsize = 14
            elif width < 450:
                fsize = 32
                bsize = 16
            else:
                fsize = 36
                bsize = 18
            self.pantalla.config(font=("Segoe UI", fsize, "bold"))
            for btn in self.botones.values():
                btn.config(font=("Segoe UI", bsize, "bold"))

    def configurar_teclado(self):
        self.root.bind("<Return>", lambda e: self.calcular())
        self.root.bind("<KP_Enter>", lambda e: self.calcular())
        self.root.bind("<Escape>", lambda e: self.limpiar())
        self.root.bind("<BackSpace>", lambda e: self.borrar())

        for i in range(10):
            self.root.bind(str(i), lambda e, n=str(i): self.agregar_numero(n))

        self.root.bind("+", lambda e: self.operacion("+"))
        self.root.bind("-", lambda e: self.operacion("-"))
        self.root.bind("*", lambda e: self.operacion("×"))
        self.root.bind("/", lambda e: self.operacion("÷"))
        self.root.bind(".", lambda e: self.agregar_numero("."))

    def color_hover(self, color):
        colores = {
            "#ef4444": "#dc2626",
            "#f59e0b": "#d97706",
            "#6366f1": "#4f46e5",
            "#10b981": "#059669",
            "#374151": "#4b5563",
            "#4b5563": "#6b7280",
        }
        return colores.get(color, color)

    # ======================================================
    # NÚMEROS Y OPERADORES
    # ======================================================
    def agregar_numero(self, num):
        if self.resetear_pantalla:
            self.pantalla_texto = ""
            self.resetear_pantalla = False

        if len(self.pantalla_texto) >= self.MAX_CARACTERES:
            self.mostrar_advertencia_limite()
            return

        if num == "." and "." in self.pantalla_texto:
            return

        if num == "0" and self.pantalla_texto == "0":
            return

        if self.pantalla_texto == "0" and num != ".":
            self.pantalla_texto = num
        else:
            self.pantalla_texto += num

        self.actualizar_pantalla()
        self.actualizar_contador_caracteres()

    def agregar_operador(self, operador):
        if self.pantalla_texto and self.pantalla_texto[-1] not in ["+", "-", "×", "÷", "%"]:
            self.pantalla_texto += operador
            self.actualizar_pantalla()

    def operacion(self, op):
        if not self.pantalla_texto:
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
            self.pantalla_operacion.config(text=f"{self.primer_numero} {op}")
            self.resetear_pantalla = True
        except:
            messagebox.showerror("Error", "Número inválido")
            self.limpiar()

    # ======================================================
    # CALCULAR RESULTADO
    # ======================================================
    def calcular(self):
        if not self.operacion_actual or not self.pantalla_texto:
            return

        try:
            segundo = float(self.pantalla_texto)

            # OPERACIONES NORMALES
            if self.operacion_actual == "+":
                resultado = self.calc.sumar(self.primer_numero, segundo)

            elif self.operacion_actual == "-":
                resultado = self.calc.restar(self.primer_numero, segundo)

            elif self.operacion_actual == "×":
                resultado = self.calc.multiplicar(self.primer_numero, segundo)

            elif self.operacion_actual == "÷":
                resultado = self.calc.dividir(self.primer_numero, segundo)
                if isinstance(resultado, str):
                    messagebox.showerror("Error", resultado)
                    self.limpiar()
                    return

            # POTENCIA x^y
            elif self.operacion_actual == "^":
                resultado = self.calc.potencia(self.primer_numero, segundo)

            # Formatear
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            resultado_str = str(resultado)
            if len(resultado_str) > self.MAX_CARACTERES:
                resultado_str = f"{resultado:.3e}"

            self.pantalla_operacion.config(
                text=f"{self.primer_numero} {self.operacion_actual} {segundo} ="
            )
            self.pantalla_texto = resultado_str
            self.actualizar_pantalla()
            self.actualizar_historial()

            self.operacion_actual = None
            self.primer_numero = None
            self.resetear_pantalla = True

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.limpiar()

    # ======================================================
    # UTILIDADES
    # ======================================================
    def formatear_numero(self, num):
        try:
            n = float(num)
            return str(int(n)) if n.is_integer() else num
        except:
            return num

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
        self.pantalla.config(text=self.pantalla_texto if self.pantalla_texto else "0")

    def actualizar_contador_caracteres(self):
        longitud = len(self.pantalla_texto)
        color = "#ef4444" if longitud >= self.MAX_CARACTERES else "#6b7280"
        self.label_limite.config(text=f"{longitud}/{self.MAX_CARACTERES}", fg=color)

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
            for i, h in enumerate(historial, 1):
                self.texto_historial.insert(tk.END, f"{i}. {h}\n")

        self.texto_historial.config(state=tk.DISABLED)
        self.texto_historial.see(tk.END)

    def limpiar_historial(self):
        if not self.calc.historial:
            messagebox.showinfo("Información", "El historial ya está vacío")
            return

        if messagebox.askyesno("Confirmar", "¿Deseas limpiar todo el historial?"):
            self.calc.historial.clear()
            self.actualizar_historial()
            messagebox.showinfo("Éxito", "Historial limpiado correctamente")

# Ejecutar
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCalculadora(root)
    root.mainloop()
