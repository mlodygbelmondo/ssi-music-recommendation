import math
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
    def createlist(baza):
        listOfTracks = baza["Track"].values.tolist()  # stworzenie listy z nazwami utworow
        return [track.lower().replace(" ", "") for track in listOfTracks]  # nazwy utworow do malych liter

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

class KNN:
    @staticmethod
    def distance(baza, v):
        dist = []
        for i in range(len(baza)):
            tmp = 0
            for j in range(2, 12):
                tmp += ((baza.iloc[i][j] - v[j]) ** 2)
            dist.append(math.sqrt(tmp))
        return dist

    @staticmethod
    def adddistance(baza, dist): #dodanie kolumny distance
        baza["distance"] = dist

    @staticmethod
    def dropdistance(baza): #usuniecie kolumny distance
        baza.drop(columns=["distance"])



    @staticmethod
    def sort(baza, lewa, prawa): #sortowanie
        if lewa < prawa:
            pivot = baza.iloc[prawa][5]
            j = lewa
            for i in range(lewa, prawa):
                if baza.iloc[i][5] < pivot:
                    baza.iloc[j], baza.iloc[i] = baza.iloc[i], baza.iloc[j]
                    j += 1
            baza.iloc[j], baza.iloc[prawa] = baza.iloc[prawa], baza.iloc[j]
            KNN.sort(baza, lewa, j - 1)
            KNN.sort(baza, j + 1, prawa)

    @staticmethod
    def algorithm(baza, v):
        dist=KNN.distance(baza, v) # liczymy dystans
        KNN.adddistance(baza, dist) #dodajemy kolumne z dystansem
        #KNN.sort(baza, 0, len(baza)-1)
        baza = baza.sort_values(by="distance")
        print(baza.head())
        print(f"Na podstawie utworu: {v[1]}, autorstwa: {v[0]}, mogą ci się spodobać następjące utwory:")
        for i in range(1, 6):
            print(f"{i}. Utwór: {baza.iloc[i][1]}, Autor: {baza.iloc[i][0]}")
        KNN.dropdistance(baza) #usuwamy dystans zeby potem znowu moc dodac

        # @staticmethod
        # def knn_algorithm(baza, k=4):
        #     ProcessingData.shuffle(baza)
        #     ProcessingData.normalization(baza)
        #     irisTrainMain, irisTest = ProcessingData.split(iris, 0.7)
        #
        #     iloscDobrych = 0
        #     for i in range(len(irisTest)):
        #         irisTrain = irisTrainMain.copy()
        #         v = irisTest.iloc[i][0:4]
        #         dist = KNN.distance(irisTrain, v)
        #         KNN.adddistance(irisTrain, dist)
        #         KNN.sort(irisTrain, 0, len(irisTrain) - 1)
        #         if KNN.check(irisTrain, k) == irisTest.iloc[i][4]:
        #             iloscDobrych += 1
        #         print(i)
        #
        #     print(f"Skutecznosc = {iloscDobrych / len(irisTest) * 100}%")


def get_user_prompt(listOfTracks):
    user_string_data = []
    doContinue = True
    while doContinue:
        # artist = input("Proszę podać artystę: ").lower().replace(" ", "")
        song = input("Proszę podać tytuł utworu: ").lower().replace(" ", "")
        # user_string_data.append([artist, song])
        if song in listOfTracks:
            if song not in user_string_data:
                user_string_data.append(song)
            else:
                print("Ten utwór został już podany.")
        else:
            print("Brak podanego tytułu w naszej bazie.")
        doContinue = input("Czy chcesz dodać kolejny utwór? (t/n): ").lower() == "t"
    return user_string_data


def main():
    music_data = pd.read_csv('Spotify_Youtube.csv') #wczytanie bazy
    music_data_transformed = ProcessingData.transformate(music_data) #usuniecie kolumn ktorych nie uzyjemy
    ProcessingData.normalization(music_data_transformed) #normalizacja bazy
    listOfTracks = ProcessingData.createlist(music_data_transformed)
    print("Witaj w aplikacji do rekomendacji muzyki!") #chico mexicano
    user_string_data = get_user_prompt(listOfTracks) #pobranie danych od uzytkownika

    for track in user_string_data:
        index=listOfTracks.index(track)
        v=music_data_transformed.iloc[index][:]
        KNN.algorithm(music_data_transformed, v)
        music_data_transformed.drop(range(6))
        listOfTracks = ProcessingData.createlist(music_data_transformed)
'''
    for track in user_string_data:
        KNN(track) #jescze nie zrobione, ale moze cos na zasadzie ze knn zwraca stringa:
                   #na podstawie utworu 'tytul' autorstwa 'artysta' podajemy 5 utworow ktore moga ci sie spodobac
                   #1. tytul: 'tytul', artysta: 'artysta' itd...
                    index = listOfTracks.index(track)  # index danego utworu
                    music_data_transformed.drop(index)  # usuniecie rzedu danego utworu(zrobic to w knn)

        #ogolnie ten caly knn to sie jeszcze cos wymysli
'''

main()


