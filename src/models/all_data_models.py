from pydantic import BaseModel
from .prematch_data_models import Prematch_Data, Prematch_Data_Create, Prematch_Data_Update
from .autonomous_data_models import Autonomous_Data, Autonomous_Data_Create, Autonomous_Data_Update
from .teleop_data_models import Teleop_Data, Teleop_Data_Create, Teleop_Data_Update
from .endgame_data_models import Endgame_Data, Endgame_Data_Create, Endgame_Data_Update
from .postmatch_data_models import Postmatch_Data, Postmatch_Data_Create, Postmatch_Data_Update

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

class All_Data_Update(BaseModel):
    prematch: Prematch_Data_Update 
    autonomous: Autonomous_Data_Update
    teleop: Teleop_Data_Update
    endgame: Endgame_Data_Update
    postmatch: Postmatch_Data_Update

class All_Data_Delete(BaseModel):
    prematch: list[Prematch_Data]
    autonomous: list[Autonomous_Data]
    teleop: list[Teleop_Data]
    endgame: list[Endgame_Data]
    postmatch: list[Postmatch_Data]