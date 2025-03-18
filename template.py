import utils
import time
import copy

class PlayerAI:
    
    def __init__(self):
        import random
        
        self.table = {}
        self.zobrist_table = [[[random.getrandbits(64) for k in range(2)] for j in range(6)] for i in range(6)]
        
    def hash(self, board):
        zobrist_key = 0
        for i in range(6):
            for j in range(6):
                if board[i][j] == 'B':
                    zobrist_key ^= self.zobrist_table[i][j][0]
                if board[i][j] == 'W':
                    zobrist_key ^= self.zobrist_table[i][j][1]
        return zobrist_key
    
    def make_move(self, board):
       
        depth = 1
        currentBest = None
        start_time = time.time()
        while True:
            _, currentBest = self.minimax(board, depth, float('-inf'), float('inf'), True, start_time)
            if time.time() - start_time >= 2.9:               
                
                break
            print(f'depth = {depth}')
            depth += 1
            
        return currentBest
    def next_move(self, board, ):
        moves = []
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] == 'B'):
                    if utils.is_valid_move(board, [i, j], [i + 1, j]):
                        moves.append(([i, j], [i + 1, j]))
                    if utils.is_valid_move(board, [i, j], [i + 1, j + 1]):
                        moves.append(([i, j], [i + 1, j + 1]))
                    if utils.is_valid_move(board, [i, j], [i + 1, j - 1]):
                        moves.append(([i, j], [i + 1, j - 1]))
        return moves
    
    def is_winning_position(self, board):
        
        for j in range(6):
            if board[4][j] == 'B':
                return True
        return False
     
    def get_winning_move(self, board):
        for j in range(6):
            if board[4][j] == 'B':
                if j - 1 >= 0:
                    return ([4, j], [5, j - 1])
                if board[5][j] != 'W':
                    return ([4, j], [5, j])
                return ([4, j], [5, j + 1])
        return ([0,0], [0,0])
    
    def minimax(self, board, depth, alpha, beta, maxPlayer, start_time):
        if utils.is_game_over(board):
            return self.final_result(board), None
        if depth == 0:
            return self.evaluation(board), None
        #if maxPlayer and self.is_winning_position(board):
        #    return 100, self.get_winning_move(board)
        if maxPlayer:
            if time.time() - start_time > 2.9:
                return 0, None
            
            key = self.hash(board)
            if key in self.table:
                value = self.table[key]
                if value[2] >= depth:
                    #print('retrieving from table')
                    return value[0], value[1]
            
            maxEval = float('-inf')
            bestMove = None
            nextMoves = self.next_move(board)
            # for move in nextMoves:
            #     if move[0][0] == 4 and move[1][0] == 5:
            #         return 100, move
                
            nextStates = list(map(lambda move: utils.state_change(board, move[0], move[1], False), nextMoves))
            nextEval = list(map(lambda state: self.evaluation(state), nextStates))
            combined = zip(nextMoves, nextStates, nextEval)
            combined = sorted(combined, key=lambda x : x[2], reverse=True)
            for elem in combined:
                #new_state = utils.state_change(board, moves[0], moves[1], False)
                currentEval, _ = self.minimax(elem[1], depth - 1, alpha, beta, False, start_time)
                if currentEval > maxEval:
                    maxEval = currentEval
                    bestMove = elem[0]
                alpha = max(alpha, currentEval)
                if beta <= alpha:
                    break
            
            self.table[key] = [maxEval, bestMove, depth]
            #self.print_table()
            return maxEval, bestMove
        
        else:
            if time.time() - start_time > 2.9:
                return 0, None
            
            key = self.hash(board)
            if key in self.table:
                value = self.table[key]
                if value[2] >= depth:
                    #print('retrieving from table')
                    return value[0], value[1]
            
            minEval = float('inf')
            bestMove = None
            inverted_board = utils.invert_board(board, False)
            nextMoves = self.next_move(inverted_board)
            nextStates = list(map(lambda move: utils.state_change(inverted_board, move[0], move[1], False), nextMoves))
            nextStates = list(map(lambda state: utils.invert_board(state, False), nextStates))
            nextEval = list(map(lambda state: self.evaluation(state), nextStates))
            combined = zip(nextMoves, nextStates, nextEval)
            combined = sorted(combined, key=lambda x : x[2])
            for elem in combined:
                currentEval, _ = self.minimax(elem[1], depth - 1, alpha, beta, True, start_time)
                if currentEval < minEval:
                    minEval = currentEval
                    bestMove = elem[0]
                beta = min(beta, currentEval)
                if beta <= alpha:
                    break
            
            self.table[key] = [minEval, bestMove, depth]
            #self.print_table()
            return minEval, bestMove
        
    def final_result(self, board):
        winner = 'black'
        for j in range(len(board)):
            if board[0][j] == 'W':
                winner = 'white'
                return -30
        bcount = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 'B':
                    bcount += 1
        if bcount == 0:
            winner = 'white'
        if winner == 'black':
            return 30
        else:
            return -30
    
    def evaluation(self, board):
    # Define a constant that represents the value of controlling the center of the board.
        # Define variables to keep track of the scores of each player.
        black_score = 0
        white_score = 0
        # Compute the distance from each player's pawns to the opponent's goal line.
        for i in range(6):
            for j in range(6):
                if board[i][j] == 'B':
                    black_score += i
                elif board[i][j] == 'W':
                    white_score += 5 - i
        for i in range(6):
            for j in range(6):
                if board[i][j] == 'B' and i > 3:
                    black_score += 3 * i
                elif board[i][j] == 'W' and i < 3:
                    white_score += 3 * (5 - i)
        # Compute the difference in the number of pawns between the two players.
        black_pawns = board.count('B')
        white_pawns = board.count('W')
        pawn_count_diff = black_pawns - white_pawns
        # Compute the mobility of each player's pawns.
        black_mobility = len(self.next_move(board))
        white_mobility = len(self.next_move(utils.invert_board(board, False)))
        mobility_diff = black_mobility - white_mobility
        # Compute the control of the center of the board.
        black_center_control = 0
        white_center_control = 0
        for i in range(2, 4):
            for j in range(2, 4):
                if board[i][j] == 'B':
                    black_center_control += 1
                elif board[i][j] == 'W':
                    white_center_control += 1
        center_control_diff = black_center_control - white_center_control
        # Compute the total score by weighting the pawn count, distance, mobility, and center control differences.
        return 3 * pawn_count_diff + 0.1 * mobility_diff + 0.5 * center_control_diff + black_score - white_score
    
    
