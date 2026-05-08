from core.interfaces import ICrud
from core.mixins import CalculosMixin
from core.decoradores import decorador_interfaz, manejar_errores, Color, Pantalla, error_flash
from core.json_manager import JsonManager
from models.categoria import Categoria


class CategoriaController(ICrud, CalculosMixin):

    ARCHIVO = "categorias.json"

    def __init__(self):
        self._categorias: list[Categoria] = self._cargar()

    def _cargar(self) -> list[Categoria]:
        return list(map(Categoria.from_dict, JsonManager.leer(self.ARCHIVO)))

    def _guardar(self) -> None:
        JsonManager.escribir(self.ARCHIVO, list(map(lambda c: c.to_dict(), self._categorias)))

    def todos(self) -> list[Categoria]:
        return self._categorias

    def buscar_por_id(self, cat_id: int):
        return next((c for c in self._categorias if c.id == cat_id), None)

    def siguiente_id(self) -> int:
        return max((c.id for c in self._categorias), default=0) + 1

    @decorador_interfaz("REGISTRO DE CATEGORÍA")
    @manejar_errores
    def crear(self):
        TITULO = "REGISTRO DE CATEGORÍA"

        def _encabezado():
            print(Color.texto("  Complete los datos de la nueva categoría:\n", Color.NARANJA))

        _encabezado()

        nombre = self.pedir_nombre("  Nombre      : ", titulo=TITULO, contexto=_encabezado)

        def _ctx_desc():
            print(Color.texto("  Complete los datos de la nueva categoría:\n", Color.NARANJA))
            print(f"  Nombre      : {Color.texto(nombre, Color.BLANCO)}")

        descripcion = self.pedir_descripcion("  Descripción : ", titulo=TITULO, contexto=_ctx_desc)

        print(Pantalla.linea())
        print(Color.titulo("  RESUMEN DE NUEVA CATEGORÍA", Color.NARANJA))
        print(Pantalla.linea())
        print(f"  Nombre      : {Color.texto(nombre, Color.BLANCO)}")
        print(f"  Descripción : {Color.texto(descripcion, Color.BLANCO)}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(Color.texto("  ¿Desea guardar? (S/N): ", Color.DORADO))
        if confirmacion == "S":
            cat = Categoria(self.siguiente_id(), nombre, descripcion)
            self._categorias.append(cat)
            self._guardar()
            print(Color.texto(f"\n  ✔  Categoría '{nombre}' guardada con éxito.", Color.MENTA))
        else:
            print(Color.texto("\n  ✖  Registro cancelado.", Color.ROJO))

        Pantalla.pausar()

    @decorador_interfaz("LISTADO DE CATEGORÍAS")
    def consultar(self):
        if not self._categorias:
            print(Color.texto("  (Sin categorías registradas)", Color.DORADO))
            Pantalla.pausar()
            return

        print(Pantalla.linea("─", 65))
        for cat in self._categorias:
            print(f"  {Color.texto(str(cat), Color.BLANCO)}")
        print(Pantalla.linea("─", 65))
        print(Color.texto(f"  Total categorías: {len(self._categorias)}", Color.NARANJA))
        Pantalla.pausar()

    @decorador_interfaz("BUSCAR CATEGORÍA")
    @manejar_errores
    def buscar(self, id: int = None):
        if not self._categorias:
            print(Color.texto("  No hay categorías registradas.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "BUSCAR CATEGORÍA"

        if id is None:
            while True:
                self._listar_simple()
                print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
                id = self.pedir_entero(
                    Color.texto("\n  ID de categoría a buscar: ", Color.DORADO), "ID")
                if id == 0:
                    print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                    Pantalla.pausar()
                    return
                cat = self.buscar_por_id(id)
                if cat:
                    break
                error_flash("Categoría no encontrada.", TITULO)
                Pantalla.encabezado(TITULO)
        else:
            cat = self.buscar_por_id(id)
            if not cat:
                error_flash("Categoría no encontrada.", TITULO)
                return

        print(Pantalla.linea("─", 55))
        print(f"  {Color.texto('ID          :', Color.DORADO)} {cat.id}")
        print(f"  {Color.texto('Nombre      :', Color.DORADO)} {cat.nombre}")
        print(f"  {Color.texto('Descripción :', Color.DORADO)} {cat.descripcion}")
        print(Pantalla.linea("─", 55))
        Pantalla.pausar()

    @decorador_interfaz("ACTUALIZAR CATEGORÍA")
    @manejar_errores
    def actualizar(self, id: int = None):
        if not self._categorias:
            print(Color.texto("  No hay categorías registradas.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "ACTUALIZAR CATEGORÍA"

        if id is None:
            while True:
                self._listar_simple()
                print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
                id = self.pedir_entero(
                    Color.texto("\n  ID de categoría a actualizar: ", Color.DORADO), "ID")
                if id == 0:
                    print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                    Pantalla.pausar()
                    return
                cat = self.buscar_por_id(id)
                if cat:
                    break
                error_flash("Categoría no encontrada.", TITULO)
                Pantalla.encabezado(TITULO)

        print(Pantalla.linea())
        print(Color.texto("  Datos actuales:", Color.NARANJA))
        print(f"  Nombre      : {cat.nombre}")
        print(f"  Descripción : {cat.descripcion}")
        print(Pantalla.linea())
        print(Color.texto("  Ingrese nuevos datos (Enter para mantener el actual):\n", Color.DORADO))

        raw_n = input(f"  Nombre      [{cat.nombre}]: ").strip()
        nuevo_nombre = self.validar_texto_general(raw_n, "nombre") if raw_n else cat.nombre

        raw_d = input(f"  Descripción [{cat.descripcion}]: ").strip()
        nueva_desc = self.validar_texto_general(raw_d, "descripción") if raw_d else cat.descripcion

        print(Pantalla.linea())
        print(Color.titulo("  RESUMEN DE CAMBIOS", Color.NARANJA))
        print(Pantalla.linea())
        print(f"  Nombre      : {Color.texto(nuevo_nombre, Color.BLANCO)}")
        print(f"  Descripción : {Color.texto(nueva_desc, Color.BLANCO)}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(Color.texto("  ¿Confirmar cambios? (S/N): ", Color.DORADO))
        if confirmacion == "S":
            cat.nombre      = nuevo_nombre
            cat.descripcion = nueva_desc
            self._guardar()
            print(Color.texto("\n  ✔  Categoría actualizada correctamente.", Color.MENTA))
        else:
            print(Color.texto("\n  ✖  Actualización cancelada.", Color.ROJO))

        Pantalla.pausar()

    @decorador_interfaz("ELIMINAR CATEGORÍA")
    @manejar_errores
    def eliminar(self):
        if not self._categorias:
            print(Color.texto("  No hay categorías registradas.", Color.DORADO))
            Pantalla.pausar()
            return

        TITULO = "ELIMINAR CATEGORÍA"

        while True:
            self._listar_simple()
            print(Color.texto("  (Ingrese 0 para cancelar)", Color.AZUL))
            cat_id = self.pedir_entero(
                Color.texto("\n  ID de categoría a eliminar: ", Color.DORADO), "ID")
            if cat_id == 0:
                print(Color.texto("\n  ✖  Operación cancelada.", Color.ROJO))
                Pantalla.pausar()
                return
            cat = self.buscar_por_id(cat_id)
            if cat:
                break
            error_flash("Categoría no encontrada.", TITULO)
            Pantalla.encabezado(TITULO)

        print(Pantalla.linea())
        print(f"  Categoría   : {Color.texto(cat.nombre, Color.NARANJA)}")
        print(f"  Descripción : {cat.descripcion}")
        print(Pantalla.linea())

        confirmacion = self.pedir_si_no(
            Color.texto("  ¿Confirmar eliminación? (S/N): ", Color.ROJO))
        if confirmacion == "S":
            self._categorias = list(filter(lambda c: c.id != cat_id, self._categorias))
            self._guardar()
            print(Color.texto("\n  ✔  Categoría eliminada.", Color.MENTA))
            Pantalla.pausar()
            return cat_id

        Pantalla.pausar()
        return None

    def eliminar_por_id(self, cat_id: int) -> None:
        self._categorias = list(filter(lambda c: c.id != cat_id, self._categorias))
        self._guardar()

    def _listar_simple(self):
        print(Pantalla.linea())
        for cat in self._categorias:
            print(
                f"  {Color.texto(f'ID {cat.id:>3}', Color.DORADO)} | "
                f"{cat.nombre}"
            )
        print(Pantalla.linea())
