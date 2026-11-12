"""Bounded bencode validation prevents opening login HTML as a torrent."""
from pathlib import Path

LIMIT = 16 * 1024 * 1024

def validate_file(filename):
    path = Path(filename).resolve()
    if path.suffix.lower() != '.torrent':
        raise ValueError('Selecciona un archivo .torrent.')
    with path.open('rb') as stream:
        data = stream.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError('El torrent supera el límite de 16 MB.')
    index = 0
    nodes = 0
    def parse(depth=0):
        nonlocal index, nodes
        nodes += 1
        if depth > 40 or nodes > 200000 or index >= len(data):
            raise ValueError('Torrent no válido.')
        token = data[index:index+1]
        if token == b'i':
            index += 1
            end = data.find(b'e', index)
            value = data[index:end]
            if end < 0 or len(value) > 30 or not value or value in (b'-0', b'-'):
                raise ValueError('Entero no válido.')
            digits = value[1:] if value.startswith(b'-') else value
            if not digits.isdigit() or len(digits)>1 and digits.startswith(b'0'):
                raise ValueError('Entero no válido.')
            index = end + 1
            return int(value)
        if token in (b'd', b'l'):
            index += 1
            result = {} if token == b'd' else []
            while index < len(data) and data[index:index+1] != b'e':
                value = parse(depth+1)
                if token == b'd':
                    if not isinstance(value, bytes) or value in result:
                        raise ValueError('Diccionario no válido.')
                    result[value] = parse(depth+1)
                else:
                    result.append(value)
            if index >= len(data): raise ValueError('Torrent incompleto.')
            index += 1
            return result
        colon = data.find(b':', index, index+12)
        size = data[index:colon]
        if colon < 0 or not size.isdigit() or len(size)>1 and size.startswith(b'0'):
            raise ValueError('Cadena no válida.')
        length = int(size); index = colon+1
        end = index + length
        if end > len(data): raise ValueError('Torrent incompleto.')
        result = data[index:end]; index = end
        return result
    try:
        result = parse()
        if index != len(data) or not isinstance(result, dict) or not isinstance(result.get(b'info'), dict):
            raise ValueError('Falta el diccionario info del torrent.')
    except (ValueError, OverflowError, RecursionError) as error:
        raise ValueError('No es un archivo torrent válido; podría ser una página de acceso.') from error
    return path
