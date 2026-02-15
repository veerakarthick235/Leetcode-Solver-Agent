import json
import os

class Memory:
    def __init__(self, db_file="data/problems.json"):
        self.db_file = db_file
        if not os.path.exists("data"): os.makedirs("data")
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f: json.dump({}, f)

    def is_solved(self, slug):
        with open(self.db_file, 'r') as f:
            data = json.load(f)
        return slug in data and data[slug].get("status") == "Accepted"

    def save(self, slug, code, status):
        with open(self.db_file, 'r') as f:
            data = json.load(f)
        data[slug] = {"code": code, "status": status}
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
