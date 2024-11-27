import time
import hashlib

class User:

    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = password
        self.age = age

    # Дополнительные методы...
    def __str__(self):
        return f'{self.nickname}'

    def __hash__(self):
        return hash(self.password)

    def __int__(self):
        return f'{self.age}'

class Video:

    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    # Дополнительные методы...
    def __str__(self):
        return f'{self.title}'

    def __eq__(self, other):
        return self.title == other.title

    def __contains__(self, item):
        return item in self.title

class UrTube:

    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def __str__(self):
        return f"UrTube: {', '.join(user.nickname for user in self.users)}"

    def __eq__(self, other):
        # Сравнение двух объектов UrTube по содержимому
        if isinstance(other, UrTube):
            return self.users == other.users and self.videos == other.videos
        else:
            return False

    def add_user(self, user):
        self.users.append(user)

    def add_video(self, video):
        self.videos.append(video)

    def set_current_user(self, user):
        self.current_user = user

    # Дополнительные методы...
    # Метод для входа пользователя
    def log_in(self, nickname, password):
        # Поиск пользователя по никнейму
        for user in self.users:
            if user.nickname == nickname:
                # Проверка пароля путем сравнения хэшей
                if hash(password) == user.password:
                    # Установка текущего пользователя
                    self.set_current_user(user)
                    return True
        return False

    # Регистрация пользователя
    def register(self, nickname, password, age):
        if not any(user.nickname == nickname for user in self.users):
            user = User(nickname, hash(password), age)
            self.add_user(user)
            self.log_in(nickname, password)  # Автоматический вход после регистрации
        else:
            print("Пользователь {} уже существует".format(nickname))

    # Выход из системы
    def log_out(self):
        self.set_current_user(None)

    # Добавление видео
    def add(self, *videos):
        for video in videos:
            self.add_video(video)

    # Поиск видео по поисковому слову
    def get_videos(self, search_word):
        search_word = search_word.lower()  # Приводим поисковое слово к нижнему регистру
        result = []  # Создаем пустой список для хранения результатов
        for video in self.videos:
            title = video.title.lower()  # Приводим название видео к нижнему регистру
            if search_word in title:  # Проверяем, содержит ли название видео поисковое слово
                result.append(video.title)  # Добавляем название видео в список результатов
        return result  # Возвращаем список результатов

    def __contains__(self, item):
        # Переопределяем оператор 'in' для проверки наличия элемента в списке videos
        return item in self.videos

    # Просмотр видео
    def watch_video(self, title):
        if self.current_user is None:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return
        elif not self.is_adult_allowed(title):
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
        else:
            for video in self.videos:
                if video.title == title or video.title.startswith(
                        title):  # Ищем точное совпадение или начало строки
                    video.time_now = 0  # Сброс времени просмотра
                    print(f"Начало видео: {title}")
                    while True:
                        print(video.duration - video.time_now)
                        time.sleep(1)
                        video.time_now += 1
                        if video.time_now >= video.duration:
                            break
                    print("Конец видео!")
                    break  # После первого найденного видео прекращаем поиск

    # Проверка на возрастное ограничение
    def is_adult_allowed(self,title):
        for video in self.videos:
            if video.adult_mode and self.current_user.age < 18:
                return False  # Если видео имеет возрастные ограничения и найдено, то просмотр запрещён
        return True  # По умолчанию просмотр разрешён

ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')