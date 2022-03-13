from datetime import date, datetime
import json
import argparse
from typing import Union

from db_connectors import open_db


class SqliteWriter():

    def __init__(self, filename: str):

        self.filename = filename
        with open('create_table.sql') as query_file:
            with open_db(self.filename) as cur:
                cur.execute(query_file.read())

    def write_data(self, task_name: str, task_date: date):

        with open_db(self.filename) as cur:

            select_query = 'SELECT tasks FROM todos WHERE task_date = ?'
            result = cur.execute(select_query, (str(task_date),))
            values = result.fetchall()
            if not values:
                insert_query = 'INSERT INTO todos(task_date, tasks) VALUES (?, ?)'
                cur.execute(insert_query, (str(task_date), json.dumps([task_name])))
            else:
                tasks = list(json.loads(values[0][0])) + [task_name]
                update_query = 'UPDATE todos SET tasks = ? WHERE task_date = ?'
                cur.execute(update_query, (json.dumps(tasks), str(task_date)))


class JsonWriter():

    def __init__(self, filename: str):

        self.filename = filename

    def write_data(self, task_name: str, task_date: date):

        date_as_key = str(task_date)

        try:

            with open(self.filename) as f:

                data = json.load(f)
                try:
                    data[date_as_key].append(task_name)
                except KeyError:
                    data[date_as_key] = [task_name]

        except FileNotFoundError:
            data = {date_as_key: [task_name]}

        with open(self.filename, 'w') as f:

            json.dump(data, f, ensure_ascii=False, indent=4)


def get_date(user_date: str) -> date:

    today = date.today()

    try:
        task_date = datetime.strptime(user_date, "%d.%m").date()
        task_date = task_date.replace(year=today.year)

    except (AttributeError, ValueError):

        offsets = {
            'сегодня': 0,
            'завтра': 1,
            'послезавтра': 2,
        }

        if user_date in offsets:
            offset = offsets[user_date]
        else:
            raise ValueError(f"Invalid date: {user_date}")

        task_date = today.replace(day=today.day + offset)

    if task_date < today:
        task_date = task_date.replace(year=today.year+1)

    return task_date


def main(wrapper: Union[JsonWriter, SqliteWriter], task_desc: str, task_date: str):

    task_date = get_date(task_date)
    wrapper.write_data(task_desc, task_date)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='cli todo implementation',
        usage='python3 todo.py <task> <date>'
    )
    parser.add_argument('task', help="todo description")
    parser.add_argument('date', help="sets the current date: format is `day.month`")
    parser.add_argument(
        '-ext', help='datafile extension',
        choices=['sqlite', 'json'], default='sqlite'
        )

    args = parser.parse_args()
    if args.ext == 'json':
        wrapper = JsonWriter('tasks.json')
    elif args.ext == 'sqlite':
        wrapper = SqliteWriter('tasks.db')
    main(wrapper, args.task, args.date.lower())
