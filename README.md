# API para las inscripciones de AVAST



## Desarrollo

Preparar el entorno de Python:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_dev.txt
```

Ejecutar la aplicación:
```bash
flask run --debugger --debug --reload --host=0.0.0.0
```


### Operaciones con la base de datos

flask db --help

flask db init
flask db migrate -m "Crear tabla Actividades"

Migraciones:
- flask db upgrade
- flask db downgrade
- flask db downgrade base
- flask db downgrade <revision>

### Ejecutar pruebas

Para ejecutar las pruebas primero debes iniciar el servidor de base de datos. Puedes utilizar el docker-compose que hay incluido por defecto:
```
docker-compose up db
```

Luego, ejecutar las pruebas con pytest:

```bash
pytest
```


@pytest.mark.run_this
pytest tests -k run_this
