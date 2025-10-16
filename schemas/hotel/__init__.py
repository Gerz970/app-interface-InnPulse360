# Hotel schemas package
from .hotel_base import HotelBase
from .hotel_create import HotelCreate
from .hotel_update import HotelUpdate
from .hotel_response import HotelResponse

__all__ = ["HotelBase", "HotelCreate", "HotelUpdate", "HotelResponse"]
