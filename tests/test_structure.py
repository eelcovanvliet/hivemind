from hivemind.structural import Structure
import pytest

from gmsh_utils import utils


class ExampleStructure(Structure):
    
    @property
    def change_state(self):
        raise NotImplementedError()
    
    def get_ballast_tanks(self):
        raise NotImplementedError()
    
    def get_geometry(self) -> utils.VolumeComponent:
        utils.start('structure')
        volume = utils.make_trapezodial_prism([
            [0,0,0],
            [1,0,0],
            [1,1,0],
            [0,1,0],
            
            [0,0,1],
            [1,0,1],
            [1,1,1],
            [0,1,1],
        ])
        return volume
    
    @property
    def get_inertia(self):
        raise NotImplementedError()
    
    @property
    def parameters(self):
        raise NotImplementedError()
    
    @property
    def possible_states(self):
        raise NotImplementedError()
    
    @property
    def previous_state(self):
        raise NotImplementedError()
    
    @property
    def state(self):
        raise NotImplementedError()


class TestCase:

    structure = ExampleStructure()

    def test_cut(self):
        geom = self.structure.get_geometry()
        submerged, waterplane = self.structure.cut_geometry(geom, 1/2, roll=0)
        submerged_volume = submerged.get_size()
        surface_area = waterplane.get_size()
        assert submerged_volume == pytest.approx(0.5)
        assert surface_area == pytest.approx(1)

