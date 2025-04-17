import csv
import pickle
from utils import input_str, input_int


class CsvSerializer:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for key, value in data.items():
                writer.writerow([key, value])

    def load(self):
        data = {}
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                key, value = row
                data[key] = int(value)
        return data


class PickleSerializer:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'wb') as file:
            pickle.dump(data, file)

    def load(self):
        with open(self.filename, 'rb') as file:
            return pickle.load(file)


class TeamManager:
    def __init__(self, serializer):
        self.serializer = serializer

    def save_teams(self, teams):
        self.serializer.save(teams)

    def load_teams(self):
        return self.serializer.load()

    def get_best_team(self):
        teams = self.load_teams()
        best_team = max(teams, key=teams.get)
        return best_team

    def get_sorted_teams(self):
        teams = self.load_teams()
        sorted_teams = sorted(teams.keys(), key=lambda x: teams[x], reverse=True)
        return sorted_teams

    def get_team_score(self, team_name):
        teams = self.load_teams()
        return teams.get(team_name, None)

    def __str__(self):
        return f"TeamManager with serializer: {self.serializer.__class__.__name__}"


if __name__ == '__main__':
    while True:
        serializer = input_str("Choose serializer (csv/pickle): ").strip().lower()
        if serializer == "csv":
            serializer = CsvSerializer('data/first_task.csv')
            break
        elif serializer == "pickle":
            serializer = PickleSerializer('data/first_task.pkl')
            break
        else:
            print("Invalid serializer. Please choose 'csv' or 'pickle'.")
            continue

    data = {
        "first_team": 300,
        "second_team": 200,
        "third_team": 100,
        "fourth_team": 320
    }

    team_manager = TeamManager(serializer)
    team_manager.save_teams(data)

    while True:
        print("1. Get best team")
        print("2. Get sorted teams")
        print("3. Get team score")
        print("4. Exit")

        choice = input_int("Choose an option: ")
        match choice:
            case 1:
                best_team = team_manager.get_best_team()
                print(f"Best team: {best_team}")
            case 2:
                sorted_teams = team_manager.get_sorted_teams()
                print(f"Sorted teams: {', '.join(sorted_teams)}")
            case 3:
                team_name = input_str("Enter team name: ")
                score = team_manager.get_team_score(team_name)
                if score is not None:
                    print(f"Score of {team_name}: {score}")
                else:
                    print(f"Team '{team_name}' not found.")
            case 4:
                break
            case _:
                print("Invalid choice. Please try again.")

