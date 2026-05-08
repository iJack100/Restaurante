class Plato:

    def __init__(self, id: int, nombre: str, id_categoria: int,
                 precio: float, descripcion: str, disponible: str):
        self.id           = id
        self.nombre       = nombre.strip()
        self.id_categoria = id_categoria
        self.precio       = round(float(precio), 2)
        self.descripcion  = descripcion.strip()
        self.disponible   = disponible.upper()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "id_categoria": self.id_categoria,
            "precio": self.precio,
            "descripcion": self.descripcion,
            "disponible": self.disponible,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Plato":
        return cls(
            data["id"],
            data["nombre"],
            data["id_categoria"],
            data["precio"],
            data.get("descripcion", ""),
            data.get("disponible", "S"),
        )

    def disponible_label(self) -> str:
        return "Disponible" if self.disponible == "S" else "No disponible"

    def __str__(self) -> str:
        estado = "✔" if self.disponible == "S" else "✖"
        return (
            f"ID: {self.id:>3} | {self.nombre:<28} | "
            f"$ {self.precio:>8,.2f} | {estado}"
        )
