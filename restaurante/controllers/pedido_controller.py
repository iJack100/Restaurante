from datetime import datetime
from core.interfaces import ICrud
from core.mixins import CalculosMixin
from core.decoradores import decorador_interfaz, manejar_errores, Color, Pantalla, error_flash
from core.json_manager import JsonManager
from models.pedido import Pedido


class PedidoController(ICrud, CalculosMixin):

    ARCHIVO = "pedidos.json"

    def __init__(self, plato_ctrl, cat_ctrl):
        self._pedidos: list[Pedido] = self._cargar()
        self._plato = plato_ctrl
        self._cat   = cat_ctrl

    def _cargar(self) -> list[Pedido]:
        return list(map(Pedido.from_dict, JsonManager.leer(self.ARCHIVO)))

    def _guardar(self) -> None:
        JsonManager.escribir(self.ARCHIVO, list(map(lambda p: p.to_dict(), self._pedidos)))

    def todos(self) -> list[Pedido]:
        return self._pedidos

    def buscar_por_id(self, ped_id: int):
        return next((p for p in self._pedidos if p.id == ped_id), None)

    def siguiente_id(self) -> int:
        return max((p.id for p in self._pedidos), default=0) + 1

    @decorador_interfaz("REGISTRAR PEDIDO")
    @manejar_errores
    def crear(self):
        TITULO = "REGISTRAR PEDIDO"
        platos_disp = list(filter(lambda p: p.disponible == "S", self._plato.todos()))

        if not platos_disp:
            print(Color.texto("  ⚠  No hay platos disponibles en este momento.", Color.ROJO))
            Pantalla.pausar()
            return

        def _encabezado():
            print(Color.texto("  Complete los datos del nuevo pedido:\n", Color.NARANJA))

        _encabezado()

        mesa = self.pedir_entero(
            Color.texto("  Número de mesa : ", Color.DORADO), "mesa",
            titulo=TITULO, contexto=_encabezado)
        if mesa == 0:
            print(Color.texto("\n  ✖  Pedido cancelado.", Color.ROJO))
            Pantalla.pausar()
            return

        # Mostrar platos disponibles
        print(Pantalla.linea())
        print(Color.texto("  Platos disponibles:", Color.NARANJA))
        for pl in platos_disp:
            cat = self._cat.buscar_por_id(pl.id_categoria)
            cat_n = cat.nombre if cat else "?"
            print(
                f"    {Color.texto(f'[{pl.id}]', Color.DORADO)} "
                f"{pl.nombre:<28} "
                f"{Color.texto(self.formatear_moneda(pl.precio), Color.MENTA)} "
                f"| {Color.texto(cat_n, Color.NARANJA)}"
            )
        print(Pantalla.linea())

        def _ctx_plato():
            print(Color.texto("  Complete los datos del nuevo pedido:\n", Color.NARANJA))
            print(f"  Mesa        : {Color.texto(str(mesa), Color.BLANCO)}")

        while True:
            plato_id = self.pedir_entero(
                Color.texto("  ID del plato  : ", Color.DORADO), "ID plato",
                titulo=TITULO, contexto=_ctx_plato)
            if plato_id == 0:
                print(Color.texto("\n  ✖  Pedido cancelado.", Color.ROJO))
                Pantalla.pausar()
                return
            plato = self._plato.buscar_por_id(plato_id)
            if plato and plato.disponible == "S":
                break
            error_flash("Plato no encontrado o no disponible.", TITULO, _ctx_plato)
            Pantalla.encabezado(TITULO)
            _ctx_plato()
            print(Pantalla.linea())
            print(Color.texto("  Platos disponibles:", Color.NARANJA))
            for pl in platos_disp:
                cat = self._cat.buscar_por_id(pl.id_categoria)
                cat_n = cat.nombre if cat else "?"
                print(f"    {Color.texto(f'[{pl.id}]', Color.DORADO)} {pl.nombre:<28} "
                      f"{Color.texto(self.formatear_moneda(pl.precio), Color.MENTA)} | {cat_n}")
            print(Pantalla.linea())

        def _ctx_cant():
            print(Color.texto("  Complete los datos del nuevo pedido:\n", Color.NARANJA))
            print(f"  Mesa        : {Color.texto(str(mesa), Color.BLANCO)}")
            print(f"  Plato       : {Color.texto(plato.nombre, Color.BLANCO)}")

        cantidad = self.pedir_entero(
            Color.texto("  Cantidad      : ", Color.DORADO), "cantidad",
            titulo=TITULO, contexto=_ctx_cant)
        if cantidad == 0:
            print(Color.texto("\n  ✖  Pedido cancelado.", Color.ROJO))
            Pantalla.pausar()
            return

        total = self.calcular_subtotal(plato.precio, cantidad)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        print(Pantalla.linea())
        print(Color.titulo("  RESUMEN DEL PEDIDO", Color.NARANJA))
        print(Pantalla.linea())
        print(f"  Mesa        : {Color.texto(str(mesa), Color.BLANCO)}")
        print(f"  Plato       : {Color.texto(plato.nombre, Color.BLANCO)}")
        print(f"  Precio unit.: {Color.texto(self.formatear_moneda(plato.precio), Color.MENTA)}")
        print(f"  Cantidad    : {Color.texto(str(cantidad), Color.BLANCO)}")
        print(f"  Total       : {Color.texto(self.formatear_moneda(total), Color.MENTA)}")
        print(f"  Fecha/Hora  : {Color.texto(fecha, Color.BLANCO)}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(Color.texto("  ¿Confirmar pedido? (S/N): ", Color.DORADO))
        if confirmacion == "S":
            pedido = Pedido(self.siguiente_id(), mesa, plato_id, cantidad, total, "P", fecha)
            self._pedidos.append(pedido)
            self._guardar()
            print(Color.texto(f"\n  ✔  Pedido #{pedido.id} registrado. ¡Buen provecho!", Color.MENTA))
        else:
            print(Color.texto("\n  ✖  Pedido cancelado.", Color.ROJO))

        Pantalla.pausar()

    @decorador_interfaz("LISTADO DE PEDIDOS")
    def consultar(self):
        if not self._pedidos:
            print(Color.texto("  (Sin pedidos registrados)", Color.DORADO))
            Pantalla.pausar()
            return

        print(Pantalla.linea("─", 80))
        for ped in self._pedidos:
            plato = self._plato.buscar_por_id(ped.id_plato)
            plato_n = plato.nombre if plato else "Plato eliminado"
            est_color = {
                "P": Color.DORADO, "E": Color.NARANJA,
                "L": Color.MENTA, "C": Color.ROJO
            }.get(ped.estado, Color.BLANCO)
            print(
                f"  {Color.texto(f'#{ped.id:>3}', Color.NARANJA)} | "
                f"Mesa {Color.texto(str(ped.mesa), Color.DORADO):>2} | "
                f"{plato_n:<28} | "
                f"x{ped.cantidad} | "
                f"{Color.texto(self.formatear_moneda(ped.total), Color.MENTA)} | "
                f"{Color.texto(ped.estado_label(), est_color)}"
            )
        print(Pantalla.linea("─", 80))
        print(Color.texto(f"  Total pedidos: {len(self._pedidos)}", Color.NARANJA))
        Pantalla.pausar()

    @decorador_interfaz("BUSCAR PEDIDO")
    @manejar_errores
    def buscar(self, id: int = None):
        if not self._pedidos:
            print(Color.texto("  No hay pedidos registrados.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "BUSCAR PEDIDO"

        if id is None:
            while True:
                self._listar_simple()
                print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
                id = self.pedir_entero(
                    Color.texto("\n  ID del pedido a buscar: ", Color.DORADO), "ID")
                if id == 0:
                    print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                    Pantalla.pausar()
                    return
                ped = self.buscar_por_id(id)
                if ped:
                    break
                error_flash("Pedido no encontrado.", TITULO)
                Pantalla.encabezado(TITULO)

        ped = self.buscar_por_id(id)
        if not ped:
            error_flash("Pedido no encontrado.", TITULO)
            return

        plato = self._plato.buscar_por_id(ped.id_plato)
        plato_n = plato.nombre if plato else "Plato eliminado"

        print(Pantalla.linea("─", 60))
        print(f"  {Color.texto('ID Pedido   :', Color.DORADO)} {ped.id}")
        print(f"  {Color.texto('Mesa        :', Color.DORADO)} {ped.mesa}")
        print(f"  {Color.texto('Plato       :', Color.DORADO)} {plato_n}")
        print(f"  {Color.texto('Cantidad    :', Color.DORADO)} {ped.cantidad}")
        print(f"  {Color.texto('Total       :', Color.DORADO)} {self.formatear_moneda(ped.total)}")
        print(f"  {Color.texto('Estado      :', Color.DORADO)} {ped.estado_label()}")
        print(f"  {Color.texto('Fecha       :', Color.DORADO)} {ped.fecha}")
        print(Pantalla.linea("─", 60))
        Pantalla.pausar()

    @decorador_interfaz("ACTUALIZAR PEDIDO")
    @manejar_errores
    def actualizar(self, id: int = None):
        if not self._pedidos:
            print(Color.texto("  No hay pedidos registrados.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "ACTUALIZAR PEDIDO"

        if id is None:
            while True:
                self._listar_simple()
                print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
                id = self.pedir_entero(
                    Color.texto("\n  ID del pedido a actualizar: ", Color.DORADO), "ID")
                if id == 0:
                    print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                    Pantalla.pausar()
                    return
                ped = self.buscar_por_id(id)
                if ped:
                    break
                error_flash("Pedido no encontrado.", TITULO)
                Pantalla.encabezado(TITULO)

        plato = self._plato.buscar_por_id(ped.id_plato)
        plato_n = plato.nombre if plato else "?"

        print(Pantalla.linea())
        print(Color.texto("  Datos actuales:", Color.NARANJA))
        print(f"  Mesa   : {ped.mesa}")
        print(f"  Plato  : {plato_n}")
        print(f"  Estado : {ped.estado_label()}")
        print(Pantalla.linea())
        print(Color.texto("  Estados: P=Pendiente  E=En preparación  L=Listo  C=Cancelado\n", Color.DORADO))

        raw_estado = input(f"  Nuevo estado [{ped.estado}]: ").strip().upper()
        if raw_estado and raw_estado in ("P", "E", "L", "C"):
            nuevo_estado = raw_estado
        elif raw_estado:
            print(Color.texto("  ⚠  Estado inválido, se mantiene el actual.", Color.ROJO))
            nuevo_estado = ped.estado
        else:
            nuevo_estado = ped.estado

        raw_mesa = input(f"  Nueva mesa [{ped.mesa}]: ").strip()
        nueva_mesa = int(raw_mesa) if raw_mesa.isdigit() and int(raw_mesa) > 0 else ped.mesa

        print(Pantalla.linea())
        print(Color.titulo("  RESUMEN DE CAMBIOS", Color.NARANJA))
        print(Pantalla.linea())
        estado_labels = {"P": "Pendiente", "E": "En preparación", "L": "Listo", "C": "Cancelado"}
        print(f"  Mesa   : {Color.texto(str(nueva_mesa), Color.BLANCO)}")
        print(f"  Estado : {Color.texto(estado_labels.get(nuevo_estado, nuevo_estado), Color.MENTA)}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(Color.texto("  ¿Confirmar cambios? (S/N): ", Color.DORADO))
        if confirmacion == "S":
            ped.estado = nuevo_estado
            ped.mesa   = nueva_mesa
            self._guardar()
            print(Color.texto("\n  ✔  Pedido actualizado correctamente.", Color.MENTA))
        else:
            print(Color.texto("\n  ✖  Actualización cancelada.", Color.ROJO))

        Pantalla.pausar()

    @decorador_interfaz("ELIMINAR PEDIDO")
    @manejar_errores
    def eliminar(self):
        if not self._pedidos:
            print(Color.texto("  No hay pedidos registrados.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "ELIMINAR PEDIDO"

        while True:
            self._listar_simple()
            print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
            ped_id = self.pedir_entero(
                Color.texto("\n  ID del pedido a eliminar: ", Color.DORADO), "ID")
            if ped_id == 0:
                print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                Pantalla.pausar()
                return
            ped = self.buscar_por_id(ped_id)
            if ped:
                break
            error_flash("Pedido no encontrado.", TITULO)
            Pantalla.encabezado(TITULO)

        plato = self._plato.buscar_por_id(ped.id_plato)
        plato_n = plato.nombre if plato else "?"

        print(Pantalla.linea())
        print(f"  Pedido # : {Color.texto(str(ped.id), Color.NARANJA)}")
        print(f"  Mesa     : {ped.mesa}")
        print(f"  Plato    : {plato_n}")
        print(f"  Total    : {Color.texto(self.formatear_moneda(ped.total), Color.MENTA)}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(
            Color.texto("  ¿Confirmar eliminación? (S/N): ", Color.ROJO))
        if confirmacion == "S":
            self._pedidos = list(filter(lambda p: p.id != ped_id, self._pedidos))
            self._guardar()
            print(Color.texto("\n  ✔  Pedido eliminado.", Color.MENTA))
            Pantalla.pausar()
            return ped_id

        Pantalla.pausar()
        return None

    def eliminar_por_plato(self, plato_id: int) -> None:
        self._pedidos = list(filter(lambda p: p.id_plato != plato_id, self._pedidos))
        self._guardar()

    @decorador_interfaz("ESTADÍSTICAS DE PEDIDOS")
    def estadisticas(self):
        if not self._pedidos:
            print(Color.texto("  No hay pedidos registrados.", Color.DORADO))
            Pantalla.pausar()
            return

        estados = {"P": 0, "E": 0, "L": 0, "C": 0}
        for ped in self._pedidos:
            estados[ped.estado] = estados.get(ped.estado, 0) + 1

        total_ingresos = sum(p.total for p in self._pedidos if p.estado != "C")

        print(Pantalla.linea("─", 52))
        print(Color.titulo("  ESTADO DE PEDIDOS", Color.NARANJA))
        print(Pantalla.linea("─", 52))
        labels = {"P": "Pendientes", "E": "En preparación", "L": "Listos", "C": "Cancelados"}
        colors = {"P": Color.DORADO, "E": Color.NARANJA, "L": Color.MENTA, "C": Color.ROJO}
        for k, label in labels.items():
            bar = "█" * estados[k]
            print(f"  {Color.texto(f'{label:<18}', colors[k])} {estados[k]:>3}  {Color.texto(bar, colors[k])}")

        print(Pantalla.linea("─", 52))
        print(Color.titulo("  INGRESOS", Color.NARANJA))
        print(Pantalla.linea("─", 52))
        print(f"  {Color.texto('Total facturado :', Color.MENTA)} {Color.texto(self.formatear_moneda(total_ingresos), Color.MENTA)}")

        if self._pedidos:
            plato_conteo: dict = {}
            for ped in self._pedidos:
                plato_conteo[ped.id_plato] = plato_conteo.get(ped.id_plato, 0) + ped.cantidad
            top_id = max(plato_conteo, key=lambda k: plato_conteo[k])
            top_plato = self._plato.buscar_por_id(top_id)
            top_nombre = top_plato.nombre if top_plato else f"ID {top_id}"
            print(f"  {Color.texto('Plato más pedido:', Color.DORADO)} {top_nombre} ({plato_conteo[top_id]} uds.)")

        print(Pantalla.linea("─", 52))
        Pantalla.pausar()

    def _listar_simple(self):
        print(Pantalla.linea())
        for ped in self._pedidos:
            plato = self._plato.buscar_por_id(ped.id_plato)
            plato_n = plato.nombre if plato else "?"
            est_color = {
                "P": Color.DORADO, "E": Color.NARANJA, "L": Color.MENTA, "C": Color.ROJO
            }.get(ped.estado, Color.BLANCO)
            print(
                f"  {Color.texto(f'#{ped.id:>3}', Color.NARANJA)} | "
                f"Mesa {ped.mesa:>2} | "
                f"{plato_n:<28} | "
                f"{Color.texto(ped.estado_label(), est_color)}"
            )
        print(Pantalla.linea())
