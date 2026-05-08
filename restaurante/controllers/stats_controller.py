from core.decoradores import decorador_interfaz, Color, Pantalla
from core.mixins import CalculosMixin


class StatsController(CalculosMixin):

    def __init__(self, cat_ctrl, plato_ctrl, pedido_ctrl):
        self._cat    = cat_ctrl
        self._plato  = plato_ctrl
        self._pedido = pedido_ctrl

    @decorador_interfaz("RESUMEN GENERAL DEL RESTAURANTE")
    def resumen_general(self):
        categorias = self._cat.todos()
        platos     = self._plato.todos()
        pedidos    = self._pedido.todos()

        print(Pantalla.linea("─", 52))
        print(Color.titulo("  TOTALES", Color.NARANJA))
        print(Pantalla.linea("─", 52))
        print(f"  {Color.texto('Categorías registradas :', Color.DORADO)} {len(categorias)}")
        print(f"  {Color.texto('Platos en menú         :', Color.DORADO)} {len(platos)}")
        disp = len(list(filter(lambda p: p.disponible == "S", platos)))
        print(f"  {Color.texto('Platos disponibles     :', Color.DORADO)} {disp}")
        print(f"  {Color.texto('Pedidos totales        :', Color.DORADO)} {len(pedidos)}")

        if platos:
            plato_caro = max(platos, key=lambda p: p.precio)
            plato_bara = min(platos, key=lambda p: p.precio)
            prom_precio = round(sum(p.precio for p in platos) / len(platos), 2)

            print(Pantalla.linea("─", 52))
            print(Color.titulo("  PRECIOS DEL MENÚ", Color.NARANJA))
            print(Pantalla.linea("─", 52))
            print(
                f"  {Color.texto('Más caro   :', Color.MENTA)} "
                f"{plato_caro.nombre:<28} {Color.texto(self.formatear_moneda(plato_caro.precio), Color.MENTA)}"
            )
            print(
                f"  {Color.texto('Más barato :', Color.DORADO)} "
                f"{plato_bara.nombre:<28} {Color.texto(self.formatear_moneda(plato_bara.precio), Color.DORADO)}"
            )
            print(
                f"  {Color.texto('Promedio   :', Color.NARANJA)} "
                f"{Color.texto(self.formatear_moneda(prom_precio), Color.NARANJA)}"
            )

        if pedidos:
            pedidos_activos = list(filter(lambda p: p.estado != "C", pedidos))
            total_facturado = sum(p.total for p in pedidos_activos)
            pedido_mayor    = max(pedidos, key=lambda p: p.total)

            pl_mayor = self._plato.buscar_por_id(pedido_mayor.id_plato)
            nombre_mayor = pl_mayor.nombre if pl_mayor else "Desconocido"

            print(Pantalla.linea("─", 52))
            print(Color.titulo("  VENTAS", Color.NARANJA))
            print(Pantalla.linea("─", 52))
            print(
                f"  {Color.texto('Total facturado :', Color.MENTA)} "
                f"{Color.texto(self.formatear_moneda(total_facturado), Color.MENTA)}"
            )
            print(
                f"  {Color.texto('Pedido mayor    :', Color.DORADO)} "
                f"{nombre_mayor:<25} {Color.texto(self.formatear_moneda(pedido_mayor.total), Color.DORADO)}"
            )

        print(Pantalla.linea("─", 52))
        Pantalla.pausar()
