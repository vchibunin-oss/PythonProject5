import json

import pytest

from main import Category, Product, load_categories_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def product_1():
    return Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )


@pytest.fixture
def product_2():
    return Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
    )


@pytest.fixture
def category_1(product_1, product_2):
    return Category(
        name="Смартфоны",
        description="Телефоны и смартфоны",
        products=[product_1, product_2],
    )


def test_product_attributes(product_1):
    assert product_1.name == "Samsung Galaxy S23 Ultra"
    assert product_1.description == "256GB, Серый цвет, 200MP камера"
    assert product_1.price == 180000.0
    assert product_1.quantity == 5


def test_category_attributes(category_1, product_1, product_2):
    assert category_1.name == "Смартфоны"
    assert category_1.description == "Телефоны и смартфоны"
    assert category_1.products == [product_1, product_2]


def test_category_count(category_1):
    assert Category.category_count == 1


def test_product_count(category_1):
    assert Category.product_count == 2

def test_load_categories_from_json(tmp_path):
    data = [
        {
            "name": "Смартфоны",
            "description": "Телефоны и смартфоны",
            "products": [
                {
                     "name": "Samsung Galaxy S23 Ultra",
                     "description": "256GB, Серый цвет, 200MP камера",
                     "price": 180000.0,
                     "quantity": 5,
                },
                {
                      "name": "Iphone 15",
                      "description": "512GB, Gray space",
                      "price": 210000.0,
                      "quantity": 8,
                },
            ],
        }
    ]

    file_path = tmp_path / "products.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    categories = load_categories_from_json(file_path)

    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"
    assert categories[0].description == "Телефоны и смартфоны"
    assert len(categories[0].products) == 2
    assert categories[0].products[0].name == "Samsung Galaxy S23 Ultra"
    assert categories[0].products[1].name == "Iphone 15"

