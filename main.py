import json
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для продуктов."""

    @abstractmethod
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity


class PrintMixin:
    """Миксин для вывода информации о создании объекта."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(
            f"Создан объект класса {self.__class__.__name__} "
            f"с параметрами: {args}, {kwargs}"
        )


class Product(PrintMixin, BaseProduct):
    """Класс, описывающий товар."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ):
        super().__init__(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
        )

    @classmethod
    def new_product(cls, product_data):
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного класса")
        return self.price * self.quantity + other.price * other.quantity

    def add(self, other):
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного класса")
        return self.price * self.quantity + other.price * other.quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value > 0:
            self._price = value
        else:
            print("Цена не должна быть нулевой или отрицательная")

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, "
            f"{self.description!r}, "
            f"{self.price!r}, "
            f"{self.quantity!r})"
        )


class Smartphone(Product):
    """Класс смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[Product],
    ):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только товары")
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self):
        return "".join(
            f"{product.name}, {product.price} руб. "
            f"Остаток: {product.quantity} шт.\n"
            for product in self.__products
        )


def load_categories_from_json(file_path: str) -> list[Category]:
    """Читает JSON-файл и создаёт объекты Category и Product."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    for category_data in data:
        products = [
            Product.new_product(product_data)
            for product_data in category_data["products"]
        ]

        category = Category(
            category_data["name"],
            category_data["description"],
            products,
        )

        categories.append(category)

    return categories


if __name__ == "__main__":
    categories = load_categories_from_json("products.json")

    for cat in categories:
        print(cat.name)

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
