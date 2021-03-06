"""
Code for easy gamemode in Tic
Tac Toe where two UR3 robots go
against eachother... like 2 year olds..

Code by: Kevin Moen Storvik
Version: 1.1
"""
from modbus_communication import ModbusClient
from gamechecker import GameChecker
import random
import cv2
import time

array = [1, 2, 3, 4, 5, 6, 7, 8, 9]

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

drawboard = ['2', '5', '6', '10', '11']

# Main loop
if __name__ == '__main__':
    UR31 = ModbusClient(ip='158.38.140.249')
    UR32 = ModbusClient(ip='158.38.140.250')
    cap = cv2.VideoCapture(1)

    game = GameChecker(capture=cap, watch=True)

    players = [UR31, UR32]
    playerstest = ["player1", "player2"]

    startplayer = random.randint(0, 1)  # Decides who starts
    turn = startplayer

    while UR31.isConnected() and UR32.isConnected():
        clean = game.cleanBoard()

        if not clean:
            UR32.sendInt(address=143, value=0)
            time.sleep(1)
            UR32.sendInt(address=143, value=69)
            time.sleep(1)
            UR32.wait_feedback()
        else:
            print("Machine idle and board clean...")

        # making sure our robot is 'reset'
        UR31.sendInt(address=141, value=0)
        time.sleep(1)
        print("Drawing board.")
        UR31.sendInt(address=141, value=20)
        time.sleep(1)
        UR31.wait_feedback_drawboard()

        turnstaken = 0

        for x in range(len(numbers)):

            winnerFound = game.didSomeoneWin()

            if winnerFound:
                print("Winner found.")
                break

            turnstaken += 1
            player = players[turn]
            turn = (turn + 1) % len(players)

            selection = random.randint(0, len(numbers) - 1)
            goner = numbers.pop(selection)
            print(goner)

            print(str(player) + " picks " + goner)

            player.sendInt(address=143, value=int(goner))
            time.sleep(1)
            player.wait_feedback()

        print("Turns taken " + str(turnstaken))

        wincombo = game.getWinCombo()

        print(wincombo)

        UR32.sendInt(address=150, value=wincombo)
        time.sleep(1)
        break
    game.stop()
    UR31.close()
    UR32.close()
