import json


class Product:
    """Класс, описывающий товар."""

    def __init__(
            self,
            name: __str__,
            description: __str__,
            price: float,
            quantity: int,
    ):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data):
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __add__(self, other):
        return self.price * self.quantity + other.price * other.quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value > 0:
            self.__price = value
        else:
            print("Цена не должна быть нулевой или отрицательная")

    def __str__(self):
         return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product):
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self):
        return "".join(
            f"{product.name}, {product.price} руб. Остаток: "
            f"{product.quantity} шт.\n"
            for product in self.__products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


def load_categories_from_json(file_path: str) -> list[Category]:
    """Читает JSON-файл и создаёт объекты Category и Product."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    categories = []

    for category_data in data:
        products = [
            Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            for product_data in category_data["products"]
        ]

        category = Category(
            name=category_data["name"],
            description=category_data[
                "description"
            ],
            products=products,
        )

        categories.append(category)

    return categories


if __name__ == "__main__":
    categories = load_categories_from_json("products.json")
    for cat in categories:
        print(f"{cat.name}: {len(cat.products)} товаров")

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
