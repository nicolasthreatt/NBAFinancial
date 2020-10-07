'''
Steps to follow: https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/python-sql-driver-pyodbc?view=sql-server-ver15
Connect to Azure SQL Database: https://docs.microsoft.com/en-us/azure/azure-sql/database/connect-query-python?tabs=windows 
'''

import pyodbc
import os


def connect():

    # Database Credentials
    server   = os.getenv('azureServer')
    database = os.getenv('azureDBFinancial')
    username = os.getenv('azureDBUsername')
    password = os.getenv('azureDBPswd')
    driver   = '{ODBC Driver 17 for SQL Server}'

    # Connect to Database
    cnxn = pyodbc.connect('DRIVER='+driver+';      \
                           SERVER='+server+';      \
                           PORT=1433;              \
                           DATABASE='+database+';  \
                           UID='+username+';       \
                           PWD='+ password)
    return cnxn

def readTable(schema, table):
    
    import pandas as pd

    # Connect to Database
    cnxn = connect()

    # Get Stats from Database
    table = pd.read_sql_query(
        '''SELECT *
            FROM [{}].[{}]'''.format(schema, table), cnxn)

    return table

def insertTeamsSalaryCapInfo(cnxn, teams):

    # Create connection
    cursor = cnxn.cursor()

    # Delete previous data from table and reseed primary keys
    cursor.execute("TRUNCATE TABLE [Teams].[SalaryCapOverview2019-20]")
    cursor.execute("DBCC CHECKIDENT ('[Teams].[SalaryCapOverview2019-20]', RESEED, 1)")

    insert_query = '''INSERT INTO [Teams].[SalaryCapOverview2019-20]
                            ([Team],
                             [2019-20], [2020-21], [2021-22], [2022-23], [2023-24], [2024-25])
                      VALUES (?, ?, ?, ?, ?, ?, ?)'''

    for team, data in teams.items():

        values = (team,                                                    \
                  teams[team].year1, teams[team].year2, teams[team].year3, \
                  teams[team].year4, teams[team].year5, teams[team].year6)

        cursor.execute(insert_query, values)

    # Commit Inserts
    cnxn.commit()

def insertPlayersPayrollInfo(cnxn, players):

    # Create connection
    cursor = cnxn.cursor()

    # Delete previous data from table and reseed primary keys
    cursor.execute("TRUNCATE TABLE [Players].[Payroll2019-20]")
    cursor.execute("DBCC CHECKIDENT ('[Players].[Payroll2019-20]', RESEED, 1)")

    insert_query = '''INSERT INTO [Players].[Payroll2019-20]
                            ([Team], 
                             [Player], [Age],
                             [2019-20], [2020-21], [2021-22], [2022-23], [2023-24], [2024-25],
                             [SignedUsing], [Guaranteed])
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    for player in players:

        values = (player.team,                              \
                  player.name,  player.age,                 \
                  player.year1, player.year2, player.year3, \
                  player.year4, player.year5, player.year6,
                  player.signedUsing, player.guaranteed)

        cursor.execute(insert_query, values)

    # Commit Inserts
    cnxn.commit()