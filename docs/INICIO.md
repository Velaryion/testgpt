# Primera versión: Bolsillo

## Decisiones

- Objetivo: registrar y entender los gastos e ingresos personales.
- Interfaz: web adaptable a móvil y escritorio, en español y euros.
- Tecnología: HTML, CSS y módulos JavaScript nativos, sin paquetes externos.
- Datos: importes enteros en céntimos y fechas de calendario; persistencia local por navegador/origen.
- Copias: JSON versionado, máximo 10 MB y 50.000 movimientos; restauración con sustitución explícita, no fusión.
- Licencia: pendiente de elección del titular.

## Verificación manual

1. Abrir la app vacía: balance, ingresos y gastos a cero y explicación para empezar.
2. Añadir un ingreso de 1.000 € y un gasto de 12,34 € en el mismo mes: balance de 987,66 €.
3. Recargar: los dos movimientos permanecen.
4. Editar el gasto, buscar su concepto y alternar filtros.
5. Cambiar de mes y comprobar que el resumen y el reparto por categorías cambian.
6. Exportar una copia; cancelar una eliminación y comprobar que no cambia nada.
7. Eliminar el gasto, restaurar la copia y comprobar que reaparece tras confirmar.
8. Intentar importar un JSON dañado: la app informa del error y conserva los datos actuales.
9. Repetir el formulario y los filtros en móvil; comprobar navegación por teclado y cierre con Escape.

## Límites y siguiente paso

No hay cuenta, sincronización, conexión bancaria, gastos recurrentes ni presupuestos. La copia exportada contiene los movimientos en texto legible. El balance es la diferencia del mes seleccionado, no el saldo de una cuenta bancaria. La siguiente mejora puede ser un presupuesto por categoría o sincronización con una cuenta, según el uso real.
