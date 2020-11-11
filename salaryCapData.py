'''
File: salaryCapSummary.py

Description:
    - Scrapes from https://www.basketball-reference.com/contracts/ to collect teams salary cap data
    - Stores data into a cloud database
'''


from bs4 import BeautifulSoup
import financialDB
import utils
from urllib.request import urlopen


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


class PlayerContractsInfo:
    def __init__(self):
        self.name         = str()
        self.age          = int()
        self.team         = str()
        self.year1        = str()
        self.year2        = str()
        self.year3        = str()
        self.year4        = str()
        self.year5        = str()
        self.year6        = str()
        self.signed_using = str()
        self.guaranteed   = str()


def getPlayerContracts(season, db=False):

    print('\nGetting PLayers'' contracts infomation...\n')

    player_contracts = list()
    for team in utils.getTeams():

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

        for player, data in zip(players, players_contracts_data):

            player_contracts_info = PlayerContractsInfo()

            player_contracts_info.name         = player
            player_contracts_info.team         = team[1]
            player_contracts_info.age          = data[0]
            player_contracts_info.year1        = data[1]
            player_contracts_info.year2        = data[2]
            player_contracts_info.year3        = data[3]
            player_contracts_info.year4        = data[4]
            player_contracts_info.year5        = data[5]
            player_contracts_info.year6        = data[6]
            player_contracts_info.signed_using = data[7]
            player_contracts_info.guaranteed   = data[8]

            player_contracts.append(player_contracts_info)

    if db:
        cnxn = financialDB.connect("Players", "Payroll{}".format(season))
        financialDB.insertPlayersPayrollInfo(cnxn, player_contracts)


def getTeamSalaryCapInfo(season, db=False):

    print('\nGetting Team''s salary cap infomation...\n')

    url = 'https://www.basketball-reference.com/contracts/'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')

    teams_contracts_table = soup.find('table')
    teams_contracts_table_rows = teams_contracts_table.find_all('tr')

    teams_contracts_data = list()
    for tr in teams_contracts_table_rows:

        # Row Data
        td = tr.find_all('td')
        row_data = [str(i.text).replace(u'\xa0', '') for i in td]
        if row_data: teams_contracts_data.append(row_data)

    teams_to_contracts = dict()
    for team_contract_data in teams_contracts_data:
        team  = team_contract_data[0]

        teams_to_contracts[team] = SalaryCapTeamInfo()
        teams_to_contracts[team].year1 = team_contract_data[1]
        teams_to_contracts[team].year2 = team_contract_data[2]
        teams_to_contracts[team].year3 = team_contract_data[3]
        teams_to_contracts[team].year4 = team_contract_data[4]
        teams_to_contracts[team].year5 = team_contract_data[5]
        teams_to_contracts[team].year6 = team_contract_data[6]

    if db:
        cnxn = financialDB.connect("Teams", "SalaryCapOverview{}".format(season))
        financialDB.insertTeamsSalaryCapInfo(cnxn, teams_to_contracts)

    return teams_to_contracts


if __name__ == "__main__":
    args = utils.processCmdArgs()

    if args.tscrape: getTeamSalaryCapInfo(args.season, db=args.db)
    if args.pscrape: getPlayerContracts(args.season, db=args.db)