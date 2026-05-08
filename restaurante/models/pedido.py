class Pedido:

    ESTADOS_VALIDOS = ("P", "E", "L", "C")

    def __init__(self, id: int, mesa: int, id_plato: int,
                 cantidad: int, total: float, estado: str, fecha: str):
        self.id        = id
        self.mesa      = int(mesa)
        self.id_plato  = id_plato
        self.cantidad  = int(cantidad)
        self.total     = round(float(total), 2)
        self.estado    = estado.upper()
        if self.estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: '{estado}'. Use P/E/L/C.")
        self.fecha = fecha

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "mesa": self.mesa,
            "id_plato": self.id_plato,
            "cantidad": self.cantidad,
            "total": self.total,
            "estado": self.estado,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pedido":
        return cls(
            data["id"],
            data["mesa"],
            data["id_plato"],
            data["cantidad"],
            data["total"],
            data["estado"],
            data.get("fecha", ""),
        )

    def estado_label(self) -> str:
        mapa = {
            "P": "Pendiente",
            "E": "En preparación",
            "L": "Listo",
            "C": "Cancelado",
        }
        return mapa.get(self.estado, self.estado)

    def __str__(self) -> str:
        return (
            f"ID: {self.id:>3} | Mesa: {self.mesa:>2} | "
            f"Plato ID: {self.id_plato} | Cant: {self.cantidad} | "
            f"Total: $ {self.total:>8,.2f} | {self.estado_label()}"
        )
