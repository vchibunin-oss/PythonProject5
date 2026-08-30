import json


class Product:
    """Класс, описывающий товар."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


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
        description=category_data["description"],
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
