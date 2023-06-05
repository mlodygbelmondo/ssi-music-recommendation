import math
import random as rn
import pandas as pd
import numpy as np

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
    def addIndex(baza):
        baza["index"] = [i for i in range(len(baza))]

    @staticmethod
    def normalization(x):  # normalizacja 'transformowanej' bazy
        for column in x.columns:
            if column in ["Artist", "Track", "index"]:#ddddddddddddddddddddddddddddddddddddddd
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
    def adddistance(baza, dist):  # dodanie kolumny distance
        baza["distance"] = dist

    @staticmethod
    def dropdistance(baza):  # usuniecie kolumny distance
        baza.drop(columns=["distance"])

    @staticmethod
    def algorithm(baza, index, user_string_data):

        #ProcessingData.addIndex(baza) # dodajemy kolumne z indeksami
        v = baza.iloc[index]
        #print(v.iloc[12])
        dist = KNN.distance(baza, v)  # liczymy dystans
        KNN.adddistance(baza, dist)  # dodajemy kolumne z dystansem
        # KNN.sort(baza, 0, len(baza)-1)
        baza = baza.sort_values(by="distance")
        #print(baza.head())
        print(f"Na podstawie utworu: {v[1]}, autorstwa: {v[0]}, mogą ci się spodobać następjące utwory:")
        indexes_to_erase = []
        j=1
        for i in range(1, 6):
            track = baza.iloc[j]
            if track[1].lower().replace(" ", "") not in user_string_data: #if zeby sprawdzic czy proponowana piosenka nie jest podana przez uzytkownika
                print(f"{i}. Utwór: {track[1]}, Autor: {track[0]}")
                j+=1
            else:
                j+=1
                track = baza.iloc[j]
                print(f"{i}. Utwór: {track[1]}, Autor: {track[0]}")
                j+=1

            if track[1].lower().replace(" ", "") not in user_string_data:#ddddddddddddddddddddddddddddd raczej ifa mozna usunac
                #print("lol")
                indexes_to_erase.append(track.iloc[12])
                #baza = baza.drop(track.iloc[12], axis=0) # usuwanie utworu ktory nie jest podany dalej przez uzytkownika
        for index in indexes_to_erase:
            baza = baza.drop(index, axis=0) # usuwamy wszystkie utwory ktore nie sa na liscie podanych przez uzytkownika
        baza = baza.drop(v.iloc[12], axis=0) # usuwanie utworu ktory teraz byl podany do sprawdzenia
        KNN.dropdistance(baza)  # usuwamy dystans zeby potem znowu moc dodac
        return baza


def get_user_prompt(listOfTracks):
    user_string_data = []
    doContinue = True
    while doContinue:
        song = input("Proszę podać tytuł utworu: ").lower().replace(" ", "")
        if song in listOfTracks:
            if song not in user_string_data:
                user_string_data.append(song)
            else:
                print("Ten utwór został już przez ciebie podany.")
        else:
            print("Brak podanego tytułu w naszej bazie.")
        doContinue = input("Czy chcesz dodać kolejny utwór? (t/n): ").lower() == "t"
    return user_string_data


def main():
    music_data = pd.read_csv('Spotify_Youtube.csv')  # wczytanie bazy
    music_data_transformed = ProcessingData.transformate(music_data)  # usuniecie kolumn ktorych nie uzyjemy
    ProcessingData.normalization(music_data_transformed)  # normalizacja bazy
    listOfTracks = ProcessingData.createlist(music_data_transformed)  # stworzenie listy utworow
    print("Witaj w aplikacji do rekomendacji muzyki!")
    user_string_data = get_user_prompt(listOfTracks)  # pobranie danych od uzytkownika
    ProcessingData.addIndex(music_data_transformed) # dodajemy kolumne z indeksami

    for track in user_string_data:
        index = listOfTracks.index(track)
        #v = music_data_transformed.iloc[index]
        music_data_transformed = KNN.algorithm(music_data_transformed, index, user_string_data)

        listOfTracks = ProcessingData.createlist(music_data_transformed)


main()
# music_data = pd.read_csv('Spotify_Youtube.csv')
# music_data_transformed = ProcessingData.transformate(music_data)
# print(music_data_transformed.head())
# #music_data_transformed.iloc[0] , music_data_transformed.iloc[1] = music_data_transformed.iloc[1] , music_data_transformed.iloc[0]
# print(music_data_transformed.head())
