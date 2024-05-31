from pydantic import BaseModel
from typing import List
from .Program import Program


class Astronaut(BaseModel):
    astronaut_first_name: str
    astronaut_last_name: str
    programs: List[Program]
    image_url: str
