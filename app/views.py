from app import app
from flask import make_response, render_template, session, redirect, url_for, request, flash
from datetime import date
import os
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, Date, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

BASEPATH = os.path.abspath(os.path.dirname(__file__))
DBPATH = os.path.join(BASEPATH, 'database.db')

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

class User_role(Base):
    __tablename__ = "User_role"
    name: Mapped[str] = mapped_column(String(length=50), primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

class User(Base):
    __tablename__ = "User"
    login: Mapped[str] = mapped_column(String(length=50), primary_key=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    last_name: Mapped[str]  = mapped_column(String(length=100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    father_name: Mapped[str] = mapped_column(String(length=100))
    role: Mapped[str] = mapped_column(String(length=50), ForeignKey("User_role.name"), nullable=False)

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
    date: Mapped[date]  = mapped_column(Date, nullable=False)
    status: Mapped[str]  = mapped_column(String(length=50), nullable=False)
    contact: Mapped[str]  = mapped_column(String(length=255), nullable=False)
    animal_id: Mapped[int] = mapped_column(Integer, ForeignKey("Animal.id"), primary_key=True, nullable=False)
    user_login: Mapped[str] = mapped_column(String(length=50), ForeignKey("User.login"), primary_key=True, nullable=False)

Base.metadata.create_all(db)

def get_animals():
    try:
        with Session() as session:
            animals = session.query(Animal).all()
            if not animals:
                flash("Error getting animals from database")
                return False
            return animals
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def get_animal_image_by_id(animal_id):
    try:
        with Session() as session:
            animal_image = session.query(Animal_image).filter_by(animal_id=animal_id).first()
            if not animal_image:
                flash("Error getting image from database")
                return None
            return animal_image
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
            user_animal = session.query(User_has_Animal).filter_by(animal_id=animal_id).first()
            
            if user_animal:
                return user_animal.date
            else:
                return date(9999, 12, 31)
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return date(9999, 12, 31)

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
                if count > 0:
                    animal.status = "reserved"
                else:
                    animal.status = "available"
            session.commit()
            return True
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def get_user_role_by_login(login):
    try:
        with Session() as session:
            user = session.get(User, login)
            if not user:
                return None
            return user.role
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return None

def add_user_has_animal(user_has_animal):
    try:
        with Session() as session:
            if user_has_animal:
                session.add(user_has_animal)
                session.commit()
                update_all_animals_request_counts
                flash('Заявка успешно отправлена', 'success')
                return True
            return False
    except Exception as e:
        flash(f"Database error: {str(e)}")
        return False

def sort_animals(animals):
    if not animals:
        return []
    return sorted(animals, key=lambda x: (
        1 if x.status == 'available' else 0,
        get_animal_date_by_id(x.id)),
        reverse=True
    )

def paginate_animals(animals, page, per_page=10):
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    return animals[start_idx:end_idx]

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_login(user_id)
    if user:
        return UserLogin(user)
    return None

@app.route('/')
def index():
    update_all_animals_request_counts()
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
                        get_animal_count=update_animal_request_count_by_id)

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
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        error = "Wrong password or login"
        flash(error, 'error')
    return render_template('login.html', title='Log in', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    error = None
    if request.method == "POST":
        try:
            with Session() as session:
                existing_user = session.get(User, request.form['login'])
                if existing_user:
                    error = "User with this login already exists"
                else:
                    hash = generate_password_hash(request.form['password'])
                    new_user = User(
                        login=request.form['login'],
                        password=hash,
                        last_name=request.form['last_name'],
                        first_name=request.form['first_name'],
                        father_name=request.form.get('father_name', ''),
                        role='user'
                    )
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
def animal_view(animal_id):
    animal = get_animal_by_id(animal_id)
    if not animal:
        flash('Animal not found')
        return redirect(url_for('index'))
    
    error = None
    if request.method == "POST":
        contact = request.form['contact']
        today_date = date.today()
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

    animal_image = get_animal_image_by_id(animal_id)
    if not animal_image:
        animal_image = Animal_image(file_name='default_image.jpg', file_type="jpeg", animal_id=animal_id)
    return render_template('animal_view.html', animal=animal, animal_image=animal_image)

@app.route('/animal_edit/<int:animal_id>')
def animal_edit(animal_id):
    animal = get_animal_by_id(animal_id)
    return render_template('animal_edit.html', animal=animal)

@app.route('/animal_add/<int:animal_id>')
def animal_add(animal_id):
    animal = get_animal_by_id(animal_id)
    return render_template('animal_add.html', animal=animal)

@app.route('/animal_delete/<int:animal_id>', methods=['POST'])
def animal_delete(animal_id):
    # delete_animal(animal_id)
    return redirect(url_for('index'))
