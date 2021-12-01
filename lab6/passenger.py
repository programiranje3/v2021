"""
LAB 6, class Passenger
"""

"""
Create the FlightService enumeration that defines the following items (services):
snack, refreshments, meal, priority boarding, onboard wifi, onboard media, 
and an item for cases when services are not specified.
"""




"""
Modify the Passenger class from Lab5 as follows:

In addition to the existing attributes, the class should also have the following attributes:
- airfare - the price the passenger has paid for the flight
- checked_in - a boolean indicator, true if the passenger has checked in 
- services - the attribute represents a list of flight services available to the passenger; 
  these services should be defined as elements of the FlightService enumeration.

The following methods of the Passenger class need to be revised:

- constructor (__init__()) - it should receive 5 input arguments, one for each attribute except the 
  *airfare* and *services* attributes. The arguments for the passenger's name, country, and passport 
  have to be specified; the arguments for *checked_in* and *is_COVID_safe* are False by default. 
  The *services* attribute should be initialised to an empty list, whereas *airfare* should be 
  defined as private and set to None.

- a method that returns a string representation of a given Passenger object (__str__()) so that it describes 
  a passenger with the extended set of attributes.

Finally, the following new methods should be added:

- get and set methods (using appropriate decorators) for the *airfare* attribute; the set method: 
  i) should assure that a non-negative integer value is assigned to this attribute, and 
  ii) should be able to handle both float and string value as the input argument

- get and set methods (using appropriate decorators) for the *checked_in* attribute; the attribute 
  should be made private; the set method should assure that a passenger can check in only if they are COVID safe
"""



"""
Create the EconomyPassenger class that extends the Passenger class and has:

- method add_service_selection that receives a dictionary where keys are services the passenger has bought
  while values are the prices paid for those services. The services should be added to the passenger's 
  *services* list, while the prices should be used to increase the value of the *airfare* attribute, BUT this
  should be done only if the passenger has paid the airfare.
  The method should also print a report about the added services and the resulting increase in the airfare. 
  Note: keys in the input dictionary are expected to be elements of the FlightService enumeration.  

- overridden __str__ method so that it first prints "Economy class passenger" and then the available information 
  about the passenger
"""




"""
Create class BusinessPassenger that extends the Passenger class and has:

- the constructor (__init__()) that receives the same arguments as the constructor of the upper class
  plus a list of services to be assigned to the *services* attribute. This additional argument should be 
  a tuple of either strings (service names) or elements of the FlightService enumeration; its default value
  is FlightService.unspecified. The method should check the validity of the tuple elements before adding 
  them to the *services* attribute. 
  Important: the constructor should be written in a way that makes the class ready for multiple inheritance.

- overridden __str__ method so that it first prints "Business class passenger" and then 
  the available information about the passengers

"""



if __name__ == '__main__':

    pass

    # jim = EconomyPassenger("Jim Jonas", 'UK', '123456', is_covid_safe=True)
    # print(jim)
    # print()
    #
    # # Try adding extra services to Jim
    # extra_services = {
    #     FlightService.refreshments: 10,
    #     FlightService.onboard_media: 15
    # }
    # jim.add_service_selection(extra_services)
    #
    # jim.airfare = 450
    # jim.add_service_selection(extra_services)
    #
    # bob = EconomyPassenger("Bob Jones", 'Denmark', '987654', checked_in=True)
    # print(bob)
    # print()
    #
    # mike = BusinessPassenger(name="Mike Stone", country="USA",
    #                          passport='234567', is_covid_safe=True,
    #                          services=(FlightService.priority_boarding, FlightService.onboard_wifi))
    # print(mike)
    # print()
    # print(mike.__dict__)
    #
    # brian = BusinessPassenger(name="Brian Brown", country="UK",
    #                           passport='546234', is_covid_safe=True,
    #                           services=("priority_boarding", "onboard media", "drinks"))
    # print(brian)
