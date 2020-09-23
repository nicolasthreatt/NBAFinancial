'''
SalaryCapSummary.py

TODO:
    Add logging
    Make graphs
    Cleanup and uncomment dbStorage
'''

import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import financialDB

class SalaryCapTeamInfo:
    def __init__(self):
        self.players = list()
        self.rank    = int()
        self.year1   = str()
        self.year2   = str()
        self.year3   = str()
        self.year4   = str()
        self.year5   = str()
        self.year6   = str()

    def addPlayer(player):
        self.players.append(player)


class PlayerContractsInfo:
    def __init__(self):
        self.name        = str()
        self.age         = int()
        self.year1       = str()
        self.year2       = str()
        self.year3       = str()
        self.year4       = str()
        self.year5       = str()
        self.year6       = str()
        self.signedUsing = str()
        self.guaranteed  = str()


def getPlayerContracts():
    teams = [
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

    player_contracts_dict = dict()
    for team in teams:
        print(team[0])
        url = 'https://www.basketball-reference.com/contracts/' + team[0] + '.html'
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')

        players_contracts_table = soup.find('table')
        players_contracts_table_rows = players_contracts_table.find_all('tr')

        players = list()
        players_contracts_data = list()

        for tr in players_contracts_table_rows:

            # Header
            th = tr.find_all('th')
            header_data = [i.text for i in th]
            if len(header_data) == 1: players.append(header_data[0])

            # Row Data
            td = tr.find_all('td')
            row_data = [str(i.text).replace(u'\xa0', '') for i in td]
            if row_data and row_data[0]: players_contracts_data.append(row_data)

        players_data = list()
        for player, data in zip(players, players_contracts_data):

            player_contract_data = PlayerContractsInfo()

            player_contract_data.name        = player
            player_contract_data.age         = data[0]
            player_contract_data.year1       = data[1]
            player_contract_data.year2       = data[2]
            player_contract_data.year3       = data[3]
            player_contract_data.year4       = data[4]
            player_contract_data.year5       = data[5]
            player_contract_data.year6       = data[6]
            player_contract_data.signedUsing = data[7]
            player_contract_data.guaranteed  = data[8]

            player_contracts_dict[team[1]] = SalaryCapTeamInfo()
            player_contracts_dict[team[1]].players.append(player_contract_data)

    # Store to database [Players].[Payroll2019-20]
    # cnxn = financialDB.connect()
    # financialDB.insertPlayersPayrollInfo(cnxn, player_contracts_dict)


def getTeamSalaryCapInfo():

    print('Getting Team''s salary cap infomation...')

    url = 'https://www.basketball-reference.com/contracts/'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')

    teams_contracts_table = soup.find('table')
    teams_contracts_table_rows = teams_contracts_table.find_all('tr')

    teams_contracts_data   = list()

    for tr in teams_contracts_table_rows:

        # Row Data
        td = tr.find_all('td')
        row_data = [str(i.text).replace(u'\xa0', '') for i in td]
        if row_data: teams_contracts_data.append(row_data)

    teams_contract_dict = dict()

    for team_contract_data in teams_contracts_data:
        team  = team_contract_data[0]

        teams_contract_dict[team] = SalaryCapTeamInfo()
        teams_contract_dict[team].year1 = team_contract_data[1]
        teams_contract_dict[team].year2 = team_contract_data[2]
        teams_contract_dict[team].year3 = team_contract_data[3]
        teams_contract_dict[team].year4 = team_contract_data[4]
        teams_contract_dict[team].year5 = team_contract_data[5]
        teams_contract_dict[team].year6 = team_contract_data[6]

    # Store to database [Teams].[SalaryCapOverview2019-20]
    # cnxn = financialDB.connect()
    # financialDB.insertTeamsSalaryCapInfo(cnxn, teams_contract_dict)

def processCmdArgs():

    parser = argparse.ArgumentParser(description='Collect teams salary cap infomation from https://www.basketball-reference.com/contracts/')

    parser.add_argument('--teams', dest='teams', required=False, action='store_true',
                         help='Insert Teams Salary Cap Infomation Data into Existing Table in Database')

    parser.add_argument('--players', dest='players', required=False, action='store_true',
                        help='Insert Players contracts information into Existing Table in Database')

    return parser.parse_args()

if __name__ == "__main__":
    args = processCmdArgs()

    if args.teams:
        getTeamSalaryCapInfo()
    if args.players:
        getPlayerContracts()