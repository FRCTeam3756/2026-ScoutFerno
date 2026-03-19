from pydantic import BaseModel
from .auto_data_models import Auto_Data_Read
from .interview_data_models import Interview_Data_Read
from .teleop_data_models import Teleop_Data_Read

class All_Data(BaseModel):
    auto: list[Auto_Data_Read]
    interview: list[Interview_Data_Read]
    teleop: list[Teleop_Data_Read]