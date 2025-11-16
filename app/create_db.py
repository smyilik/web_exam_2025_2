import sqlite3 as db
from werkzeug.security import generate_password_hash
import os

if os.path.exists('database.db'):
    os.remove('database.db')

conn = db.connect('database.db')

create_user_table_query = (''' CREATE TABLE IF NOT EXISTS User (
    login VARCHAR(50) PRIMARY KEY NOT NULL,
    password VARCHAR(255) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100)
    );''')

create_user_role_table_query = (''' CREATE TABLE IF NOT EXISTS User_role (
    user_login VARCHAR(50) PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_login) REFERENCES User(login)
    );''')

create_animal_table_query = (''' CREATE TABLE IF NOT EXISTS Animal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    age INTEGER NOT NULL,
    breed VARCHAR(100) NOT NULL,
    sex VARCHAR(10) NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL
    );''')

create_animal_image_table_query = (''' CREATE TABLE IF NOT EXISTS Animal_image (
    file_name VARCHAR(255) PRIMARY KEY NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    animal_id INTEGER NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES Animal(id)
    );''')

create_user_has_animal_table_query = (''' CREATE TABLE IF NOT EXISTS User_has_Animal (
    animal_id INTEGER NOT NULL,
    user_login VARCHAR(50) NOT NULL,
    date DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    PRIMARY KEY (animal_id, user_login),
    FOREIGN KEY (animal_id) REFERENCES Animal(id),
    FOREIGN KEY (user_login) REFERENCES User(login)
    );''')

conn.execute(create_user_table_query)
conn.execute(create_user_role_table_query)
conn.execute(create_animal_table_query)
conn.execute(create_animal_image_table_query)
conn.execute(create_user_has_animal_table_query)

conn.execute("PRAGMA foreign_keys = ON")

hash = generate_password_hash('123')
conn.execute(f"INSERT INTO User (login, password, last_name, first_name, father_name) VALUES\
    ('admin', '{ hash }', 'admin', 'admin', 'admin'),\
    ('moderator', '{ hash }', 'moderator', 'moderator', 'moderator'),\
    ('ivanov', '{ hash }', 'Иванов', 'Иван', 'Иванович'),\
    ('smirnova', '{ hash }', 'Смирнова', 'Анна', 'Владимировна'),\
    ('kuznetsov', '{ hash }', 'Кузнецов', 'Алексей', 'Сергеевич'),\
    ('popova', '{ hash }', 'Попова', 'Екатерина', 'Дмитриевна'),\
    ('sokolov', '{ hash }', 'Соколов', 'Дмитрий', 'Александрович'),\
    ('lebedeva', '{ hash }', 'Лебедева', 'Ольга', 'Петровна'),\
    ('kozlov', '{ hash }', 'Козлов', 'Сергей', 'Васильевич'),\
    ('volkova', '{ hash }', 'Волкова', 'Наталья', 'Алексеевна');")

conn.execute("INSERT INTO User_role (user_login, name) VALUES\
    ('admin', 'admin'),\
    ('moderator', 'moderator'),\
    ('ivanov', 'user'),\
    ('smirnova', 'user'),\
    ('kuznetsov', 'user'),\
    ('popova', 'user'),\
    ('sokolov', 'user'),\
    ('lebedeva', 'user'),\
    ('kozlov', 'user'),\
    ('volkova', 'user');")

