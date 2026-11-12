"""Native top-level browser: the user logs into the real site, never into our code.

No JS bridge, cookie extraction, or automated login. The WebView handles HTTPS
and authenticated downloads; only user-selected local torrents reach Transmission.
"""
from pathlib import Path
from urllib.parse import urlsplit
import sys
import tempfile
from transmission import find_transmission, save_transmission, send_file_to_transmission

TRACKER = 'https://torrent.unionfansub.com/browse.php'

def is_tracker(url):
    try:
        p = urlsplit(url)
        return p.scheme == 'https' and p.hostname == 'torrent.unionfansub.com' and not p.username and not p.password
    except ValueError:
        return False

def run(smoke_test=False):
    import webview
    from webview.menu import Menu, MenuAction
    window = None

    def open_torrent():
        try:
            paths = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False,
                                             file_types=('Torrent (*.torrent)',))
            if not paths:
                return
            executable = find_transmission()
            if not executable:
                selected = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False,
                                                     file_types=('Transmission (*.exe)',))
                if not selected:
                    return
                executable = save_transmission(selected[0])
            path = Path(paths[0])
            if window.create_confirmation_dialog('Enviar a Transmission', f'¿Abrir {path.name} en Transmission?'):
                send_file_to_transmission(executable, path)
        except Exception:
            # Do not include URLs or tracker/account details in errors or logs.
            window.create_confirmation_dialog('No se pudo abrir el torrent',
                'Selecciona un archivo .torrent válido y comprueba la ubicación de Transmission.')

    webview.settings['ALLOW_DOWNLOADS'] = True
    window = webview.create_window(
        'UnionFansub · Inicia sesión, busca y descarga · AnimeDesk',
        html='<html><body>Prueba de navegador integrado</body></html>' if smoke_test else None,
        url=None if smoke_test else TRACKER,
        width=1150, height=800, min_size=(850, 550))
    menu = [Menu('Transmission', [MenuAction('Abrir archivo .torrent descargado…', open_torrent)])]
    smoke_errors = []
    def close_smoke_window():
        try:
            if not window.events.loaded.wait(25):
                raise RuntimeError('WebView2 no terminó de cargar el HTML local.')
            if window.evaluate_js('document.body.textContent') != 'Prueba de navegador integrado':
                raise RuntimeError('WebView2 no renderizó el documento esperado.')
        except Exception as error:
            smoke_errors.append(error)
        finally:
            window.destroy()
    # Private profile: session survives navigation, not closing the browser.
    with tempfile.TemporaryDirectory(prefix='AnimeDesk-WebView-', ignore_cleanup_errors=True) as profile:
        webview.start(func=close_smoke_window if smoke_test else None,
                      gui='edgechromium' if sys.platform == 'win32' else None,
                      private_mode=True, storage_path=profile, menu=menu)
    if smoke_errors:
        raise RuntimeError('Falló la comprobación local del navegador.') from smoke_errors[0]

if __name__ == '__main__':
    run('--smoke-test' in sys.argv)
