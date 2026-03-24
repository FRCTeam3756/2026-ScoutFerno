from pydantic import BaseModel
from .auto_data_models import Auto_Data
from .interview_data_models import Interview_Data
from .teleop_data_models import Teleop_Data

class All_Data(BaseModel):
    auto: list[Auto_Data]
    postmatch: list[Interview_Data]
    teleop: list[Teleop_Data]