'''
File:
    - utils.py

Description:
    - Commonly used functions
'''

import argparse
import sys


def getFutureSeasons(currentSeason, futureSeason):
    return [ "Guaranteed",
             str(currentSeason)   + '-' + str(futureSeason),
             str(currentSeason+1) + '-' + str(futureSeason+1),
             str(currentSeason+2) + '-' + str(futureSeason+2),
             str(currentSeason+3) + '-' + str(futureSeason+3),
             str(currentSeason+4) + '-' + str(futureSeason+4),
             str(currentSeason+5) + '-' + str(futureSeason+5) ]


def getTeams():
    return [
             ("ATL", "Atlanta Hawks"),          ("BOS", "Boston Celtics"),     ("BRK", "Brooklyn Nets"), 
             ("CHO", "Charlotte Hornets"),      ("CHI", "Chicago Bulls"),      ("CLE", "Cleveland Cavaliers"), 
             ("DAL", "Dallas Mavericks"),       ("DEN", "Denver Nuggets"),     ("DET", "Detroit Pistons"), 
             ("GSW", "Golden State Warriors"),  ("HOU", "Houston Rockets"),    ("IND", "Indiana Pacers"),
             ("LAC", "Los Angeles Clippers"),   ("LAL", "Los Angeles Lakers"), ("MEM", "Memphis Grizzlies"),
             ("MIA", "Miami Heat"),             ("MIL", "Milwaukee Bucks"),    ("MIN", "Minnesota Timberwolves"),
             ("NOP", "New Orleans Pelicans"),   ("NYK", "New York Knicks"),    ("OKC", "Oklahoma City Thunder"),
             ("ORL", "Orlando Magic"),          ("PHI", "Philadelphia 76ers"), ("PHO", "Phoenix Suns"),
             ("POR", "Portland Trail Blazers"), ("SAC", "Sacramento Kings"),   ("SAS", "San Antonio Spurs"),
             ("TOR", "Toronto Raptors"),        ("UTA", "Utah Jazz"),          ("WAS", "Washington Wizards"),
            ]


def getCmdTeam(cmdTeamAbr):

    for team in getTeams():
        if cmdTeamAbr == team[0]:
            return team[1]

    sys.exit('Invalid Team!')


def processCmdArgs():

    parser = argparse.ArgumentParser(description='Command Line Agrument Options')

    parser.add_argument('--season', dest='season', type=str, metavar='', required=False, default='2019-20',
                         help="Teams' Season for Salary Cap Infomation")

    parser.add_argument('--teams', dest='teams', nargs='+', type=str, metavar='', required=False, default=list(),
                         help="Abbreviated Teams City")

    parser.add_argument('--players', dest='players', nargs='+', type=str, metavar='', required=False, default=list(),
                         help="Player(s)")

    parser.add_argument('--plot', dest='plot', nargs='?', type=str, metavar='', required=False,
                        const='',
                        choices=('bar', 'line', 'pie'),
                        help='List of plot types')

    # salaryCapData.py
    parser.add_argument('--tscrape', dest='tscrape', required=False, action='store_true',
                         help='Scrape Teams Salary Cap Infomation Data')

    parser.add_argument('--pscrape', dest='pscrape', required=False, action='store_true',
                        help='Scrape Players contracts information')

    parser.add_argument('--db', dest='db', required=False, action='store_true',
                         help='Insert Data into Existing Table in Database')                         

    # teamSalaryPlot.py
    parser.add_argument('--years', dest='years', nargs='+', type=str, metavar='', required=False, default=list(),
                         help="Selected Year(s)")

    parser.add_argument('--compare', dest='compare', action='store_true', required=False,
                         help='Compare Teams Seasons') # TeamA TeamB YearA YearB

    parser.add_argument('--line', dest='line', action='store_true', required=False,
                         help='Line Graph Plot')

    return parser.parse_args()