import time
import datetime

class Game:
    ''' Stores the values for each game listed '''
    def __init__(self, name: str, genre: str):
        self.name = name
        self.genre = genre
        self.has_been_played = False
        self.last_played_timestamp = 0

    def set_last_played_timestamp(date: str):
        self.has_been_played = True
        self.last_played_timestamp = (get_timestamp_from_date(date))

    def get_timestamp_from_date(date:str) -> int:
        ''' Converts a date string into int unix epoch time.
        date argument must be formatted as dd/mm/yy
        '''
        return time.mktime(datetime.datetime.strptime(date, "%d/%m/%y").timetuple())

def main():
    pass

if __name__ == "__main__":
    main()

