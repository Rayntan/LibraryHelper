import json


CONFIG_PATH = "config.json"
REPORT_KEY = "report_dir_path"
DB_KEY = "db"

CONFIG_TEMPLATE = {
    REPORT_KEY: "",
    DB_KEY: {
        "host": "",
        "port": "",
        "user": "",
        "password": "",
        "dbname": ""
      }
}


class Config:
    def __init__(self):
        self.__data = None
        self.load_config()

    def load_config(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                self.__data = json.load(f)
        except FileNotFoundError:
            self.__data = CONFIG_TEMPLATE
            self._save_config()

    def _save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.__data, f)

    @property
    def db_data(self):
        return self.__data[DB_KEY]

    @db_data.setter
    def db_data(self, new_db_data: dict):
        self.__data[DB_KEY] = new_db_data
        self._save_config()

    @property
    def report_dir_path(self):
        return self.__data[REPORT_KEY]

    @report_dir_path.setter
    def report_dir_path(self, new_dir_path: str):
        self.__data[REPORT_KEY] = new_dir_path
        self._save_config()
