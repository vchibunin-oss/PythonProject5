Домашнее задание: классы Product и Category
Функционал
Класс Product — товар с атрибутами: name, description, price, quantity.
Класс Category — категория с атрибутами: name, description, products (список объектов Product).
У класса Category есть атрибуты класса category_count и product_count, которые автоматически увеличиваются при создании каждого нового объекта Category.
Функция load_categories_from_json(file_path) читает JSON-файл (products.json) и создаёт из него объекты Category и Product.
Запуск
poetry install
poetry run python main.pyТесты
poetry run pytest --cov=main --cov-report=term-missing
Проект выполнен в рамках домашнего задания.