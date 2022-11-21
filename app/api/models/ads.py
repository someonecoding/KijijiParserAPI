from pydantic import BaseModel
from typing import Optional


class AdDetails(BaseModel):
    hydro: Optional[bool] = None
    heat: Optional[bool] = None
    water: Optional[bool] = None
    internet: Optional[bool] = None
    cable: Optional[bool] = None
    parking: Optional[str] = None
    agreement: Optional[str] = None
    pets: Optional[bool] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    furnished: Optional[bool] = None
    laundry_iu: Optional[bool] = None
    laundry_ib: Optional[bool] = None
    dishwasher: Optional[bool] = None
    fridge: Optional[bool] = None
    conditioning: Optional[bool] = None
    yard: Optional[bool] = None
    balcony: Optional[bool] = None
    smoking: Optional[bool] = None

