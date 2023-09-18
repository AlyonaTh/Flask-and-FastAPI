from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import enum


db = SQLAlchemy()


class GenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum(GenderEnum))
    group = db.Column(db.Integer)
    faq = db.Column(db.Integer, db.ForeignKey('faq.id'))

    def __repr__(self):
        return f'Student ({self.name})'


class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    students = db.relationship('Student', backref='faculty', lazy=True)


# В таблице "Оценки" должны быть следующие поля: id, id студента, название предмета и оценка.
class Estimate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = db.relationship('Student', backref='estimates', lazy=True)
    faculty = db.Column(db.String, db.ForeignKey('faq.title'))
    faq = db.relationship('Faq', backref='estimates', lazy=True)
    value = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.value}'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer)
    author = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return f'Book ({self.title})'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    books = db.relationship('Book', backref='author_name', lazy=True)

    def __repr__(self):
        return f'Author ({self.name} {self.surname})'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class User2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    surname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)