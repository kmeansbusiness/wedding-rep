from bs4 import BeautifulSoup
from collections import defaultdict

import requests


class SilverScraper(object):
    def __init__(self):
        '''
        Initialize links we will use to scrape songsheets
        '''
        self.base_url = 'https://www.silverarrowband.com/Astro/DB'
        self.master_url = 'https://www.silverarrowband.com/Astro/DB/MusicianViewGigs.php?MusicianID=ChrisMcCarthy&SiD=61915660&HistoricalSearch=On'
        self.song_dict = defaultdict(int)


    def get_song_dict(self):
        '''
        Scrape each song sheet into a song dictionary of counts
        '''
        worksheets = self.get_worksheets(self.master_url)
        print(f'found {len(worksheets)} worksheets')
        for i, worksheet in enumerate(worksheets):
            print(f'scraping {worksheet} {i} / {len(worksheets)}')
            setlists = self.get_setlists(worksheet)
            for setlist in setlists:
                songs = self.get_songs(setlist)
                for song in songs:
                    self.song_dict[song] += 1


    def get_songs(self, setlist_link):
        '''
        Format backend request to setlist service
        '''

        url = f'{self.base_url}/{setlist_link}'
        html = requests.get(url).text
        soup = BeautifulSoup(html, features='html.parser')
        song_p = soup.find_all('p')[2]  # weird 3-level nesting
        
        setlist = []
        for song in song_p.stripped_strings:
            setlist.append(self.clean_song_name(song))

        return setlist


    def clean_song_name(self, song):
        '''
        There's inconsistency with how people write song names, so we need to clean it up.
        
        e.g. lowercase, parse out key info
        '''

        return song.lower()


    def get_setlists(self, worksheet_link):
        '''
        Given a worksheet, parse out the setlists and return as a list.

        This is the only info we need to query the setlist service.
        '''
        url = f'{self.base_url}/{worksheet_link}'
        html = requests.get(url).text
        soup = BeautifulSoup(html, features='html.parser')
        
        musicians = soup.find(attrs={'class': 'group ws-musicians'})
        
        setlists = []
        if musicians:
            musician_list = musicians.find_all(attrs={'class': 'ws-group-item'})
            for musician in musician_list:
                setlist = musician.find(attrs={'title': 'Setlist'})
                if setlist:
                    setlist_link = setlist.attrs['href']
                    setlists.append(setlist_link)
        else:
            print('no div found with class=group ws-musicians')
        
        return setlists


    def get_worksheets(self, master_url):
        '''
        Parse out worksheet urls
        '''
        html = requests.get(master_url).text
        soup = BeautifulSoup(html, features='html.parser')
        worksheets = soup.find_all(attrs={'title': 'Worksheet for this event'})
        if worksheets != []:
            worksheet_links = [worksheet.attrs['href'] for worksheet in worksheets]
            return worksheet_links
        else:
            print('no worksheets found')
            return []



if __name__ == '__main__':
    parser = WeddingParser()
    parser.get_song_dict()
