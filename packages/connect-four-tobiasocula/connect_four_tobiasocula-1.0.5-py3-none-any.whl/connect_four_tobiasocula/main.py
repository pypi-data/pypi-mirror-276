import numpy as np

def play():

    def print_frame(frame):
        
        for row in frame:
            print(7*'|---'+'|')
            for el in row:
                print(f'| {el} ',end='')
            print('|')
        print(7*'|---'+'|')
        print('  A   B   C   D   E   F   G')

    def update_frame(player, play, frame, letters):
        
        x = letters.index(play)
        y = 5
        while frame[y][x]!=' ':
            y-=1
        frame[y][x] = player
        return frame

    def won(player, frame):

        def updown(y,x):
            local_array = []
            for i in range(1,4):
                try:
                    local_array.append(frame[y+i][x]==frame[y][x]==str(player))
                except:
                    return False
            return all(local_array)
        def leftright(y,x):
            local_array = []
            for i in range(1,4):
                try:
                    local_array.append(frame[y][x+i]==frame[y][x]==str(player))
                except:
                    return False
            return all(local_array)
        def diagonal_1(y,x):
            local_array = []
            for i in range(1,4):
                try:
                    local_array.append(frame[y+i][x+i]==frame[y][x]==str(player))
                except:
                    return False
            return all(local_array)
        def diagonal_2(y,x):
            local_array = []
            for i in range(1,4):
                try:
                    local_array.append(frame[y+i][x-i]==frame[y][x]==str(player))
                except:
                    return False
            return all(local_array)
        
        for y in range(6):
            for x in range(7):
                if (
                    leftright(y,x) or
                    updown(y,x) or
                    diagonal_1(y,x) or
                    diagonal_2(y,x)
                ):
                    return player
        return False

    player = 1
    frame = np.full((6,7),' ')
    counter = 0
    
    while True:

        print_frame(frame)
        letters = 'abcdefg'
        player = 1 if counter%2==0 else 2

        while True:
            play = input(f'Player {player}\'s turn:').lower()
            if play in letters:
                index = letters.index(play)
                if frame[0][index]!=' ':
                    print('Column', play.capitalize(), 'is full!')
                else:
                    break
            else:
                print('No valid column!')

        frame = update_frame(player, play, frame, letters)
        counter+=1

        if bool(won(player, frame)):
            print_frame(frame)
            print('Player', player, 'has won!')
            break
        elif counter==42:
            print_frame(frame)
            print('Draw!')
            break