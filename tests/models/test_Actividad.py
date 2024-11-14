import pytest
from datetime import time
from app.models.actividad import Actividad
from app import create_app,db

@pytest.fixture(scope='module')
def app():
    """Fixture para crear y configurar la aplicación de pruebas."""
    app = create_app()  # Asegúrate de que tu aplicación Flask esté correctamente configurada.
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope='module')
def app_context(app):
    """Fixture to push and pop the app context for each test."""
    with app.app_context():  # Automatically push the app context
        yield  # This runs the test
        # After the test completes, the context is automatically popped

@pytest.fixture(scope='module', autouse=True)
def before_all(app):
    """Inicializa la base de datos para las pruebas."""
    print("Inicializando base de datos")
    with app.app_context():
        db.create_all()  # Crea las tablas

    with app.app_context():
        yield

    with app.app_context():
        db.drop_all()  # Elimina las tablas después de las pruebas

@pytest.fixture(scope='function', autouse=True)
def before_each():
    """Elimina todos los registros de la tabla de actividades antes de cada prueba."""
    db.session.query(Actividad).delete()
    db.session.commit()
    yield

@pytest.fixture
def actividad_valida():
    """Fixture de una actividad válida."""
    return Actividad(
        descripcion="Actividad de prueba",
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        año_minimo=2000,
        año_maximo=2020
    )

@pytest.mark.run_this
def test_actividad_valida(actividad_valida):
    """Prueba que una actividad válida sea insertada correctamente en la base de datos."""
    db.session.add(actividad_valida)
    db.session.commit()
    assert actividad_valida.id is not None

def test_hora_fin_menor_hora_inicio():
    """Prueba que falle al intentar guardar una actividad donde `hora_fin` es menor que `hora_inicio`."""
    actividad = Actividad(
        descripcion="Hora fin menor que hora inicio",
        hora_inicio=time(10, 0),
        hora_fin=time(9, 0),
        año_minimo=2000,
        año_maximo=2020
    )
    with pytest.raises(ValueError):
        db.session.add(actividad)
        db.session.commit()

    db.session.rollback()

def test_año_maximo_menor_año_minimo():
    """Prueba que falle al intentar guardar una actividad donde `año_maximo` es menor que `año_minimo`."""
    actividad = Actividad(
        descripcion="Año máximo menor que año mínimo",
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        año_minimo=2020,
        año_maximo=2000
    )
    with pytest.raises(ValueError):
        db.session.add(actividad)
        db.session.commit()

    db.session.rollback()

def test_años_negativos():
    """Prueba que falle al intentar guardar una actividad con `año_minimo` o `año_maximo` negativos."""
    with pytest.raises(ValueError):
        actividad = Actividad(
            descripcion="Años negativos",
            hora_inicio=time(9, 0),
            hora_fin=time(10, 0),
            año_minimo=-2000,
            año_maximo=2020
        )

    with pytest.raises(ValueError):
        actividad = Actividad(
            descripcion="Años negativos",
            hora_inicio=time(9, 0),
            hora_fin=time(10, 0),
            año_minimo=2000,
            año_maximo=-2020
        )
