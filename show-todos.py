import argparse
import json
from datetime import date
from typing import Union, List


def get_date(user_date: str) -> date:

    task_date = date.fromisoformat(user_date)
    return task_date


def find_closest(arr: List[str], value: date) -> int:

    for pos, el in enumerate(map(lambda x: date.fromisoformat(x), arr)):
        if el >= value:
            return pos
    return -1


def display_from_to(dates: list, data: dict, from_: int, to: int, step=1) -> None:
    if from_ < 0 < to:
        from_ = 0
    for cur_date in dates[from_: to: step]:
        print(f"\t{cur_date}: ", end='')
        print(*data[cur_date], sep=', ')


def show_tasks(filename: str, quantity: Union[int, None] = 5, today: date = date.today()) -> None:

    try:
        with open(filename) as f:
            tasks = json.load(f)
            dates = sorted(tasks.keys())
            today_pos = find_closest(dates, today)
            if quantity:
                print("New tasks: ")
                if today_pos != -1:
                    display_from_to(dates, tasks, today_pos, today_pos+quantity)
                print('old tasks: ')
                display_from_to(dates, tasks, today_pos, today_pos-quantity, -1)
            else:
                print("all tasks: ")
                for cur_date in dates:
                    print(f"\t{cur_date}", end=' ')
                    print(*tasks[cur_date], sep=', ')
    except FileNotFoundError:
        print("There is no date yet")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        usage='python3 show-tasks.py'
        )
    parser.add_argument('-n',  help='amount of dates displayed', default=5, type=int)
    parser.add_argument('--all', '-a', action='store_true', help='shows all tasks')
    parser.add_argument('--from-date', '-d', help='sets this date as an origin')

    args = parser.parse_args()

    file = "tasks.json"

    assert args.n > 0

    if args.all:
        show_tasks(file, None)
        if args.from_date:
            show_tasks(file, None, get_date(args.from_date))
    elif args.from_date:
        show_tasks(file, args.n, get_date(args.from_date))
    else:
        show_tasks(file, args.n)
