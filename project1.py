from ean13 import decode_ean_13



class Load:
    """Класс загрузки данных"""
    data = []

    @classmethod
    def load_items(cls, file_name):
        """Метод для загрузки данных о товарах магазина из файла"""
        with open(file_name, 'r') as file:
            count = len(file.readlines())
        with open(file_name, 'r') as file:
            for _ in range(count):
                line = file.readline()
                line = line.replace('\n', '')
                item = Item(int(line))
                Load.data.append(item)


class Item:
    """Класс товара интернет магазина"""

    def __init__(self, ean_13):
        if isinstance(ean_13, int) and len(str(ean_13)) == 13:
            self.__ean_13 = ean_13
            self.__country = Item.decode_ean_13(str(self.__ean_13)[:3], 'country')
            self.__producer = Item.decode_ean_13(str(self.__ean_13)[3:9],
                                                 'producer')
            self.__item_name = Item.decode_ean_13(str(self.__ean_13)[9:12],
                                                  'item_name')[0]
            self.__price = Item.decode_ean_13(str(self.__ean_13)[9:12],
                                              'item_name')[1]
        else:
            self.__ean_13 = None
            self.__country = None
            self.__producer = None
            self.__item_name = None
            self.__price = None

    price = property()
    country = property()
    ean_13 = property()
    producer = property()
    item_name = property()

    @country.setter
    def country(self, country):
        pass

    @ean_13.setter
    def ean_13(self, new_ean_13):
        pass

    @producer.setter
    def producer(self, new_producer):
        pass

    @item_name.setter
    def item_name(self, new_item_name):
        pass

    @price.setter
    def price(self, new_price):
        pass

    @country.getter
    def country(self):
        return self.__country

    @ean_13.getter
    def ean_13(self):
        return self.__ean_13

    @producer.getter
    def producer(self):
        return self.__producer

    @item_name.getter
    def item_name(self):
        return self.__item_name

    @price.getter
    def price(self):
        return self.__price

    @staticmethod
    def decode_ean_13(number, type):
        if number in decode_ean_13[type]:
            return decode_ean_13[type][number]
        else:
            return None

    def __str__(self):
        """Метод cтрокового представления"""
        if self.__ean_13:
            return '\nEAN-13: {}\nТовар: {}\nБренд: {}\nСтр' \
                   'ана производства: {}\nЦена: {}\n' \
                .format(self.__ean_13,
                        self.__item_name,
                        self.__producer,
                        self.__country,
                        self.__price)
        else:
            return str(None)

    def __repr__(self):
        """Метод представления"""
        return self.__str__()


