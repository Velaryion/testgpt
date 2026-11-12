# AnimeDesk · primera versión para Transmission

App de escritorio independiente de Bolsillo, con Python 3.12 y Tkinter. Ejecutar desde esta carpeta: `python app.py` (Windows: `py app.py`). No requiere paquetes de producción.

## Usar con Transmission

1. Instala Transmission Qt para Windows.
2. AnimeDesk busca `transmission-qt.exe` en las ubicaciones habituales. Si no lo encuentra, pulsa **Configurar Transmission** y selecciona el ejecutable. Guarda la ruta en `%APPDATA%\AnimeDesk\settings.json`.
3. Busca en Nyaa, selecciona un resultado y pulsa **Descargar**. Confirma el envío y comprueba en Transmission el torrent y su carpeta de destino. Admite enlaces magnet y URL HTTPS `.torrent`, enviados como argumentos a Transmission sin ejecutar una shell.
4. Las transferencias y su progreso se gestionan en Transmission; esta versión no muestra el progreso dentro de AnimeDesk.

## Fuentes

- Nyaa: búsqueda RSS de anime, títulos, tamaño, semillas. El RSS muestra los resultados recientes proporcionados por la fuente; no admite paginación. Afina la búsqueda para encontrar un episodio concreto.
- Puedes pegar otra URL RSS HTTPS o página pública con enlaces magnet/.torrent.
- UnionFansub: pega una sección pública para listar sus temas. El filtro solo busca entre los enlaces de esa página. Si requiere cuenta, usa **Abrir web**, inicia sesión en el navegador y pega el magnet o URL .torrent. No importa cookies ni accede a contenido privado automáticamente. El índice puede no mostrar temas o torrents.
- Usa contenido que tengas derecho a descargar. No se almacenan contraseñas.

## Crear EXE en Windows

Instala **Python 3.12 para Windows**, incluido su lanzador `py`. Haz doble clic en `crear-exe.cmd`: crea un entorno aislado, instala PyInstaller 6.16.0, ejecuta las pruebas, genera el EXE y comprueba su arranque. Abre la carpeta de salida al terminar. Requiere Internet para instalar PyInstaller.

Resultado: `dist/AnimeDesk.exe`. El equipo donde uses ese EXE no necesita Python; sí Transmission. El ejecutable no está firmado. El script instala y compila localmente; no sube archivos ni publica nada.

Alternativa: ejecutar manualmente el workflow **Compilar AnimeDesk para Windows** tras subir el código a GitHub. Descarga su artefacto `AnimeDesk-Windows`. El workflow comprueba también el arranque del EXE antes de ofrecer el artefacto; publica una release con `AnimeDesk.exe` si la compilación y el arranque pasan. También se activa al subir cambios de la app a la rama `anime-desk`.

## Estado de validación

`python -m unittest discover -s tests -v`: nueve pruebas de RSS, enlaces del foro, deduplicación, validación, configuración y envío a Transmission (proceso simulado).

En el entorno Linux actual, no se ha podido validar la interfaz gráfica por falta de pantalla, ni generar/ejecutar un EXE de Windows. Los accesos a Nyaa y UnionFansub reciben 403 del proxy del entorno; la API de GitHub también devuelve Forbidden, lo que impide lanzar Actions desde aquí. No se ha descargado ningún torrent.

Pendiente en Windows: compilar, comprobar búsquedas reales y envío a una instalación real de Transmission. Las pruebas simuladas no demuestran que las fuentes actuales funcionen.

## Interfaz corregida

El botón **Descargar en Transmission** está junto a Buscar. También puedes hacer doble clic en el torrent. Se ha quitado Siguiente porque el RSS de Nyaa no admite esa paginación. La tabla se ajusta a la ventana para mantener los botones y mensajes visibles.
