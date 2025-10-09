from pydantic import BaseModel, Field


class CommonResultSearchEngine(BaseModel):
    title: str = Field(alias="title")
    url: str = Field(alias="url")
    description: str = Field(alias="description")

class CommonResultsEngine(BaseModel):
    result: CommonResultSearchEngine = Field(alias="result")
    similarity_score: float = Field(alias="similarity_score")