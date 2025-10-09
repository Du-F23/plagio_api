from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class Engines(Enum):
    DUCKDUCKGO = "duckduckgo"
    BRAVE = "brave"

class SearchParamsRequest(BaseModel):
    query: str = Field(alias="q")
    num_results: int = Field(alias="num_results", default=10)
    engines: Optional[List[Engines]] = Field(alias="engines", default=[
        Engines.BRAVE.value,
        Engines.DUCKDUCKGO.value
    ])