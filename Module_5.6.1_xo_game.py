import random

tilefield = [1, 2, 3, 4, 5, 6, 7, 8, 9]
player1, player2, score1, score2 = None, None, 0, 0
turncount = 0
roundcount = 1

def refreshfield():
    global tilefield
    global turncount
    tilefield = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    turncount = 0

##################################

def gamefield():
    print('\n')
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(tilefield[0], tilefield[1], tilefield[2]))
    print('\t_____|_____|_____')

    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(tilefield[3], tilefield[4], tilefield[5]))
    print('\t_____|_____|_____')

    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(tilefield[6], tilefield[7], tilefield[8]))
    print('\t     |     |')
    print("\n")

#################################

def playerturn(curplayer):
    while True:
        print(f'ROUND: {roundcount}')
        curchoice = input(f"<{curplayer}>, IT'S YOUR TURN. CHOOSE EMPTY TILE: ")
        if not curchoice.isdigit():
            print('\t*Invalid input. You need choose 1 - 9 tile*')
            continue

        curchoice = int(curchoice)

        if curchoice not in range(1, 10):
            print('\t*Invalid input. You need choose 1 - 9 tile*')
            continue

        if tilefield[curchoice - 1] == 'x' or tilefield[curchoice - 1] == 'o':
            print('\t*Invalid input. You need choose empty tile*')
            continue

        curchoice -= 1
        return curchoice

##################################

def comp_choice():
    while True:
        compch = str(random.choice(tilefield))
        if compch.isdigit():
            return compch

##################################

def wincheck():
    winfield = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    for i in winfield:
        if tilefield[i[0]] == tilefield[i[1]] == tilefield[i[2]]:
            return tilefield[i[0]]

    return False

####################################

def nextround():
    while True:
        nextround = input('DO YOU WANT THE NEXT ROUND OF CURRENT GAME? [y/n]: ')
        if nextround == 'y':
            refreshfield()
            gamefield()
            return True
        if nextround == 'n':
            refreshall()
            return False
        else:
            print('\t*Invalid input.*')

##################################

def scoreboard():
    global player1
    global player2
    global score1
    global score2
    print('\t--------------------------------------\n'
          '\t            SCORE BOARD\n'
          '\t          <CROSSES ZEROES>\n'
          f'\t\t\n  <x> PLAYER <{player1}> SCORE: {score1}'
          f'\t\t\n  <o> PLAYER <{player2}> SCORE: {score2}\n'
          '\t--------------------------------------')

##################################

def refreshall():
    global player1
    global player2
    global score1
    global score2
    global tilefield
    global turncount
    global roundcount
    player1, player2, score1, score2, turncount, roundcount = None, None, 0, 0, 0, 1
    tilefield = [1, 2, 3, 4, 5, 6, 7, 8, 9]

##################################

def start_2players_game():
    global player1
    global player2
    global score1
    global score2
    global turncount
    global roundcount

    player1 = input('\nENTER <x> PLAYER NAME: ')
    player2 = input('ENTER <o> PLAYER NAME: ')

    gamefield()

    while True:
        if turncount % 2 == 0:
            curplayersign = 'x'
            curplayer = player1
        else:
            curplayersign = 'o'
            curplayer = player2
        turncount += 1

        tilefield[playerturn(curplayer)] = curplayersign

        gamefield()

        if wincheck() == 'x':
            print(f'* AND THE WINNER IS <{curplayer}>! *')
            score1 += 1
            scoreboard()
            if nextround():
                roundcount += 1
                continue
            break

        if wincheck() == 'o':
            print(f'* AND THE WINNER IS <{curplayer}>! *')
            score2 += 1
            scoreboard()
            if nextround():
                roundcount += 1
                continue
            break

        if turncount == 9:
            print(f"* DRAW *")
            scoreboard()
            if nextround():
                roundcount += 1
                continue
            break

        else:
            continue

####################################

def start_single_game():
    global player1
    global player2
    global score1
    global score2
    global turncount
    global roundcount

    player1 = input('\nENTER <x> PLAYER NAME: ')
    player2 = 'COMPLUCTER'

    gamefield()

    while True:
        if turncount % 2 == 0:
            curplayersign = 'x'
            curplayer = player1
            tilefield[playerturn(curplayer)] = curplayersign
        else:
            curplayersign = 'o'
            curplayer = player2
            x = int(comp_choice()) - 1
            tilefield[x] = curplayersign
            print(f'<{player2}> CHOSE TILE NUMBER {x + 1}')
        turncount += 1


        gamefield()

        if wincheck() == 'x':
            print(f'* AND THE WINNER IS <{curplayer}>! *')
            score1 += 1
            scoreboard()
            if nextround():
                roundcount += 1
                continue
            break

        if wincheck() == 'o':
            print(f'* AND THE WINNER IS <{curplayer}>! *')
            score2 += 1
            print(f'<{curplayer}>: hehe')
            scoreboard()
            print('')
            if nextround():
                roundcount += 1
                continue
            break

        if turncount == 9:
            print(f"* DRAW *")
            scoreboard()
            if nextround():
                roundcount += 1
                continue
            break

        else:
            continue


###################################


def gamemodchoice():
    refreshall()

    while True:
        print('\n'
              '\t--------------------------------------------------\n'
              '\t                   WELLCOME TO\n'
              '\t                <CROSSES ZEROES>\n\n'
              '\t(tic tak toe cosmic adventure distraction edition)\n'
              '\t--------------------------------------------------')
        print('1 RULES OF THE GAME\n'
              '2 FOR SINGLE GAME WITH <COMPLUCTER>\n'
              '3 FOR PLAY 2 PLAYERS MODE\n'
              '4 FOR QUIT')

        gamemod = input('CHOOSE GAME MODE: ')

        if not gamemod.isdigit():
            print('\t*Invalid input.*')
            continue

        gamemod = int(gamemod)

        if gamemod not in range(1, 5):
            print('\t*Invalid input.*')
            continue

        if gamemod == 1:
            print("\n<CROSSES ZEROES> RULES"
                  "\n1. The game is played on a grid that's 3 tiles by 3 tiles."
                  "\n2. You are <x>, your friend is <o>, or vice versa. Players take turns putting their marks in empty tiles."
                  "\n3. The first player to get 3 of marks in a row (up, down, across, or diagonally) is the winner."
                  "\n4. When all 9 tiles are full, the game is over. If no player has 3 marks in a row, the game ends in a draw.")
            pause = input('\nPRESS ENTER TO BACK IN MAIN MENU: ')
            if pause == 'hehe':
                print(f'<COMPLUCTER>: hehe')

            continue
        if gamemod == 2:
            start_single_game()
        if gamemod == 3:
            start_2players_game()
        if gamemod == 4:
            print('\n')
            break



gamemodchoice()
