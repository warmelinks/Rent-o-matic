from time import sleep
from os import system
import pandas

class Vehicle(object):
    def __init__(self, id_num, type_name, model, 
                 base_cost, fuel_cost, 
                 mileage, available, description):
        self.id_num      = id_num
        self.type_name   = type_name
        self.model       = model
        self.base_cost   = base_cost
        self.fuel_cost   = fuel_cost
        self.mileage     = mileage
        self.available   = available
        self.description = description

    def info(self):
        print "Info about the " + self.model + " " + self.type_name + " (ID: " + str(self.id_num) + "):"
        print "Cost: E" + str(self.base_cost) +",- + E" + \
        str(self.fuel_cost) + ",- per hour after the first two hours."
        print "Available: ", "Yes" if self.available else "No", "\n" 

    def calculate_rental_cost(self, hours):
        return self.base_cost + max(0, self.fuel_cost * (hours - 2))

def get_available(vehicles, model):
    count = 0
    for vehicle in vehicles:
        if vehicle.model == model and vehicle.available:
               count += 1
    return count

def provide_change(cost, payment):
    print "You are paying with", str(payment), \
          "and the total cost is", str(cost)
    change = payment - cost
    coins  = []
    euro_options = [500, 200, 100, 50, 20, 10, 5, 2, 1]
    
    if change < 0:
        print "You did not provide enough payment."
        sleep(2)
        return False
    else:
        while change > 0:
            for option in euro_options:
                if change - option >= 0:
                    coins.append(option)
                    change -= option
                    break
    
    print "Your change is as follows:", coins
    print "Press [ENTER] to return."
    raw_input(">> ")
    return True


def parse_input(vehicles):
    while True:
        print_header()
        print "What would you like to do?"
        print "(1): View all vehicles."
        print "(2): View more info on a specific Vehicle."
        print "(3): Rent a vehicle."
        print "(4): Return a rented vehicle."
        print "(9): Help"

        menu_dict = {
            '1' : 'Tesla S',
            '2' : 'Opel Zafira',
            '3' : 'Lagoon 40',
            '4' : 'Gazelle'
        }

        user_input = raw_input(">> ")
        if user_input == '1':
            view_all_vehicles(vehicles)
        elif user_input == '2':
            view_specific_vehicle(vehicles, menu_dict)
        elif user_input == '3':
            rent_vehicle_menu(vehicles, menu_dict)
        elif user_input == '4':
            return_vehicle(vehicles)
        elif user_input == '9':
            print_help()
        else:
            print "Please input either (1), (2), (3), (4), or (9)"
            sleep(2)

def view_all_vehicles(vehicles):
    print_header()
    for vehicle in vehicles:
        vehicle.info()
    raw_input("Press [ENTER] to continue.")

def print_vehicle(vehicles, model):
    for vehicle in vehicles:
        if vehicle.model == model:
            print_header()
            vehicle.info()
            print "----------------"
            print vehicle.description
            print "----------------"
            raw_input("Press [ENTER] to continue.")
            return

def print_vehicle_options():
    print "(1) [CAR]\tThe Tesla model S."
    print "(2) [CAR]\tThe Opel Zafira."
    print "(3) [BOAT]\tThe Lagoon 40."
    print "(4) [BICYCLE]\tThe Gazelle."
    print "(5) Return." 
    print "(9) Help."

def view_specific_vehicle(vehicles, menu_dict):
    while True:
        print_header()
        print "What vehicle would you like more information on?"
        print_vehicle_options()
        user_input = raw_input(">> ")
        if user_input in menu_dict.keys():
            print_vehicle(vehicles, menu_dict[user_input])
        elif user_input == '5':
            break
        elif user_input == '9':
            print_help()
        else:
            print "Please input either (1), (2), (3), (4), (5), or (9)"
            sleep(2)

def rent_vehicle(vehicles, model):
    while True:
        print_header() 
        print "How many " + model + "s would you like to rent?"
        
        num_rentals = int(raw_input(">> "))
        if num_rentals <= 0:
            print "You can only rent a positive, nonzero number of vehicles."
            sleep(2)
            break
        
        currently_available = get_available(vehicles, model)
        if num_rentals > currently_available:
            print "Not enough rentals available. Currently available:", currently_available
            sleep(2)
            break
        
        print "For how many hours would you like to rent the "+ model +"(s)?"
        num_hours = int(raw_input(">> "))
        total_cost = 0
        for vehicle in vehicles:
            if vehicle.model == model:
                total_cost = num_rentals * vehicle.calculate_rental_cost(num_hours)
                break

        print "Total cost: E" + str(total_cost) + ",-. Please insert money: "
        money_inserted = int(raw_input(">> "))
        if provide_change(total_cost, money_inserted):
            for vehicle in vehicles:
                if vehicle.model == model and vehicle.available: 
                    if num_rentals > 0:
                        vehicle.available = False
                        num_rentals -= 1
                    else:
                        break
            update_database(vehicles)
            break

def rent_vehicle_menu(vehicles, menu_dict):
    while True:
        print_header()
        print "Which vehicle would you like to rent?"
        print_vehicle_options()

        user_input = raw_input(">> ")
        if user_input in menu_dict.keys():
            rent_vehicle(vehicles, menu_dict[user_input])
        elif user_input == '5':
            break
        elif user_input == '9':
            print_help()
        else:
            print "Please input either (1), (2), (3), (4), (5), or (9)"
            sleep(2)

# NYI. Updates database file (CSV)
def update_database(vehicles):
    pass

def return_vehicle(vehicles):
    pass

def print_header():
    system('clear')
    print "Welcome to Rent-o-Matic!"

def print_help():
    print_header()    
    print "This is a generic help message..."
    raw_input("Press [ENTER] to continue.")

def rent_o_matic(vehicles):
    while True:
        print_header()
        print "Please select one of the following: "
        print "(1): Get Started."
        print "(9): Help."

        user_input = raw_input(">> ")
        if user_input == '1':
            parse_input(vehicles)
        elif user_input == '9':
            print_help()
        else:
            print "Please input either (1), or (9)."
            sleep(2)

# Load vehicles from csv file to get current inventory
def load_database(path):
    # Create list to store our current inventory
    inventory = []
    # Read CSV using pandas
    vehicles = pandas.read_csv(path, converters = {
                "ID"         : int,
                "Type"       : str, 
                "Model"      : str, 
                "Base_cost"  : int, 
                "Fuel_cost"  : int, 
                "Mileage"    : int,
                "Available"  : bool, 
                "Description": str })
    
    # Create objects based on database
    for _, data in vehicles.iterrows():
        inventory.append(Vehicle(
            data["ID"],
            data["Type"],
            data["Model"],
            data["Base_cost"], 
            data["Fuel_cost"],
            data["Mileage"],
            data["Available"],
            data["Description"]))
    return inventory

if __name__ == "__main__":
    vehicles = load_database('database/vehicle_db.csv')
    rent_o_matic(vehicles)