import random as rn
import pandas as pd
import seaborn as sns

dataFrame = pd.read_csv(r'Spotify_Youtube.csv')
class ProcessingData:
    @staticmethod
    def transformate(dataFrame):#usuwamy niepotrzebne kolumny
        neededColumns=["Track", "Artist", "Danceability", "Energy", "Key", "Loudness", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo"]
        for column in dataFrame.columns:
            if column not in neededColumns:
                del dataFrame[column]
        return dataFrame
    @staticmethod
    def shuffle(x):
        for i in range(len(x) - 1, 0, -1):
            j = rn.randint(0, i - 1)
            x.iloc[i], x.iloc[j] = x.iloc[j], x.iloc[i]

    @staticmethod
    def normalization(x):#normalizacja 'transformowanej' bazy
        for column in x.columns:
            if column in ["Artist", "Track"]:
                continue
            lista = list(x.loc[:, column])
            mini = min(lista)
            maxi = max(lista)
            for i in range(len(x)):
                x.at[i, column] = (x.at[i, column] - mini) / (maxi - mini)


def get_user_prompt():
    user_string_data = []
    doContinue = True
    while doContinue:
        artist = input("Proszę podać artystę: ").lower().replace(" ", "")
        song = input("Proszę podać tytuł utworu: ").lower().replace(" ", "")
        user_string_data.append([artist, song])
        doContinue = input("Czy chcesz dodać kolejny utwór? (t/n): ").lower() == "t"
    

def main():
    print("Witaj w aplikacji do rekomendacji muzyki!")
    user_string_data = get_user_prompt()
    music_data = pd.read_csv('Spotify_Youtube.csv')
    print(music_data.head())

#main()
print(dataFrame.head())
dataFrameFormated = ProcessingData.transformate(dataFrame)
print(dataFrame.head())
ProcessingData.normalization(dataFrameFormated)
print(dataFrame.head())

