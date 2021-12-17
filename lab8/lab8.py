"""
LAB 8
"""

"""
The task is to write a Python program (script) that determines which countries
gave large number of athletes that are considered to be among the 100 greatest
sport stars ever.
To that end, the program should do the following:
- collect names of the "100 Greatest Sport Stars Ever" from:
  https://ivansmith.co.uk/?page_id=475
- for each athlete, determine the country of birth by scraping relevant
  data (birthplace) from their Wikipedia page
- stores the data about athletes and their country of origin in a json file
- prints a sorted list of identified countries and for each country, the number
  of greatest athletes it gave

Note: to retrieve web page content, we will use the *requests* library
Quick start guide is available at: https://requests.readthedocs.io/en/master/user/quickstart/

Documentation for BeautifulSoup is available at:
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

"""

import json
import requests
from sys import stderr
from bs4 import BeautifulSoup
from pathlib import Path

RESULTS_JSON = "athletes_origin.json"

def get_content_from_url(url):
    """
    Returns the content of the web page with the given URL or None
    if the page content cannot be retrieved
    Note: in case the request generates the 406 status code, follow the instructions laid out
    in this post: https://stackoverflow.com/questions/56101612/python-requests-http-response-406
    :param url: url of the page
    :return: content of the page as string or None
    """

    def response_OK():
        # print(response.status_code)
        return response.status_code == requests.codes.ok and \
               response.headers['content-type'] and \
               'html' in response.headers['content-type']

    try:
        with requests.get(url, headers={"User-Agent": "P3_FON"}) as response:
            return response.text if response_OK() else None
    except requests.RequestException as err:
        stderr.write(f"The following error occurred while trying to get content from: {url}:\n{err}\n")
        return None


def scrape_athletes_names(url):
    """
    Retrieves the web page with a list of top athletes,
    extracts athletes' names and returns a list of those names
    :param url: url of the page to scrape data from
    :return: a list of athletes' names
    """

    athletes_names = list()

    page_content = get_content_from_url(url)
    if not page_content:
        stderr.write(f"Could not retrieve content from: {url}\n")
        return athletes_names

    page_soup = BeautifulSoup(page_content, features='html.parser')
    if not page_soup:
        stderr.write(f"Could not parse content from: {url}\n")
        return athletes_names

    div_element = page_soup.find('div', {'id':'content'})
    for li in div_element.find('ol').find_all('li'):
        name = li.find('strong').text
        if name:
            athletes_names.append(name.strip())

    return athletes_names


def to_json(fpath, data):
    """
    Auxiiary function for storing the collected data
    :param fpath: path to the file where data will be stored
    :param data: data to store
    :return: nothing
    """
    try:
        with open(fpath, 'w') as fobj:
            json.dump(data, fobj, indent=4)
    except OSError as err:
        stderr.write(f"An error occurred while writing athletes' data to file:\n{err}\n")



def get_athletes_names(url):
    """
    The function, first, tries to load the data (athletes' names) from a local file;
    if the file does not exist (= data was not collected yet), it collects the
    data by calling the scrape_athletes_names() f. and stores the collected data
    for potential later use; the data is also returned as a list of athletes' names
    :param url: url of the page to scrape data from
    :return: a list of athletes' names
    """

    data_file = Path.cwd() / 'athletes_names.json'
    try:
        with open(data_file, 'r') as fobj:
            return json.load(fobj)
    except FileNotFoundError:
        stderr.write("Athletes names have not been collected yet. Will be done now!\n")
    except OSError as err:
        stderr.write(f"An error occurred while reading athletes' names from file:\n{err}\n")
        stderr.write("Collecting athletes' names will be done again\n")

    athletes_names = scrape_athletes_names(url)

    if len(athletes_names) == 0:
        raise RuntimeError("Athletes' names not available - cannot proceed!")

    to_json(data_file, athletes_names)

    return athletes_names


def get_country_from_str(country_string):
    complete_string = "".join([s for s in country_string])
    if ',' in complete_string:
        _, country = complete_string.rsplit(',', maxsplit=1)
    else:
        _, country = complete_string.rsplit(maxsplit=1)

    if country:
        import re
        return re.sub('\[\d+\]', "", country).lstrip().rstrip(')')

    return None


