from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, BOOLEAN, ForeignKey, FLOAT, DATETIME
from sqlalchemy.orm import relationship
from ManageFlightApp import admin, db, app
from flask_login import UserMixin
import enum


class Person(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class Customer(Person, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    phone = Column(String(12), nullable=True)
    Identify = Column(String(20), nullable=True)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    receipts = relationship("Receipt", backref="customer", lazy=True)
    Customer_ticket = relationship('Ticket', backref='customer', lazy=True)


class Employee(Person):
    salary = Column(FLOAT, nullable=True)


class Seat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_seat = Column(Integer, nullable=True)
    kind_seat = Column(String(50), nullable=True)
    status = Column(BOOLEAN, default=False)
    plane_id = Column(Integer, ForeignKey('plane.id'), nullable=False)
    kind_id = Column(Integer, ForeignKey('kind.id'), nullable=False)
    plane_seat = relationship('Plane', backref='seat', lazy=True)
    kind_seat = relationship('Kind', backref='seat', lazy=True)


class Flight(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    departure_time = Column(DATETIME)
    arrival_time = Column(DATETIME)
    flight_ticket = relationship('Ticket', backref='flight', lazy=True)


class TicketClass(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    quantity = Column(Integer, default=0)  # Số lượng hạng vé


class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_time = Column(DATETIME, nullable=False)  # Thời gian mua vé
    booking_time = Column(DATETIME, nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    Employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    fight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    ticket_class_id = Column(Integer, ForeignKey(TicketClass.id), nullable=False)


class Plane(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DATETIME, default=datetime.now())
    user_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    total_money = Column(FLOAT, default=0)
    detail_receipt = relationship("ReceiptDetail", backref="receipt", lazy=True)


class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), primary_key=True, nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True, nullable=False)
    quantity = Column(Integer, default=0)
    unit_price = Column(FLOAT, default=0)


class Schedules(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    plane_id = Column(Integer, ForeignKey(Plane.id), primary_key=True, nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True, nullable=False)
    date_department = Column(DATETIME, default=datetime.now())


class Route(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # Tên của tuyến đường
    description = Column(String(1000))  # Mô tả tuyến đường
    distance = Column(FLOAT)  # Khoảng cách của tuyến đường (đơn vị: km)
    arrival = Column(String(255), nullable=False)
    departure = Column(String(255), nullable=False)
    stops_route = relationship('Stop', backref='route', lazy=True)


class Airport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(3), unique=True, nullable=False)  # Mã sân bay (3 ký tự)
    name = Column(String(255), nullable=False)  # Tên sân bay
    location = Column(String(255))  # Địa điểm sân bay
    airline_id = Column(Integer, ForeignKey("airline.id"), nullable=False)
    stops_airport = relationship('Stop', backref='airport', lazy=True)


class TicketPrice(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(FLOAT, default=0)  # Đơn giá vé
    ticket_class_id = Column(Integer, ForeignKey(TicketClass.id), nullable=False)
    states = Column(BOOLEAN, default=False)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)


class Stop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)  # Khóa ngoại liên kết với sân bay
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)  # Khóa ngoại liên kết với tuyến đường
    order = Column(Integer)  # Thứ tự của điểm dừng trên tuyến đường
    arrival_time_max = Column(DATETIME)  # Thời gian Đếm
    departure_time_min = Column(DATETIME)  # Thời gian khởi hành


class Airline(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(String(1000))
    max_airports_served = Column(Integer, default=0)  # Số lượng sân bay tối đa mà hãng vận tải có thể phục vụ


class Kind(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # import hashlib
        # u = User(name='User1', username='U1',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()))
        # db.session.add(u)
        # db.session.commit()
