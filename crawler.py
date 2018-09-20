"""Basic web crawler application"""
import re
from contextlib import closing
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


class GetPage:
    """
    General Class used for:
        parsing html sites
        extract data
        downloading files
    """

    def __init__(self, url):
        """
       Init instance variables

       Attributes:
           url (string) : 'https://www.example.com'
           soup (obj): Beatifulsoup object
           link_list (list): provide links from the parsed html
        """
        self.url = url
        self.soup = None
        self.link_list = []
        self.simple_get()

    def simple_get(self):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(get(self.url, stream=True)) as resp:
                # pylint: disable=E1101
                if self.is_good_response(resp):
                    self.soup = BeautifulSoup(resp.content, "html.parser")
        except RequestException as error:
            self.log_error('Error during requests to {0} : {1}'.format(self.url, str(error)))
            self.soup = None

    @staticmethod
    def is_good_response(resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    @staticmethod
    def log_error(error):
        """
        It is always a good idea to log errors.
        This function just prints them, but you can
        make it do anything.
        """
        print(error)

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
            self.link_list.append(link.get('href').replace(" ", "%20"))
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

    @staticmethod
    def downloader(download_url, destination=r'.\download', delay_time=5.0):
        """
        Download the files from the url to the destination path.
        Beware: many websites don't like it very much when you automatically
        scrape their documents and you get blocked. That's why delay time required.

        Args:
            download_url (string): https://www.bot.or.th/example.html
            destination (string): Destination of file
            delay_time (float): Wait time between downloads

        Returns:

        """
        from urllib.request import urlretrieve
        from time import sleep
        for url in download_url:
            urlretrieve(url, "%s/%s" % (destination, url.split('/')[-1]))
            sleep(delay_time)

    def extract_emails(self):
        """
        TBD
        Returns:

        """
        pass


if __name__ == "__main__":
    PDF_EXAMPLE_LINK = \
        'https://www.bot.or.th/English/MonetaryPolicy/Northern/EconomicReport/Pages/Releass_Economic_north.aspx'
    OBJ = GetPage(PDF_EXAMPLE_LINK)
    OBJ.extract_link()
    PDFS = OBJ.filter_links(['pdf'])
    GetPage.downloader(PDFS)
