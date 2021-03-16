## Script to randomly assign faction and team to players or draw a random faction.
## Fall 2020

import math
import numpy as np
import pandas as pd
from itertools import compress

def random_matchup(players, teams = np.nan, split = True, duplicates = False):

    # specify available factions
    good = ['Gondor', 'Rohan', 'Erebor', 'Lothlórien', 'Rivendell', 'Woodland Realm']
    evil = ['Mordor', 'Isengard', 'Misty Mountains', 'Dol Guldur']

    # calculate matchup characteristics
    teams = teams if not math.isnan(teams) else 2
    total_players = teams*math.ceil(len(players)/teams)
    team_size = int(total_players/teams)

    # initialize dataframe
    setup = pd.DataFrame(columns=['Team', 'Player', 'Faction'], index = range(0, total_players))
    setup['Team'] = ['Team ' + str(i) for i in range(1, teams+1)]*team_size

    # create random teams
    players_sample = []
    p_dummy = players
    while len(p_dummy) > 0:
        if len(p_dummy) > (team_size-1):
            players_sample = players_sample + list(np.random.choice(p_dummy, team_size, replace = False))
            p_dummy = list(compress(p_dummy, [i not in players_sample for i in p_dummy]))
        else:
            players_sample = players_sample + list(np.random.choice(p_dummy, len(p_dummy), replace = False))
            p_dummy = []

    if len(players_sample) != total_players:
        for i in range(1, total_players-len(players_sample) + 1):
            players_sample = players_sample + ['Bot ' + str(i)]
    setup['Player'] = players_sample

    # assign allegiance and faction
    if split and (teams % 2) == 0:
        # assign allegiance
        pool = ['Good', 'Evil'] * int(len(pd.unique(setup['Team'])) / 2)
        setup['Allegiance'] = list(np.random.choice(pool, len(pool), replace=False)) * team_size

        # assign faction
        faction = []
        if duplicates:
            for p in list(setup['Allegiance']):
                if p == 'Good':
                    faction = faction + list(np.random.choice(good, 1))
                else:
                    faction = faction + list(np.random.choice(evil, 1))
            setup['Faction'] = faction
        else:
            setup['Faction'][setup['Allegiance'] == 'Good'] = np.random.choice(good, int(total_players/2), replace=False)
            setup['Faction'][setup['Allegiance'] == 'Evil'] = np.random.choice(evil, int(total_players/2), replace=False)
    else:
        if duplicates:
            setup['Faction'] = np.random.choice(good+evil, total_players)
        else:
            setup['Faction'] = np.random.choice(good+evil, total_players, replace=False)

    # print results
    setup = setup.sort_values(by=['Team'])
    if split:
        for index, row in setup.iterrows():
            print(row['Team'], ' (', row['Allegiance'], '): ', row['Player'], '  -  ', row['Faction'], sep='')
    else:
        for index, row in setup.iterrows():
            print(row['Team'], ': ', row['Player'], '  -  ', row['Faction'], sep='')

def random_team(n = 1, allegiance = None, duplicates = False):

    # specify available factions
    good = ['Gondor', 'Rohan', 'Erebor', 'Lothlórien', 'Rivendell', 'Woodland Realm']
    evil = ['Mordor', 'Isengard', 'Misty Mountains', 'Dol Guldur']

    # define eligible factions
    if allegiance is not None:
        if allegiance == 'good':
            factions = good
        elif allegiance == 'evil':
            factions = evil
    else:
        factions = good+evil

    # select factions
    if duplicates:
        selected = np.random.choice(factions, n)
    else:
        selected = np.random.choice(factions, n, replace=False)

    # print results
    [print(i) for i in selected]

random_matchup(players=['Player 1', 'Player 2', 'Player 3', 'Player 4'], teams=2, split=False, duplicates=False)
random_team(allegiance='evil')