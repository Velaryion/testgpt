# testgpt

Repositorio en fase inicial. El objetivo funcional y la tecnología están pendientes de definir.

## Estado actual

Esta base contiene documentación y configuración básica de Git. Todavía no hay una aplicación ejecutable, dependencias ni pruebas automatizadas.

## Empezar

Necesitas Git para obtener una copia local:

```sh
git clone https://github.com/Velaryion/testgpt.git
cd testgpt
```

Lee [la guía de inicio](docs/INICIO.md) y concreta el primer caso de uso antes de añadir código o herramientas.

## Organización

- `README.md`: estado del proyecto y primeros pasos.
- `.gitignore`: exclusiones básicas para archivos locales.
- `docs/INICIO.md`: decisiones pendientes y criterios para la primera versión.

Las carpetas de código y pruebas se crearán cuando se elija la tecnología, siguiendo sus convenciones.

## Flujo de trabajo

1. Define un cambio pequeño y su resultado esperado.
2. Crea una rama para desarrollarlo: `git switch -c feat/nombre-del-cambio`.
3. Añade instrucciones para ejecutar y verificar cualquier funcionalidad nueva.
4. Revisa el diff antes del commit y abre una pull request hacia `main`.

No subas credenciales ni datos personales. Si el proyecto necesita variables de entorno, documenta sus nombres en un `.env.example` con valores ficticios.

## Licencia

Pendiente de elección por el titular del proyecto. Esta base no incluye un archivo `LICENSE`.
