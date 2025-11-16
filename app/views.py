from app import app
from flask import make_response, render_template, session, redirect, url_for, request, flash
from datetime import date, datetime
import os
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, Date, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps

BASEPATH = os.path.abspath(os.path.dirname(__file__))
DBPATH = os.path.join(BASEPATH, 'database.db')
UPLOADPATH = os.path.join(BASEPATH, 'static', 'images')

db = sa.create_engine(f"sqlite:///{DBPATH}")
Session = sessionmaker(bind=db)
Base = declarative_base()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class UserLogin(UserMixin):
    def __init__(self, user=None):
        if user:
            self.id = user.login
            self.user = user
        else:
            self.id = None
            self.user = None

    @property
    def is_authenticated(self):
        return self.user is not None
    
    @property
    def is_active(self):
        return self.user is not None
    
    @property
    def is_anonymous(self):
        return self.user is None
    
    def get_id(self):
        return self.id

class User(Base):
    __tablename__ = "User"
    login: Mapped[str] = mapped_column(String(length=50), primary_key=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    last_name: Mapped[str]  = mapped_column(String(length=100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    father_name: Mapped[str] = mapped_column(String(length=100))

class User_role(Base):
    __tablename__ = "User_role"
    user_login: Mapped[str] = mapped_column(String(length=50), ForeignKey("User.login"), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)

class Animal(Base):
    __tablename__ = "Animal"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]  = mapped_column(String(length=100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String(length=100), nullable=False)
    sex: Mapped[str] = mapped_column(String(length=10), nullable=False)
    request_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(length=50), nullable=False)

class Animal_image(Base):
    __tablename__ = "Animal_image"
    file_name: Mapped[str]  = mapped_column(String(length=255), primary_key=True, nullable=False)
    file_type: Mapped[str]  = mapped_column(String(length=100), nullable=False)
    animal_id: Mapped[int] = mapped_column(ForeignKey("Animal.id"), nullable=False)

class User_has_Animal(Base):
    __tablename__ = "User_has_Animal"
    date: Mapped[date]  = mapped_column(DateTime, nullable=False)
    status: Mapped[str]  = mapped_column(String(length=50), nullable=False)
    contact: Mapped[str]  = mapped_column(String(length=255), nullable=False)
    animal_id: Mapped[int] = mapped_column(Integer, ForeignKey("Animal.id"), primary_key=True, nullable=False)
    user_login: Mapped[str] = mapped_column(String(length=50), ForeignKey("User.login"), primary_key=True, nullable=False)

Base.metadata.create_all(db)

def get_user_role_by_login(login):
    try:
        with Session() as session:
            role = session.get(User_role, login)
            if not role:
                return None
            return role.name
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return None

def get_animals():
    try:
        with Session() as session:
            animals = session.query(Animal).all()
            if not animals:
                flash("Ошибка при запросе Animal из базы данных", 'error')
                return False
            return animals
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def get_animal_by_id(animal_id):
    try:
        with Session() as session:
            animal = session.get(Animal, animal_id)
            if not animal:
                flash("Ошибка при запросе Animal из базы данных", 'error')
                return False
            return animal
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def get_animal_image_by_id(animal_id):
    try:
        with Session() as session:
            animal_image = session.query(Animal_image).filter_by(animal_id=animal_id).first()
            if not animal_image:
                default_image = Animal_image(
                    file_name='default.jpg',
                    file_type='jpeg',
                    animal_id=animal_id)
                return default_image
            return animal_image
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return None

def get_animal_images_by_id(animal_id):
    try:
        with Session() as session:
            animal_images = session.query(Animal_image)#.filter_by(animal_id=animal_id).first()
            res = []
            if not animal_images:
                default_image = Animal_image(
                file_name='default.jpg',
                file_type='jpeg',
                animal_id=animal_id)
                res.append(default_image)
            else:
                for animal_image in animal_images:
                    if animal_image.animal_id == animal_id:
                        res.append(animal_image)
            return res
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return None

def get_user_by_login(login):
    try:
        with Session() as session:
            user = session.get(User, login)
            if not user:
                return None
            return user
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return None

def get_animal_date_by_id(animal_id):
    try:
        with Session() as session:
            user_has_animal = session.query(User_has_Animal)\
            .filter_by(animal_id=animal_id)\
            .order_by(User_has_Animal.date.desc())\
            .first()
            if user_has_animal:
                return user_has_animal.date
            return datetime(2000, 1, 1, 00, 00, 00)
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return datetime(2000, 1, 1, 00, 00, 00)

def get_animal_by_id(animal_id):
    try:
        with Session() as session:
            animal = session.get(Animal, animal_id)
            if animal:
                return animal
            else:
                return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def get_user_has_animals():
    try:
        with Session() as session:
            user_has_animals = session.query(User_has_Animal).all()
            if not user_has_animals:
                flash("Ошибка при запросе User_has_Animal из базы данных", 'error')
                return False
            return user_has_animals
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def get_user_has_animal(animal_id, user_login):
    try:
        with Session() as session:
            user_has_animal = session.get(User_has_Animal, animal_id, user_login)
            if not user_has_animal:
                flash("Ошибка при запросе User_has_Animal из базы данных", 'error')
                return False
            return user_has_animal
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def update_animal_status(animal_id, status):
    try:
        with Session() as session:
            animal = session.get(Animal, animal_id)
            if not animal:
                flash("Ошибка при запросе Animal из базы данных", 'error')
                return False
            animal.status = status
            session.commit()
            return True
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def update_animal_request_count_by_id(animal_id):
    try:
        with Session() as session:
            count = session.query(User_has_Animal)\
                .filter_by(animal_id=animal_id)\
                .count()
            
            animal = session.get(Animal, animal_id)
            if animal:
                animal.request_count = count
                session.commit()
                return count
            return 0
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return 0

def update_all_animals_request_counts():
    try:
        with Session() as session:
            animals = session.query(Animal).all()
            for animal in animals:
                count = session.query(User_has_Animal).filter_by(animal_id=animal.id).count()
                animal.request_count = count
                if count > 0 and animal.status == 'available':
                    animal.status = "reserved"
            session.commit()
            return True
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def update_animal(animal):
    try:
        with Session() as session:
            new_animal = session.get(Animal, animal.id)
            if new_animal:
                new_animal.name = animal.name
                new_animal.breed = animal.breed
                new_animal.age = animal.age
                new_animal.sex = animal.sex
                new_animal.description = animal.description
                new_animal.request_count = animal.request_count
                new_animal.status = animal.status
                session.commit()
                flash("Запись успешно изменена", 'success')
                return new_animal
            error = "Произошла ошибка при отправке заявки"
            flash(error, 'error')
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def update_user_has_animal_status(animal_id, user_login, status):
    try:
        with Session() as session:
            user_has_animal = session.get(User_has_Animal, (animal_id, user_login))
            if user_has_animal:
                user_has_animal.status = status
                session.commit()
                flash("Статус заявки успешно изменён", 'success')
                return True
            error = "Произошла ошибка при изменении статуса заявки"
            flash(error, 'error')
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def does_user_has_user_has_animal(user_has_animal):
    try:
        with Session() as session:
            if user_has_animal:
                db_user_has_animal = session.query(User_has_Animal).filter_by(
                    animal_id=user_has_animal.animal_id,
                    user_login=user_has_animal.user_login
                ).first()
                if db_user_has_animal:
                    return True
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def add_user_role_by_login(user_login):
    try:
        with Session() as session:
            if user_login:
                user_role = User_role(
                    user_login=user_login,
                    name='user'
                )
                session.add(user_role)
                session.commit()
                flash('Роль успешно добавлена', 'success')
                return True
            error = "Произошла ошибка при добавлении роли"
            flash(error, 'error')
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def add_animal(animal):
    try:
        with Session() as session:
            if animal:
                session.add(animal)
                session.commit()
                new_animal = session.query(Animal).filter_by(
                    name=animal.name,
                    description=animal.description,
                    age=animal.age,
                    breed=animal.breed,
                    sex=animal.sex,
                    request_count=animal.request_count,
                    status=animal.status
                ).first()
                update_all_animals_request_counts()
                flash('Животное успешно добавлено', 'success')
                return new_animal.id
            error = "Произошла ошибка при добавлении животного"
            flash(error, 'error')
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def add_animal_image(file_name, file_type, animal_id):
    try:
        with Session() as session:
            animal_image = Animal_image(
                file_name=file_name,
                file_type=file_type,
                animal_id=animal_id)
            if animal_image:
                session.add(animal_image)
                session.commit()
                return True
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def add_user_has_animal(user_has_animal):
    try:
        with Session() as session:
            if user_has_animal:
                request_exists = does_user_has_user_has_animal(user_has_animal)
                if not request_exists:
                    session.add(user_has_animal)
                    session.commit()
                    update_all_animals_request_counts()
                    flash('Заявка успешно отправлена', 'success')
                    return True
                flash('Вы уже отправили заявку на усыновление этого питомца', 'error')
                return False
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def add_image_files_by_id(animal_id, files):
    filecounter = 0
    for file in files:
        filecounter += 1
        if file and file.filename != '':
            file_name, file_extension = os.path.splitext(secure_filename(file.filename))
            file_name = f"{animal_id}_{filecounter}{file_extension}"
            file_path = os.path.join(UPLOADPATH, file_name)
            add_animal_image(file_name, file_extension, animal_id)
            file.save(file_path)
    flash('Изображения успешно добавлены', 'success')

def delete_animal_image_by_id(animal_id):
    try:
        with Session() as session:
            animal_images = session.query(Animal_image)
            if animal_images:
                for animal_image in animal_images:
                    if animal_image.animal_id == animal_id:
                        file_location = os.path.join(UPLOADPATH, animal_image.file_name)
                        os.remove(file_location)
                        session.delete(animal_image)
                        session.commit()
                flash("Изображения успешно удалены", 'success')
                return True
            return False
    except Exception as e:
        flash(f"Error: {str(e)}")
        return False

def delete_all_user_has_animal_by_id(animal_id):
    try:
        with Session() as session:
            user_has_animals = session.query(User_has_Animal)
            if user_has_animals:
                for user_has_animal in user_has_animals:
                    if user_has_animal.animal_id == animal_id:
                        session.delete(user_has_animal)
                session.commit()
                flash("Заявки на усыновление животного успешно удалены", 'success')
                return True
            return False
    except Exception as e:
        flash(f"Error: {str(e)}")
        return False

'''
def delete_user_has_animal(animal_id, user_login):
    try:
        with Session() as session:
            user_has_animal = session.get(User_has_Animal, (animal_id, user_login))
            if user_has_animal:
                session.delete(User_has_Animal, animal_id, user_login)
                session.commit()
                flash("Заявка успешно удалена", 'success')
                return True
            error = "Произошла ошибка при удалении заявки"
            flash(error, 'error')
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False
'''

def delete_animal_by_id(animal_id):
    try:
        with Session() as session:
            animal = session.get(Animal, animal_id)
            if animal:
                delete_animal_image_by_id(animal_id)
                delete_all_user_has_animal_by_id(animal_id)
                session.delete(animal)
                session.commit()
                flash("Запись успешно удалена", 'success')
                return True
            error = "Произошла ошибка при удалении животного"
            flash(error, 'error')
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def sort_animals(animals):
    if not animals:
        return []
    return sorted(animals, key=lambda x: (
        2 if x.status == 'transitioning' else 1 if x.status == 'reserved' else 0,
        get_animal_date_by_id(x.id)),
        reverse=False
    )

def paginate_animals(animals, page, per_page=10):
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    return animals[start_idx:end_idx]

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if get_user_role_by_login(current_user.user.login) == required_role or\
                required_role == 'user' and\
                    (get_user_role_by_login(current_user.user.login) == 'moderator' or\
                     get_user_role_by_login(current_user.user.login) == 'admin') or\
                required_role == 'moderator' and get_user_role_by_login(current_user.user.login) == 'admin':
                return f(*args, **kwargs)
            flash(f"Необходима роль {required_role}", 'error')
            return redirect(url_for('login'))
        return decorated_function
    return decorator

update_all_animals_request_counts()

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_login(user_id)
    if user:
        return UserLogin(user)
    return None

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    sorted_animals = sort_animals(get_animals())
    animals_per_page = 10
    total_pages = (len(sorted_animals) + animals_per_page - 1) // animals_per_page
    paginated_animals = paginate_animals(sorted_animals, page, animals_per_page)

    return render_template('index.html',
                        animals=paginated_animals,
                        current_page=page,
                        total_pages=total_pages,
                        get_animal_image_by_id=get_animal_image_by_id,
                        get_animal_count=update_animal_request_count_by_id,
                        get_user_role_by_login=get_user_role_by_login)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        user = get_user_by_login(login)
        if user and check_password_hash(user.password , password):
            user_login = UserLogin(user)
            login_user(user_login)
            flash('Вы успешно вошли в аккаунт', 'success')
            return redirect(url_for('index'))
        error = "Неверный пароль или логин"
        flash(error, 'error')
    return render_template('login.html', title='Log in', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('index'))

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    error = None
    if request.method == "POST":
        try:
            with Session() as session:
                existing_user = session.get(User, request.form['login'])
                if existing_user:
                    error = "Пользователь с таким логином уже существует"
                    flash(error, 'error')
                    return redirect(url_for('reg'))
                else:
                    hash = generate_password_hash(request.form['password'])
                    new_user = User(
                        login=request.form['login'],
                        password=hash,
                        last_name=request.form['last_name'],
                        first_name=request.form['first_name'],
                        father_name=request.form.get('father_name', '')
                    )
                    add_user_role_by_login(new_user.login)
                    session.add(new_user)
                    session.commit()
                    
                    user_login = UserLogin(new_user)
                    login_user(user_login)
                    flash('Registration successful!', 'success')
                    return redirect(url_for('index'))
        except Exception as e:
            error = f"Registration error: {str(e)}"
            flash(error, 'error')
    
    return render_template("reg.html", title="Registration", error=error)

@app.route('/animal_view/<int:animal_id>', methods=['GET', 'POST'])
@login_required
@role_required('user')
def animal_view(animal_id):
    animal = get_animal_by_id(animal_id)
    if not animal:
        flash('Animal not found')
        return redirect(url_for('index'))
    
    error = None
    if request.method == "POST":
        contact = request.form['contact']
        today_date = datetime.now()
        user = current_user.user
        user_has_animal = User_has_Animal(date=today_date,
                                              status="pending",
                                              contact=contact,
                                              animal_id=animal.id,
                                              user_login=user.login)
        if user_has_animal:
            add_user_has_animal(user_has_animal)
            return redirect(url_for('index'))
        error = "Произошла ошибка при отправке заявки"
        flash(error, 'error')

    animal_images = get_animal_images_by_id(animal_id)
    return render_template('animal_view.html',
                        animal=animal,
                        animal_images=animal_images,
                        get_user_role_by_login=get_user_role_by_login)

@app.route('/animal_edit/<int:animal_id>', methods=['GET', 'POST'])
@login_required
@role_required('moderator')
def animal_edit(animal_id):
    animal = get_animal_by_id(animal_id)
    error = None
    if request.method == "POST":
        id = animal_id
        name = request.form['name']
        breed = request.form['breed']
        age = request.form['age']
        sex = request.form['sex']
        description = request.form['description']
        request_count = update_animal_request_count_by_id(animal_id)
        status = "available"
        if request_count > 0:
            status = "reserved"
        animall = Animal(id=id,
                        name=name,
                        breed=breed,
                        age=age,
                        sex=sex,
                        description=description,
                        request_count=request_count,
                        status=status)
        if animall:
            update_animal(animall)
            if 'images' in request.files:
                delete_animal_image_by_id(animal_id)
                files = request.files.getlist('images')
                add_image_files_by_id(animal_id, files)
            return redirect(url_for('index'))
        error = "Произошла ошибка при отправке запроса"
        flash(error, 'error')

    animal_images = get_animal_images_by_id(animal_id)
    return render_template('animal_edit.html',
                        animal=animal,
                        animal_images=animal_images,
                        get_user_role_by_login=get_user_role_by_login)

@app.route('/animal_add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def animal_add():
    error = None
    if request.method == "POST":
        animal = Animal(
            name=request.form['name'],
            description=request.form['description'],
            age=int(request.form['age']),
            breed=request.form['breed'],
            sex=request.form['sex'],
            status="available",
            request_count=0
        )
        
        if animal:
            animal_id = add_animal(animal)
            
            if 'images' in request.files:
                files = request.files.getlist('images')
                
                add_image_files_by_id(animal_id, files)
            return redirect(url_for('index'))
    
    return render_template('animal_add.html')

@app.route('/animal_delete/<int:animal_id>')
@login_required
@role_required('admin')
def animal_delete(animal_id):
    delete_animal_by_id(animal_id)
    return redirect(url_for('index'))

@app.route('/requests')
@login_required
@role_required('moderator')
def requests():
    page = request.args.get('page', 1, type=int)

    requestss = sorted(get_user_has_animals(), key=lambda x: (
        0 if x.status == 'pending' else 1 if x.status == 'approved' else 2,
        x.date),
        reverse=False)
    requests_per_page = 10
    total_pages = (len(requestss) + requests_per_page - 1) // requests_per_page
    paginated_requests = paginate_animals(requestss, page, requests_per_page)

    return render_template('requests.html',
                        requestss=paginated_requests,
                        get_animal_by_id=get_animal_by_id,
                        get_animal_image_by_id=get_animal_image_by_id,
                        get_user_by_login=get_user_by_login,
                        current_page=page,
                        total_pages=total_pages)

@app.route('/request_approve/<int:animal_id>/<string:user_login>')
@login_required
@role_required('moderator')
def request_approve(animal_id, user_login):
    update_user_has_animal_status(animal_id, user_login, 'approved')
    update_animal_status(animal_id, 'transitioning')
    return redirect(url_for('requests'))

request_approve
@app.route('/request_disapprove/<int:animal_id>/<string:user_login>')
@login_required
@role_required('moderator')
def request_disapprove(animal_id, user_login):
    update_user_has_animal_status(animal_id, user_login, 'rejected')
    return redirect(url_for('requests'))
