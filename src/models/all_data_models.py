from pydantic import BaseModel
from .prematch_data_models import Prematch_Data, Prematch_Data_Create
from .autonomous_data_models import Autonomous_Data, Autonomous_Data_Create
from .teleop_data_models import Teleop_Data, Teleop_Data_Create
from .endgame_data_models import Endgame_Data, Endgame_Data_Create
from .postmatch_data_models import Postmatch_Data, Postmatch_Data_Create

class All_Data(BaseModel):
    prematch: list[Prematch_Data]
    autonomous: list[Autonomous_Data]
    teleop: list[Teleop_Data]
    endgame: list[Endgame_Data]
    postmatch: list[Postmatch_Data]

class All_Data_Create(BaseModel):
    prematch: Prematch_Data_Create
    autonomous: Autonomous_Data_Create
    teleop: Teleop_Data_Create
    endgame: Endgame_Data_Create
    postmatch: Postmatch_Data_Create