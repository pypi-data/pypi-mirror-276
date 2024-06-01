from pydantic import BaseModel

class Experiment(BaseModel):
    name: str
    description: str
    metadata: dict
    metrics: dict

    class Config:
        orm_mode = True
