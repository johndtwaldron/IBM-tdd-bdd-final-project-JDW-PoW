# tests/factories.py
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal

from service.models import Product, Category


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""
        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(
        choices=[
            "Hat",
            "Pants",
            "Shirt",
            "Apple",
            "Banana",
            "Pots",
            "Towels",
            "Ford",
            "Chevy",
            "Hammer",
            "Wrench",
        ]
    )
    description = factory.Faker("text")
    price = FuzzyDecimal(0.5, 2000.0, 2)          # returns Decimal with 2 dp
    available = FuzzyChoice(choices=[True, False])
    category = FuzzyChoice(
        choices=[
            Category.UNKNOWN,
            Category.CLOTHS,       # note: lab uses "CLOTHS" (not "CLOTHES")
            Category.FOOD,
            Category.HOUSEWARES,
            Category.AUTOMOTIVE,
            Category.TOOLS,
        ]
    )
