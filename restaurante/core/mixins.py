import re
from datetime import datetime


class CalculosMixin:

    def formatear_moneda(self, valor: float) -> str:
        return f"$ {valor:,.2f}"

    def calcular_subtotal(self, precio: float, cantidad: int, descuento_pct: float = 0.0) -> float:
        subtotal = precio * cantidad
        return round(subtotal * (1 - descuento_pct / 100), 2)

    @staticmethod
    def validar_no_vacio(valor: str, campo: str) -> str:
        v = valor.strip()
        if not v:
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        return v

    @staticmethod
    def validar_solo_letras(valor: str, campo: str) -> str:
        v = valor.strip()
        if not v:
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        if not re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+", v):
            raise ValueError(f"'{campo}' solo puede contener letras y espacios.")
        return v

    @staticmethod
    def validar_texto_general(valor: str, campo: str, min_len: int = 3) -> str:
        v = valor.strip()
        if not v:
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        if len(v) < min_len:
            raise ValueError(f"'{campo}' debe tener al menos {min_len} caracteres.")
        if v.isdigit():
            raise ValueError(f"'{campo}' no puede ser solo números.")
        return v

    @staticmethod
    def validar_entero_positivo(valor: str, campo: str) -> int:
        v = valor.strip()
        if not v.isdigit():
            raise ValueError(f"'{campo}' debe ser un número entero válido (0 para cancelar).")
        n = int(v)
        if n < 0:
            raise ValueError(f"'{campo}' no puede ser negativo.")
        return n

    @staticmethod
    def validar_positivo(valor: str, campo: str) -> float:
        v = valor.strip().replace(",", ".")
        try:
            n = float(v)
        except ValueError:
            raise ValueError(f"'{campo}' debe ser un número válido (ej: 12.50).")
        if n <= 0:
            raise ValueError(f"'{campo}' debe ser mayor a 0.")
        return n

    @staticmethod
    def validar_si_no(valor: str) -> str:
        v = valor.strip().upper()
        if v not in ("S", "N"):
            raise ValueError("Respuesta debe ser 'S' o 'N'.")
        return v

    @staticmethod
    def validar_disponibilidad(valor: str) -> str:
        v = valor.strip().upper()
        if v not in ("S", "N"):
            raise ValueError("Disponibilidad debe ser 'S' o 'N'.")
        return v

    @staticmethod
    def validar_estado_pedido(valor: str) -> str:
        v = valor.strip().upper()
        opciones = ("P", "E", "L", "C")
        if v not in opciones:
            raise ValueError("Estado debe ser P (Pendiente), E (En preparación), L (Listo), C (Cancelado).")
        return v

    @staticmethod
    def _pedir(prompt: str, validador, color_prompt=None, color_error=None,
               titulo: str = "", contexto=None) -> object:
        from core.decoradores import Color, Pantalla
        cp = color_prompt or Color.BLANCO
        ce = color_error  or Color.ROJO
        while True:
            try:
                raw = input(f"{cp}{prompt}{Color.RESET}")
                return validador(raw)
            except (ValueError, TypeError) as e:
                print(f"\n{ce}  ⚠  {e}{Color.RESET}")
                input(f"\033[90m  Presione ENTER para continuar...\033[0m")
                Pantalla.limpiar()
                if titulo:
                    ancho = 52
                    print(Color.texto("═" * ancho, Color.NARANJA))
                    print(Color.titulo(titulo.center(ancho), Color.NARANJA))
                    print(Color.texto("═" * ancho, Color.NARANJA))
                if contexto:
                    contexto()

    @classmethod
    def pedir_nombre(cls, prompt: str = "  Nombre       : ",
                     titulo: str = "", contexto=None) -> str:
        return cls._pedir(prompt, lambda v: cls.validar_texto_general(v, "nombre"),
                          titulo=titulo, contexto=contexto)

    @classmethod
    def pedir_descripcion(cls, prompt: str = "  Descripción  : ",
                          titulo: str = "", contexto=None) -> str:
        return cls._pedir(prompt, lambda v: cls.validar_texto_general(v, "descripción"),
                          titulo=titulo, contexto=contexto)

    @classmethod
    def pedir_precio(cls, prompt: str = "  Precio       : ",
                     titulo: str = "", contexto=None) -> float:
        return cls._pedir(prompt, lambda v: cls.validar_positivo(v, "precio"),
                          titulo=titulo, contexto=contexto)

    @classmethod
    def pedir_entero(cls, prompt: str, campo: str = "valor",
                     titulo: str = "", contexto=None) -> int:
        return cls._pedir(prompt, lambda v: cls.validar_entero_positivo(v, campo),
                          titulo=titulo, contexto=contexto)

    @classmethod
    def pedir_decimal(cls, prompt: str, campo: str = "valor",
                      titulo: str = "", contexto=None) -> float:
        return cls._pedir(prompt, lambda v: cls.validar_positivo(v, campo),
                          titulo=titulo, contexto=contexto)

    @classmethod
    def pedir_si_no(cls, prompt: str, titulo: str = "", contexto=None) -> str:
        return cls._pedir(prompt, lambda v: cls.validar_si_no(v),
                          titulo=titulo, contexto=contexto)

    @classmethod
    def pedir_disponibilidad(cls, prompt: str = "  Disponible (S/N): ",
                              titulo: str = "", contexto=None) -> str:
        return cls._pedir(prompt, lambda v: cls.validar_disponibilidad(v),
                          titulo=titulo, contexto=contexto)

    @classmethod
    def pedir_estado_pedido(cls, prompt: str = "  Estado (P/E/L/C): ",
                             titulo: str = "", contexto=None) -> str:
        return cls._pedir(prompt, lambda v: cls.validar_estado_pedido(v),
                          titulo=titulo, contexto=contexto)
