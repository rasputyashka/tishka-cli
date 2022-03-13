import argparse
import json
from datetime import date
from typing import List, Optional, Tuple

from db_connectors import open_db


class JsonReader():
    def __init__(self, filename):
        self.filename = filename

    def display_from_to(
            self,
            dates: list,
            data: dict,
            from_: Optional[int] = 0,
            to: Optional[int] = None,
            step: int = 1
            ):

        if from_ < 0 < to:
            from_ = 0

        for cur_date in dates[from_:to:step]:
            print(f"\t{cur_date}: ", end='')
            print(*data[cur_date], sep=', ')

    def find_idx(self, arr: List[str], value: date) -> int:
        """хз, насколько есть смысл делать его методом,
        но он используется только классом Json"""

        # most likely you can compare two dates in their string representation
        value = str(value)
        for pos, el in enumerate(arr):
            if el >= value:
                return pos
        return -1

    def show_tasks(self, quantity: Optional[int] = 5, today: date = date.today()):

        try:
            with open(self.filename) as f:

                tasks = json.load(f)
                dates = sorted(tasks)  # the same as sorted(tasks.keys())
                today_pos = self.find_idx(dates, today)
                if quantity:
                    print("new tasks: ")
                    if today_pos != -1:
                        self.display_from_to(dates, tasks, today_pos, today_pos+quantity)
                    print('old tasks: ')
                    self.display_from_to(dates, tasks, today_pos, today_pos-quantity, -1)
                else:
                    print("all tasks: ")
                    self.display_from_to(dates, tasks)

        except FileNotFoundError:

            print("There is no date yet")


class SqliteReader():
    def __init__(self, filename):

        self.filename = filename

    def display_tasks(self, result: Tuple[str, str]):
        """
        self.display(tasks, ('2022-12-12', '["a", "b"]'))
        >>>    2022-12-12: a, b
        """
        for row in result:
            print(f"\t{row[0]}: ", end=' ')
            print(*json.loads(row[1]), sep=', ')

    def show_tasks(self, quantity: int = 5, today: date = date.today()):
        with open_db(self.filename) as cur:

            if quantity:
                less_select_query = """
                    SELECT task_date, tasks
                    FROM todos
                    WHERE task_date < ?
                    ORDER BY task_date DESC
                    LIMIT ?"""

                greater_select_query = """
                    SELECT task_date, tasks
                    FROM todos
                    WHERE task_date >= ?
                    ORDER BY task_date ASC
                    LIMIT ?"""

                past = cur.execute(less_select_query, (str(today), quantity)).fetchall()
                print('old tasks: ')
                self.display_tasks(past)

                future = cur.execute(greater_select_query, (str(today), quantity))
                print('new tasks: ')
                self.display_tasks(future)

            else:

                select_query = 'SELECT task_date, tasks FROM todos ORDER BY task_date ASC'
                all_tasks = cur.execute(select_query).fetchall()
                print("all tasks: ")
                self.display_tasks(all_tasks)


def get_date(user_date: str) -> date:

    task_date = date.fromisoformat(user_date)
    return task_date


def main():

    parser = argparse.ArgumentParser(
        usage='python3 show-tasks.py')

    parser.add_argument('-n',  help='amount of dates displayed', default=5, type=int)
    parser.add_argument('--all', '-a', action='store_true', help='shows all tasks')
    parser.add_argument('--from-date', '-d', help='sets this date as an origin')
    parser.add_argument(
        '-ext', help='looks data in given file',
        choices=['json', 'sqlite'], default='json'
        )

    args = parser.parse_args()

    if args.ext == 'json':
        reader = JsonReader('tasks.json')
    elif args.ext == 'sqlite':
        reader = SqliteReader('tasks.db')

    assert args.n > 0

    if args.all:
        if args.from_date:
            reader.show_tasks(None, get_date(args.from_date))
        else:
            reader.show_tasks(None)
    elif args.from_date:
        reader.show_tasks(args.n, get_date(args.from_date))
    else:
        reader.show_tasks(args.n)


if __name__ == "__main__":
    main()
