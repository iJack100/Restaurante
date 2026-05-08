import json
import os


class JsonManager:

    BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

    @classmethod
    def _ruta(cls, nombre_archivo: str) -> str:
        return os.path.join(cls.BASE_DIR, nombre_archivo)

    @classmethod
    def leer(cls, nombre_archivo: str) -> list:
        ruta = cls._ruta(nombre_archivo)
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def escribir(cls, nombre_archivo: str, datos: list) -> None:
        ruta = cls._ruta(nombre_archivo)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
