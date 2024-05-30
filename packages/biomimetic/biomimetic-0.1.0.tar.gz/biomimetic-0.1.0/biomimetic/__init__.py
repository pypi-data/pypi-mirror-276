# biomimetic/__init__.py
import numpy as np

# simple models
from .SBmc import SimpleBiomimeticCell
from .SBmcModel import SimpleBmcModel
from .SBBmc import SimpleBiasBiomimeticCell
from .SBBmcModel import SimpleBiasBmcModel
from .SMBBmc import SimpleModeBiasBiomimeticCell
from .SMBBmcModel import SimpleModeBiasBmcModel

# parallel models
from .POMBmc import ParallelOMBiomimeticCell
from .POMBmcModel import ParallelOMBmcModel
from .PMOBmc import ParallelMOBiomimeticCell
from .PMOBmcModel import ParallelMOBmcModel
from .PMMBmc import ParallelMMBiomimeticCell
from .PMMBmcModel import ParallelMMBmcModel

# mutlimodal parallel models
from .MOMBmc import ModeOMBiomimeticCell
from .MOMBmcModel import ModeOMBmcModel
from .MMOBmc import ModeMOBiomimeticCell
from .MMOBmcModel import ModeMOBmcModel
from .MMMBmc import ModeMMBiomimeticCell
from .MMMBmcModel import ModeMMBmcModel


# from biomimetic import *
__all__ = [
    "SimpleBiomimeticCell"
    "SimpleBmcModel"
    "SimpleBiasBiomimeticCell"
    "SimpleBiasBmcModel"
    "SimpleModeBiasBiomimeticCell"
    "SimpleModeBiasBmcModel"
    "ParallelOMBiomimeticCell"
    "ParallelOMBmcModel"
    "ParallelMOBiomimeticCell"
    "ParallelMOBmcModel"
    "ParallelMMBiomimeticCell"
    "ParallelMMBmcModel"
    "ModeOMBiomimeticCell"
    "ModeOMBmcModel"
    "ModeMOBiomimeticCell"
    "ModeMOBmcModel"
    "ModeMMBiomimeticCell"
    "ModeMMBmcModel"
]
