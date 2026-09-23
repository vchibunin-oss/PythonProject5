# PythonProject5

## Домашнее задание: классы Product и Category

### Функционал

Класс `Product` — товар с атрибутами:
- `name`
- `description`
- `price`
- `quantity`

Класс `Category` — категория с атрибутами:
- `name`
- `description`
- `products`

У класса `Category` есть атрибуты класса `category_count` и `product_count`.

Функция `load_categories_from_json(file_path)` читает JSON-файл
`products.json` и создаёт объекты `Category` и `Product`.

### Домашнее задание 16.2 — множественное наследование

В проект добавлен абстрактный базовый класс `BaseProduct`,
который является родительским классом для `Product`.

Классы `Smartphone` и `LawnGrass` наследуются от `Product`.

Также реализован класс-миксин `PrintMixin`.
Он выводит в консоль информацию о создании объекта и его параметрах.

`Product` использует множественное наследование:

```python
class Product(PrintMixin, BaseProduct):