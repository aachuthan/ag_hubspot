import random
from typing import Dict, Any
from .base import BaseGenerator

class ProductGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        price = random.randint(10, 1000)
        return {
            "name": f"Product {self.fake.bs().title()}",
            "description": self.fake.sentence(),
            "price": str(price),
            "recurringbillingfrequency": random.choice(["monthly", "quarterly", "annually", None]),
        }
