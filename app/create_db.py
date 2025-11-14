import sqlite3 as db
from werkzeug.security import generate_password_hash

conn = db.connect('database.db')

create_user_role_table_query = (''' CREATE TABLE User_role (
    name VARCHAR(50) PRIMARY KEY NOT NULL,
    description TEXT NOT NULL);
    ''')

create_user_table_query = (''' CREATE TABLE User (
    login VARCHAR(50) PRIMARY KEY NOT NULL,
    password VARCHAR(255) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    role VARCHAR(50) NOT NULL,
    FOREIGN KEY (role) REFERENCES User_role(name)
    );''')

create_animal_table_query = (''' CREATE TABLE Animal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    age INTEGER NOT NULL,
    breed VARCHAR(100) NOT NULL,
    sex VARCHAR(10) NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL
    );''')

create_animal_image_table_query = (''' CREATE TABLE Animal_image (
    file_name VARCHAR(255) PRIMARY KEY NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    animal_id INTEGER NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES Animal(id)
    );''')

create_user_has_animal_table_query = (''' CREATE TABLE User_has_Animal (
    animal_id INTEGER NOT NULL,
    user_login VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    PRIMARY KEY (animal_id, user_login),
    FOREIGN KEY (animal_id) REFERENCES Animal(id),
    FOREIGN KEY (user_login) REFERENCES User(login)
    );''')

conn.execute(create_user_role_table_query)
conn.execute(create_user_table_query)
conn.execute(create_animal_table_query)
conn.execute(create_animal_image_table_query)
conn.execute(create_user_has_animal_table_query)

conn.execute("PRAGMA foreign_keys = ON")

conn.execute("INSERT INTO User_role (name, description) VALUES\
    ('admin', 'Администратор системы с полными правами доступа'),\
    ('user', 'Обычный пользователь, может подавать заявки на животных'),\
    ('moderator', 'Модератор, может управлять животными и заявками');")

admin_hash = generate_password_hash('123')
petrov_hash = generate_password_hash('12')
sidorova_hash = generate_password_hash('1')

conn.execute(f"INSERT INTO User (login, password, last_name, first_name, father_name, role) VALUES\
    ('admin', '{ admin_hash }', 'Иванов', 'Иван', 'Иванович', 'admin'),\
    ('petrov', '{ petrov_hash }', 'Петров', 'Петр', 'Петрович', 'user'),\
    ('sidorova', '{ sidorova_hash }', 'Сидорова', 'Мария', 'Сергеевна', 'user');")
             
conn.execute("INSERT INTO Animal (name, description, age, breed, sex, request_count, status) VALUES\
    ('Барсик', 'Дружелюбный и преданный золотистый ретривер с золотистой шерстью. Очень умный, хорошо поддается дрессировке, обожает плавать и приносить мячик. Идеальный компаньон для активной семьи.', 24, 'Золотистый ретривер', 'Мужской', 0, 'available'),\
    ('Мурка', 'Очаровательная французская бульдожка с большими ушами-локаторами. Очень ласковая, любит внимание и комфорт. Прекрасно подходит для жизни в квартире, обладает веселым нравом.', 12, 'Французский Бульдог', 'Женский', 0, 'available'),\
    ('Шарик', 'Энергичный и добродушный лабрадор с шоколадной шерстью. Обладает отличным аппетитом и безграничной любовью к людям. Прошел базовую дрессировку, знает основные команды.', 36, 'Лабрадор', 'Мужской', 1, 'reserved'),\
    ('Рекс', 'Великолепная немецкая овчарка с классическим окрасом. Умная, преданная, с развитым охранным инстинктом. Нуждается в активном хозяине и регулярных физических нагрузках.', 48, 'Немецкая Овчарка', 'Мужской', 0, 'available'),\
    ('Люси', 'Милый щенок-дворняжка с веселым характером и преданным взглядом. Очень сообразительная, быстро учится, обожает игры и прогулки. Идеальный выбор для первой собаки в семье.', 6, 'Дворняжка', 'Женский', 0, 'available'),\
    ('Васька', 'Красивая сибирская хаски с голубыми глазами и густой шерстью. Очень активная и дружелюбная, нуждается в длительных прогулках и физической активности. Обожает снег и зимние забавы.', 18, 'Сибирская Хаски', 'Мужской', 0, 'available'),\
    ('Зевс', 'Статный ротвейлер с мощным телосложением и уверенным характером. Преданный защитник, нуждается в опытном хозяине и последовательной дрессировке. Отлично подходит для охраны.', 24, 'Ротвейлер', 'Мужской', 1, 'reserved'),\
    ('Снежок', 'Изящная салюки с белоснежной шерстью и аристократичной внешностью. Спокойная и грациозная, обладает развитым охотничьим инстинктом. Нуждается в безопасном выгуле на поводке.', 36, 'Салюки', 'Мужской', 0, 'available'),\
    ('Герда', 'Жизнерадостная такса с длинным телом и короткими лапками. Очень любопытная и смелая, обожает исследовать новые места. Преданный компаньон с большим сердцем.', 24, 'Такса', 'Женский', 0, 'available'),\
    ('Боня', 'Энергичный джек-рассел-терьер с ярким характером. Неутомимый игрок, обожает мячики и активные игры. Очень умный, но нуждается в последовательном воспитании.', 12, 'Джек-рассел-терьер', 'Мужской', 0, 'available'),\
    ('Лиза', 'Очаровательная корги с короткими лапками и веселым нравом. Очень общительная и умная, хорошо поддается дрессировке. Обладает забавной походкой и дружелюбным характером.', 24, 'Корги', 'Женский', 0, 'available');")


conn.execute("INSERT INTO Animal_image (file_name, file_type, animal_id) VALUES\
    ('1.jpg', 'jpeg', 1),\
    ('2.jpg', 'jpeg', 2),\
    ('3.jpg', 'jpeg', 3),\
    ('4.jpg', 'jpeg', 4),\
    ('5.jpg', 'jpeg', 5),\
    ('6.jpg', 'jpeg', 6),\
    ('7.jpg', 'jpeg', 7),\
    ('8.jpg', 'jpeg', 8),\
    ('9.jpg', 'jpeg', 9),\
    ('10.jpg', 'jpeg', 10),\
    ('11.jpg', 'jpeg', 11);")


conn.execute("INSERT INTO User_has_Animal (animal_id, user_login, date, status, contact) VALUES\
    (3, 'petrov', '2024-01-15', 'pending', 'petrov@email.com, +7-123-456-7890'),\
    (7, 'sidorova', '2024-01-14', 'approved', 'sidorova@email.com, +7-987-654-3210');")

conn.commit()

conn.close()
