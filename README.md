# Bolsillo · testgpt

Aplicación web personal para llevar ingresos y gastos en euros desde el móvil o el PC. HTML, CSS y JavaScript nativos, sin dependencias de producción ni servidor de datos.

## Funciones

- Crear, editar y eliminar movimientos con concepto, importe, fecha y categoría.
- Resumen mensual de ingresos, gastos y balance; reparto del gasto por categoría.
- Buscar por concepto o categoría y filtrar ingresos/gastos.
- Guardado automático en el navegador y actualización entre pestañas.
- Exportar y restaurar copias JSON con validación y confirmación antes de reemplazar datos.

La aplicación empieza vacía. No hay conexión bancaria ni sincronización entre dispositivos. Los datos se guardan en `localStorage` para cada origen y navegador; se pueden perder al borrar sus datos o usar navegación privada. Exporta copias con regularidad. El código público no incluye tus movimientos.

## Ejecutar en tu equipo

Clona el repositorio y sirve la carpeta `dist` con cualquier servidor estático. Por ejemplo, con Python 3 instalado:

```sh
git clone https://github.com/Velaryion/testgpt.git
cd testgpt
python -m http.server 8080 --directory dist
```

Abre http://localhost:8080. En Windows también puedes usar `py -m http.server 8080 --directory dist`. Mantén el mismo origen y puerto para acceder a los datos guardados. Para utilizarla desde otros dispositivos, sírvela mediante HTTPS; no abras `index.html` directamente como archivo.

## Comprobaciones

Con Node.js 20 o superior, sin instalar paquetes:

```sh
npm test
npm run check
```

Las pruebas cubren importes en céntimos, fechas, cálculos y validación de copias. El almacenamiento es local y no está cifrado por la aplicación.

## Estructura

- `dist/`: aplicación estática lista para servir; se edita directamente, no requiere compilación.
- `dist/core.mjs`: validación y cálculos independientes de la interfaz.
- `tests/`: pruebas con el ejecutor integrado de Node.js.
- `docs/INICIO.md`: alcance, decisiones y comprobación manual.
- `.openai/hosting.json`: configuración de la versión privada en Sites.

## Licencia

Pendiente de elección por el titular. No se ha añadido una licencia automáticamente.
