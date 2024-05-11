import random
from functools import lru_cache


def set_the_flag():
    global flags
    global all_field_for_user
    if flags >= 1:
        flags -= 1
        massive = list(map(int, input('Coordinates of the flag ').split())) 
        all_field_for_user[massive[0]][massive[1]] = 'F'
        print_user_field()
    else:
        print("Alas, you can't add flags.")


def delete_the_flag():
    global flags
    global all_field_for_user
    if flags < 10:
        massive = list(map(int, input('Coordinates of the flag ').split()))
        if all_field_for_user[massive[0]][massive[1]] != 'F':
            print('There is no flag there')
            return
        all_field_for_user[massive[0]][massive[1]] = '*'
        print_user_field()
        flags += 1
    else:
        print('Alas, you cannot take away the flags')


def end_of_game():
    dd, mm = 0, 0
    for i in all_field_for_user:
        for j in i:
            if j not in ['_', '*']:
                dd += 1
            elif j == '_':
                mm += 1
    if 81 - dd - mm == 10:
        return True
    return False


def print_user_field():  # display the map that the user sees
    for i in all_field_for_user:
        print(*i)
    print(f'Flags amount: {flags}')


def print_admin_field():  # display the card that the admin sees
    for i in all_field_for_admin:
        print(*i)


@lru_cache
def fill(i, j):
    global all_field_for_admin
    if not 0 <= i < 9 or not 0 <= j < 9 or all_field_for_admin[i][j] != 0:
        return
    all_field_for_admin[i][j] = 'S'
    # recurse launches
    fill(i - 1, j)
    fill(i + 1, j)
    fill(i, j - 1)
    fill(i, j + 1)


if __name__ == "__main__":
    all_field_for_user = [['*' for i in range(9)] for i in range(9)]
    print('Minesweeper 9x9 game')
    print('To put a flag, write the word FLAG instead of coordinates')
    print('To remove the flag, write the expression DELETE FLAG instead of coordinates')
    running = True
    flags = 10
    """
    Designations:
    F - flag
    Number - the number of bombs surrounding the cage
    * - it is unknown what is there
    _ - empty
    B - bomb
    """
    move = None
    while move is None:
        message = input('Your turn (numbering from 0 to 8), first a row, then a column separated by a space: ')
        if message == 'FLAG':
            set_the_flag()
        elif message == 'DELETEFLAG':
            delete_the_flag()
        else:
            move = list(map(int, message.split()))
    all_field_for_admin = [['0' for i in range(9)] for i in range(9)]
    indexes_mines = []
    for i in range(10):  # creating mines
        while True:
            n, m = random.randint(0, 8), random.randint(0, 8)
            if [n, m] not in indexes_mines and [n, m] != [move[0], move[1]]:
                indexes_mines.append([n, m])
                all_field_for_admin[n][m] = 'B'
                break
    for i in range(9):  # building a board
        for j in range(9):
            if all_field_for_admin[i][j] != 'B':
                cc = 0
                for shift_i in ([-1, 0, 1]):
                    for shift_j in ([-1, 0, 1]):
                        t, p = i + shift_i, j + shift_j
                        if 0 <= (t) <= 8 and 0 <= (p) <= 8 and all_field_for_admin[t][p] == 'B':
                            cc += 1
                all_field_for_admin[i][j] = cc

    not_boom = True
    while not_boom:
        if all_field_for_user[move[0]][move[1]] != 'F':
            if end_of_game():
                break
            if all_field_for_admin[move[0]][move[1]] == 'B':
                not_boom = False
                break
            elif all_field_for_admin[move[0]][move[1]] not in ['B', 0, 'S']:
                all_field_for_user[move[0]][move[1]] = all_field_for_admin[move[0]][move[1]]
            else:  # prescribe 0
                fill(move[0], move[1])

                for m in range(9):
                    for n in range(9):
                        smth = all_field_for_admin
                        if all_field_for_user[m][n] == 'S':
                            all_field_for_user[m][n] = '_'
                        if all_field_for_admin[m][n] == 'S':
                            all_field_for_user[m][n] = '_'
                        elif n - 1 >= 0 and smth[m][n - 1] == 'S' and smth[m][n] not in ['S', 0]:
                            all_field_for_user[m][n] = smth[m][n]
                        elif n + 1 < 9 and smth[m][n + 1] == 'S' and smth[m][n] not in ['S', 0]:
                            all_field_for_user[m][n] = smth[m][n]
                        elif m + 1 < 9 and smth[m + 1][n] == 'S' and smth[m][n] not in ['S', 0]:
                            all_field_for_user[m][n] = smth[m][n]
                        elif m - 1 >= 0 and smth[m - 1][n] == 'S' and smth[m][n] not in ['S', 0]:
                            all_field_for_user[m][n] = smth[m][n]

                        elif n + 1 < 9 and m + 1 < 9 and smth[m + 1][n + 1] == 'S' and smth[m][n] not in ['S', 0]:
                            all_field_for_user[m][n] = smth[m][n]
                        elif n - 1 >= 0 and m - 1 >= 0 and smth[m - 1][n - 1] == 'S' and smth[m][n] not in ['S', 0]:
                            all_field_for_user[m][n] = smth[m][n]
                        elif n - 1 >= 0 and m + 1 < 9 and smth[m + 1][n - 1] == 'S' and smth[m][n] not in ['S', 0]:
                            all_field_for_user[m][n] = smth[m][n]
                        elif m - 1 >= 0 and n + 1 < 9 and smth[m - 1][n + 1] == 'S' and smth[m][n] not in ['S', 0]:
                            all_field_for_user[m][n] = smth[m][n]
            print_user_field()
        else:
            print('You have a flag there')
        if end_of_game():
            break
        move = None
        while move is None:
            message = input('Your turn (numbering from 0 to 8), first a row, then a column separated by a space: ')
            if message == 'FLAG':
                set_the_flag()
            elif message == 'DELETEFLAG':
                delete_the_flag()
            else:
                move = list(map(int, message.split()))

    if not_boom:
        print('You won')
    else:
        print('You lost')
