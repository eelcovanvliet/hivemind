from generic_mooring import Mooring
from carg_io.abstracts import ParameterSet


class CatenaryDesign(ParameterSet):
    AnchorRadius = 100

class Catenary(Mooring):

    def __init__(self, parameters:ParameterSet):
        self._parameters = parameters

    def change_state(self):
        return super().change_state()

    def parameters(self) -> CatenaryDesign:
        return self._parameters
    
if __name__ == "__main__":
    design = CatenaryDesign()
    cat = Catenary(design)
    cat.change_state()

