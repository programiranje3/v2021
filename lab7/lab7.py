"""
LAB 7
"""

from pathlib import Path
from sys import stderr
from datetime import time
import pickle
import csv
import json

def get_data_dir():
    data_dir = Path.cwd() / 'data'
    if not data_dir.exists(): data_dir.mkdir()
    return data_dir

def get_results_dir():
    results_dir = Path.cwd() / 'results'
    results_dir.mkdir(exist_ok=True)
    return results_dir

"""
TASK 1:

Write the *read_sort_write* function that reads in the content of the given text file,  
sorts it, and writes the (sorted) content to new textual files.
Assume that the content of the given file consists of file names, some of which 
have an extension ('hello.txt'), others do not ('results').
Each file name is given in a separate line.
Sorting should be case insensitive and done in the ascending alphabetical
order, as follows:
- for files with extension: first based on the extension and then based on the file name,
- for files without extension, based on the file name.
After sorting, file names with extension should be writen in one textual file 
(e.g., "task1_files_with_extension.txt") and file names without extension in another text 
file (e.g. "task1_files_no_extension.txt")
Include appropriate try except blocks to prevent program from crushing in case of a non 
existing file, or any other problem occurring while reading from / writing to a file.

To test the function, use the 'data/file_names_sample.txt' file
"""

def write_to_txt_file(data, fname):

    try:
        with open(fname, 'w') as fobj:
            for line in data:
                fobj.write(line + '\n')
    except IOError as err:
        stderr.write(f"An error ocurred while trying to write to file {fname}:\n{err}\n")


def read_sort_write(src_file):

    def sort_order(fname):
        name, ext = fname.split('.', maxsplit=1)
        return ext.lower(), name.lower()

    with_ext = []
    no_ext = []
    try:
        with open(src_file, 'r') as fobj:
            for line in [l.rstrip('\n') for l in fobj.readlines()]:
                if '.' in line:
                    with_ext.append(line)
                else:
                    no_ext.append(line)
    except FileNotFoundError:
        stderr.write(f"The file {src_file}, passed as the input argument, does not exist - cannot proceed\n")
    except OSError as err:
        stderr.write(f"An error ocurred while reading from file {src_file}:\n{err.strerror}\n")
    else:
        no_ext.sort()
        with_ext.sort(key=sort_order)

        write_to_txt_file(no_ext, get_results_dir() / 'task1_files_no_extension.txt')
        write_to_txt_file(with_ext, get_results_dir() / 'task1_files_with_extension')


"""
TASK: 2

The file 'cities_and_times.txt' contains city names and time data.
More precisely, each line contains the name of a city, followed by
abbreviated weekday (e.g. "Sun"), and the time in the form "%H:%M".
Write the 'process_city_data' function that reads in the file and 
creates a time-ordered list of the form:
[('San Francisco', 'Sun', datetime.time(0, 52)),
 ('Las Vegas', 'Sun', datetime.time(0, 52)), ...].
Note that the hour and minute data are used to create an object of
the type datetime.time.
Th function should also:
- serialise the list into a file, as a list object (using the pickle module)
- write the list content into a csv file, in the format:
   city; weekday; time
  where time is represented in the format '%H:%M:%S'
Include appropriate try except blocks to prevent the program from crushing
in the case of a non existing file, or a problem while reading from / writing to 
a file, or transforming data values.

Note: for a list of things that can be pickled, see this page:
https://docs.python.org/3/library/pickle.html#pickle-picklable

Bonus 1: try using named tuple (collections.namedtuple) to represent and
then manipulate the data read from the text file
The following article can help you learn more about named tuples:
https://realpython.com/python-namedtuple/  

Bonus 2: in the "main section" ('__name__ == __main__'), use csv.DictReader
to read in and print the content of the csv file
"""

from collections import namedtuple

CityTime = namedtuple('CityTime', ('name', 'weekday', 'time'))

def process_city_data(src_file):

    def write_to_csv(fname):
        try:
            with open(fname, 'w') as fobj:
                csv_writer = csv.writer(fobj, delimiter = ';')
                # csv_writer.writerow(('city', 'weekday', 'time'))
                csv_writer.writerow(CityTime._fields)
                for item in processed_data:
                    # name, day, city_time = item
                    # csv_writer.writerow((name, day, time.strftime(city_time, '%H:%M:%S')))
                    csv_writer.writerow((item.name, item.weekday, time.strftime(item.time, '%H:%M:%S')))
        except csv.Error as err:
            stderr.write(f"Error while trying to write city data to a csv file:\n{err}\n")

    processed_data = []
    try:
        with open(src_file, 'r') as fobj:
            city_data_list = [l.rstrip('\n') for l in fobj.readlines()]
    except OSError as err:
        stderr.write(f"An error ocurred while trying to read from file '{src_file}':\n{err.strerror}\n")
        stderr.write("Cannot proceed!\n")
    else:
        for city_data in city_data_list:
            city_name, city_day, city_time = city_data.rsplit(maxsplit=2)
            hour, min = city_time.split(':')
            try:
                # processed_data.append((city_name, city_day, time(int(hour), int(min))))
                processed_data.append(CityTime(name=city_name,
                                               weekday=city_day,
                                               time=time(int(hour), int(min))))
            except ValueError as err:
                stderr.write(f"An error occurred while trying to create a time object:\n{err}\n")

        processed_data.sort(key=lambda item: item[2])

        serialise_object_to_file(processed_data, get_results_dir() / 'task2_cities_and_times.pkl')

        write_to_csv(get_results_dir() / 'task2_cities_and_times.csv')


