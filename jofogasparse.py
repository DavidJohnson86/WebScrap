
from web_requests import  GetPage
import os
from time import sleep


class JofogasParser():

    def __init__(self, link):
        self.link = link
        self.offer_links = None

    def search_links(self):
        """
        Search Potential Links what refers to the Offers

        Returns:

        """
        find_offers = GetPage(link)
        find_offers.simple_get()
        find_offers.extract_link()
        self.offer_links = find_offers.filter_links(['kiado'.lower(), 'alberlet'.lower()])


    def get_offers(self):
       for offer_links in self.offer_links:
            current_offer = GetPage(offer_links)
            current_offer.simple_get()
            html_text = current_offer.soup
            for link in html_text.findAll('div', attrs={'class': 'date'}):
                write_line = 'Title: %s Date: %s' % (offer_links, link.text.rstrip().lstrip().replace('Feladás dátuma: ', ''))
                #JofogasParser.logging_data(write_line)
            self.log_host(write_line)

    def log_host(self, offer):

        pathdir = os.path.dirname(__file__)
        logfile = pathdir + '\\Logs\\' + 'Data'
        with open(logfile, 'r') as logfile:
            data = logfile.read().splitlines()
        if offer not in data:
            print('TALÁLTAM EGY ALBÉRLETET: %s' %(offer))

    @staticmethod
    def logging_data(message):
        """

        Write only if file not empty
        Args:
            message:

        Returns:

        """
        pathdir = os.path.dirname(__file__)
        logfile = pathdir + '\\Logs\\' + 'Data'
        logfile = open(pathdir + '\\Logs\\' + 'Data', "a")
        logfile.write(str(message) + '\n')
        logfile.close()

if __name__=="__main__":
    link = r'https://ingatlan.jofogas.hu/veszprem/veszprem-/lakas?max_price=100000&min_price=50000&st=u'
    obj = JofogasParser(link)
    obj.search_links()
    while True:
        print('Request Offers')
        obj.get_offers()
        sleep(60)

