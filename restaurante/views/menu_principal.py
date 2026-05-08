from controllers.categoria_controller import CategoriaController
from controllers.plato_controller import PlatoController
from controllers.pedido_controller import PedidoController
from controllers.stats_controller import StatsController
from core.decoradores import Color, Pantalla, error_flash


class MenuPrincipal:

    def __init__(self):
        self._cat    = CategoriaController()
        self._plato  = PlatoController(self._cat)
        self._pedido = PedidoController(self._plato, self._cat)
        self._stats  = StatsController(self._cat, self._plato, self._pedido)

    def _imprimir_menu(self, titulo: str, opciones: list[tuple]):
        Pantalla.encabezado(titulo)
        for clave, etiqueta in opciones:
            if clave == "0":
                print(Color.texto(f"  {clave}. {etiqueta}", Color.ROJO))
            else:
                print(Color.texto(f"  {clave}. ", Color.DORADO) + etiqueta)
        print(Pantalla.linea())
        return input(Color.texto("  Seleccione: ", Color.NARANJA)).strip()

    def _menu_registrar(self):
        opciones = {
            "1": ("Registrar Categoría", self._cat.crear),
            "2": ("Registrar Plato",     self._plato.crear),
            "3": ("Registrar Pedido",    self._pedido.crear),
        }
        self._ejecutar_submenu("REGISTRAR", opciones)

    def _menu_consultar(self):
        opciones = {
            "1": ("Categorías", self._cat.consultar),
            "2": ("Platos",     self._plato.consultar),
            "3": ("Pedidos",    self._pedido.consultar),
        }
        self._ejecutar_submenu("CONSULTAR", opciones)

    def _menu_buscar(self):
        opciones = {
            "1": ("Buscar Categoría", lambda: self._cat.buscar()),
            "2": ("Buscar Plato",     lambda: self._plato.buscar()),
            "3": ("Buscar Pedido",    lambda: self._pedido.buscar()),
        }
        self._ejecutar_submenu("BUSCAR", opciones)

    def _menu_actualizar(self):
        opciones = {
            "1": ("Actualizar Categoría", lambda: self._cat.actualizar()),
            "2": ("Actualizar Plato",     lambda: self._plato.actualizar()),
            "3": ("Actualizar Pedido",    lambda: self._pedido.actualizar()),
        }
        self._ejecutar_submenu("ACTUALIZAR", opciones)

    def _menu_eliminar(self):
        Pantalla.encabezado("ELIMINAR REGISTRO")
        print(Color.texto("  1. ", Color.DORADO) + "Eliminar Categoría")
        print(Color.texto("  2. ", Color.DORADO) + "Eliminar Plato")
        print(Color.texto("  3. ", Color.DORADO) + "Eliminar Pedido")
        print(Color.texto("  0. ", Color.ROJO)   + "Volver")
        print(Pantalla.linea())
        opc = input(Color.texto("  Seleccione: ", Color.NARANJA)).strip()

        if opc == "1":
            cat_id = self._cat.eliminar()
            if cat_id:
                vinculados = len(list(filter(
                    lambda p: p.id_categoria == cat_id, self._plato.todos())))
                if vinculados:
                    print(Color.texto(
                        f"  ⚠  Se eliminarán {vinculados} plato(s) y sus pedidos vinculados.",
                        Color.DORADO))
                    if input(Color.texto("  ¿Continuar? (1. Sí / 2. No): ", Color.ROJO)).strip() == "1":
                        # Eliminar pedidos de esos platos primero
                        for plato in list(filter(lambda p: p.id_categoria == cat_id, self._plato.todos())):
                            self._pedido.eliminar_por_plato(plato.id)
                        self._plato.eliminar_por_categoria(cat_id)
                        self._cat.eliminar_por_id(cat_id)
                        print(Color.texto("  ✔  Categoría y datos vinculados eliminados.", Color.MENTA))
        elif opc == "2":
            plato_id = self._plato.eliminar()
            if plato_id:
                vinculados = len(list(filter(
                    lambda p: p.id_plato == plato_id, self._pedido.todos())))
                if vinculados:
                    print(Color.texto(
                        f"  ⚠  Se eliminarán {vinculados} pedido(s) vinculado(s).",
                        Color.DORADO))
                    if input(Color.texto("  ¿Continuar? (1. Sí / 2. No): ", Color.ROJO)).strip() == "1":
                        self._pedido.eliminar_por_plato(plato_id)
                        self._plato.eliminar_por_id(plato_id)
                        print(Color.texto("  ✔  Plato y pedidos eliminados.", Color.MENTA))
        elif opc == "3":
            self._pedido.eliminar()
        elif opc == "0":
            return
        else:
            error_flash("Opción no válida.", "")

    def _ejecutar_submenu(self, titulo: str, opciones: dict):
        while True:
            lista = [(k, label) for k, (label, _) in opciones.items()]
            lista.append(("0", "Volver"))
            opc = self._imprimir_menu(titulo, lista)
            if opc == "0":
                break
            elif opc in opciones:
                opciones[opc][1]()
            else:
                error_flash("Opción no válida.", "")

    def ejecutar(self):
        opciones = [
            ("1", "Registrar"),
            ("2", "Consultar"),
            ("3", "Buscar"),
            ("4", "Actualizar"),
            ("5", "Eliminar"),
            ("6", "Estadísticas de Pedidos"),
            ("7", "Resumen General"),
            ("0", "Salir"),
        ]
        acciones = {
            "1": self._menu_registrar,
            "2": self._menu_consultar,
            "3": self._menu_buscar,
            "4": self._menu_actualizar,
            "5": self._menu_eliminar,
            "6": self._pedido.estadisticas,
            "7": self._stats.resumen_general,
        }

        while True:
            opc = self._imprimir_menu("SISTEMA DE GESTIÓN DE RESTAURANTE", opciones)
            if opc == "0":
                Pantalla.limpiar()
                print(Color.texto("\n  🍽  ¡Hasta pronto! Gracias por usar el sistema.\n", Color.MENTA))
                break
            elif opc in acciones:
                acciones[opc]()
            else:
                error_flash("Opción no válida.", "")
