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

def test_product_str(product_1: Product):
    assert str(product_1) == (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
    )
def test_product_add(product_1: Product, product_2: Product):
        assert product_1 + product_2 == 2580000.0

def test_category_attributes(category_1, product_1, product_2):
    assert category_1.name == "Смартфоны"
    assert category_1.description == "Телефоны и смартфоны"
    assert category_1.products == (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
    )

def test_category_str(category_1: Category):
    assert str(category_1) == "Смартфоны, количество продуктов: 13 шт."

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
    assert "Samsung Galaxy S23 Ultra" in categories[0].products
    assert "Iphone 15" in categories[0].products


def test_product_new_product():
    product_data = {
        "name": "Test Product",
        "description": "Test description",
        "price": 1000.0,
        "quantity": 10,
    }

    product = Product.new_product(product_data)

    assert isinstance(product, Product)
    assert product.name == "Test Product"
    assert product.description == "Test description"
    assert product.price == 1000.0
    assert product.quantity == 10


def test_product_price_setter(product_1: Product):
    product_1.price = 200000.0

    assert product_1.price == 200000.0


def test_product_price_setter_invalid(product_1: Product, capsys):
    product_1.price = 0

    captured = capsys.readouterr()

    assert product_1.price == 180000.0
    assert captured.out.strip() == (
        "Цена не должна быть нулевой "
        "или отрицательная"
    )


def test_category_add_product(category_1: Category, product_1: Product):
    category_1.add_product(product_1)

    assert "Samsung Galaxy S23 Ultra" in category_1.products
    assert Category.product_count == 3


def test_category_products_getter(category_1):
    expected = (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
    )
    assert category_1.products == expected
