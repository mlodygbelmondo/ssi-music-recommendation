import pandas as pd

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

main()

