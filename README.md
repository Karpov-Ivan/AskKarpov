# AskKarpov

AskKarpov - это платформа, где вы можете задавать вопросы и получать на них ответы от других пользователей. Будь то технические проблемы, личные вопросы или просто любопытство, AskKarpov - это место, где вас ждет помощь и знания.

## Как работает AskKarpov?
- Задавайте вопросы: Создайте учетную запись и задайте любой вопрос, который вас интересует.
- Получайте ответы: Другие пользователи с удовольствием помогут вам найти ответы.
- Взаимодействуйте: Голосуйте за лучшие ответы, комментируйте и участвуйте в обсуждениях, формируя активное сообщество.
- Изучайте: Просматривайте вопросы по различным темам, ищите решения для своих задач и делитесь своими знаниями с другими.

## Ключевые особенности:
- Простой интерфейс: AskKarpov имеет интуитивно понятный дизайн, что делает его доступным для всех пользователей.
- Разнообразные темы: Задавайте вопросы на любую тему - от программирования до кулинарии!
- Система рейтинга: Оценка ответов и вопросов позволяет найти самые качественные и полезные ответы.
- Поиск по тегам: Используйте теги, чтобы быстро найти вопросы и ответы по интересующей вас теме.

## Используемые технологии
- Python + Django для написания кода приложения;
- Gunicorn для запуска приложения;
- PostgreSQL для работы с базой данных;
- Nginx для отдачи статических файлов;
- Memcached для кэширования данных;
- Twitter Bootstrap для вёрстки;
- JavaScript/jQuery для взаимодействия интерфейса с пользователем;
- Django.contrib.auth для авторизации и хранения пользователей.

## Основные сущности
- Пользователь: email, никнейм, пароль, аватарка, дата регистрации, рейтинг;
- Вопрос: заголовок, содержание, автор, дата создания, теги, рейтинг;
- Ответ: содержание, автор, дата написания, флаг правильного ответа, рейтинг;
- Тег: слово тега.
