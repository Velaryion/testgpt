# AnimeDesk para Transmission

App Windows con Python 3.12, Tkinter, pywebview 5.4 y Microsoft Edge WebView2 Runtime. El EXE incluye Python y pywebview, pero necesita WebView2 (habitual en Windows 10/11) y Transmission Qt instalados.

## Nyaa

Busca, selecciona y pulsa **Descargar en Transmission**, o haz doble clic. El RSS muestra resultados recientes y no admite paginación. La app detecta Transmission o permite seleccionar `transmission-qt.exe`. Guarda esa ruta en `%APPDATA%\AnimeDesk\settings.json`.

## UnionFansub con tu cuenta

1. Selecciona `https://torrent.unionfansub.com/browse.php` y pulsa **Iniciar sesión / Catálogo**.
2. La ventana integrada abre la web real. Inicia sesión y usa el buscador del tracker. La caja principal de búsqueda de Nyaa se desactiva para esta fuente.
3. Descarga el `.torrent` desde la web y elige dónde guardarlo.
4. Abre el menú de esa ventana **Transmission → Abrir archivo .torrent descargado…**, selecciona el archivo y confirma su envío.
5. También puedes usar **Abrir .torrent local** en la ventana principal.

El catálogo del tracker se muestra en su propia ventana integrada, no en la tabla RSS de Nyaa. El navegador descarga el torrent con tu sesión; Transmission recibe el archivo local, sin necesitar tus cookies. Si hay captcha o segundo factor, resuélvelo en la web.

La sesión dura mientras mantengas abierta esa ventana. El perfil es privado y debes volver a iniciar sesión al cerrarla. AnimeDesk no guarda tu contraseña ni expone una API de Python al sitio. Los `.torrent` privados pueden contener identificadores de tu cuenta: no los compartas. Cerrar AnimeDesk no cierra automáticamente una ventana de UnionFansub en uso. Si ya está abierta, vuelve a ella desde la barra de tareas.

Si falta WebView2, instala Microsoft Edge WebView2 Runtime desde Microsoft y vuelve a abrirla. Transmission gestiona progreso y carpeta de destino.

## Otras fuentes

RSS HTTPS y páginas públicas con enlaces magnet/.torrent o temas `showthread.php?tid=…`. No es un buscador universal. **Ver publicación** usa tu navegador habitual. **Pegar magnet / .torrent** acepta enlaces públicos; para descargas privadas, guarda el torrent desde UnionFansub y ábrelo localmente.

Usa contenido que tengas derecho a descargar.

## Ejecutar o compilar

En Windows con Python 3.12: `python -m pip install -r requirements-windows.txt` y `python app.py`. Para compilar, doble clic en `crear-exe.cmd`. Resultado: `dist/AnimeDesk.exe`, sin Python en el equipo de destino. No está firmado.

El workflow **Compilar AnimeDesk para Windows** publica una release al subir cambios a `anime-desk`, si pasan las pruebas y los arranques de ambas ventanas.

## Validación

`python ci_tests.py` comprueba RSS, enlaces, archivos torrent, envío simulado a Transmission y controles de interfaz en Windows. La prueba del navegador integrado usa HTML local y no inicia sesión ni contacta con UnionFansub.

El entorno de desarrollo bloquea `torrent.unionfansub.com`. No se ha probado el acceso real con una cuenta, la búsqueda ni la descarga autenticada: sigue pendiente en el equipo del usuario. No se han descargado episodios durante el desarrollo.
