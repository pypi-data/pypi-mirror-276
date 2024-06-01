from pydantic import BaseModel
from typing import List


class Program(BaseModel):
    program: str
    image_url: str
