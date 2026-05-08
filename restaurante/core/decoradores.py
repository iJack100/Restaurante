import os
import functools

_ROJO    = "\033[31m"
_RESET   = "\033[0m"
_GRIS    = "\033[90m"


def error_y_pausa(mensaje: str) -> None:
    print(f"\n{_ROJO}  ⚠  {mensaje}{_RESET}")
    input(f"{_GRIS}  Presione ENTER para continuar...{_RESET}")
    os.system("cls" if os.name == "nt" else "clear")


def error_flash(mensaje: str, titulo: str, redibujar=None) -> None:
    print(f"\n{_ROJO}  ⚠  {mensaje}{_RESET}")
    input(f"{_GRIS}  Presione ENTER para continuar...{_RESET}")
    os.system("cls" if os.name == "nt" else "clear")
    if titulo:
        from core.decoradores import Color
        ancho = 52
        print(Color.texto("═" * ancho, Color.NARANJA))
        print(Color.titulo(titulo.center(ancho), Color.NARANJA))
        print(Color.texto("═" * ancho, Color.NARANJA))
    if redibujar:
        redibujar()


class Color:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    ROJO     = "\033[31m"
    VERDE    = "\033[32m"
    AMARILLO = "\033[33m"
    AZUL     = "\033[34m"
    MAGENTA  = "\033[35m"
    CYAN     = "\033[36m"
    BLANCO   = "\033[37m"
    # Paleta restaurante: naranja via secuencia 256-color, dorado, verde menta
    NARANJA  = "\033[38;5;208m"
    DORADO   = "\033[38;5;220m"
    MENTA    = "\033[38;5;120m"
    SALMON   = "\033[38;5;209m"

    @staticmethod
    def texto(texto, color):
        return f"{color}{texto}{Color.RESET}"

    @staticmethod
    def titulo(texto, color=None):
        color = color or Color.NARANJA
        return f"{Color.BOLD}{color}{texto}{Color.RESET}"


class Pantalla:

    @staticmethod
    def limpiar():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def gotoxy(x, y):
        print(f"\033[{y};{x}H", end="", flush=True)

    @staticmethod
    def pausar():
        input(f"\n  {Color.texto('Presione ENTER para continuar...', Color.DORADO)}")

    @staticmethod
    def linea(caracter="─", ancho=52, color=None):
        return Color.texto(caracter * ancho, color or Color.NARANJA)

    @staticmethod
    def encabezado(titulo, color=None):
        color = color or Color.NARANJA
        ancho = 52
        Pantalla.limpiar()
        icono = "🍽 "
        linea_dec = "═" * ancho
        print(Color.texto(linea_dec, color))
        print(Color.titulo(f"{icono}{titulo.center(ancho - 4)}{icono}", color))
        print(Color.texto(linea_dec, color))


def decorador_interfaz(titulo: str):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            Pantalla.encabezado(titulo)
            return func(*args, **kwargs)
        return inner
    return wrapper


def manejar_errores(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(Color.texto(f"\n  ⚠  Error de valor: {e}", Color.ROJO))
        except FileNotFoundError as e:
            print(Color.texto(f"\n  ⚠  Error de archivo: {e}", Color.ROJO))
        except Exception as e:
            print(Color.texto(f"\n  ⚠  Error inesperado: {type(e).__name__} — {e}", Color.ROJO))
    return wrapper
