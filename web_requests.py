from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
from pprint import pprint


class GetPage:
    """
    General Class used for parsing html sites

    """

    def __init__(self, url):
        """
       Init instance variables

       Args:
           testcase_name(url) : string
           testcase_id(soup): Beatifulsoup object
           link_list(list): provide links from the parsed html
        """
        self.url = url
        self.soup = None
        self.link_list = []

    def simple_get(self):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(get(self.url, stream=True)) as resp:
                if self.is_good_response(resp):
                    self.soup = BeautifulSoup(resp.content, "html.parser")
        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(self.url, str(e)))
            self.soup = None

    def is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)


    def log_error(self, e):
        """
        It is always a good idea to log errors.
        This function just prints them, but you can
        make it do anything.
        """
        print(e)

    def extract_link(self):
        """
        Extract link from given Beautfilsoup object.

        Args:
           soup(class 'bs4.BeautifulSoup) : parsed bs html

        Returns:
            list: list of links

        Example:
            >>> soup = BeautifulSoup(raw_data)
            >>> extract_link(soup)
        """
        for link in self.soup.findAll('a', attrs={'href': re.compile("^https://")}):
            self.link_list.append(link.get('href'))
        return self.link_list

    def filter_links(self, words):
        """
        Find and returns the links what contains the given word

        Args:
            link_list (list): list of url links
            words (list): a word to looking for

        Returns:
            list: list of filtered links

        Example:
            >>> filter_links(link_list,['money'])
            >>> filter_links(link_list,['money','life'])
        """
        filtered_link_list = []
        for link in self.link_list:
            for word in words:
                if word in link and link not in filtered_link_list:
                    filtered_link_list.append(link)
        return filtered_link_list


