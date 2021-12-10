"""
LAB 6, class Flight
"""

"""
Modify the Flight class from Lab5 as follows:

In addition to the flight_num, departure, and passengers attributes, the class should also have 
the following attributes:
- route - the route of the flight as a tuple of the form (origin, destination)
- operated_by - the company that operates the flight

The following methods of the Flight class need to be revised:

- the constructor (__init__()) - it should receive 4 input arguments for the *flight number*, *departure*,
  *route*, and *operated_by* attributes; the arguments for the *route* and *operator* arguments have default 
  value None; the *passengers* attribute should be initialised to an empty list

- the set method for the *departure* attribute, so that it properly handles situations when departure date 
  and time are given as a string in an unknown format (that is, in the format other than the *departure_format*)

- the add_passenger() method for adding a passenger to the flight; in addition to receiving the passenger to 
  be added, the method also receives an argument for the airfare to be paid by the passenger. The method adds 
  the new passenger to the *passengers* list if they are not already in the list. If successfully added, the 
  value of the 2nd argument is assigned to the passenger's airfare attribute.  
  Note: checking for valid COVID permit is now moved to check-in. 

- the method that returns a string representation of the given Flight object (__str__()) so that it describes 
  the flight with the extended set of attributes

Furthermore, the following new methods should be added:

- get and set methods (using appropriate decorators) for the *route* attribute; the set method
  should allow for different ways of setting the route, that is, it should be able to handle input 
  value given as a list or a tuple (of two elements) or a string with the origin and destination 
  separated by a comma (Belgrade, Rome), a hyphen (Belgrade - Rome), or a '>' char (Belgrade > Roma)
  (Hint: consider using split method from the re (regular expressions) module)

- class method from_dict() for creating a Flight object (alternative constructor) out of the flight-related 
  data provided as a dictionary with the following keys: fl_num, origin, destination, departure, operator. 
  Consider that the input value might not contain the expected dictionary elements, that is,
  dictionary keys might not match the expected ones.

- a generator method that generates a sequence of passengers who have not yet checked in; at the end - after 
  yielding all those who haven't checked in yet - the method prints the number of such passengers.

- a generator method that generates a sequence of candidate passengers for an upgrade to the business class; 
  those are the passengers of the economy class whose airfare exceed the given threshold (input parameter) 
  and who have checked in for the flight; the generated sequence should consider the passengers airfare, 
  so that those who paid more are prioritised for the upgrade option.

"""

from datetime import datetime
from sys import stderr
import re
from lab6.passenger import Passenger, EconomyPassenger, BusinessPassenger