conn.execute("INSERT INTO Animal (name, description, age, breed, sex, request_count, status) VALUES\
    ('Барсик', 'Дружелюбный и преданный золотистый ретривер с золотистой шерстью. Очень умный, хорошо поддается дрессировке, обожает плавать и приносить мячик. Идеальный компаньон для активной семьи.', 24, 'Золотистый ретривер', 'Мужской', 0, 'transitioning'),\
    ('Мурка', 'Очаровательная французская бульдожка с большими ушами-локаторами. Очень ласковая, любит внимание и комфорт. Прекрасно подходит для жизни в квартире, обладает веселым нравом.', 12, 'Французский Бульдог', 'Женский', 0, 'available'),\
    ('Шарик', 'Энергичный и добродушный лабрадор с шоколадной шерстью. Обладает отличным аппетитом и безграничной любовью к людям. Прошел базовую дрессировку, знает основные команды.', 36, 'Лабрадор', 'Мужской', 1, 'reserved'),\
    ('Рекс', 'Великолепная немецкая овчарка с классическим окрасом. Умная, преданная, с развитым охранным инстинктом. Нуждается в активном хозяине и регулярных физических нагрузках.', 48, 'Немецкая Овчарка', 'Мужской', 0, 'available'),\
    ('Люси', 'Милый щенок-дворняжка с веселым характером и преданным взглядом. Очень сообразительная, быстро учится, обожает игры и прогулки. Идеальный выбор для первой собаки в семье.', 6, 'Дворняжка', 'Женский', 0, 'available'),\
    ('Васька', 'Красивая сибирская хаски с голубыми глазами и густой шерстью. Очень активная и дружелюбная, нуждается в длительных прогулках и физической активности. Обожает снег и зимние забавы.', 18, 'Сибирская Хаски', 'Мужской', 0, 'available'),\
    ('Зевс', 'Статный ротвейлер с мощным телосложением и уверенным характером. Преданный защитник, нуждается в опытном хозяине и последовательной дрессировке. Отлично подходит для охраны.', 24, 'Ротвейлер', 'Мужской', 1, 'transitioning'),\
    ('Снежок', 'Изящная салюки с белоснежной шерстью и аристократичной внешностью. Спокойная и грациозная, обладает развитым охотничьим инстинктом. Нуждается в безопасном выгуле на поводке.', 36, 'Салюки', 'Мужской', 0, 'available'),\
    ('Герда', 'Жизнерадостная такса с длинным телом и короткими лапками. Очень любопытная и смелая, обожает исследовать новые места. Преданный компаньон с большим сердцем.', 24, 'Такса', 'Женский', 0, 'available'),\
    ('Боня', 'Энергичный джек-рассел-терьер с ярким характером. Неутомимый игрок, обожает мячики и активные игры. Очень умный, но нуждается в последовательном воспитании.', 12, 'Джек-рассел-терьер', 'Мужской', 0, 'available'),\
    ('Лиза', 'Очаровательная корги с короткими лапками и веселым нравом. Очень общительная и умная, хорошо поддается дрессировке. Обладает забавной походкой и дружелюбным характером.', 24, 'Корги', 'Женский', 0, 'available');")

conn.execute("INSERT INTO Animal_image (file_name, file_type, animal_id) VALUES\
    ('1_1.jpg', 'jpeg', 1),\
    ('2_1.jpg', 'jpeg', 2),\
    ('3_1.jpg', 'jpeg', 3),\
    ('4_1.jpg', 'jpeg', 4),\
    ('5_1.jpg', 'jpeg', 5),\
    ('6_1.jpg', 'jpeg', 6),\
    ('7_1.jpg', 'jpeg', 7),\
    ('8_1.jpg', 'jpeg', 8),\
    ('9_1.jpg', 'jpeg', 9),\
    ('10_1.jpg', 'jpeg', 10),\
    ('11_1.jpg', 'jpeg', 11);")

conn.execute("INSERT INTO User_has_Animal (animal_id, user_login, date, status, contact) VALUES\
    (1, 'ivanov', '2024-01-16 10:30:00', 'pending', 'ivanov@email.com, +7-111-222-3333'),\
    (1, 'smirnova', '2024-01-15 14:20:00', 'approved', 'smirnova@email.com, +7-222-333-4444'),\
    (5, 'popova', '2024-01-14 16:45:00', 'rejected', 'popova@email.com, +7-444-555-6666'),\
    (6, 'sokolov', '2024-01-18 11:00:00', 'pending', 'sokolov@email.com, +7-555-666-7777'),\
    (7, 'lebedeva', '2024-01-13 13:25:00', 'approved', 'lebedeva@email.com, +7-666-777-8888'),\
    (9, 'kozlov', '2024-01-19 15:30:00', 'pending', 'kozlov@email.com, +7-777-888-9999'),\
    (1, 'volkova', '2024-01-21 17:20:00', 'pending', 'volkova@email.com, +7-000-111-2222'),\
    (7, 'smirnova', '2024-01-23 14:30:00', 'pending', 'smirnova@email.com, +7-222-333-4444');")

conn.commit()

conn.close()
