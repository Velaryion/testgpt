"""Launch Transmission Qt with a validated URL, without a shell."""
import json
import os
from pathlib import Path
import shutil
import subprocess
from core import downloadable

def config_file():
    root = Path(os.environ.get('APPDATA') or Path.home() / '.config')
    return root / 'AnimeDesk' / 'settings.json'

def find_transmission():
    try:
        value = json.loads(config_file().read_text(encoding='utf-8')).get('transmission', '')
        if value and Path(value).is_file():
            return value
    except (OSError, ValueError, TypeError, AttributeError):
        pass
    for name in ('transmission-qt', 'transmission-qt.exe'):
        value = shutil.which(name)
        if value:
            return value
    for variable in ('ProgramFiles', 'ProgramFiles(x86)', 'LOCALAPPDATA'):
        root = os.environ.get(variable)
        if root:
            for relative in ('Transmission/transmission-qt.exe', 'Programs/Transmission/transmission-qt.exe'):
                path = Path(root) / relative
                if path.is_file():
                    return str(path)
    return ''

def save_transmission(path):
    path = Path(path).resolve()
    if not path.is_file():
        raise ValueError('Selecciona el ejecutable de Transmission instalado.')
    target = config_file()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps({'transmission': str(path)}), encoding='utf-8')
    temporary.replace(target)
    return str(path)

def send_to_transmission(executable, url):
    url = downloadable(url)
    if not executable or not Path(executable).is_file():
        raise ValueError('Configura la ubicación de Transmission antes de descargar.')
    return subprocess.Popen([str(executable), url], shell=False)
