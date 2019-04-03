import time
import datetime
import argparse
import csv
from sys import exit
import getpass
import requests
import json
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SurveyMonkeyRequest:
    def __init__(self, access_token):
        self.access_token = access_token

    def create_empty_survey(self):
        s = requests.Session()
        s.headers.update({
        "Authorization": "Bearer %s" % self.access_token,
        "Content-Type": "application/json"
        })

        payload = {
            "title": "TEST SURVEY CREATION"
            }
        url = "https://api.surveymonkey.com/v3/surveys"
        response = s.post(url, json=payload)
        return response.json()


class Game:
    ''' Stores the values for each game listed '''
    def __init__(self, name: str, genre: str, setup_amount: int):
        self.name = name
        self.genre = genre
        self.has_been_played = False
        self.last_played_timestamp = 0
        self.setup_amount = setup_amount

    def set_last_played_timestamp(self, date: str):
        ''' For played games, set the appropriate timestamp.
        The date string has already been validated, no need to check it again here.
        '''
        self.has_been_played = True
        self.last_played_timestamp = (get_timestamp_from_date(date))

def get_timestamp_from_date(date: str) -> int:
    ''' Converts a date string into int unix epoch time.
    date argument must be formatted as dd/mm/yy
    '''
    return time.mktime(datetime.datetime.strptime(date, "%d/%m/%y").timetuple())

def CONST_WEEK_TIMESTAMP() -> int:
    ''' Returns a constant value of on eweek's worth of time in Unix Epoch time '''
    return 604800

def debug_test_game_class():
    ''' Creates and prints a test game object for debug testing purposes '''
    print("debug_test_game_class() START")
    test_game = Game("mario brother", "jump", 2)
    print("name: " + test_game.name)
    print("genre: " + test_game.genre)
    print("setup amount: " + str(test_game.setup_amount))
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
            game_setup_amount = int(row[4])
            planned_game = Game(game_name, game_genre, game_setup_amount)
            planned_games.append(planned_game)
            row_count += 1
    #print(row_count)
    return planned_games

def debug_test_planned_games(planned_games: [Game]):
    ''' Prints the title and genre of every planned game for debug testing purposes '''
    print("debug_test_game_class() START")
    for pg in planned_games:
        print(pg.name + " - " + pg.genre + " - setups: " + str(pg.setup_amount))
    print("debug_test_game_class() END")

def set_games_played(path_to_games_played_csv: str, planned_games: [Game]):
    ''' Iterates through the planned game list, setting every played game's appropriate timestamps '''
    with open(path_to_games_played_csv, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(csvreader)  # skip header line
        for row in csvreader:
            played_title = row[1]
            played_date = row[2]
            if is_date_string_valid(played_date):
                for g in planned_games:
                    if played_title == g.name:
                        g.set_last_played_timestamp(played_date)

def debug_test_games_played(planned_games: [Game]):
    ''' Prints the most recent timestamp for every played game for debug testing purposes '''
    for pg in planned_games:
        if pg.has_been_played:
            print("'" + pg.name + "' was last played: " + str(pg.last_played_timestamp))

def get_valid_games(planned_games: [Game], date_of_tournament: str, weeks_between_replay: int) -> [Game]:
    ''' Returns a list of valid side bracket games for the poll '''
    valid_games = []
    for pg in planned_games:
        if pg.setup_amount > 0:
            if (not pg.has_been_played or get_enough_weeks_passed(pg.last_played_timestamp, date_of_tournament,
                weeks_between_replay)):
                valid_games.append(pg)
    return valid_games

def get_enough_weeks_passed(last_played_timestamp: float, date_of_tournament: str, weeks_between_replay: int) -> bool:
    ''' Return whether enough weeks have passed since the game was last played to be considered for playing again '''
    return get_timestamp_from_date(date_of_tournament) > last_played_timestamp + (weeks_between_replay *
            CONST_WEEK_TIMESTAMP())

def is_date_string_valid(date: str) -> bool:
    ''' Checks to see if supplied date string is valid.
    Exits with an error message if not.
    '''
    valid = False
    if type(date) is str:
        # check if formated as dd/mm/yy
        if len(date) == 8 and (date[2] == "/" and date[5] == "/"):
            valid = True
    if not valid:
        print("ERROR: '" + date + "' is not a valid date string")
        exit(1)
    return valid

def get_personal_access_token() -> str:
    return getpass.getpass("Enter SurveyMonkey API personal access token: ")

def print_request_response(request_response: json):
    print(json.dumps(request_response, indent=4))

def arg_parse() -> []:
    '''Returns a list of parsed command line arguments'''
    #parser = argparse.ArgumentParser(version='2.1')
    parser = argparse.ArgumentParser()
    parser.add_argument('planned_games_csv_path', action='store', type=str,
            help='Input CSV containing details of planned side bracket games')
    parser.add_argument('played_games_csv_path', action='store', type=str,
            help='Input CSV containing details of played side bracket games')
    # TODO: add a default value for the following
    parser.add_argument('-d', action='store', dest='date_of_tournament', type=str,
            help='Date of the tournament this poll will decide')
    parser.add_argument('-g', action='store', dest='weeks_between_replay', type=int, default=4,
            help='How many weeks should be leave before running a game again? Defaults to 1 month')
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
    # Check user supplied date string to see if we need to terminate early
    if is_date_string_valid(args.date_of_tournament):
        # Parse data from input CSVs
        planned_games = get_planned_games(args.planned_games_csv_path)
        #debug_test_planned_games(planned_games)
        set_games_played(args.played_games_csv_path, planned_games)
        #debug_test_games_played(planned_games)
        valid_games = get_valid_games(planned_games, args.date_of_tournament, args.weeks_between_replay)
        #debug_test_planned_games(valid_games)
        # Make poll
        personal_access_token = get_personal_access_token()
        create_survey_response = SurveyMonkeyRequest(personal_access_token).create_empty_survey()
        print_request_response(create_survey_response)

if __name__ == "__main__":
    main()

