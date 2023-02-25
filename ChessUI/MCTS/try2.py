import chess
import math
import random

board = chess.Board()

print(board)

board.push_san('e4')
print(board)
print()
print(board.legal_moves)
print()
board.push_san('e5')
print(board)
print()
board.push_san('Bc4')
print(board)
print(board.legal_moves)
print()

board.push_san('Nc6')
print(board)
print()
board.push_san('Qf3')
print(board)
print(board.legal_moves)
print()
board.push_san('Nge7')
print(board)
print()

class Node:
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.wins = 0
        self.visits = 0
    
    def __str__(self) -> str:
        return f'state = \n{self.state}\nwins = {self.wins}, visits = {self.visits}'

    def ucb_score(self):
        if self.visits == 0:
            return float('inf')
        
        return (self.wins / self.visits) + 1.4 * math.sqrt(2 * math.log(self.visits) / self.visits)

    def expand(self):
        # print(f'expansion \n{self.state}')
        legal_moves = list(self.state.legal_moves)
        for move in legal_moves:
            new_state = self.state.copy()
            new_state.push(move)
            self.children[move] = Node(new_state, self)

    def select_child(self):
        #print(f'selection \n{self.state}')
        best_score = float('-inf')
        best_move = None
        for move, child in self.children:
            score = self.ucb_score()
            if score > best_score:
                best_score = score
                best_move = move
        # print(f'best_child = \n{best_child}')
        return best_move
    
    def update(self, result):
        #print(f'updation \n{self.state} \nresult = {result}')
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.update(result)

class MCTS:
    def __init__(self, state):
        self.root = Node(state)

    def select_move(self, iterations = 100):
        node = self.root
        for i in range(iterations):
            if node.visits == 0 or node.visits == 1:
                node.expand()
                for move, child in node.children:
                    result = self.simulate(child.state.copy())
                    child.update(result)

                # print(f'after expansion \n{node}')
            else:
                node = node.select_child()

            # if i % 10 == 0:
            #     print(f'selected state = \n{node.state}, i = {i/10}')
            
            # print(node.parent)
            # result = self.simulate(node.parent.state.copy())
            # node.update(result)

        best_move = self.root.select_child()
        print(f'best move = \n{best_move}')
        return best_move.state
    
    def simulate(self, state):
        #print(f'simulation \n{state}')
        game_over = False
        i = 0
        while not game_over:
            if i % 20 == 0:
                # print(f'state = \n{state}, i = {i/20}')
                pass

            legal_moves = list(state.legal_moves)
            # print(legal_moves)
            if not legal_moves:
                if state.is_checkmate():
                    if state.turn:
                        return 0
                    else:
                        return 1
                else:
                    return 0.5
            move = random.choice(legal_moves)
            state.push(move)
            game_over = state.is_game_over()
        # print(f'final state = \n{state} and {state.result()}')
        if state.result() == "1-0":
            return 1
        elif state.result() == "0-1":
            return 0
        else:
            return 0.5

player = MCTS(board)
best_move = player.select_move()
print(f'main best move = \n{best_move}')
board.push(best_move)
print(board)
