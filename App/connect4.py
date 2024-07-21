HEIGHT, WIDTH = 6, 7

P1 = 'O'
P2 = 'X'

def createGrid():
    grid = []
    for i in range(HEIGHT):
        row = [' ' for j in range(WIDTH)]
        grid.append(row)
    return grid

def displayGrid(grid):
    print("------------GRID------------")
    for i in range(HEIGHT):
        for j in range(WIDTH):
            print(grid[i][j], end = ' ')
            if (j != WIDTH - 1):
                print('|', end = ' ')
            else:
                print('')
        if i != HEIGHT - 1:
            print("-"*(((WIDTH-2)*4)+5))
            
    for i in range(7):
        print(i, end = '   ')
    print()

def selectSlot(grid, player, col):
    for i in range(HEIGHT-1):
        if grid[i+1][col] != ' ':
            grid[i][col] = player
            break
        elif i == HEIGHT-2:
            grid[HEIGHT-1][col] = player
            break
    
def checkFullSlot(grid, col):
    if grid[0][col] != ' ':
        return True
    return False

def checkTie(grid):  #assume checkWin used first
    for i in range(WIDTH):
        if grid[0][i] == ' ':
            return False
    return True

##-----------BITWISE OPERATIONS-------------------------

def get_bitmap(grid, player):
    full_grid = ''
    p_grid = ''

    for i in range(WIDTH):
        full_grid += '0'
        p_grid += '0'

        for j in range(HEIGHT):
            if grid[j][i] == ' ':
                full_grid += '0'
                p_grid += '0'
            elif grid[j][i] == player:
                full_grid += '1'
                p_grid += '1'
            else:
                full_grid += '1'
                p_grid += '0'
    
    return int(full_grid, 2), int(p_grid, 2)



def print_bitmap(bit_str):
    print("BitMap")
    for i in range(WIDTH):
        for j in range(WIDTH):
            print(bit_str[i+7*j], end = '')
        print()

def checkWin(pGrid):
    #check horizontal
    m = pGrid & (pGrid >> 7)
    if m & (m >> 14):
        return True, 

    #check vertical 
    m = pGrid & (pGrid >> 1)
    if m & (m >> 2):
        return True

    #check diaganol /
    m = pGrid & (pGrid >> 6)
    if m & (m >> 12):
        return True

    #check anti-diagonal \
    m = pGrid & (pGrid >> 8)
    if m & (m >> 16):
        return True
    
    return False

    
def bit_select_move(full_grid, p_grid, col):
    new_p_grid = full_grid ^ p_grid   #get opponent grid since he is next   
    col = 6 - col
    new_grid = full_grid | (full_grid + (1 << (col*7)))
    return new_grid, new_p_grid


def dec_to_bin(dec):
    bin = 0
    w = 1
    while dec >= 1:
        bin += (dec % 2) * w
        dec = dec // 2
        w *= 10

    return bin

def dec_to_str(dec):
    bin = dec_to_bin(dec)
    str_bin = str(bin)
    if len(str_bin) != WIDTH*WIDTH:
        temp = (WIDTH*WIDTH) - len(str_bin)
        str_bin = ('0'*temp) + str_bin
    
    return str_bin

def  isTie_bitwise(fullgrid):
    value = ''
    for i in range(7):
        value = value + '0'
        value += ('1'*7)

    value = int(value, 2)
    if fullgrid == value:
        return True
    return False

def valid_moves(full_bit):
    lst = []
    col = 6
    full_bit = full_bit >> 5
    # print("bit:", dec_to_str(full_bit))

    for i in range(7):
        if (full_bit & 1) == 0:
            lst.append(col)
        full_bit = full_bit >> 7
        # print('bit:', dec_to_str(full_bit))
        col -= 1

    return lst
    

        

###-----------------------------------------------------------

def getTurn(grid):
    p1_count = 0
    p2_count = 0

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if grid[i][j] == P1:
                p1_count += 1
            elif grid[i][j] == P2:
                p2_count += 1

    if p1_count > p2_count:
        return P2
    return P1