def retrieve_country_of_origin(name):
    """
    Receives the full name of an athlete.
    Returns the country of birth of the athlete extracted from their
    Wikipedia page or None if the information is not available.
    :param name: name of an athlete
    :return: country of birth (string) or None
    """

    print(f"Collecting data for {name}")

    page_url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"

    page_content = get_content_from_url(page_url)
    if not page_content:
        stderr.write(f"Could not retrieve page for: {name}\n")
        return None

    page_soup = BeautifulSoup(page_content, features='html.parser')
    if not page_soup:
        stderr.write(f"Could not parse page for: {name}\n")
        return None

    info_box = page_soup.find('table', class_=lambda c: c and 'infobox' in c and 'vcard' in c)
    if not info_box:
        if page_soup.find('div', {'id':'disambigbox'}):
            stderr.write(f"Arrived at disambiguation page for: {name}\n")
        else:
            stderr.write(f"No infobox data for: {name}\n")
        return None

    th_born = info_box.find('th', text=lambda t: t and ('born' in t.lower() or 'place of birth' in t.lower()))
    if th_born:
        td_born = th_born.find_next_sibling('td')
        if td_born and td_born.stripped_strings:
            return get_country_from_str(td_born.stripped_strings)
    else:
        bold_born = info_box.find(lambda b: b.name=='b' and b.parent.name=='td' and b.text and 'born' in b.text.lower())
        if bold_born and bold_born.parent.stripped_strings:
            return get_country_from_str(bold_born.parent.stripped_strings)

    return None


def collect_athletes_data(athletes_url):
    """
    The function puts several parts together:
    - obtains a list of athletes' names
    - iterates over the list of names to retrieve the country for each
    athlete by 'consulting' their Wikipedia page
    - stores the collected data in a json file
    - prints names of athletes whose birthplace data could not have been collected
    :param athletes_url: url of the web page with athletes data
    :return: dictionary with atheletes names (as keys) and origin (as values)
    """

    print("Getting a list of athletes' names...")
    athletes_names = get_athletes_names(athletes_url)
    print('...done')

    print(f'Gathered names for {len(athletes_names)} athletes.')

    print("\nCollecting data about the athletes' country of origin...")
    athletes_dict = dict()
    not_found = list()
    for name in athletes_names:
        country = retrieve_country_of_origin(name)
        if country:
            athletes_dict[name] = country
        else:
            not_found.append(name)
    print('...done')

    for athlete, origin in athletes_dict.items():
        print(f"{athlete}: {origin}")

    to_json(Path.cwd() / RESULTS_JSON, athletes_dict)

    print(f"\nInformation about country of origin was not found for the following {len(not_found)} athletes:")
    print(", ".join(not_found))

    return athletes_dict


def create_country_labels_mapping():
    """
    Creates a mapping between a country and different ways it was referred to
    in the collected data
    :return: a dictionary with countries as the keys and the different terms used
    to refer to them as values
    """

    country_lbls_dict = dict()

    country_lbls_dict['USA'] = ['California', 'New York', 'United States', 'Florida', 'Oklahoma', 'US', 'U.S.',
                                'Pennsylvania', 'Ohio', 'Mississippi', 'Alabama', 'Indian Territory', 'Maryland']
    country_lbls_dict['Germany'] = ['West Germany']
    country_lbls_dict['Australia'] = ['Victoria', 'Western Australia', 'New South Wales']
    country_lbls_dict['UK'] = ['England', 'UK', 'British Leeward Islands', 'United Kingdom']

    return country_lbls_dict



def most_represented_countries(athletes_dict):
    """
    Creates and prints a list of countries based on how well they
    are represented in the collected athletes data
    :return: nothing
    """

    country_lbls_dict = create_country_labels_mapping()
    for athlete, country in athletes_dict.items():
        for c_name, c_labels in country_lbls_dict.items():
            if country in c_labels:
                athletes_dict[athlete] = c_name
                break

    from collections import defaultdict
    country_counts = defaultdict(int)
    for athlete, country in athletes_dict.items():
        country_counts[country] += 1

    print("Number of top athletes per country of origin:")
    for country, cnt in sorted(country_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"{country}: {cnt}")





if __name__ == '__main__':

    top_athletes_url = 'https://ivansmith.co.uk/?page_id=475'
    try:
        athletes_data = collect_athletes_data(top_athletes_url)
        most_represented_countries(athletes_data)
    except RuntimeError as err:
        stderr.write(f"Terminating the program due to the following runtime error:\n{err}")
