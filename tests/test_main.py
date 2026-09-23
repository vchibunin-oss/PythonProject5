import json

import pytest

from main import (BaseProduct, Category, LawnGrass, Product, Smartphone,
                  load_categories_from_json)


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product_1():
    return Product(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
    )


@pytest.fixture
def product_2():
    return Product(
        name="Iphone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=8,
    )


@pytest.fixture
def category_1(product_1, product_2):
    return Category(
        name="Смартфоны",
        description="Телефоны",
        products=[product_1, product_2],
    )


def test_product_attributes(product_1):
    assert product_1.name == "Samsung Galaxy S23 Ultra"
    assert product_1.description == "256GB, Серый цвет, 200MP камера"
    assert product_1.price == 180000.0
    assert product_1.quantity == 5


def test_product_str(product_1):
    assert str(product_1) == ("Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.")


def test_product_add(product_1, product_2):
    assert product_1 + product_2 == 2580000.0


def test_product_add_method(product_1, product_2):
    assert product_1.add(product_2) == 2580000.0


def test_product_add_different_types(product_1):
    smartphone = Smartphone(
        "iPhone",
        "Телефон",
        100000,
        2,
        95.5,
        "15 Pro",
        256,
        "Black",
    )

    with pytest.raises(
        TypeError,
        match="Можно складывать только товары одного класса",
    ):
        product_1 + smartphone


def test_product_add_method_different_types(product_1):
    smartphone = Smartphone(
        "iPhone",
        "Телефон",
        100000,
        2,
        95.5,
        "15 Pro",
        256,
        "Black",
    )

    with pytest.raises(
        TypeError,
        match="Можно складывать только товары одного класса",
    ):
        product_1.add(smartphone)


def test_category_attributes(category_1):
    assert category_1.name == "Смартфоны"
    assert category_1.description == "Телефоны"


def test_category_str(category_1):
    assert str(category_1) == "Смартфоны, количество продуктов: 13 шт."


def test_category_count(category_1):
    assert Category.category_count == 1


def test_product_count(category_1):
    assert Category.product_count == 2


def test_category_add_product(category_1):
    product = Product(
        "Xiaomi",
        "Телефон",
        50000,
        3,
    )

    category_1.add_product(product)

    assert Category.product_count == 3


def test_category_products_property(category_1):
    result = category_1.products

    assert "Samsung Galaxy S23 Ultra" in result
    assert "Iphone 15" in result
    assert "180000.0 руб." in result
    assert "210000.0 руб." in result


def test_load_categories_from_json(tmp_path):
    data = [
        {
            "name": "Смартфоны",
            "description": "Телефоны",
            "products": [
                {
                    "name": "iPhone 15",
                    "description": "512GB",
                    "price": 210000.0,
                    "quantity": 8,
                }
            ],
        }
    ]

    file_path = tmp_path / "products.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

    categories = load_categories_from_json(file_path)

    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"
    assert categories[0].description == "Телефоны"


def test_new_product():
    product_data = {
        "name": "iPhone 15",
        "description": "512GB",
        "price": 210000.0,
        "quantity": 8,
    }

    product = Product.new_product(product_data)

    assert product.name == "iPhone 15"
    assert product.description == "512GB"
    assert product.price == 210000.0
    assert product.quantity == 8


def test_price_setter_valid(product_1):
    product_1.price = 200000.0

    assert product_1.price == 200000.0


def test_price_setter_invalid(product_1, capsys):
    product_1.price = 0

    captured = capsys.readouterr()

    assert "Цена не должна быть нулевой или отрицательная" in captured.out
    assert product_1.price == 180000.0


def test_smartphone_attributes():
    smartphone = Smartphone(
        "iPhone 15 Pro",
        "Новый смартфон",
        150000,
        3,
        98.5,
        "15 Pro",
        256,
        "Black",
    )

    assert smartphone.efficiency == 98.5
    assert smartphone.model == "15 Pro"
    assert smartphone.memory == 256
    assert smartphone.color == "Black"


def test_lawn_grass_attributes():
    grass = LawnGrass(
        "Газонная трава",
        "Для сада",
        1000,
        5,
        "Россия",
        "10 дней",
        "Зеленый",
    )

    assert grass.country == "Россия"
    assert grass.germination_period == "10 дней"
    assert grass.color == "Зеленый"


def test_category_add_invalid_product(category_1):
    with pytest.raises(TypeError, match="Можно добавлять только товары"):
        category_1.add_product("Не товар")


def test_product_inherits_from_base_product():
    assert issubclass(Product, BaseProduct)


def test_product_mixin_print(capsys):
    Product(
        "Тестовый продукт",
        "Описание",
        1000.0,
        5,
    )

    captured = capsys.readouterr()

    assert "Тестовый продукт" in captured.out
    assert "1000.0" in captured.out
    assert "5" in captured.out


def test_smartphone_and_lawn_grass_are_products():
    smartphone = Smartphone(
        "iPhone",
        "Телефон",
        100000,
        2,
        95.5,
        "15 Pro",
        256,
        "Black",
    )

    grass = LawnGrass(
        "Газонная трава",
        "Для сада",
        1000,
        5,
        "Россия",
        "10 дней",
        "Зеленый",
    )

    assert isinstance(smartphone, Product)
    assert isinstance(grass, Product)


def test_product_zero_quantity():
    with pytest.raises(
        ValueError,
        match="Товар с нулевым количеством не может быть добавлен",
    ):
        Product(
            "Тестовый продукт",
            "Описание",
            1000.0,
            0,
        )


def test_category_average_price(category_1):
    assert category_1.average_price() == 195000.0


def test_category_average_price_empty():
    category = Category(
        "Пустая категория",
        "Описание",
        [],
    )

    assert category.average_price() == 0