##-----------------------AI-----------------------
def evaluate(bin, player):
    ## player to determine whether user:True or AI:False
    ## +25 points if win
    ## -25 points if lose
    ## 0 points if draw
    ## +2 point for every centre row piece
    ## -2 point for every opp centre row piece
    ## subtract from result no of moves, so higher points for lesser moves
    result = 0

    #check no of moves
    temp_bin = bin
    move_count = 0
    for i in range(49):
        move_count += temp_bin & 0b1
        temp_bin = temp_bin >> 1


    if checkWin(bin):
        result += (25 - move_count)

        if not player:
            return (result * -1), 1
        return result, 1

    #check mid
    mid_bin = bin & 0b111111000000000000000000000
    mid_bin = mid_bin >> 21
    # print("mid_bin:", bitwise.dec_to_str(mid_bin))
    for i in range(6):
        result += (mid_bin & 0b000001)*2
        mid_bin = mid_bin >> 1


    if not player:
        return (result * -1), 2
    return result, 2

def minimax(f_grid, p_grid, depth, maxTurn, maxDepth, alpha, beta):
    score, type = evaluate(p_grid, maxTurn)
    if type == 1: #win/lose
        # bitwise.print_bitmap(bitwise.dec_to_str(p_grid)) 
        # print("winlose score:", score) 
        # print("winner User:", maxTurn)
        return score
    
    if depth > maxDepth:
        # bitwise.print_bitmap(bitwise.dec_to_str(p_grid)) 
        # print("score:", score)
        return score
    
    if isTie_bitwise(f_grid):
        # bitwise.print_bitmap(bitwise.dec_to_str(p_grid)) 
        # print("score:", score)
        return score
    

    if maxTurn:  #AI turn
        maxValue = -float("inf")
        valid_moves_arr = valid_moves(f_grid)
        for col in valid_moves_arr:
            temp_f_grid = f_grid
            temp_p_grid = p_grid
            f_grid, p_grid = bit_select_move(f_grid, p_grid, col)
            value = minimax(f_grid, p_grid, depth+1, not maxTurn, maxDepth, alpha, beta)
            f_grid = temp_f_grid
            p_grid = temp_p_grid
            maxValue = max(maxValue, value)
            # cprint(f"maxValue: {str(maxValue)}", "green")

            #alpha-beta pruning
            alpha = max(alpha, maxValue)
            if beta <= alpha:
                break

        return maxValue
    
    else:  #user turn
        minValue = float("inf")
        valid_moves_arr = valid_moves(f_grid)
        for col in valid_moves_arr:
            temp_f_grid = f_grid
            temp_p_grid = p_grid
            f_grid, p_grid = bit_select_move(f_grid, p_grid, col)
            value = minimax(f_grid, p_grid, depth+1, not maxTurn, maxDepth, alpha, beta)
            f_grid = temp_f_grid
            p_grid = temp_p_grid
            minValue = min(minValue, value)
            # cprint(f"minValue: {str(minValue)}", "red")

            #alpha-beta pruning
            beta = min(beta, minValue)
            if beta <= alpha:
                break

        return minValue
    

def bestMove(f_grid, p_grid, depth):
    best_value = -1000
    best_move = -1
    mid_col_value = -1000

    valid_moves_arr = valid_moves(f_grid)
    for col in valid_moves_arr:
        temp_f_grid = f_grid
        temp_p_grid = p_grid
        f_grid, p_grid = bit_select_move(f_grid, p_grid, col)
        move_value = minimax(f_grid, p_grid, 0, False, depth, -float("inf"), float("inf"))
        f_grid = temp_f_grid
        p_grid = temp_p_grid
        
        if col == 3:
            mid_col_value = move_value

        if move_value > best_value:
            best_value = move_value
            best_move = col

        # cprint(f"col: {str(col)}", "yellow")
        # cprint(f"move_value: {str(move_value)}", "yellow")
        # cprint(f"best_move: {str(best_move)}", "yellow")

    if best_value == mid_col_value:
        best_move = 3
        
    return best_move
