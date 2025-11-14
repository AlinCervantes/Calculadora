#Calculadora basica en Python

class Calculadora:
    def __init__(self):
        self.historial = []

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

    #Para obtener el historial de operaciones
    def obtener_historial(self):
        return self.historial