from sqlalchemy import Column, Integer, String, Enum
from ManageFlightApp import db, app
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)


if __name__ == '__main__':
        with app.app_context():
            db.create_all()
            import hashlib
            u = User(name='User1', username='U1',
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()))
            db.session.add(u)
            db.session.commit()
