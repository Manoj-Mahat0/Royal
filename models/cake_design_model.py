#cake_design_model
from pydantic import BaseModel
from typing import List

class CakeDesignMetadata(BaseModel):
    name: str
    description: str = ""
    tags: List[str] = []
