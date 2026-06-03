import os
import json


class Leaderboard():

    def __init__(self, path: str = "../high_score/leaderboard.json") -> None:

        self.path: str = path

        self.scores: list[dict] = []
        self.load()

    def load(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        if not os.path.exists(self.path):

            struct = {"scores": []}

            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(struct, f, ensure_ascii=False, indent=4)

        try:
            with open(self.path, "r") as f:
                data = json.load(f)

                if not isinstance(data, dict):
                    raise ValueError("JSON not a dict")

                if "scores" not in data:
                    raise ValueError("Not key 'scores'")

                if not isinstance(data["scores"], list):
                    raise ValueError("'scores' is not a list")

                for entry in data["scores"]:
                    valid = True
                    if not isinstance(entry.get("name"), str):
                        valid = False

                    if not isinstance(
                         entry.get("score"), int) or entry["score"] < 0:
                        valid = False

                    if len(entry["name"].strip()) == 0:
                        valid = False

                    if len(entry["name"]) > 10:
                        valid = False

                    if not all(c.isalnum() or c == " " for c in entry["name"]):
                        valid = False

                    if valid is True:

                        self.scores.append(entry)

                    else:
                        print(f"Invalid entry skipped: {entry}")
                        continue

            self.save()

        except Exception as e:
            print(f"Corrupted leaderboard: {e}. "
                  "Regenerating a clean leaderboard")

            struct = {"scores": []}

            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(struct, f, ensure_ascii=False, indent=4)

    def save(self) -> None:

        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(
                    {"scores": self.scores}, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"Error saving leaderboard:{e}")

    def can_enter(self, score) -> bool:

        if len(self.scores) < 10:
            return True

        else:
            return score > self.scores[-1]["score"]

    def add_score(self, name: str, score: int) -> None:

        if not isinstance(name, str):
            print("Invalid name: must be a string")
            return

        if len(name.strip()) == 0:
            print("Invalid name: cannot be empty!")
            return

        if len(name) > 10:
            print("Invalid name: max 10 characters")
            return

        if not all(c.isalnum() or c == " " for c in name):
            print("Invalid name: alphanumeric and spaces only")
            return

        if not isinstance(score, int) or score < 0:
            print("Invalid score: must be not a non-negative integer")
            return

        if not self.can_enter(score):
            print("score not high enought to enter leaderboard")
            return

        self.scores.append({"name": name, "score": score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]
        self.save()

    def get_scores(self) -> list[dict]:
        return self.scores
