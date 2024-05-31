from pydantic import BaseModel
from typing import List


class Astronaut(BaseModel):
    astronaut_first_name: str
    astronaut_last_name: str
    image_url: str
    missions: List[str]
