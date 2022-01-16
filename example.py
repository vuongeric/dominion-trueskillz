from trueskill import Rating, rate, TrueSkill

# Assumptions:
# Max 5 players per game
# Rows in CSV are chronological

# Read CSV
# headers: datetime, 1st, 2nd, 3rd, 4th, 5th
EXPECTED_HEADERS = [
    "datetime",
    "player_a",
    "player_b",
    "player_c",
    "player_d",
    "player_e",
]


def load_games(csv_file):
    f = open(csv_file, "r")
    lines = f.read().split("\n")
    f.close()
    headers = lines[0].split(",")
    # validate input
    assert len(headers) == 6, RuntimeError
    assert all(
        [expected == actual for expected, actual in zip(EXPECTED_HEADERS, headers)]
    ), RuntimeError("wrong headers")

    csv_rows = [x.split(",") for x in lines[1:]]
    games = [x[1:] for x in csv_rows]  # remove datetime
    games = [
        list(filter(lambda x: x != "", game)) for game in games
    ]  # remove empty cells

    return games


def get_new_ratings(players_rating):
    # compute new rating
    current_ratings = [x[1] for x in players_rating]
    return rate([(x,) for x in current_ratings])


def get_key(val, hash):
    for key, value in hash.items():
        if val == value:
            return key

    raise KeyError


def run():

    env = TrueSkill(mu=0, sigma=1)
    games = load_games("./test.csv")
    PLAYERS = {player: Rating() for players in games for player in players}

    for game in games:
        players_rating = [(player, PLAYERS[player]) for player in game]
        player_names = [x[0] for x in players_rating]
        new_ratings = get_new_ratings(players_rating)

        # Update new Ratings
        for player_name, new_rating in zip(player_names, new_ratings):
            PLAYERS[player_name] = new_rating[0]

    leaderboard = sorted(list(PLAYERS.values()), key=env.expose, reverse=True)

    rankings = [get_key(rating, PLAYERS) for rating in leaderboard]
    print("rankings:", rankings)


run()
