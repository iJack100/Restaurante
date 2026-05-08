from core.interfaces import ICrud
from core.mixins import CalculosMixin
from core.decoradores import decorador_interfaz, manejar_errores, Color, Pantalla, error_flash
from core.json_manager import JsonManager
from models.plato import Plato


class PlatoController(ICrud, CalculosMixin):

    ARCHIVO = "platos.json"

    def __init__(self, cat_ctrl):
        self._platos: list[Plato] = self._cargar()
        self._cat = cat_ctrl

    def _cargar(self) -> list[Plato]:
        return list(map(Plato.from_dict, JsonManager.leer(self.ARCHIVO)))

    def _guardar(self) -> None:
        JsonManager.escribir(self.ARCHIVO, list(map(lambda p: p.to_dict(), self._platos)))

    def todos(self) -> list[Plato]:
        return self._platos

    def buscar_por_id(self, plato_id: int):
        return next((p for p in self._platos if p.id == plato_id), None)

    def siguiente_id(self) -> int:
        return max((p.id for p in self._platos), default=0) + 1

    @decorador_interfaz("REGISTRO DE PLATO")
    @manejar_errores
    def crear(self):
        TITULO = "REGISTRO DE PLATO"
        categorias = self._cat.todos()

        if not categorias:
            print(Color.texto("  ⚠  Debe registrar al menos una categoría primero.", Color.ROJO))
            Pantalla.pausar()
            return

        def _encabezado():
            print(Color.texto("  Complete los datos del nuevo plato:\n", Color.NARANJA))

        _encabezado()

        nombre = self.pedir_nombre("  Nombre      : ", titulo=TITULO, contexto=_encabezado)

        def _ctx_desc():
            print(Color.texto("  Complete los datos del nuevo plato:\n", Color.NARANJA))
            print(f"  Nombre      : {Color.texto(nombre, Color.BLANCO)}")

        descripcion = self.pedir_descripcion("  Descripción : ", titulo=TITULO, contexto=_ctx_desc)

        # Seleccionar categoría
        print(Pantalla.linea())
        print(Color.texto("  Categorías disponibles:", Color.NARANJA))
        for cat in categorias:
            print(f"    {Color.texto(f'[{cat.id}]', Color.DORADO)} {cat.nombre}")
        print(Pantalla.linea())

        def _ctx_cat():
            print(Color.texto("  Complete los datos del nuevo plato:\n", Color.NARANJA))
            print(f"  Nombre      : {Color.texto(nombre, Color.BLANCO)}")
            print(f"  Descripción : {Color.texto(descripcion, Color.BLANCO)}")

        while True:
            cat_id = self.pedir_entero(
                Color.texto("  ID Categoría : ", Color.DORADO), "ID categoría",
                titulo=TITULO, contexto=_ctx_cat)
            cat = self._cat.buscar_por_id(cat_id)
            if cat:
                break
            error_flash("Categoría no encontrada.", TITULO, _ctx_cat)
            Pantalla.encabezado(TITULO)
            _ctx_cat()
            print(Pantalla.linea())
            print(Color.texto("  Categorías disponibles:", Color.NARANJA))
            for c in categorias:
                print(f"    {Color.texto(f'[{c.id}]', Color.DORADO)} {c.nombre}")
            print(Pantalla.linea())

        def _ctx_precio():
            print(Color.texto("  Complete los datos del nuevo plato:\n", Color.NARANJA))
            print(f"  Nombre      : {Color.texto(nombre, Color.BLANCO)}")
            print(f"  Descripción : {Color.texto(descripcion, Color.BLANCO)}")
            print(f"  Categoría   : {Color.texto(cat.nombre, Color.BLANCO)}")

        precio = self.pedir_precio("  Precio ($)   : ", titulo=TITULO, contexto=_ctx_precio)
        disponible = self.pedir_disponibilidad(
            Color.texto("  Disponible (S/N): ", Color.DORADO), titulo=TITULO, contexto=_ctx_precio)

        print(Pantalla.linea())
        print(Color.titulo("  RESUMEN DEL NUEVO PLATO", Color.NARANJA))
        print(Pantalla.linea())
        print(f"  Nombre      : {Color.texto(nombre, Color.BLANCO)}")
        print(f"  Descripción : {Color.texto(descripcion, Color.BLANCO)}")
        print(f"  Categoría   : {Color.texto(cat.nombre, Color.BLANCO)}")
        print(f"  Precio      : {Color.texto(self.formatear_moneda(precio), Color.MENTA)}")
        disp_label = "Disponible" if disponible == "S" else "No disponible"
        print(f"  Estado      : {Color.texto(disp_label, Color.MENTA)}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(Color.texto("  ¿Desea guardar? (S/N): ", Color.DORADO))
        if confirmacion == "S":
            plato = Plato(self.siguiente_id(), nombre, cat_id, precio, descripcion, disponible)
            self._platos.append(plato)
            self._guardar()
            print(Color.texto(f"\n  ✔  Plato '{nombre}' guardado con éxito.", Color.MENTA))
        else:
            print(Color.texto("\n  ✖  Registro cancelado.", Color.ROJO))

        Pantalla.pausar()

    @decorador_interfaz("MENÚ — LISTADO DE PLATOS")
    def consultar(self):
        if not self._platos:
            print(Color.texto("  (Sin platos registrados)", Color.DORADO))
            Pantalla.pausar()
            return

        print(Pantalla.linea("─", 70))
        for plato in self._platos:
            cat = self._cat.buscar_por_id(plato.id_categoria)
            cat_nombre = cat.nombre if cat else "?"
            print(
                f"  {Color.texto(str(plato), Color.BLANCO)} | "
                f"Cat: {Color.texto(cat_nombre, Color.DORADO)}"
            )
        print(Pantalla.linea("─", 70))
        print(Color.texto(f"  Total platos: {len(self._platos)}", Color.NARANJA))
        Pantalla.pausar()

    @decorador_interfaz("BUSCAR PLATO")
    @manejar_errores
    def buscar(self, id: int = None):
        if not self._platos:
            print(Color.texto("  No hay platos registrados.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "BUSCAR PLATO"

        if id is None:
            while True:
                self._listar_simple()
                print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
                id = self.pedir_entero(
                    Color.texto("\n  ID del plato a buscar: ", Color.DORADO), "ID")
                if id == 0:
                    print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                    Pantalla.pausar()
                    return
                plato = self.buscar_por_id(id)
                if plato:
                    break
                error_flash("Plato no encontrado.", TITULO)
                Pantalla.encabezado(TITULO)

        plato = self.buscar_por_id(id)
        if not plato:
            error_flash("Plato no encontrado.", TITULO)
            return

        cat = self._cat.buscar_por_id(plato.id_categoria)
        cat_nombre = cat.nombre if cat else "Desconocida"

        print(Pantalla.linea("─", 60))
        print(f"  {Color.texto('ID          :', Color.DORADO)} {plato.id}")
        print(f"  {Color.texto('Nombre      :', Color.DORADO)} {plato.nombre}")
        print(f"  {Color.texto('Descripción :', Color.DORADO)} {plato.descripcion}")
        print(f"  {Color.texto('Categoría   :', Color.DORADO)} {cat_nombre}")
        print(f"  {Color.texto('Precio      :', Color.DORADO)} {self.formatear_moneda(plato.precio)}")
        print(f"  {Color.texto('Disponible  :', Color.DORADO)} {plato.disponible_label()}")
        print(Pantalla.linea("─", 60))
        Pantalla.pausar()

    @decorador_interfaz("ACTUALIZAR PLATO")
    @manejar_errores
    def actualizar(self, id: int = None):
        if not self._platos:
            print(Color.texto("  No hay platos registrados.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "ACTUALIZAR PLATO"

        if id is None:
            while True:
                self._listar_simple()
                print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
                id = self.pedir_entero(
                    Color.texto("\n  ID del plato a actualizar: ", Color.DORADO), "ID")
                if id == 0:
                    print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                    Pantalla.pausar()
                    return
                plato = self.buscar_por_id(id)
                if plato:
                    break
                error_flash("Plato no encontrado.", TITULO)
                Pantalla.encabezado(TITULO)

        print(Pantalla.linea())
        print(Color.texto("  Datos actuales:", Color.NARANJA))
        print(f"  Nombre      : {plato.nombre}")
        print(f"  Descripción : {plato.descripcion}")
        print(f"  Precio      : {self.formatear_moneda(plato.precio)}")
        print(f"  Disponible  : {plato.disponible_label()}")
        print(Pantalla.linea())
        print(Color.texto("  Ingrese nuevos datos (Enter para mantener el actual):\n", Color.DORADO))

        raw_n = input(f"  Nombre      [{plato.nombre}]: ").strip()
        nuevo_nombre = self.validar_texto_general(raw_n, "nombre") if raw_n else plato.nombre

        raw_d = input(f"  Descripción [{plato.descripcion}]: ").strip()
        nueva_desc = self.validar_texto_general(raw_d, "descripción") if raw_d else plato.descripcion

        raw_p = input(f"  Precio      [{plato.precio}]: ").strip()
        nuevo_precio = self.validar_positivo(raw_p, "precio") if raw_p else plato.precio

        raw_disp = input(f"  Disponible  [{plato.disponible}] (S/N): ").strip().upper()
        nueva_disp = raw_disp if raw_disp in ("S", "N") else plato.disponible

        print(Pantalla.linea())
        print(Color.titulo("  RESUMEN DE CAMBIOS", Color.NARANJA))
        print(Pantalla.linea())
        print(f"  Nombre      : {Color.texto(nuevo_nombre, Color.BLANCO)}")
        print(f"  Descripción : {Color.texto(nueva_desc, Color.BLANCO)}")
        print(f"  Precio      : {Color.texto(self.formatear_moneda(nuevo_precio), Color.MENTA)}")
        disp_label = "Disponible" if nueva_disp == "S" else "No disponible"
        print(f"  Estado      : {Color.texto(disp_label, Color.MENTA)}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(Color.texto("  ¿Confirmar cambios? (S/N): ", Color.DORADO))
        if confirmacion == "S":
            plato.nombre      = nuevo_nombre
            plato.descripcion = nueva_desc
            plato.precio      = nuevo_precio
            plato.disponible  = nueva_disp
            self._guardar()
            print(Color.texto("\n  ✔  Plato actualizado correctamente.", Color.MENTA))
        else:
            print(Color.texto("\n  ✖  Actualización cancelada.", Color.ROJO))

        Pantalla.pausar()

    @decorador_interfaz("ELIMINAR PLATO")
    @manejar_errores
    def eliminar(self):
        if not self._platos:
            print(Color.texto("  No hay platos registrados.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "ELIMINAR PLATO"

        while True:
            self._listar_simple()
            print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
            plato_id = self.pedir_entero(
                Color.texto("\n  ID del plato a eliminar: ", Color.DORADO), "ID")
            if plato_id == 0:
                print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                Pantalla.pausar()
                return
            plato = self.buscar_por_id(plato_id)
            if plato:
                break
            error_flash("Plato no encontrado.", TITULO)
            Pantalla.encabezado(TITULO)

        print(Pantalla.linea())
        print(f"  Plato       : {Color.texto(plato.nombre, Color.NARANJA)}")
        print(f"  Precio      : {Color.texto(self.formatear_moneda(plato.precio), Color.MENTA)}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(
            Color.texto("  ¿Confirmar eliminación? (S/N): ", Color.ROJO))
        if confirmacion == "S":
            self._platos = list(filter(lambda p: p.id != plato_id, self._platos))
            self._guardar()
            print(Color.texto("\n  ✔  Plato eliminado.", Color.MENTA))
            Pantalla.pausar()
            return plato_id

        Pantalla.pausar()
        return None

    def eliminar_por_categoria(self, cat_id: int) -> None:
        self._platos = list(filter(lambda p: p.id_categoria != cat_id, self._platos))
        self._guardar()

    def eliminar_por_id(self, plato_id: int) -> None:
        self._platos = list(filter(lambda p: p.id != plato_id, self._platos))
        self._guardar()

    def _listar_simple(self):
        print(Pantalla.linea())
        for p in self._platos:
            cat = self._cat.buscar_por_id(p.id_categoria)
            cat_n = cat.nombre if cat else "?"
            disp = "✔" if p.disponible == "S" else "✖"
            print(
                f"  {Color.texto(f'ID {p.id:>3}', Color.DORADO)} | "
                f"{p.nombre:<28} | "
                f"{Color.texto(self.formatear_moneda(p.precio), Color.MENTA)} | "
                f"{Color.texto(cat_n, Color.NARANJA)} {disp}"
            )
        print(Pantalla.linea())
