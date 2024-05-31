# mass_mailing_service

Сервис управления рассылками, администрирования и получения статистики "1001 mails"

Цель проекта заключается в создании сервиса по автоматической рассылке, согласно заданного расписания.

Установка и использование

- Для работы программы необходимо установить зависимости, указанные в файле pyproject.toml
- Заполнить файл .env своими данными (на примере файла .env.sample)
- Запустить команду python manage.py csu для создания Суперпользователя
- Запустить команду python manage.py ccmg для создания группы "Контент-менеджер"


Описание приложений

- mailing отвечает за создание и управление рассылками
- client отвечает за создание и управление клиентами рассылок
- message отвечает за создание и управление сообщениями рассылки
- users отвечает за регистрацию, верификацию и механизмы авторизации пользователей сайта
- blog содержит статьи

Дополнительная информация
scheduler содержит функцию, которая вызывается для запуска планировщика задач
Основным приложением является mailing.

На сайте реализован механизм кэширования:
- полный кэш страниц блога
- кэширование списка статей, выводимых случайным образом на индексной странице