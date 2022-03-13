from datetime import date, datetime
import json
import argparse


def write_data(filename: str, task_name: str, task_date: date):

    date_as_key = str(task_date)

    try:

        with open(filename) as f:

            data = json.load(f)
            try:
                data[date_as_key].append(task_name)
            except KeyError:
                data[date_as_key] = [task_name]

    except FileNotFoundError:
        data = {date_as_key: [task_name]}

    with open(filename, 'w') as f:

        json.dump(data, f, ensure_ascii=False, indent=4)


def get_date(user_date: str) -> date:

    today = date.today()

    try:
        task_date = datetime.strptime(user_date, "%d.%m").date()
        task_date = task_date.replace(year=today.year)

    except (AttributeError, ValueError):

        aliases = {
            'сегодня': 0,
            'завтра': 1,
            'послезавтра': 2,
        }

        if user_date in aliases:
            offset = aliases[user_date]
        else:
            raise ValueError("Дата неверна")

        task_date = today.replace(day=today.day + offset)

    if task_date < today:
        task_date = task_date.replace(year=today.year+1)

    return task_date


def main(filename, task_desc, task_date):

    write_data(filename, task_desc, get_date(task_date))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='cli todo implementation',
        usage='python3 todo.py <task> <date>'
    )
    parser.add_argument('task', help="todo description")
    parser.add_argument('date', help="sets the date in `day.month` format")

    args = parser.parse_args()

    main('tasks.json', args.task, args.date.lower())
