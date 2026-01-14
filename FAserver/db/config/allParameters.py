from db.config.modelsParameters.textsParams import TextsParameters
from db.config.modelsParameters.wordsParams import WordsParameters
from db.config.namesOfTables import NamesOfTables

class AllParameters():
    def __init__(self):
        self.namesOfTables = NamesOfTables()
        self.wordsParameters = WordsParameters("The_Secret_Garden_Vocabulary_B1-C1.xlsx")
        self.textsParameters = TextsParameters("The secret garden.txt")