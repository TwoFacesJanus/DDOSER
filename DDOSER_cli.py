import glob
import json
import os
from tracemalloc import start


def find_dosbox() -> True:
    for file in (glob.glob('**/*.exe', recursive=True)):
        if file == "DOSBox.exe":
            return True
    return False


def work_with_config() -> dict:
    with open("config.json", "r") as file:
        json_config = json.load(file)
    return json_config


def all_games(json_config):
    for game in range(len(json_config['Games'])):
        print("| -", game, json_config['Games'][game]['Name'])


def add_game():
    game = str(input("Game name: "))
    path = str(input("Path: "))
    executable_path = str(input("Executable Path: "))
    new_data = {"Name": game, "Path": path, "Exec":executable_path}
    with open("config.json", "r+") as file:
        file_data = json.load(file)
        file_data['Games'].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent= 4)


def select_game(json_config) -> str:
    selected_game = int(input("Enter Game number: "))
    executable_path = json_config['Games'][selected_game]["Exec"]
    print(executable_path)
    return executable_path

    

def start_game(executable_path):
    os.system("DOSBox.exe " + executable_path)



def main():
    all_games(work_with_config())
    choice = str(input("What do u want? [0-GameList, 1-StartGame, 2-AddGame]: "))
    if choice == "0":
        print(all_games(work_with_config()))
    elif choice == "1":
        start_game(select_game(work_with_config()))
    elif choice == "2":
        add_game()
    main()

main()
