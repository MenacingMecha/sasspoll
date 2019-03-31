import time
import datetime

class Game:
    ''' Stores the values for each game listed '''
    def __init__(self, name: str, genre: str):
        self.name = name
        self.genre = genre
        self.has_been_played = False
        self.last_played_timestamp = 0

    def set_last_played_timestamp(self, date: str):
        self.has_been_played = True
        self.last_played_timestamp = (self.get_timestamp_from_date(date))

    @staticmethod
    def get_timestamp_from_date(date: str) -> int:
        ''' Converts a date string into int unix epoch time.
        date argument must be formatted as dd/mm/yy
        '''
        return time.mktime(datetime.datetime.strptime(date, "%d/%m/%y").timetuple())

def debug_test_game_class():
    print("debug_test_game_class() START")
    test_game = Game("mario brother", "jump")
    print("name: " + test_game.name)
    print("genre: " + test_game.genre)
    last_date_played = "31/03/19"
    test_game.set_last_played_timestamp(last_date_played)
    print("last played timestamp: " + str(test_game.last_played_timestamp))
    print("debug_test_game_class() END")

def main():
    debug_test_game_class()

if __name__ == "__main__":
    main()

