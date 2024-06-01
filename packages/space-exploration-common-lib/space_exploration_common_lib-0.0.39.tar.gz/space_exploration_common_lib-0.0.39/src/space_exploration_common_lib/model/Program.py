from pydantic import BaseModel
from typing import List


class Program(BaseModel):
    program: str
    missions: List[str]
    image_url: str
