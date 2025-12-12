from faker import Faker
from typing import List, Dict, Any
from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    def __init__(self, locale: str = 'en_US'):
        self.fake = Faker(locale)
    
    @abstractmethod
    def generate_one(self) -> Dict[str, Any]:
        """Generate a single record dictionary."""
        pass

    def generate(self, count: int) -> List[Dict[str, Any]]:
        """Generate a list of records."""
        return [self.generate_one() for _ in range(count)]
