from datetime import date, datetime
from typing import Dict, List, Optional

from backend.models.base import Base

class Survey(Base):
    def __init__(
            self,
            first_name: Optional[str]=None,
            birth_date: Optional[datetime]=None,
            gender: Optional[str]=None,
            departure_city: Optional[str]=None,
            arrival_city: Optional[str]=None,
            date_range: List[Optional[datetime]]=[None, None],
            trip_purpose: Optional[str]=None,
            daily_budget: Optional[int]=None,
            transportation_preference: Optional[str]=None,
            interests: List[str]=[],
            other_interests: Optional[str]=None,
            other_cities: bool=False,
            other_companions: bool=False,
            social_media_link: Optional[str]=None) -> None:
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.date_range = date_range
        self.trip_purpose = trip_purpose
        self.daily_budget = daily_budget
        self.transportation_preference = transportation_preference
        self.interests = interests
        self.other_interests = other_interests
        self.other_cities = other_cities
        self.other_companions = other_companions
        self.social_media_link = social_media_link

    @property
    def trip_kind(self) -> str:
        if self.other_companions:
            return "Group Trip"
        return "Solo Trip"

    def to_dict(self) -> Dict:
        self.date_range = [datetime.combine(d, datetime.min.time()) if isinstance(d, date) else d for d in self.date_range]
        self.birth_date = datetime.combine(self.birth_date, datetime.min.time()) if isinstance(self.birth_date, date) else self.birth_date
        return super().to_dict()
