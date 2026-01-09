import pandas as pd


def normalize_age_price(game_df, profile_df):

    game = game_df.copy()
    profile = profile_df.copy()

    age_max = game["required_age"].max()
    price_max = game["price"].max()

    for df in (game, profile):
        df["required_age"] = 1-(age_max - df["required_age"]) / age_max
        df["price"] = 1-(price_max - df["price"]) / price_max

    return game, profile 