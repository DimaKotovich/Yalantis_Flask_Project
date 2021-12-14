from Flask import db

# from flask_migrate import Migrate
# #
# from FlaskProject import app

import datetime


# Migrate(app, db)


class Driver(db.Model):
    """ Drivers model """

    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True, )
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    vehicle = db.relationship('Vehicle', backref='driver', uselist=False)

    def init(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = None
        self.updated_at = None

    def repr(self):
        return f'First name: {self.first_name}, lastname: {self.last_name}, created at: {self.created_at},' \
               f'updated at: {self.updated_at}'


class Vehicle(db.Model):
    """ The vehicle model """

    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    make = db.Column(db.String(64))
    model = db.Column(db.String(64))
    plate_number = db.Column(db.String(64))
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), server_default=db.func.now(), onupdate=datetime.datetime.now)

    def init(self, driver_id, make, model, plate_number):
        self.driver_id = driver_id
        self.make = make
        self.model = model
        self.plate_number = plate_number
        self.created_at = None
        self.updated_at = None

    def repr(self):
        return f'Driver id: {self.driver_id}, make: {self.make}, model: {self.model}, ' \
               f'plate number: {self.plate_number}, created at: {self.created_at},' \
               f'updated at: {self.updated_at}'


db.create_all()