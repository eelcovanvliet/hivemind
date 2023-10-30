from hivemind.abstracts import Inertia
import pytest


initial_mass = 100
initial_location_x = 0
initial_location_y = 10
initial_location_z = 2

inertia_object = Inertia(mass=initial_mass, location=(initial_location_x, initial_location_y, initial_location_z))

def test_inertia_object_location():
    """Test to assess if location properties returned equal initial defined location"""

    location_x = inertia_object.location_x
    location_y = inertia_object.location_y
    location_z = inertia_object.location_z

    assert location_x == pytest.approx(initial_location_x)
    assert location_y == pytest.approx(initial_location_y)
    assert location_z == pytest.approx(initial_location_z)


def test_inertia_object_mass():
    """Test to assess if mass property returned equal initial defined mass"""

    mass = inertia_object.mass

    assert mass == pytest.approx(initial_mass)



print('hallo')
