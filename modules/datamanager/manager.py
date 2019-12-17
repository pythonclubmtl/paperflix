from tinydb import TinyDB, Query
from datetime import datetime
import os

class DataManager():

    def __init__(self, dbname):
        databases_dir = "./databases/"
        check_folder = os.path.isdir(databases_dir)
        if not check_folder:
            os.makedirs(databases_dir)
        self.db = TinyDB("./databases/"+dbname+".json")

    def update_user_db(self):
        result = {}
        dtime = datetime.now()
        result["last_bib_update"] = str(dtime)
        self.db.insert(result)