def serialise_object_to_file(obj, fname):

    try:
        with open(fname, 'wb') as fobj:
            pickle.dump(obj, fobj)
    except pickle.PicklingError as err:
        stderr.write(f"An error occurred during serialisation:\n")
        stderr.write(f"{err}\n")
    except OSError as err:
        stderr.write(f"Exception thrown by 'serialise_object_to_file' function:\n{err.strerror}\n")


"""
TASK 3:

In the data folder, there is a text file ('image_files_for_training.txt') that lists 
file paths for a bunch of images (one image file path per line). 
Write the 'process_image_files' function that reads in the content of this text file 
and does the following:
- counts the number of images in each category, and stores the computed
  counts in a csv file in the format: category, image_count
- creates and stores (in a file) a dictionary with the image category as
  the key and a list of image names in the corresponding category as value;
  for storage use 1) pickle and 2) json.
"""

def process_image_files(src_file):

    from collections import defaultdict

    def write_to_csv(fname):

        try:
            with open(fname, 'w') as fobj:
                csv_writer = csv.writer(fobj)
                csv_writer.writerow(('category', 'image_count'))
                for category, img_list in img_dict.items():
                    csv_writer.writerow((category, len(img_list)))
        except csv.Error as err:
            stderr.write(f"Error while writing data to csv file {fname}:\n{err}\n")

    try:
        with open(src_file, 'r') as fobj:
            image_paths = [l.rstrip('\n') for l in fobj.readlines()]
    except OSError as err:
        stderr.write(f"Error whie trying to read from file '{src_file}':\n{err.strerror}\n")
    else:
        img_dict = defaultdict(list)
        for img_path in image_paths:
            rest, img_name = img_path.rsplit("/", maxsplit=1)
            _, img_category = rest.lstrip('/').split('/', maxsplit=1)
            img_category = img_category.replace("/", "_")
            img_dict[img_category].append(img_name)

        write_to_csv(get_results_dir() / 'task3_image_category_data.csv')

        serialise_object_to_file(img_dict, get_results_dir() / 'task3_image_category_data.pkl')

        write_to_json(img_dict, get_results_dir() / 'task3_image_category_data.json')


def write_to_json(obj, fname):
    try:
        with open(fname, 'w') as fobj:
            json.dump(obj, fobj, indent=4)
    except OSError as err:
        stderr.write(f"Error while serialising data to json file {fname}:\n{err}\n")


"""
TASK 4:

Write the 'identify_shared_numbers' function that receives two text files 
with lists of numbers (integers), one number per line. 
The function identifies the numbers present in both lists and 
serialises them to json, as a (new) list of numbers, in a (new) file.

Note: it may happen that not all lines in the input files contain numbers, so,
after reading in the content of the files, assure that only numerical values are
considered for comparison.

To test the function use the files 'happy_numbers.txt' and 'prime_numbers.txt'
available in the 'data' folder.

Note: based on this exercise:
https://www.practicepython.org/exercise/2014/12/14/23-file-overlap.html
"""

def is_number(string):
    return all([ch.isdigit() for ch in string])

def read_numbers_from_file(fname):
    numbers = []
    try:
        with open(fname, 'r') as fobj:
            for line in fobj.readlines():
                line = line.rstrip('\n')
                if is_number(line):
                    numbers.append(int(line))
    except OSError as err:
        stderr.write(f"Error whie trying to read from file '{fname}':\n{err.strerror}\n")

    return numbers

def identify_shared_numbers(f1, f2):

    l1 = read_numbers_from_file(f1)
    l2 = read_numbers_from_file(f2)

    if len(l1) == 0 or len(l2) == 0:
        stderr.write("Cannot complete the task as one of the files has no integer values\n")
        return

    shared = [item for item in l1 if item in l2]
    write_to_json(shared, get_results_dir() / 'task4_shared_numbers.json')



if __name__ == "__main__":

    # Task 1:
    read_sort_write(get_data_dir() / 'file_names_sample.txt')

    # Task 2:
    process_city_data(get_data_dir() / "cities_and_times.txt")

    with open(get_results_dir() / 'task2_cities_and_times.pkl', 'rb') as fpkl:
        for data_item in pickle.load(fpkl):
            print(data_item)
    print()

    with open(get_results_dir() / "task2_cities_and_times.csv") as fobj:
        data_as_dict_list = csv.DictReader(fobj, delimiter=';')
        for data_dict in data_as_dict_list:
            city, wday, t = data_dict.values()
            print(f"{city}, {wday}, {t}")
    print()

    # Task 3:
    process_image_files(get_data_dir() / "image_files_for_training.txt")

    with open(get_results_dir() / 'task3_image_category_data.csv', 'r') as csv_fobj:
        categories_data = csv.DictReader(csv_fobj)
        for category_data in categories_data:
            category, img_count = category_data.values()
            print(f"{category}: {img_count}")
    print()

    with open(get_results_dir() / 'task3_image_category_data.json', 'r') as fobj:
        loaded_data = json.load(fobj)
        for i, item in enumerate(loaded_data.items()):
            cat, img_list = item
            print(f"{i}. {cat.upper()}: " + ";".join(img_list))
    print()

    # Task 4:
    t4_f1 = get_data_dir() / "prime_numbers.txt"
    t4_f2 = get_data_dir() / "happy_numbers.txt"
    identify_shared_numbers(t4_f1, t4_f2)

    print()
    with open(get_results_dir() / 'task4_shared_numbers.json', 'r') as fobj:
        loaded_data = json.load(fobj)
        print(", ".join((str(num) for num in loaded_data)))