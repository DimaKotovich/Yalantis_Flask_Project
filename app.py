from datetime import datetime

from Flask import app, db, models

from flask import request, jsonify

from flask_migrate import Migrate

from Flask.models import Driver, Vehicle

driver_items = Driver.query.all()
vehicle_items = Vehicle.query.all()

"""
Func 'get_all_drivers_after_or_before_date ()', a function in which all drivers will be displayed, 
if you need it as another function, it is located below in func 'def get_drivers ()'
"""


@app.route('/drivers/driver/')
def get_drivers():
    """ /drivers/driver/ """

    result = []

    for items in driver_items:
        result.append({
            'driver_id': items.id,
            'driver_first_name': items.first_name,
            'driver_last_name': items.last_name,
            'driver_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            'driver_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
            })

    return jsonify(f'All drivers: ', result)


@app.route('/drivers/driver/', methods=['POST', 'GET'])
def drivers_func():
    """
     This function has different methods with drivers
     """

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    if request.method == 'GET' and request.args.get('created_at__gte'):
        """
         This part, displays drivers created after 10-11-2021

         /drivers/driver/?created_at__gte=10-11-2021
         """

        params = request.args.get('created_at__gte')
        params_format = params.replace('-', '/')

        date = datetime.strptime(params_format, "%d/%m/%Y")

        result = []

        for items in driver_items:

            if items.created_at > date:
                result.append({
                    'driver_id': items.id,
                    'driver_first_name': items.first_name,
                    'driver_last_name': items.last_name,
                    'driver_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'driver_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

            else:
                return f'No drivers were created after or before {date}'

        return jsonify(f'Drivers which were created after {date}: ', result)

    elif request.method == 'GET' and request.args.get('created_at__lte'):
        """
        Displays drivers created before 11/16/2021.

        /drivers/driver/?created_at__lte=16-11-2021
         """

        params = request.args.get('created_at__lte')
        params_format = params.replace('-', '/')

        date = datetime.strptime(params_format, "%d/%m/%Y")

        result = []

        for items in driver_items:

            if items.created_at < date:
                result.append({
                    'driver_id': items.id,
                    'driver_first_name': items.first_name,
                    'driver_last_name': items.last_name,
                    'driver_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'driver_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

            else:
                return f'No drivers were created after or before {date}'

        return jsonify(f'Drivers which were created before{date}: ', result)

    elif request.args.get('first_name') and request.args.get('last_name'):
        """
        This part,creates a new driver

        /drivers/driver/?first_name=Oleksandr&last_name=Kolomiets
         """

        result = []
        for items in driver_items:
            if items.first_name == first_name and items.last_name == last_name:
                return jsonify('Such driver already exist, but this one was created')

            else:

                new_driver = models.Driver(first_name=first_name, last_name=last_name)
                db.session.add(new_driver)
                db.session.commit()

            result.append({
                'driver_id': items.id,
                'driver_first_name': items.first_name,
                'driver_last_name': items.last_name,
                'driver_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                'driver_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
            })

        return jsonify('All drivers : ', result)

    elif not request.args.get('created_at__lte') or request.args.get('created_at__gte') or \
            request.args.get('created_at__lte'):
        """
         The part which is displaying all the drivers

         /drivers/driver/
         """

        result = []

        for items in driver_items:
            result.append({
                'driver_id': items.id,
                'driver_first_name': items.first_name,
                'driver_last_name': items.last_name,
                'driver_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                'driver_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
            })

        return jsonify(f'All drivers: ', result)


@app.route('/drivers/driver/<driver_id>/', methods=['GET', 'POST'])
def update_drivers_by_id(driver_id):
    """
    The function is responsible for updating drivers by their identifier.

    Func will only show you the changes after restarting the application.

    /drivers/driver/<driver_id>/?first_name=first_name&last_name=last_name
    """

    result = []

    if request.args.get('first_name') and request.args.get('last_name'):
        # return 'Ok'
        first_name_url = request.args.get('first_name')
        last_name_url = request.args.get('last_name')

        try:

            result = []
            updated_driver = Driver.query.filter_by(id=driver_id).update(dict(first_name=first_name_url,
                                                                              last_name=last_name_url))

            db.session.commit()

            for items in driver_items:
                result.append({
                    'driver_id': items.id,
                    'driver_first_name': items.first_name,
                    'driver_last_name': items.last_name,
                    'driver_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'driver_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

                return jsonify('Updated driver: ', result)

        except :

            return jsonify('There was a problem updating drivers')

    else:
        print('Incorrect id or params')
        pass


@app.route('/drivers/driver/<driver_id>/')
def get_drivers_by_id(driver_id):
    """
    Function that displays drivers by ID

    /drivers/driver/<driver_id>/
     """

    if driver_id is not None:

        result = []
        driver_id_int = int(driver_id)
        driver_by_id = Driver.query.filter_by(id=driver_id_int)

        for items in driver_by_id:

            if driver_id_int == items.id:
                result.append({
                    'driver_id': items.id,
                    'driver_first_name': items.first_name,
                    'driver_last_name': items.last_name,
                    'driver_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'driver_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

        return jsonify('Driver by id: ', result)

    else:
        print('driver_id can not be NoneType Object')
        pass


@app.route('/drivers/driver/<driver_id>/', methods=['GET'])
def delete_drivers(driver_id):
    """
     A function that removes drivers by id

     /drivers/driver/<driver_id>/
     """
    if driver_id is not None:

        if driver_id != [items.id for items in driver_items]:
            return 'The driver is not exits'

        else:

            driver_id_int = int(driver_id)

            for items in driver_items:

                if driver_id_int == items.id:
                    driver = Driver.query.filter_by(id=driver_id_int).first()
                    db.session.delete(driver)
                    db.session.commit()
                    return jsonify(f'The driver whith id {driver_id_int} was deleted')


@app.route('/drivers/driver/', methods=['POST', 'GET'])
def create_driver():
    """
        The function that creates the driver

        /drivers/driver/?first_name=first_name&last_name=last_name
         """

    if request.method == 'POST':

        first_name_url = str(request.args.get('first_name'))
        last_name_url = str(request.args.get('last_name'))

        # insert_readings()

        for item in driver_items:
            if item.first_name == first_name_url and item.last_name == last_name_url:
                return 'Such driver already exist'

            new_driver = models.Driver(first_name=first_name_url, last_name=last_name_url)
            db.session.add(new_driver)
            db.session.commit()

            result = []

            for items in driver_items:
                result.append({
                    'driver_id': items.id,
                    'driver_first_name': items.first_name,
                    'driver_last_name': items.last_name,
                    'driver_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'driver_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

            return jsonify('All drivers: ', result)


"""
In this part, actions take place with Vehicles 
"""


@app.route('/vehicles/vehicle/', methods=['POST', 'GET'])
def vehicles_func():
    """
     A function in which different methods of working with vehicles occur
     """

    result = []

    driver_id = request.args.get('driver_id')
    make = request.args.get('make')
    model = request.args.get('model')
    plate_number = request.args.get('plate_number')

    # vehicle_items = Vehicle.query.all()

    if request.method == 'GET' and request.args.get('with_drivers'):
        """
         Part,displays cars with driver

         /vehicles/vehicle/?with_drivers=yes
         """

        params = request.args.get('with_drivers')

        if params == 'yes':

            vehicles_with_driver = Vehicle.query.filter(Vehicle.driver_id.is_not(None))

            for items in vehicles_with_driver:
                print(isinstance(items.driver_id, int))

                type_bool = isinstance(items.driver_id, int)

                print(type_bool)

                result.append({
                    'driver_id': items.id,
                    'vehicle_make': items.make,
                    'vehicle_driver_id': items.driver_id,
                    'vehicle_model': items.model,
                    'vehicle_plate_number': items.plate_number,
                    'vehicle_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'vehicle_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

            return jsonify(f'Vehicles which have drivers: ', result)

        elif params == 'no':

            """
                    Part that displays cars that have no drivers.

                    /vehicles/vehicle/?with_drivers=no
            """

            vehicles_without_driver = Vehicle.query.filter(Vehicle.driver_id.is_(None))

            for items in vehicles_without_driver:

                result.append({
                    'driver_id': items.id,
                    'vehicle_make': items.make,
                    'vehicle_driver_id': items.driver_id,
                    'vehicle_model': items.model,
                    'vehicle_plate_number': items.plate_number,
                    'vehicle_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'vehicle_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

            return jsonify(f'Vehicles which don\'t have drivers: ', result)

    elif request.args.get('driver_id') and request.args.get('make') and request.args.get('model') and \
            request.args.get('plate_number'):
        """
        In this part, a vehicle is created

        /vehicles/vehicle/?driver_id=1&make=Toyota&model=Supra&plate_number=AA3041AB
         """

        for items in vehicle_items:

            new_vehicle = models.Vehicle(driver_id=driver_id, make=make, model=model, plate_number=plate_number)
            db.session.add(new_vehicle)
            db.session.commit()

            result.append({
                'driver_id': items.id,
                'vehicle_make': items.make,
                'vehicle_driver_id': items.driver_id,
                'vehicle_model': items.model,
                'vehicle_plate_number': items.plate_number,
                'vehicle_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                'vehicle_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
            })

        return jsonify('All vehicles : ', result)

    elif not request.args.get('driver_id') and not request.args.get('make') and not request.args.get('model') and not \
            request.args.get('plate_number'):
        """
         Part,displays all cars

         /vehicles/vehicle/
         """

        for items in vehicle_items:

            result.append({
                'driver_id': items.id,
                'vehicle_make': items.make,
                'vehicle_driver_id': items.driver_id,
                'vehicle_model': items.model,
                'vehicle_plate_number': items.plate_number,
                'vehicle_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                'vehicle_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
            })

        return jsonify(f'All vehicles: ', result)


@app.route('/vehicles/vehicle/<vehicle_id>/')
def get_vehicles_by_id(vehicle_id):
    """
    The func which is displaying vehicles by id

    /vehicles/vehicle/<vehicle_id>
     """

    if vehicle_id is not None:

        result = []
        vehicle_id_int = int(vehicle_id)
        vehicle_by_id = Vehicle.query.filter_by(id=vehicle_id)

        for items in vehicle_by_id:

            # if not driver_id_int == items.id:
            #     return f'No drivers were created with id {driver_id}'

            if vehicle_id_int == items.id:
                result.append({
                    'driver_id': items.id,
                    'vehicle_make': items.make,
                    'vehicle_driver_id': items.driver_id,
                    'vehicle_model': items.model,
                    'vehicle_plate_number': items.plate_number,
                    'vehicle_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'vehicle_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

        return jsonify('Vehicle by id: ', result)

    else:
        print('vehicle_id can not be NoneType Object')
        pass


@app.route('/vehicles/vehicle/<vehicle_id>/', methods=['GET', 'POST'])
def update_vehicles_by_id(vehicle_id):
    """
    The function is responsible for updating vehicles by their identifier.

    Func will only show you the changes after restarting the application.

    /vehicles/vehicle/<vehicle_id>/?driver_id=driver_id&make=make&model=model&plate_number=plate_number

    /vehicles/vehicle/1/?driver_id=1&make=Merced-Benz&model=E-63&plate_number=AB7777GG
    """

    if request.args.get('driver_id') and request.args.get('make') and request.args.get('model') and \
            request.args.get('plate_number'):

        driver_id = request.args.get('driver_id')
        make = request.args.get('make')
        model = request.args.get('model')
        plate_number = request.args.get('plate_number')

        try:

            result = []
            updated_vehicle = Vehicle.query.filter_by(id=vehicle_id).update(dict(driver_id=driver_id,
                                                                                 make=make, model=model,
                                                                                 plate_number=plate_number))

            db.session.commit()

            for items in vehicle_items:
                result.append({
                    'driver_id': items.id,
                    'vehicle_make': items.make,
                    'vehicle_driver_id': items.driver_id,
                    'vehicle_model': items.model,
                    'vehicle_plate_number': items.plate_number,
                    'vehicle_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    'vehicle_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                })

                return jsonify('Updated vehicle: ', result)

        except :

            return jsonify('There was a problem updating vehicles')

    else:
        print('Incorrect id or params')
        pass


@app.route('/vehicles/set_driver/<vehicle_id>/', methods=['POST', 'GET'])
def set_driver(vehicle_id):
    """
    Function responsible for placing the driver in the car

     /vehicles/set_driver/<vehicle_id>/?driver_id=driver_id
     /vehicles/set_driver/1/?driver_id=1
     """

    driver_id = request.args.get('driver_id')

    result = []

    updated_vehicle = Vehicle.query.filter_by(id=vehicle_id)

    for items in updated_vehicle:

        if items.driver_id is None:

            if driver_id and vehicle_id is not None:
                updated_vehicle = Vehicle.query.filter_by(id=vehicle_id).update(dict(driver_id=driver_id))

            db.session.commit()

        else:

            if driver_id and vehicle_id is not None:
                updated_vehicle = Vehicle.query.filter_by(id=vehicle_id).update(dict(driver_id=None))

            db.session.commit()

        result.append({
            'id': items.id,
            'vehicle_make': items.make,
            'vehicle_driver_id': items.driver_id,
            'vehicle_model': items.model,
            'vehicle_plate_number': items.plate_number,
            'vehicle_created_at': items.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            'vehicle_updated_at': items.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
        })

        return jsonify(result)


@app.route('/vehicles/vehicle/<vehicle_id>/', methods=['GET'])
def delete_vehicles(vehicle_id):
    """
     A function that removes drivers by id

     /vehicles/vehicle/<vehicle_id>/
     """
    if vehicle_id is not None:

        if vehicle_id == [items.id for items in vehicle_items]:
            return 'The vehicle is not exits'

        else:

            vehicle_id_int = int(vehicle_id)

            for items in vehicle_items:

                if vehicle_id_int == items.id:
                    vehicle = Vehicle.query.filter_by(id=vehicle_id_int).first()
                    db.session.delete(vehicle)
                    db.session.commit()
                    return jsonify(f'The vehicle with id {vehicle_id_int} was deleted')


Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
