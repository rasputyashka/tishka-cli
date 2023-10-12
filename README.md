# tishka-cli

## RU
#задание

Сделать две консольные программы для планировщика дел

Первая: спрашивает у юзера какое задание он хочет добавить. Вводится название и планируемое время в виде день.месяц. Естественно, если пользователь в декабре написал задачу на январь - это на следующий год. Так же чтобы можно было написать "завтра" или "послезавтра"

Вторая программа: выдает 5 следующих дел и 5 последних, которые прошли. Считается относительно текущей даты. Так же чтобы можно было в консоли параметром ввести на какой день считать вместо сегодняшнего.


Что тебе понадобится
1. Вынести общий код в отдельный модуль
2. Разобраться как будешь сохранять данные (json или sqlite на выбор)
3. Разобраться с аргументами командной строки (модуль Argparse)
4. Разобраться с модулем datetime.

Усложнения:
1. Использовать sqlite или json опрделеяется настройками программы
2. Сделать UI (веб или десктоп), работающий с тем же хранилищем


## EN (translated by yandex translator (i'm too lazy for that)
#task

Make two console programs for the task scheduler

First: asks the user what task he wants to add. Enter the name and the planned time in the form of a day.month. Naturally, if a user wrote a task for January in December, it is for the next year. Also so that you can write "tomorrow" or "the day after tomorrow"

The second program: gives out the next 5 cases and the last 5 that have passed. It is considered relative to the current date. Also, so that you can enter a parameter in the console for which day to count instead of today.


What will you need
1. Put the general code in a separate module
2. Figure out how you will save data (json or sqlite to choose from)
3. Deal with command line arguments (Argparse module)
4. Deal with the datetime module.

Complications:
1. Using sqlite or json is determined by the program settings
2. Make a UI (web or desktop) that works with the same storage



(The task is taken from python-beginners and the solution is written in python 3.8.10)
https://t.me/ru_python_beginners/1465630
