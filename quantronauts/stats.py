from os import path
import pandas as pd
import datetime


def stats(winner):
    file_csv = 'stats/qnim_results.csv'
    date_x = datetime.datetime.now()
    date_day = str(date_x.month) + '-' + str(date_x.year)

    robot_csv = []
    human_csv = []
    date_csv = []

    ##################################################################################
    # CSV exist
    if path.exists(file_csv):

        csv_file = pd.read_csv(file_csv, header=None)

        for i in range(len(csv_file[0])):
            robot_csv.append(csv_file[0][i])
            human_csv.append(csv_file[1][i])
            date_csv.append(csv_file[2][i])

        test = 0
        for i in range(len(date_csv)):
            if date_day == date_csv[i]:
                if winner == "robot":
                    robot_csv[i] += 1
                else:
                    human_csv[i] += 1
                test = 1

        if test == 0:
            date_csv.append(date_day)
            robot_csv.append(1)

        csv_file = {'robot': robot_csv, 'human': human_csv, 'date': date_csv}
        df = pd.DataFrame(csv_file)
        df.to_csv(file_csv, index=False, header=None)

    ##################################################################################
    # CSV doesn't exist
    if not path.exists(file_csv):

        if winner == "robot":
            robot_csv.append(1)
            human_csv.append(0)
        else:
            robot_csv.append(0)
            human_csv.append(1)
        date_csv.append(date_day)

        csv_file = {'robot': robot_csv, 'human': human_csv, 'date': date_csv}
        df = pd.DataFrame(csv_file)
        df.to_csv(file_csv, index=False, header=None)