class PlayerNaive:
    ''' A naive agent that will always return the first available valid move '''
    def make_move(self, board):
        return utils.generate_rand_move(board)


##########################
# Game playing framework #
##########################
if __name__ == "__main__":

    # public test case 1
    res1 = utils.test([['B', 'B', 'B', 'B', 'B', 'B'], ['_', 'B', 'B', 'B', 'B', 'B'], ['_', '_', '_', '_', '_', '_'], ['_', 'B', '_', '_', '_', '_'], ['_', 'W', 'W', 'W', 'W', 'W'], ['W', 'W', 'W', 'W', 'W', 'W']], PlayerAI())
    assert(res1 == True)

    # public test case 2
    res2 = utils.test([['_', 'B', 'B', 'B', 'B', 'B'], ['_', 'B', 'B', 'B', 'B', 'B'], ['_', '_', '_', '_', '_', '_'], ['_', 'B', '_', '_', '_', '_'], ['W', 'W', 'W', 'W', 'W', 'W'], ['_', '_', 'W', 'W', 'W', 'W']], PlayerAI())
    assert(res2 == True)

    # public test case 3
    res3 = utils.test([['_', '_', 'B', 'B', 'B', 'B'], ['_', 'B', 'B', 'B', 'B', 'B'], ['_', '_', '_', '_', '_', '_'], ['_', 'B', 'W', '_', '_', '_'], ['_', 'W', 'W', 'W', 'W', 'W'], ['_', '_', '_', 'W', 'W', 'W']], PlayerAI())
    assert(res3 == True)

    # template code for question 2 and question 3
    # generates initial board
    board = utils.generate_init_state()
    # game play
    res = utils.play(PlayerAI(), PlayerNaive(), board) # PlayerNaive() will be replaced by a baby agent in question 2, or a base agent in question 3
    print(res) # BLACK wins means your agent wins. Passing the test case on Coursemology means your agent wins.
