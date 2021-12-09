"""
LAB 7
"""

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



if __name__ == "__main__":

    pass

    # Task 1:
    # read_sort_write(get_data_dir() / 'file_names_sample.txt')

    # Task 2:
    # process_city_data(get_data_dir() / "cities_and_times.txt")
    #
    # with open(get_results_dir() / 'task2_cities_and_times.pkl', 'rb') as fpkl:
    #     for data_item in pickle.load(fpkl):
    #         print(data_item)

    # with open(get_results_dir() / "task2_cities_and_times.csv") as fobj:
    #     data_as_dict_list = csv.DictReader(fobj, delimiter=';')
    #     for data_dict in data_as_dict_list:
    #         city, wday, t = data_dict.values()
    #         print(f"{city}, {wday}, {t}")


    # Task 3:
    # process_image_files(get_data_dir() / "image_files_for_training.txt")

    # with open(get_results_dir() / 'task3_image_category_data.csv', 'r') as csv_fobj:
    #     categories_data = csv.DictReader(csv_fobj)
    #     for category_data in categories_data:
    #         category, img_count = category_data.values()
    #         print(f"{category}: {img_count}")

    # with open(get_results_dir() / 'task3_image_category_data.json', 'r') as fobj:
    #     loaded_data = json.load(fobj)
    #     for cat, img_list in loaded_data.items():
    #         print(f"{cat}: " + ";".join(img_list))


    # Task 4:
    # t4_f1 = get_data_dir() / "prime_numbers.txt"
    # t4_f2 = get_data_dir() / "happy_numbers.txt"
    # identify_shared_numbers(t4_f1, t4_f2)
    #
    # with open(get_results_dir() / 'task4_shared_numbers.json', 'r') as fobj:
    #     loaded_data = json.load(fobj)
    #     print(", ".join((str(num) for num in loaded_data)))