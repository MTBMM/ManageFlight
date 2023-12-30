from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, BOOLEAN, ForeignKey, FLOAT, DATETIME
from sqlalchemy.orm import relationship
from ManageFlightApp import Admin, db, app
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class Person(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')

    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)


class Customer(Person, UserMixin):
    phone = Column(String(12), nullable=True)
    Identify = Column(String(20), nullable=True)
    receipts = relationship("Receipt", backref="customer", lazy=True)
    Customer_ticket = relationship('Ticket', backref='customer', lazy=True)


class Employee(Person, UserMixin):
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


class Airport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # Tên sân bay
    location = Column(String(255))  # Địa điểm sân bay
    stops_airport = relationship('Stop', backref='airport', lazy=True)


class Route(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # Tên của tuyến đường
    distance = Column(FLOAT)  # Khoảng cách của tuyến đường (đơn vị: km)
    number_of_airport = Column(Integer,nullable=False)
    arrival_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    departure_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    stops_route = relationship('Stop', backref='route', lazy=True)




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
    time_delay_max = Column(FLOAT)  # Thời gian Đếm
    time_delay_min = Column(FLOAT)  # Thời gian khởi hành





class Kind(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib

        # u1 = Employee(name='Admin', username='admin',
        #               password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), salary=50000000,
        #               user_role=UserRoleEnum.ADMIN)
        #
        # u2 = Customer(name='Nguyễn Trung Kiên', username='TrungKienIdol',
        #               password=str(hashlib.md5('TrungKien123'.encode('utf-8')).hexdigest()))
        # u3 = Customer(name='Hồ Ngọc Nhung', username='NhungNgoc',
        #               password=str(hashlib.md5('NhungNgoc123'.encode('utf-8')).hexdigest()))
        # u4 = Customer(name='Bùi Mỹ Nhân', username='ManNhi',
        #               password=str(hashlib.md5('ManNhi123'.encode('utf-8')).hexdigest()))
        # u5 = Customer(name='Tống Thị Thu Hiền', username='ThuHien',
        #               password=str(hashlib.md5('ThuHien123'.encode('utf-8')).hexdigest()))
        # u6 = Customer(name='Huỳnh Trúc Ly', username='TrucLy',
        #               password=str(hashlib.md5('TrucLy2003'.encode('utf-8')).hexdigest()))
        # u7 = Customer(name='Duong Thi Hong Nhu', username='HongNhu',
        #               password=str(hashlib.md5('HongNhu2004'.encode('utf-8')).hexdigest()))
        # u8 = Customer(name='Nguyễn Cao', username='CaoNguyen',
        #               password=str(hashlib.md5('CaoNguyen123'.encode('utf-8')).hexdigest()))
        # u9 = Employee(name='Phương Mỹ Chi', username='MyChi',
        #               password=str(hashlib.md5('MyChi123'.encode('utf-8')).hexdigest()), salary=10000000,
        #               user_role=UserRoleEnum.EMPLOYEE)
        # u10 = Employee(name='Hồ Thị Cẩm', username='ThiCam',
        #                password=str(hashlib.md5('ThiCam123'.encode('utf-8')).hexdigest()), salary=15000000,
        #                user_role=UserRoleEnum.EMPLOYEE)
        #
        # db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10])
        # db.session.commit()

        # k1 = Kind(name='Hang Pho Thong')
        # k2 = Kind(name='Hang Thuong Gia')
        #
        # db.session.add_all([k1, k2])
        # db.session.commit()

        # A1 = Airport(name='TP.HCM', location='Bình Thạnh, Thành phố Hồ Chí Minh')
        # A2 = Airport(name='Hà Nội', location='Linh Xuân, Hà Nội')
        # A3 = Airport(name='Hải Phòng', location='Đóng Đa, Hải Phòng')
        # A4 = Airport(name='Đà Nẵng', location='Hiệp Phước, Đà Nẵng')
        # A5 = Airport(name='Cà Mau', location='Long Mỹ, Cà Mau')
        # A6 = Airport(name='Tây Ninh', location='Châu Thanh, Tây Ninh')
        # A7 = Airport(name='Sapa', location='Phnong, Sapa')
        # A8 = Airport(name='Đà Lạt', location='67, Đà Lạt')
        # A9 = Airport(name='Vũng Tàu', location='Xô Viết, Vũng tàu')
        # A10 = Airport(name='Phan Thiết', location='Trần Hưng Đạo, Phan Thiết')
        #
        # db.session.add_all([A1, A2, A3, A4, A5, A6, A7, A8, A9, A10])
        # db.session.commit()

        # r1 = Route(name='TP.HCM - HÀ NỘI', distance=1190, number_of_airport=2, arrival_id=2, departure_id=1)
        # r2 = Route(name='TP.HCM - Đà Nẵng', distance=590, number_of_airport=0, arrival_id=4, departure_id=1)
        # r3 = Route(name='Đà Nẵng - Hải Phòng', distance=200, number_of_airport=0, arrival_id=3, departure_id=4)
        # r4 = Route(name='Hải Phòng - HÀ NỘI', distance=400, number_of_airport=0, arrival_id=2, departure_id=3)
        # r5 = Route(name='TP.HCM - Cà Mau', distance=1190, number_of_airport=2, arrival_id=5, departure_id=1)
        # r6 = Route(name='SaPa - Phan thiết', distance=1190, number_of_airport=1, arrival_id=10, departure_id=7)
        # r7 = Route(name='Phan Thiết - Vũng tàu', distance=1190, number_of_airport=0, arrival_id=9, departure_id=10)
        # r8 = Route(name='Tây Ninh - Sapa', distance=1190, number_of_airport=2, arrival_id=7, departure_id=6)
        # r9 = Route(name='Đà Lạt - TP.HCM', distance=1190, number_of_airport=0, arrival_id=1, departure_id=8)
        # r10 = Route(name='Vũng Tàu - Đà Lạt', distance=1190, number_of_airport=0, arrival_id=8, departure_id=9)

        r11 = Route(name='Đà nẵng - Đà Lạt', distance=1190, number_of_airport=0, arrival_id=8, departure_id=9)
        a11 = Airport(name='Hà Giang', location='Bình Thạnh, Hà Giang')
        # db.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10])
        # db.session.commit()

        # St1 = Stop(route_id=1, airport_id=4, order=1, time_delay_max=30, time_delay_min=20)
        # St2 = Stop(route_id=1, airport_id=3, order=2, time_delay_max=30, time_delay_min=20)
        # St3 = Stop(route_id=6, airport_id=10, order=1, time_delay_max=30, time_delay_min=20)
        # St = Stop(route=r11, airport=a11, time_delay_max=30, time_delay_min=20)
        St4 = Stop(route_id=8, airport_id=10, order=1, time_delay_max=30, time_delay_min=20)
        St5 = Stop(route_id=8, airport_id=4, order=1, time_delay_max=30, time_delay_min=20)
        St6 = Stop(route_id=9, airport_id=4, order=1, time_delay_max=30, time_delay_min=20)
        St7 = Stop(route_id=6, airport_id=4, order=1, time_delay_max=30, time_delay_min=20)

        db.session.add_all([St4, St5, St6, St7])
        db.session.commit()
