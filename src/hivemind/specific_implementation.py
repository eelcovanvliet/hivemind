
from specific_MooringSystem import CatenaryDesign, Catenary


class Caternary3x4Design(CatenaryDesign):
    Spread = 1

class Caternary3x4(Catenary):

    def __init__(self, parameters: Caternary3x4Design):
        super().__init__(parameters)

class Presets:
    def NewcasteOffshoreWind():
        design = CatenaryDesign()
        design.AnchorRadius = 200
        return Catenary(design)


MooringSystem_system = Presets.NewcasteOffshoreWind()