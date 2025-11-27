import math

class Calculadora:
    def __init__(self):
        self.historial = []
        self._pi = math.pi

    def sumar(self, a, b):
        resultado = a + b
        self.historial.append(f"Sumar: {a} + {b} = {resultado}")
        return resultado

    def restar(self, a, b):
        resultado = a - b
        self.historial.append(f"Restar: {a} - {b} = {resultado}")
        return resultado

    def multiplicar(self, a, b):
        resultado = a * b
        self.historial.append(f"Multiplicar: {a} * {b} = {resultado}")
        return resultado

    def dividir(self, a, b):
        if b == 0:
            self.historial.append(f"Dividir: {a} / {b} = Error (división por cero)")
            return "Error: División por cero"
        resultado = a / b
        self.historial.append(f"Dividir: {a} / {b} = {resultado}")
        return resultado
    
    def porcentaje(self, a, b):
        resultado = a * (b / 100)
        self.historial.append(f"Porcentaje: {a} * ({b} / 100) = {resultado}")
        return resultado

    def obtener_historial(self):
        return self.historial
    
    def seno(self, a):
        x = a % (2 * self._pi)
        if x > self._pi:
            x -= 2 * self._pi   

        resultado = 0
        termino = x
        n = 1
        while abs(termino) > 1e-15 and n < 100:
            resultado += termino
            termino *= -x * x / ((2 * n) * (2 * n + 1))
            n += 1
        
        self.historial.append(f"Seno: seno({a}) = {resultado}")
        return resultado
    
    def coseno(self, a):
        x = a % (2 * self._pi)
        if x > self._pi:
            x -= 2 * self._pi

        resultado = 0
        termino = 1
        n = 1
        while abs(termino) > 1e-15 and n < 100:
            resultado += termino
            termino *= -x * x / ((2 * n - 1) * (2 * n))
            n += 1
        
        self.historial.append(f"Coseno: coseno({a}) = {resultado}")
        return resultado
    
    def tangente(self, a):
        seno_a = self.seno(a)
        coseno_a = self.coseno(a)
        if abs(coseno_a) < 1e-10:
            self.historial.append(f"Tangente: tangente({a}) = Error (coseno es cero)")
            return "Error: Tangente indefinida (coseno es cero)"
        resultado = seno_a / coseno_a
        self.historial.append(f"Tangente: tangente({a}) = {resultado}")
        return resultado
    
    def potencia(self, base, exponente):
        try:
            resultado = base ** exponente
        except OverflowError:
            self.historial.append(f"Potencia: {base}^{exponente} = Error (desbordamiento)")
            return "Error: Resultado demasiado grande"
        except Exception:
            self.historial.append(f"Potencia: {base}^{exponente} = Error (operación inválida)")
            return "Error: Operación de potencia inválida"

        self.historial.append(f"Potencia: {base}^{exponente} = {resultado}")
        return resultado
    
    def raiz_cuadrada(self, a):
        if a < 0:
            self.historial.append(f"Raíz Cuadrada: sqrt({a}) = Error (número negativo)")
            return "Error: Raíz cuadrada de número negativo"
        resultado = a ** 0.5
        self.historial.append(f"Raíz Cuadrada: sqrt({a}) = {resultado}")
        return resultado
    
    def log_natural(self, a):
        if a <= 0:
            self.historial.append(f"Logaritmo Natural: ln({a}) = Error (número no positivo)")
            return "Error: Logaritmo natural de número no positivo"
        
        resultado = math.log(a)
        self.historial.append(f"Logaritmo Natural: ln({a}) = {resultado}")
        return resultado
    
    def exponencial(self, a):
        resultado = 0
        termino = 1
        n = 0
        while abs(termino) > 1e-15 and n < 100:
            resultado += termino
            n += 1
            termino *= a / n
        
        self.historial.append(f"Exponencial: e^{a} = {resultado}")
        return resultado
    
    def raiz_enesima(self, a, n):
        if a < 0 and n % 2 == 0:
            self.historial.append(f"Raíz enésima: raiz({a}, {n}) = Error (número negativo con índice par)")
            return "Error: Raíz enésima de número negativo con índice par"
        if n == 0:
            self.historial.append(f"Raíz enésima: raiz({a}, {n}) = Error (índice cero)")
            return "Error: El índice de la raíz no puede ser cero"
            
        resultado = a ** (1 / n)
        self.historial.append(f"Raíz enésima: raiz({a}, {n}) = {resultado}")
        return resultado
    
    def inverso(self, a):
        if a == 0:
            self.historial.append(f"Inverso: 1/{a} = Error (división por cero)")
            return "Error: Inverso de cero"
        resultado = 1 / a
        self.historial.append(f"Inverso: 1/{a} = {resultado}")
        return resultado
    
    def pi(self):
        return self._pi
    
    def arcoseno(self, a):
        if a < -1 or a > 1:
            self.historial.append(f"Arco Seno: asin({a}) = Error (valor fuera de rango)")
            return "Error: Arco seno fuera de rango"
        
        resultado = math.asin(a)
        self.historial.append(f"Arco Seno: asin({a}) = {resultado}")
        return resultado
    
    def arcocoseno(self, a):
        if a < -1 or a > 1:
            self.historial.append(f"Arco Coseno: acos({a}) = Error (valor fuera de rango)")
            return "Error: Arco coseno fuera de rango"
        
        resultado = math.acos(a)
        self.historial.append(f"Arco Coseno: acos({a}) = {resultado}")
        return resultado
    
    def arcotangente(self, a):
        resultado = math.atan(a)
        self.historial.append(f"Arco Tangente: atan({a}) = {resultado}")
        return resultado  
