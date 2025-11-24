import pandas as pd


    #Tags

def true_false_format(df: pd.DataFrame) -> pd.DataFrame: 


    df["tags"] = df["tags"].fillna("NA").str.strip().str.split(";")

    tags_explode = df["tags"].explode().str.strip()
    tags_df = pd.crosstab(tags_explode.index, tags_explode)
    tags_df = tags_df.add_prefix("TAG_")



    #feature
    df["feature"] =df["feature"].fillna("NA").str.strip().str.split(";")
    feature_explode =df["feature"].explode().str.strip()
    feature_df = pd.crosstab(feature_explode.index, feature_explode)
    feature_df = feature_df.add_prefix("FEATURE_")


    #genre
    df["genre"] =df["genre"].fillna("NA").str.strip().str.split(";")
    genre_explode =df["genre"].explode().str.strip()
    genre_df = pd.crosstab(genre_explode.index, genre_explode)
    genre_df = genre_df.add_prefix("GENRE_")

    #category
    df["category"] =df["category"].fillna("NA").str.strip().str.split(";")
    category_explode =df["category"].explode().str.strip()
    category_df = pd.crosstab(category_explode.index, category_explode)
    category_df = category_df.add_prefix("CATEGORY_")


    # Alles in eine Tabelle
    onehot_df = pd.concat([genre_df, category_df, tags_df, feature_df],axis=1)

    # Anpassung der onehots
    onehot_df.columns = onehot_df.columns.str.replace(" ", "_", regex=False)
    onehot_df.columns = onehot_df.columns.str.replace("__+", "_", regex=False)
    df = df.drop(labels=["category", "feature","tags","genre"], axis=1)
    df = pd.concat([df, onehot_df], axis=1) # vertikal


    return df