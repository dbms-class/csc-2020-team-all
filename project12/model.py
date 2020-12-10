from dataclasses import dataclass

from peewee import *


@dataclass
class DrugMove:
    from_pharmacy_id: int
    to_pharmacy_id: int
    price_difference: int
    count: int