class Flight:

    departure_format = "%Y-%m-%d %H:%M"

    def __init__(self, flight_num, departure, route=None, operator=None):
        self.flight_num = flight_num
        self.departure = departure
        self.passengers = list()
        self.route = route
        self.operated_by = operator


    @property
    def departure(self):
        return self.__departure

    @departure.setter
    def departure(self, value):
        if isinstance(value, datetime):
            if value > datetime.now():
                self.__departure = value
                return
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, self.departure_format)
                if value and value > datetime.now():
                    self.__departure = value
                    return
            except ValueError as err:
                stderr.write(f"{err}\n")
                stderr.write(f"The departure should be given in {Flight.departure_format} format\n")

        stderr.write(f"Incorrect value for the departure attribute\n")
        self.__departure = None

    @property
    def route(self):
        return self.__route

    @route.setter
    def route(self, value):
        if isinstance(value, (tuple, list)) and len(value) == 2:
            self.__route = value
            return
        elif isinstance(value, str):
            parts = re.split('[,->]', value)
            if len(parts) == 2:
                orig, dest = parts
                self.__route = orig.strip(), dest.strip()
                return

        stderr.write("Error while setting route\n")
        self.__route = None


    def add_passenger(self, p, price):
        if not isinstance(p, Passenger):
            print(f"Error! Wrong input: expected a Passenger object, got {type(p)} object")
            return
        if (p not in self.passengers):
            self.passengers.append(p)
            p.airfare = price
            print(f"Successfully added: {p.name}")
        else:
            print(f"Error, passenger {p.name} could not be added, since the passenger is already "
                  f"in the passengers list")

    def __str__(self):
        flight_str = f"Data about flight {self.flight_num}:\n"
        flight_str += f"\tdeparture date and time: " \
                      f"{datetime.strftime(self.departure, self.departure_format) if self.departure else 'unknown'}\n"

        if self.route:
            origin, dest = self.route
            flight_str += f"\troute: {origin} -> {dest}\n"
        if self.operated_by:
            flight_str += f"\tflight operator: {self.operated_by}\n"
        if len(self.passengers) == 0:
            flight_str += "\tpasengers: none yet"
        else:
            flight_str += "\tpassengers:\n\t" + "\t".join([str(p) + "\n" for p in self.passengers])
        return flight_str

    def time_till_departure(self):
        if self.departure:
            time_left = self.departure - datetime.now()
            hours_left, rest_sec = divmod(time_left.seconds, 3600)
            mins_left, rest_sec = divmod(rest_sec, 60)
            return time_left.days, hours_left, mins_left

        print("Departure time is still unknown")
        return None


    def __iter__(self):
        self.__iter_counter = 0
        return self

    def __next__(self):
        if self.__iter_counter == len(self.passengers):
            raise StopIteration
        next_passenger = self.passengers[self.__iter_counter]
        self.__iter_counter += 1
        return next_passenger


    @classmethod
    def from_dict(cls, flight_dict):

        def value_or_None(key):
            return flight_dict[key] if key in flight_dict.keys() else None

        try:
            return cls(flight_dict['fl_num'], flight_dict['departure'],
                       (flight_dict['origin'], flight_dict['destination']),
                       flight_dict['operator'])
        except KeyError as err:
            stderr.write(f"Error due to invalid input value - expected:\n{err}\n")
            stderr.write("Will create a flight object with available valid data\n")

            return cls(value_or_None('fl_num'), value_or_None('departure'),
                       (value_or_None('origin'), value_or_None('destination')),
                       value_or_None('operator'))

    def not_checkedin_generator(self):
        not_checkedin_cnt = 0
        for p in self.passengers:
            if not p.checked_in:
                yield p
                not_checkedin_cnt += 1
        print(f"Flight {self.flight_num} waiting for {not_checkedin_cnt} passengers to check in")

    def candidates_for_upgrade_generator(self, threshold):
        candidates = list()
        for p in self.passengers:
            if isinstance(p, EconomyPassenger) and p.airfare > threshold and p.checked_in:
                candidates.append(p)
        for candidate in sorted(candidates, key=lambda c: c.airfare, reverse=True):
            yield candidate


if __name__ == '__main__':

    lh1411 = Flight('LH1411', '2022-03-20 6:50', ('Belgrade', 'Munich'))
    print(lh1411)
    print()

    lh992 = Flight('LH992', '2022-02-25 12:20', 'Belgrade -> Frankfurt', 'Lufthansa')
    print(lh992)
    print()

    lh1514_dict = {'fl_num':'lh1514',
                   'departure': '2021-12-30 16:30',
                   'operator': 'Lufthansa',
                   'origin': 'Paris',
                   'destination': 'Berlin'}

    lh1514 = Flight.from_dict(lh1514_dict)
    print(lh1514)
    print()


    jim = EconomyPassenger("Jim Jonas", 'UK', '123456')
    bill = EconomyPassenger("Billy Stone", 'USA', "917253", is_covid_safe=True)
    dona = EconomyPassenger("Dona Stone", 'Australia', "917251", is_covid_safe=True)
    kate = BusinessPassenger(name="Kate Fox", country='Canada', passport="114252", is_covid_safe=True)
    bob = BusinessPassenger(name="Bob Smith", country='UK', passport="123456", checked_in=True)

    passengers = [jim, bill, dona, kate, bob]
    airfares = [450, 950, 1500, 1000, 475]
    for p, fare  in zip(passengers, airfares):
        lh992.add_passenger(p, fare)

    print(f"\nAfter adding passengers to flight {lh992.flight_num}:\n")
    print(lh992)
    print()

    print("Last call to passengers who have not yet checked in!")
    for passenger in lh992.not_checkedin_generator():
        print(passenger)

    # check in some economy class passengers to be able to test the next method
    dona.checked_in = True
    bill.checked_in = True

    print()
    print("Passengers offered an upgrade opportunity:")
    for ind, passenger in enumerate(lh992.candidates_for_upgrade_generator(500)):
        print(f"{ind+1}. {passenger}")

    print()
    print("Candidates for upgrade to business class:")
    g = lh992.candidates_for_upgrade_generator(500)
    try:
        while True:
            print(next(g))
    except StopIteration:
        print("--- end of candidates list ---")