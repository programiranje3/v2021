"""
LAB 5, class Passenger
"""

"""
Create the Passenger class with the following methods:

- a constructor (__init__()) that receives four input arguments that are used to 
  initialise the following 4 attributes:
     - name - the passenger's name and surname
     - country - the passanger's country of origin
     - passport - the passenger's passport number
     - is_covid_safe - a boolean indicator variable; it is true if the passenger is vaccinated 
     or has recently been tested negative; the default value of this argument is False

- get and set methods for the *passport* attribute (using appropriate decorators);
  designate this attribute as private and assure that it is a string of length 6,
  consisting of digits only

- a method that sets *is_COVID_safe* based on the value of its input parameters: 
  - evidence type: a string that should be either 'vaccinated' or 'tested_negative'
  - evidence date: the date of vaccination / PCR test; if given as a string, it is 
  expected to be in the following format: %d/%m/%Y
  The method sets *is_COVID_safe* to True if:
  - the vaccination was within the last 6 months OR
  - the negative test is not older than 3 days    
  Note: for datetime formatting codes, check this table:
  https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

- class method covid_free_Aussie_passenger for creating a passenger from Australia who is COVID safe
  (alternative constructor); the method receives the passenger's name and passport number.

- a method that returns a string representation of a Passenger object (__str__())

- a method that checks for equality of the given Passenger object and another object
  that is passed to the method as its input parameter (__eq__()); two passenger objects
  are considered the same if they are citizens of the same country and have the same passport number
"""


if __name__ == '__main__':

    pass

    # bob = Passenger("Bob Smith", "Serbia", "123456", True)
    # john = Passenger("John Smith", "Spain", 987656, True)
    # jane = Passenger("Jane Smith", "Italy", "987659")
    # mike = Passenger.covid_free_Aussie_passenger("Mike Brown", "123654")
    #
    # print("PASSENGERS DATA:\n")
    # print(bob)
    # print(john)
    # print(jane)
    # print(mike)
    #
    # print()
    # print("Checking if 'bob' and 'john' refer to the same passenger")
    # print(bob == john)
    #
    # print("\nPASSENGERS DATA AFTER CHECKING COVID PERMITS:\n")
    # jane.update_covid_safe('vaccinated', '12/11/2021')
    # print(jane)
    #
    # bob.update_covid_safe('tested_negative', '10/11/2021')
    # print(bob)

