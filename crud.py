from tinydb import TinyDB, Query

# Создаем базу данных и таблицу
db = TinyDB('db.json')
table = db.table('users')

# Класс для управления CRUD-операциями для пользователей
class MAIN:
    @staticmethod
    def check_in_db(id):
        User = Query()
        result = table.search(User.id == id)
        return len(result) > 0

    @staticmethod
    def register(id, nick, name, bdate, jdate):
        if not MAIN.check_in_db(id):
            table.insert({'id': id,
                          'nick': nick,
                          "name":name,
                          "bdate": bdate,
                          "jdate": jdate,
                          "warns": 0,
                          "kicks": 0,
                          "karma": 0.5,
                          "rate": 1,
                        })

    @staticmethod
    def get_user_data(id):
        User = Query()
        return table.search(User.id == id)

    @staticmethod
    def update_user(id, new_data):
        User = Query()
        table.update(new_data, User.id == id)

    @staticmethod
    def update_verify(id, value):
        User = Query()
        table.update(value, User.id == id)

    @staticmethod
    def delete_user(id):
        User = Query()
        if MAIN.check_in_db(id):
            table.remove(User.username == id)

    @staticmethod
    def get_all_users_data():
        return table.all()
