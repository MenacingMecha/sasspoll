import time
import datetime
import argparse
import csv

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
    ''' Creates and prints a test game object for debug testing purposes '''
    print("debug_test_game_class() START")
    test_game = Game("mario brother", "jump")
    print("name: " + test_game.name)
    print("genre: " + test_game.genre)
    last_date_played = "31/03/19"
    test_game.set_last_played_timestamp(last_date_played)
    print("last played timestamp: " + str(test_game.last_played_timestamp))
    print("debug_test_game_class() END")

def get_planned_games(path_to_csv: str) -> [Game]:
    ''' Returns an array of every planned game in the input csv '''
    planned_games = []
    row_count = 0
    with open(path_to_csv, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(csvreader)  # skip header line
        for row in csvreader:
            # first two columns are game title and genre
            game_name = row[0]
            game_genre = row[1]
            planned_game = Game(game_name, game_genre)
            planned_games.append(planned_game)
            row_count += 1
    #print(row_count)
    return planned_games

def debug_test_planned_games(planned_games: [Game]):
    ''' Prints the title and genre of every planned game for debug testing purposes '''
    print("debug_test_game_class() START")
    for pg in planned_games:
        print(pg.name + " - " + pg.genre)
    print("debug_test_game_class() END")

def arg_parse() -> []:
    '''Returns a list of parsed command line arguments'''
    #parser = argparse.ArgumentParser(version='2.1')
    parser = argparse.ArgumentParser()
    parser.add_argument('planned_games_csv_path', action='store',
            help='Input CSV containing details of planned side bracket games')
    parser.add_argument('played_games_csv_path', action='store',
            help='Input CSV containing details of played side bracket games')
#    parser.add_argument('-o', action='store', dest='output_file',
#            help='Output CSV to write stats to')
#    parser.add_argument('-s', '--silent', action='store_true', default=False,
#            dest="silent", help='Silences terminal output')
#    parser.add_argument('-w', action='store', dest='whitelist_file',
#            help='Newline-seperated list of players to check optionally check against')
#    parser.add_argument('--print-output', action='store_true', default=False,
#            dest='print_output',
#            help='Print stats to terminal (output is ugly, use for debugging!)')
#    parser.add_argument('-x', action='store', dest='column_offset', type=int,
#            default=0, help='How many columns to offset in the input CSV')
#    parser.add_argument('--placement-games', action='store',
#            dest='placement_games', type=int, default=5,
#            help='How many games need to be played with fudged values outputted')
#    parser.add_argument('--highest-lowest', action='store_true', default=False,
#            dest='HIGHEST_LOWEST', help="Include player's highest and lowest Elo values")
    return parser.parse_args()

def main():
    #debug_test_game_class()
    args = arg_parse()
    planned_games = get_planned_games(args.planned_games_csv_path)
    #debug_test_planned_games(planned_games)

if __name__ == "__main__":
    main()

