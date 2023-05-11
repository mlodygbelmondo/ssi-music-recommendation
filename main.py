import random as rn
import pandas as pd
import seaborn as sns


dataFrame = pd.read_csv(r'Spotify_Youtube.csv')


class ProcessingData:
    @staticmethod
    def transformate(dataFrame):  # usuwamy niepotrzebne kolumny
        neededColumns = ["Track", "Artist", "Danceability", "Energy", "Key", "Loudness", "Speechiness", "Acousticness",
                         "Instrumentalness", "Liveness", "Valence", "Tempo"]
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
    def normalization(x):  # normalizacja 'transformowanej' bazy
        for column in x.columns:
            if column in ["Artist", "Track"]:
                continue
            lista = list(x.loc[:, column])
            mini = min(lista)
            maxi = max(lista)
            for i in range(len(x)):
                x.at[i, column] = (x.at[i, column] - mini) / (maxi - mini)


def get_user_prompt(listOfTracks):
    user_string_data = []
    doContinue = True
    while doContinue:
        # artist = input("Proszę podać artystę: ").lower().replace(" ", "")
        song = input("Proszę podać tytuł utworu: ").lower().replace(" ", "")
        # user_string_data.append([artist, song])
        if song in listOfTracks:
            user_string_data.append(song)
        else:
            print("Brak podanego tytułu w naszej bazie.")
        doContinue = input("Czy chcesz dodać kolejny utwór? (t/n): ").lower() == "t"
    return user_string_data


def main():
    music_data = pd.read_csv('Spotify_Youtube.csv') #wczytanie bazy
    music_data_transformed = ProcessingData.transformate(music_data) #usuniecie kolumn ktorych nie uzyjemy
    ProcessingData.normalization(music_data_transformed) #normalizacja bazy
    listOfTracks = music_data_transformed["Track"].values.tolist() #stworzenie listy z nazwami utworow
    print("Witaj w aplikacji do rekomendacji muzyki!") #chico mexicano
    user_string_data = get_user_prompt(listOfTracks) #pobranie danych od uzytkownika

    for track in user_string_data:
        KNN(track) #jescze nie zrobione, ale moze cos na zasadzie ze knn zwraca stringa:
                   #na podstawie utworu 'tytul' autorstwa 'artysta' podajemy 5 utworow ktore moga ci sie spodobac
                   #1. tytul: 'tytul', artysta: 'artysta' itd...
                    index = listOfTracks.index(track)  # index danego utworu
                    music_data_transformed.drop(index)  # usuniecie rzedu danego utworu(zrobic to w knn)

        #ogolnie ten caly knn to sie jeszcze cos wymysli


main()



