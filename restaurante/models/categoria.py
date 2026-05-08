class Categoria:

    def __init__(self, id: int, nombre: str, descripcion: str):
        self.id          = id
        self.nombre      = nombre.strip()
        self.descripcion = descripcion.strip()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Categoria":
        return cls(data["id"], data["nombre"], data.get("descripcion", ""))

    def __str__(self) -> str:
        return (
            f"ID: {self.id:>3} | {self.nombre:<25} | {self.descripcion}"
        )
