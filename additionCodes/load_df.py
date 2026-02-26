import pandas as pd


def load_df(path):
    sheet_list = "ALL_sep"
    df = pd.read_excel(path + '\\data_for_ML\\CEFR-J Wordlist Ver1.6.xlsx', sheet_name=sheet_list)
    # IMPORTANT columns in dataset



    X_column_name = "headword"# word
    y_column_name = "CEFR" # level

    df = df[["headword", "CEFR"]]
    df = df.dropna()
    return df, X_column_name,y_column_name
