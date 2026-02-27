import pandas as pd


def load_df(path):
    sheet_list = "ALL_sep"
    df = pd.read_excel(path + '\\data_for_ML\\CEFR-J Wordlist Ver1.6.xlsx', sheet_name=sheet_list)
    # IMPORTANT columns in dataset



    X_column_name = "headword"# word
    y_column_name = "CEFR" # level

    df = df[["headword", "CEFR"]]
    df = df.dropna()

    df_add = pd.read_csv(path + '\\data_for_ML\\octanove-vocabulary-profile-c1c2-1.0.csv')
    df_add = df_add[["headword", "CEFR"]]
    df_add = df_add.dropna()
    df = pd.concat([df, df_add], axis=0)

    return df, X_column_name,y_column_name
