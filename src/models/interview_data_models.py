from sqlmodel import SQLModel, Field

class Interview_Match_Data_Base(SQLModel):
    team_number: int = Field(index=True)
    ball_storage: int = Field(index=True) # Rough amount
    drivetrain_type: str = Field(index=True) # Tank or Swerve
    shooter_type: str = Field(index=True) # Turret or Shooter
    shooter_amount: int = Field(index=True) # 1 or 2 turret | 1, 2, 3, 4 ball width shooter
    intake_type: str = Field(index=True) # Over the bumper (arm or extender) or through the bumper
    intake_sturdyness: str = Field(index=True) # not moving, moves a little, moves alot, etc
    intake_amount: int = Field(index=True) # Rough amount of balls that fit into intake
    field_elements_useabillity: str = Field(index=True) # Can it go over bump, under trench or both?
    climb_type: str = Field(index=True) # Arm, Flippy thing, Thunderstamps, etc= Field(index=True)

class Interview_Match_Data(Interview_Match_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)


class Interview_Match_Data_Create(Interview_Match_Data_Base):
    pass


class Interview_Match_Data_Update(SQLModel):
    ball_storage: int | None = None 
    drivetrain_type: str | None = None
    shooter_type: str | None = None 
    shooter_amount: int | None = None 
    intake_type: str | None = None
    intake_sturdyness: str | None = None 
    intake_amount: int | None = None 
    field_elements_useabillity: str | None = None
    climb_type: str | None = None


class Interview_Data_Read(Interview_Match_Data_Base):
    pass