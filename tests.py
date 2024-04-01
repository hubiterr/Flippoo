import getpass

def get_password():
    user = getpass.getuser()
    password = getpass.getpass("Введите пароль: ")
    return password, user

if __name__ == "__main__":
    password, user = get_password()
    print(f"Вы ввели пароль: {password}")
    print(f"{user}")
    
