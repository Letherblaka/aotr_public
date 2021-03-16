## Script to test random_teams.py by monte carlo simulations

import matplotlib.pyplot as plt

# initialize parameters
players = ['Player A', 'Player B', 'Player C', 'Player D']
teams = np.nan
split = True
duplicates = False
n_sim = 100000
df = pd.DataFrame(columns=['Player', 'Team', 'Faction'])

# specify available factions
for i in np.arange(0,n_sim)+1:

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

    # save results
    setup = setup.sort_values(by=['Player'])
    setup = setup.loc[:,['Player', 'Team', 'Faction']]
    df = df.append(setup)

    if i%100 == 0:
        print('Simulation No.', i, 'completed.')

# print results
results = pd.DataFrame(columns=np.unique(df['Faction']))
for f in results.columns:
    results[f] = [sum(df.loc[df['Faction'] == f,'Player'] == p) for p in players]

fig, ax = plt.subplots()
index = np.arange(len(players))
bar_width = 0.8/len(results.columns)
opacity = 0.8

for i in np.arange(0,len(results.columns)):
    globals()['rects' + str(i)] = plt.bar(x=index+i*bar_width,
                                          height=results[results.columns[i]],
                                          width=bar_width,
                                          alpha=opacity,
                                          #color='b',
                                          label=results.columns[i])

plt.ylabel('Number of Simulations')
plt.title('Results from ' + str(n_sim) + ' simulated draws')
plt.xticks(index+bar_width*4.5, players)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=5)

plt.tight_layout()
plt.show()
fig.savefig('simulation_results', bbox_inches='tight')