from .constants import event_metrics as event_metrics, match_metrics as match_metrics, team_event_metrics as team_event_metrics, team_match_metrics as team_match_metrics, team_metrics as team_metrics, team_year_metrics as team_year_metrics, year_metrics as year_metrics
from .validate import check_type as check_type, get_locations as get_locations, get_type as get_type
from _typeshed import Incomplete
from typing import Any, Dict, List, Optional


class Statbotics:
    BASE_URL: str
    session: Incomplete
    def __init__(self) -> None: ...

    def get_team(self, team: int, fields: List[str] = [
                 'all']) -> Dict[str, Any]: ...

    def get_teams(self, country: Optional[str] = None, state: Optional[str] = None, district: Optional[str] = None, active: Optional[bool] = True,
                  metric: str = 'team', ascending: Optional[bool] = None, limit: int = 100, offset: int = 0, fields: List[str] = ['all']) -> List[Dict[str, Any]]: ...

    def get_year(self, year: int, fields: List[str] = [
                 'all']) -> Dict[str, Any]: ...

    def get_years(self, metric: str = 'year', ascending: Optional[bool] = None, limit: int = 100,
                  offset: int = 0, fields: List[str] = ['all']) -> List[Dict[str, Any]]: ...

    def get_team_year(self, team: int, year: int, fields: List[str] = [
                      'all']) -> Dict[str, Any]: ...

    def get_team_years(self, team: Optional[int] = None, year: Optional[int] = None, country: Optional[str] = None, state: Optional[str] = None, district: Optional[str] = None,
                       metric: str = 'team', ascending: Optional[bool] = None, limit: int = 100, offset: int = 0, fields: List[str] = ['all']) -> List[Dict[str, Any]]: ...

    def get_event(self, event: str, fields: List[str] = [
                  'all']) -> Dict[str, Any]: ...

    def get_events(self, year: Optional[int] = None, country: Optional[str] = None, state: Optional[str] = None, district: Optional[str] = None, type: int | Optional[str] = None,
                   week: Optional[int] = None, metric: str = 'year', ascending: Optional[bool] = None, limit: int = 100, offset: int = 0, fields: List[str] = ['all']) -> List[Dict[str, Any]]: ...

    def get_team_event(self, team: int, event: str, fields: List[str] = [
                       'all']) -> Dict[str, Any]: ...

    def get_team_events(self, team: Optional[int] = None, year: Optional[int] = None, event: Optional[str] = None, country: Optional[str] = None, state: Optional[str] = None, district: Optional[str] = None, type: int |
                        Optional[str] = None, week: Optional[int] = None, metric: str = 'year', ascending: Optional[bool] = None, limit: int = 0, offset: int = 0, fields: List[str] = ['all']) -> List[Dict[str, Any]]: ...

    def get_match(self, match: str, fields: List[str] = [
                  'all']) -> Dict[str, Any]: ...

    def get_matches(self, team: Optional[int] = None, year: Optional[int] = None, event: Optional[str] = None, week: Optional[int] = None, elims: Optional[bool] = None,
                    metric: str = 'time', ascending: Optional[bool] = None, limit: int = 200, offset: int = 0, fields: List[str] = ['all']) -> List[Dict[str, Any]]: ...

    def get_team_match(self, team: int, match: str, fields: List[str] = [
                       'all']) -> Dict[str, Any]: ...

    def get_team_matches(self, team: Optional[int] = None, year: Optional[int] = None, event: Optional[str] = None, match: Optional[str] = None, week: Optional[int] = None, elims: bool |
                         None = None, metric: str = 'time', ascending: Optional[bool] = None, limit: int = 100, offset: int = 0, fields: List[str] = ['all']) -> List[Dict[str, Any]]: ...
