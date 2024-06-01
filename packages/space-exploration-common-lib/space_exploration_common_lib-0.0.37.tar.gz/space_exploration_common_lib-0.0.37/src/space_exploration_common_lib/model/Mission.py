import datetime
from pydantic import BaseModel
from typing import List
from ..model.Duration import Duration


class Mission(BaseModel):
    mission: str
    astronauts: List[str]
    program: str
    call_sign: str
    image_url: str
    launch_date_utc: str
    launch_mass_lbs: int
    launch_site: str
    launch_site_coord: str
    launch_vehicle: str
    orbits: int
    apogee_nmi: int
    perigee_nmi: int
    velocity_max_mph: int
    landing_date_utc: str
    landing_site: str
    landing_site_coord: str
    recovery_ship: str
    duration: Duration
