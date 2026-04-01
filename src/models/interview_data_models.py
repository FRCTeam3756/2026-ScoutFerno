from typing import Optional
from sqlmodel import SQLModel, Field

from .sql_models import Database_Data

class Interview_Data_Base(Database_Data):
    ball_storage: Optional[int] = Field(default=None, index=True) # Rough amount
    drivetrain_type: Optional[str] = Field(default=None, index=True) # Tank or Swerve
    shooter_type: Optional[str] = Field(default=None, index=True) # Turret or Drum
    shooter_ball_width: Optional[int] = Field(default=None, index=True) # 1 or 2 turret | 1, 2, 3, 4 ball width shooter
    intake_type: Optional[str] = Field(default=None, index=True) # Over the bumper (arm or extender) or through the bumper
    intake_amount: Optional[int] = Field(default=None, index=True) # Rough amount of balls that fit into intake
    field_elements_usability: Optional[str] = Field(default=None, index=True) # Can it go over bump, under trench or both?
    climb_level: Optional[str] = Field(default=None, index=True) # Arm, Flippy thing, Thunderstamps, etc= Field(index=True)
    climb_positions: Optional[str] = Field(default=None, index=True) # Inner, Outer, Both, None

class Interview_Data(Interview_Data_Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class Interview_Data_Create(Interview_Data_Base):
    pass

class Interview_Data_Update(SQLModel):
    ball_storage: Optional[int] = None 
    drivetrain_type: Optional[str] = None
    shooter_type: Optional[str] = None 
    shooter_ball_width: Optional[int] = None 
    intake_type: Optional[str] = None
    intake_amount: Optional[int] = None 
    field_elements_usability: Optional[str] = None
    climb_level: Optional[str] = None
    climb_positions: Optional[str] = None
