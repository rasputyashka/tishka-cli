import sqlite3

__all__ = [
    "open_db"
]


class open_db:

    def __init__(self, path_to_file):
        self.filename = path_to_file

    def __enter__(self):
        self.con = sqlite3.connect(self.filename)
        self.cur = self.con.cursor()
        return self.cur

    def __exit__(self, execption_type, exception_value, traceback):
        self.con.commit()
        self.cur.close()
