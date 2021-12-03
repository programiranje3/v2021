"""
Auxiliary file for Lab 6
"""

"""
instances of the FlightService enum
"""
    # snack = 'snack'
    # refreshments = 'refreshments'
    # meal = 'meal'
    # priority_boarding = 'priority boarding'
    # onboard_wifi = 'onboard wifi'
    # onboard_media = 'onboard media'
    # unspecificed = 'unspecified'


"""
__str__ for the Passenger class
"""


# def __str__(self):
#     passenger_str = f"{self.name}\n\tcountry: {self.country}\n\tpassport number: " \
#                     f"{self.__passport if self.__passport else 'unknown'}\n"
#     passenger_str += f"\tCOVID status: {'valid' if self.is_COVID_safe else 'invalid'}\n"
#     passenger_str += f"\tcheck in status: {'done' if self.checked_in else 'not yet'}\n"
#     passenger_str += f"\tairfare: {self.airfare if self.airfare else 'not paid yet'}\n"
#     passenger_str += f"\textra services: {self.get_services_as_str()}"
#     return passenger_str


"""
# __str__ for the Flight class
"""

# def __str__(self):
#     flight_str = f"Data about flight {self.flight_num}:\n"
#     flight_str += f"\tdeparture date and time: " \
#                   f"{datetime.strftime(self.departure, self.departure_format) if self.departure else 'unknown'}\n"
#
#     if self.route:
#         origin, dest = self.route
#         flight_str += f"\troute: {origin} -> {dest}\n"
#     if self.operated_by:
#         flight_str += f"\tflight operator: {self.operated_by}\n"
#     if len(self.passengers) == 0:
#         flight_str += "\tpasengers: none yet"
#     else:
#         flight_str += "\tpassengers:\n\t" + "\t".join([str(p) + "\n" for p in self.passengers])
#     return flight_str