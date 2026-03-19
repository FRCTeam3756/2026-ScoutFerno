from .auto_data_crud import read_auto_data
from .interview_data_crud import read_interview_match_data
from .teleop_data_crud import read_teleop_data


class read_all_data:
    read_interview_match_data()
    read_auto_data()
    read_teleop_data()
