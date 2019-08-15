import pandas


# Maak een class voor vehicles
class Vehicle(object):
    # Initializer
    def __init__(self, vehicle_type, base_cost, fuel_cost, mileage, model, available):
        self.vehicle_type = vehicle_type
        self.base_cost    = base_cost
        self.fuel_cost    = fuel_cost
        self.mileage      = mileage
        self.model        = model 
        self.available    = available

    def info(self):
        print "Information about %s" % self.vehicle_type
        print "Model: \t\t", self.model
        print "Base cost: \t", self.base_cost
        print "Available:\t", self.available

    def calculate_price(self):
        pass

    def rent(self):
        hours_rent = raw_input("For how many hours would you like to "\
                         + "rent this " + self.vehicle_type + "?")


# Nettere oplossing: laat alle subclasses inheriten van Vehicle. Cost function per child class 

# Load vehicles from csv file to get current inventory
def load_vehicles(path):

    # Create list to store our current inventory
    inventory = []
    # Read CSV using pandas
    vehicles = pandas.read_csv(path, converters = {
                "Type"     : str, 
                "Model"    : str, 
                "Base_cost": int, 
                "Fuel_cost": int, 
                "Mileage"  : int,
                "Available": bool })
    
    # Create objects based on database
    for _, data in vehicles.iterrows():
        print data["Type"]
        print data["Available"]
        print type(data["Available"])
        inventory.append(Vehicle(data["Type"],
            data["Base_cost"], 
            data["Fuel_cost"],
            data["Mileage"],
            data["Model"],
            data["Available"]))

    return inventory

def rent_vehicle(model, vehicle_type, current_inventory):
    print "You would like to rent the ", model, vehicle_type
    
    # Get user input
    number_to_rent = raw_input("How many " + model + " " \
                     + vehicle_type.lower() +"s would you like to rent? " )

    print "Checking availability..."
    (available, count) = check_availability(model, vehicle_type, number_to_rent)
    if not available:
        print "I'm sorry, that vehicle is not available at this time. We have " +\
              str(count) + " " + model + " " + vehicle_type + "(s) available."
    else:
        pass
        # Calculate cost (different per vehicle)
        # Update database


def check_availability(model, vehicle_type, count):
    # in your current inventory
    return True


def parse_user_input():
    user_input = raw_input("What kind of vehicle would you like to rent?\n" +
                     "Our options: Car (1), Motor boat (2), Bicycle (3).\n" +
                     "Please type the corresponding number: ")
    if user_input == '1':
        print "We have two types of cars, the Tesla model S and the Opel Zafira."
        car_choice = raw_input("For more information on the Tesla model S, type (1): \n" +
                               "For more information on the Opel Zafira, type (2): ")
        if car_choice == '1':
            return "Tesla model S", "car"
        elif car_choice == '2':
            return "Opel Zafira", "car"
        else:
            return "NAN", "NAN"
    elif user_input == 2:
        return "NAN", "NAN"
    elif user_input == 3:
        return "NAN", "NAN"
    else:
        print "This option is not available. Please pick one of the three options."
    return "NAN", "NAN"    

def rent_o_matic(vehicles):
    print "Welcome to Rent-O-Matic, the most convenient way to rent your vehicles!"
    while True:
        model, vehicle_type = parse_user_input()
        rented, vehicles = rent_vehicle(model, vehicle_type, vehicles)
        print "Thank you for your patronage. Please come again!\n\n"

if __name__ == "__main__":
    database_path = "database/vehicle_db.csv"
    current_inventory = load_vehicles(database_path)
    # print current_inventory
    # for veh in current_inventory:
    #     print veh.info()
    
    rent_o_matic(current_inventory)