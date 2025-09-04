# tests/test_models.py
from decimal import Decimal
import unittest

from service.models import Product, DataValidationError, db
from tests.factories import ProductFactory


class TestProductModelExtended(unittest.TestCase):
    """Extra model tests to cover CRUD + queries"""

    def setUp(self):
        # keep tests isolated
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        product.description = "testing"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "testing")
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "testing")

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        for _ in range(5):
            p = ProductFactory()
            p.create()
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(5)
        for p in products:
            p.create()
        name = products[0].name
        count = len([p for p in products if p.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for p in found:
            self.assertEqual(p.name, name)

    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = ProductFactory.create_batch(10)
        for p in products:
            p.create()
        available = products[0].available
        count = len([p for p in products if p.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for p in found:
            self.assertEqual(p.available, available)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = ProductFactory.create_batch(10)
        for p in products:
            p.create()
        category = products[0].category
        count = len([p for p in products if p.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for p in found:
            self.assertEqual(p.category, category)

    # Helpful extras for coverage (keep if you like)
    def test_update_without_id_raises(self):
        p = ProductFactory()
        p.id = None  # force the "no id" path
        with self.assertRaises(DataValidationError):
            p.update()

    def test_find_by_price_accepts_string(self):
        p = ProductFactory(price=Decimal("9.99"))
        p.create()
        results = list(Product.find_by_price("9.99"))
        self.assertTrue(any(r.id == p.id for r in results))

    # Helpful extras for coverage num 2

    def test_deserialize_missing_key(self):
        """It should raise on deserialize with missing 'name'"""
        p = Product()
        bad = {"description": "x", "price": "1.23", "available": True, "category": "FOOD"}
        with self.assertRaises(DataValidationError):
            p.deserialize(bad)

    def test_deserialize_bad_available_type(self):
        """It should raise on deserialize when 'available' is not bool"""
        p = Product()
        bad = {"name": "X", "description": "x", "price": "1.23", "available": "yes", "category": "FOOD"}
        with self.assertRaises(DataValidationError):
            p.deserialize(bad)

    def test_deserialize_bad_category(self):
        """It should raise on deserialize when category name is invalid"""
        p = Product()
        bad = {"name": "X", "description": "x", "price": "1.23", "available": True, "category": "BOGUS"}
        with self.assertRaises(DataValidationError):
            p.deserialize(bad)

    def test_deserialize_bad_type(self):
        """It should raise on deserialize when body is not a dict"""
        p = Product()
        with self.assertRaises(DataValidationError):
            p.deserialize("not a dict")
