# 🍽️ Sistema de Gestión de Restaurante

> Aplicación de consola en Python que gestiona categorías, platos y pedidos con arquitectura MVC y principios de Programación Orientada a Objetos.

---

## 👥 Integrantes

| Nombre |
|--------|
| Jhoan Ariel Cevallos Villavicencio |
| Jean Pierre Jiménez Bajaña |
| José Antonio Torres Torres |
| Jhonatan Gabriel Castro Belfor |
| Elian Wladimir Galeas Barén |

---

## 📋 Información del Proyecto

| Campo | Detalle |
|-------|---------|
| 📚 Materia | Programación Orientada a Objetos |
| 👨‍🏫 Docente | Ing. Daniel Vera |
| 📅 Año | 2026 |
| 🐍 Lenguaje | Python 3.12+ |

---

## 📌 Descripción

Sistema de administración de restaurante por línea de comandos. Permite gestionar **categorías**, **platos del menú** y **pedidos por mesa**, con persistencia en archivos JSON e interfaz de terminal con colores ANSI.

Aplica los pilares de la POO —encapsulamiento, herencia y polimorfismo— junto con patrones MVC, interfaces abstractas (ABC), mixins de validación y decoradores de funciones.

---

## 📁 Estructura del Proyecto

```
restaurante/
│
├── main.py                          # Punto de entrada
│
├── models/                          # Entidades del dominio
│   ├── categoria.py                 # Clase Categoria
│   ├── plato.py                     # Clase Plato
│   └── pedido.py                    # Clase Pedido (estados P/E/L/C)
│
├── core/                            # Núcleo reutilizable
│   ├── interfaces.py                # Interfaz ICrud (ABC)
│   ├── mixins.py                    # CalculosMixin: validaciones y helpers
│   ├── decoradores.py               # Color, Pantalla, @decorador_interfaz
│   └── json_manager.py              # Lectura/escritura JSON
│
├── controllers/                     # Lógica de negocio
│   ├── categoria_controller.py      # CRUD categorías
│   ├── plato_controller.py          # CRUD platos
│   ├── pedido_controller.py         # CRUD pedidos + estadísticas
│   └── stats_controller.py          # Resumen general
│
├── views/
│   └── menu_principal.py            # Menú de navegación principal
│
└── data/                            # Persistencia
    ├── categorias.json
    ├── platos.json
    └── pedidos.json
```

---

## 🧩 Modelos / Entidades

### `Categoria`
| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `id` | `int` | Identificador único |
| `nombre` | `str` | Nombre de la categoría |
| `descripcion` | `str` | Descripción breve |

### `Plato`
| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `id` | `int` | Identificador único |
| `nombre` | `str` | Nombre del plato |
| `id_categoria` | `int` | Categoría a la que pertenece |
| `precio` | `float` | Precio en dólares |
| `descripcion` | `str` | Descripción del plato |
| `disponible` | `str` | `"S"` disponible / `"N"` no disponible |

### `Pedido`
| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `id` | `int` | Identificador único |
| `mesa` | `int` | Número de mesa |
| `id_plato` | `int` | Plato solicitado |
| `cantidad` | `int` | Unidades pedidas |
| `total` | `float` | Precio total calculado |
| `estado` | `str` | `P` Pendiente · `E` En preparación · `L` Listo · `C` Cancelado |
| `fecha` | `str` | Fecha y hora del pedido |

---

## ⚙️ Funcionalidades

- ✅ **CRUD completo** para Categorías, Platos y Pedidos
- 🔗 **Eliminación en cascada** — al borrar una categoría se eliminan sus platos y pedidos vinculados
- 🛡️ **Validación robusta** de todos los campos con mensajes de error y reintento
- 💾 **Persistencia automática** en archivos JSON con codificación UTF-8
- 📊 **Estadísticas de pedidos** — estado, ingresos totales, plato más pedido
- 📈 **Resumen general** — precios promedio, plato más caro/barato, total facturado
- 🎨 **Interfaz de color** en terminal ANSI (naranja / dorado / menta)

---

## 🎓 Conceptos de POO Aplicados

| Concepto | Dónde se aplica |
|----------|----------------|
| **Clases y Objetos** | `models/*.py` |
| **Encapsulamiento** | Atributos `_categorias`, `_platos`, `_pedidos` en controllers |
| **Herencia múltiple** | Controllers heredan de `ICrud` + `CalculosMixin` |
| **Clases abstractas (ABC)** | `core/interfaces.py` — interfaz `ICrud` |
| **Mixins** | `CalculosMixin` con validaciones reutilizables |
| **Decoradores** | `@decorador_interfaz`, `@manejar_errores` |
| **Métodos de clase** | `from_dict()`, `JsonManager.leer()`, `JsonManager.escribir()` |
| **Lambdas / filter / map** | Filtrado y transformación de listas en controllers |
| **Patrón MVC** | Separación clara entre models / controllers / views |

---

## 🚀 Ejecución

```bash
# Descomprimir y entrar al directorio
cd restaurante/

# Ejecutar el sistema
python main.py
```

> **Requisitos:** Python 3.12+ — sin dependencias externas.  
> Los datos se guardan automáticamente en `restaurante/data/*.json`.

---

## 📂 Datos de Ejemplo

El proyecto incluye datos de prueba listos para usar:

**Categorías:** Entradas, Postres, Bebidas, Comida Gourmet, Helados  
**Platos:** Ceviche de camarón, Tigrillo, Seco de pollo, Churrasco, Flan de vainilla, Jugo de maracuyá, entre otros  
**Pedidos:** 4 pedidos de prueba en distintas mesas y estados

---

<div align="center">

**Sistema de Gestión de Restaurante** · Programación Orientada a Objetos · 2026

</div>
