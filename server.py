import socket
import random

"""обавить приветствие в начале и перенос строки к каждой реплике"""


def start_game():
    c[0].send(bytes("your turn. choose a word \n", encoding='UTF-8'))
    c[1].send(bytes("waiting for player 1 to choose a word \n", encoding='UTF-8'))
    c[2].send(bytes("waiting for player 1 to choose a word \n", encoding='UTF-8'))
    data = []
    while True:
        data.append(c[0].recv(1024))
        if data != []:
            break
    return data[0].decode("UTF-8")


def guess_letter(f):
    global guessed, guessed_letters, ans
    c[f].send(bytes("your turn. choose a letter \n", encoding='UTF-8'))
    c[0].send(bytes("waiting for player to choose a letter \n", encoding='UTF-8'))
    c[-f].send(bytes("waiting for player 2 to choose a letter \n", encoding='UTF-8'))
    letter = []
    while True:
        letter.append(c[f].recv(1024))
        if letter != [] and letter[0].decode("UTF-8") not in guessed_letters:
            break
        if letter[0].decode("UTF-8") in guessed_letters:
            c[f].send(bytes(
                "this letter has already been tried, choose another. your turn\n you tried these letters: " + ' '.join(
                    guessed_letters) + " \n", encoding='UTF-8'))
            letter = []
    letter = letter[0].decode("UTF-8")
    c[0].send(bytes("player chose letter " + letter + " \n", encoding='UTF-8'))
    c[-f].send(bytes("player 2 chose letter " + letter + " \n", encoding='UTF-8'))
    t = False
    guessed_letters.append(letter)
    if letter in ans:
        mes = "Correct! there's " + letter + " in the word \n"
        for i in range(len(ans)):
            if ans[i] == letter:
                guessed[i] = letter
        t = True
    else:
        mes = "Wrong( there isn't " + letter + " in the word\n"
    c[f].send(bytes(mes, encoding='UTF-8'))
    c[-f].send(bytes(mes, encoding='UTF-8'))
    return t


sock = socket.socket()
sock.bind(('', 9092))
sock.listen(3)
c = []
data = []
f = 0
a = [
    " _________________\n_|        |       \n_|        O       \n_|        |       \n_|       /|\      \n_|        |       \n_|       / \      \n_|      /   \     \n",
    " _________________\n_|        |       \n_|        O       \n_|        |       \n_|       /|\      \n_|        |       \n_|         \      \n_|          \     \n",
    " _________________\n_|        |       \n_|        O       \n_|        |       \n_|       /|\      \n_|        |       \n_|                \n_|                \n",
    " _________________\n_|        |       \n_|        O       \n_|        |       \n_|        |\      \n_|        |       \n_|                \n_|                \n",
    " _________________\n_|        |       \n_|        O       \n_|        |       \n_|        |       \n_|        |       \n_|                \n_|                \n",
    " _________________\n_|        |       \n_|        O       \n_|                \n_|                \n_|                \n_|                \n_|                \n",
    " _________________\n_|        |       \n_|                \n_|                \n_|                \n_|                \n_|                \n_|                \n"
]
while True:
    conn, addr = sock.accept()
    c.append(conn)
    conn.send(bytes("Hello! You have joined The gallows game! we're waiting for more players\n", encoding='UTF-8'))
    if len(c) == 3:
        break

while True:
    for i in c:
        i.send(bytes("your turn. ready to begin a new game? y/n\n", encoding='UTF-8'))
        data = []
        while True:
            data.append(i.recv(1024))
            if data[-1].decode("UTF-8") == "y":
                i.send(bytes("waiting for other players\n", encoding='UTF-8'))
                break
            else:
                i.send(bytes("then good bye\n", encoding='UTF-8'))
                i.close()
                c.remove(i)
                break
        if len(c) < 3:
            break
    if len(c) < 3:
        for i in c:
            i.send(bytes("another player left the game. good bye\n", encoding='UTF-8'))
            i.close()
        break
    random.shuffle(c)
    ans = start_game()
    guessed_letters = []
    guessed = ["_" for i in range(len(ans))]
    k = 0
    f = 1
    win = False
    while k < 6:
        if not guess_letter(f):
            k += 1
        if "_" not in guessed:
            win = True
            break
        f *= -1
        for i in c:
            i.send(bytes(' '.join(guessed) + "\n" + a[6 - k] + " \n", encoding='UTF-8'))
    if win:
        for i in c:
            i.send(bytes("You won! the word was " + ans + " \n", encoding='UTF-8'))
    else:
        for i in c:
            i.send(bytes("You lost( the word was " + ans + " \n", encoding='UTF-8'))

for i in c:
    i.close()
