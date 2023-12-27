import shelve

class Database:
    def __init__(self, dbName: str = "AssistantApiDatabase"):
        self.dbName = dbName

    def save_file(self, file):
        with shelve.open(self.dbName) as db:
            print("File in database", file.name)
            db["file"] = file.read()  # Save the file content

    def get_file(self):
        with shelve.open(self.dbName) as db:
            return db.get("file")
