from pydantic import BaseModel
from .prematch_data_models import Prematch_Data
from .auto_data_models import Auto_Data
from .teleop_data_models import Teleop_Data
from .endgame_data_models import Endgame_Data
from .postmatch_data_models import Postmatch_Data

class All_Data(BaseModel):
    prematch: list[Prematch_Data]
    auto: list[Auto_Data]
    teleop: list[Teleop_Data]
    endgame: list[Endgame_Data]
    postmatch: list[Postmatch_Data]