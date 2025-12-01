from pydantic import BaseModel


class TableBase(BaseModel):
    table_number: int
    capacity: int


class TableCreate(TableBase):
    pass


class TableUpdate(TableBase):
    pass


class TableResponse(TableBase):
    id: str

    class Config:
        from_attributes = True