class Basket:
    """Класс корзины интернет магазина"""

    def __init__(self):
        self.__items = []
        self.__count_of_items = len(self.__items)
        self.__total_cost = self.__calc_cost(self.__items)

    def __str__(self):
        """Метод cтрокового представления"""
        basket = '+' + '-' * 100 + '+\n' \
                 + '|{:^13}|{:42}|{:16}|{:^15}|{:^10}|\n'.format(
            'EAN-13', 'НАЗВАНИЕ ТОВАРА', 'ПРОИЗВОДИТЕЛЬ', 'СТРАНА', 'ЦЕНА')
        basket += '+' + '-' * 100 + '+\n'
        if self.__items:
            for item in self.__items:
                basket += '|{:^13}|{:42}|{:16}|{:^15}|{:^10}|\n'.format(
                    item.ean_13, item.item_name, item.producer, item.country,
                    item.price)
            basket += '+' + '-' * 100 + '+\n'
        return basket

    def __repr__(self):
        """Метод представления"""
        return self.__str__()

    def __add_item(self, ean13):
        for item in Load.data:
            if item.ean_13 == ean13:
                self.__items.append(item)
                print('ДОБАВЛЕН НОВЫЙ ТОВАР')
                print(item)
                break

    def __del_item(self, ean13):
        for item in self.__items:
            if item.ean_13 == ean13:
                self.__items.remove(item)
                print('УДАЛЕН ТОВАР')
                print(item)
                break

    def __load_in_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write(str(self))

    def __load_from_file(self, file_name):
        with open(file_name, 'r') as file:
            count = len(file.readlines())
        with open(file_name, 'r') as file:
            items = []
            for _ in range(3):
                file.readline()
            for _ in range(count - 4):
                line = file.readline()
                line = line.replace('\n', '')
                info = line.split('|')
                for data in info:
                    if data == ' ' or data == '':
                        info.remove(data)
                item = Item(int(info[0].strip()))

                items.append(item)
            self.__items += items


    @staticmethod
    def __calc_cost(items):
        cost = 0
        for item in items:
            if item.price:
                price = int(item.price.replace('руб.', ''))
                cost += price
        return cost

    @staticmethod
    def print_menu():
        print('+' + '-' * 100 + '+')
        print('|{:<100}|'.format('ГЛАВНОЕ МЕНЮ'))
        print('+' + '-' * 100 + '+')
        print('|{:<100}|'.format('1. Загрузить данные о товарах в моей корзине из файла.'))
        print('|{:<100}|'.format('2. Выгрузить данные о товарах в моей корзине в файл.'))
        print('|{:<100}|'.format('3. Добавить товар в корзину.'))
        print('|{:<100}|'.format('4. Удалить товар из корзины.'))
        print('|{:<100}|'.format('5. Показать товары в корзине.'))
        print('|{:<100}|'.format('6. Завершить рaботу.'))
        print('+' + '-' * 100 + '+')
        num = input('Введите номер операции: ')
        return num

    def menu(self):
        while True:
            action = Basket.print_menu()
            if action == '1':
                self.__load_from_file('basket.txt')
                print('ДАННЫЕ ЗАГРУЖЕНЫ')
                print(self)
            elif action == '2':
                self.__load_in_file('basket.txt')
                print('ДАННЫЕ ВЫГРУЖЕНЫ В ФАЙЛ')
            elif action == '3':
                print('+' + '-' * 100 + '+')
                print('|{:<100}|'.format('ТОВАРЫ В НАЛИЧИИ'))
                print('+' + '-' * 100 + '+')
                for item in Load.data:
                    print(item)
                print('+' + '-' * 100 + '+')
                ean13 = input('Введите код EAN-13 товара, который будет добавлен: ')
                self.__add_item(int(ean13))
                print(self)
                while True:
                    print('+' + '-' * 100 + '+')
                    print('|{:<100}|'.format('Загрузить изменения в файл?'))
                    print('|{:<100}|'.format('1. Да'))
                    print('|{:<100}|'.format('2. Нет'))
                    print('+' + '-' * 100 + '+')
                    choice = input('Введите номер ответа: ')
                    if choice == '1':
                        self.__load_in_file('basket.txt')
                        break
                    elif choice == '2':
                        break
                    else:
                        print('Данные введены некорректно, попробуйте ещё раз.')
            elif action == '4':
                print('+' + '-' * 100 + '+')
                print('|{:<100}|'.format('СОДЕРЖИМОЕ ВАШЕЙ КОРЗИНЫ'))
                print('+' + '-' * 100 + '+')
                if self.__items:
                    print(self)
                    print('+' + '-' * 100 + '+')
                    ean13 = input('Введите код EAN-13 товара, который будет удален: ')
                    self.__del_item(int(ean13))
                    print(self)
                    print('+' + '-' * 100 + '+')
                    while True:
                        print('+' + '-' * 100 + '+')
                        print('|{:<100}|'.format('Загрузить изменения в файл?'))
                        print('|{:<100}|'.format('1. Да'))
                        print('|{:<100}|'.format('2. Нет'))
                        print('+' + '-' * 100 + '+')
                        choice = input('Введите номер ответа: ')
                        if choice == '1':
                            self.__load_in_file('basket.txt')
                            break
                        elif choice == '2':
                            break
                        else:
                            print('Данные введены некорректно, попробуйте ещё раз.')
                else:
                    print(self)
                    print('ВАША КОРЗИНА ПУСТА')
            elif action == '5':
                print(self)
                if not self.__items:
                    print('ВАША КОРЗИНА ПУСТА')
            elif action == '6':
                break
            else:
                print('Данные введены некорректно, попробуйте ещё раз.')


