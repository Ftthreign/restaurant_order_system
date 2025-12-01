from pydantic import BaseModel


class MenuBase(BaseModel):
    name: str
    price: int


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuResponse(MenuBase):
    id: str

    class Config:
        from_attributes = True
