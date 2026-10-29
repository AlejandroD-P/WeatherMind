import pytest
from hypothesis import given, strategies as st

#logica de weathermind 
def clasificar_actividad(temperatura: float, prob_lluvia: float) -> str:
    if prob_lluvia >= 50.0:
        return "No salir: Alta probabilidad de lluvia"
    elif temperatura < 8.0:
        return "No salir: Frío excesivo"
    elif temperatura > 34.0:
        return "No salir: Calor excesivo"
    return "Salir: Clima favorable"

#pruebas

@given(
    temperatura=st.floats(min_value=-20.0, max_value=50.0, allow_nan=False),
    prob_lluvia=st.floats(min_value=50.0, max_value=100.0, allow_nan=False)
)
def test_prioridad_lluvia_siempre_interiores(temperatura, prob_lluvia):
    resultado = clasificar_actividad(temperatura, prob_lluvia)
    assert resultado == "No salir: Alta probabilidad de lluvia"

@given(
    temperatura=st.floats(min_value=12.0, max_value=28.0, allow_nan=False),
    prob_lluvia=st.floats(min_value=0.0, max_value=19.9, allow_nan=False)
)
def test_condiciones_optimas_siempre_aire_libre(temperatura, prob_lluvia):
    resultado = clasificar_actividad(temperatura, prob_lluvia)
    assert resultado == "Salir: Clima favorable"
