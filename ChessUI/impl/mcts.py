import chess
import random
import math

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        
    def expand(self):
        print(f'expansion \n{self.state}')
        legal_moves = list(self.state.legal_moves)
        print(legal_moves)
        for move in legal_moves:
            new_state = self.state.copy()
            new_state.push(move)
            print(new_state)
            #child = Node(new_state, self)
            self.children.append(Node(new_state, self))

    def ucb_score(self, exploration_factor = 1.4):
        if self.visits == 0:
            return float('inf')
        
        return (self.wins / self.visits) + exploration_factor*  math.sqrt(2 * math.log(self.visits) / self.visits)

    def select_child(self, exploration_factor=1.4):
        #print(f'selection \n{self.state}')
        best_child = None
        best_score = float("-inf")
        for child in self.children:
            child.visits += 1
            score = self.ucb_score(exploration_factor)
            if score > best_score:
                best_child = child
                best_score = score
        print(f'best_child = \n{best_child}')
        return best_child
        
    def update(self, result):
        #print(f'updation \n{self.state} \nresult = {result}')
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.update(result)
        
class MCTS:
    def __init__(self, state):
        self.root = Node(state)
        
    def select_move(self, iterations=100):
        node = self.root
        for i in range(iterations):  
            # while node.children:
            #     node = node.select_child()
            #     print(node)
            if node.visits == 0:
                node.expand()
                #print(node.children)
            else:
                node = node.select_child()
            
            result = self.simulate(node.state)
            node.update(result)
        best_move = None
        most_visits = -1
        for child in self.root.children:
            if child.visits > most_visits:
                best_move = child.state.peek()
                most_visits = child.visits
        print(f'best_move \n{best_move}')
        return best_move
    
    def simulate(self, state):
        #print(f'simulation \n{state}')
        game_over = False
        while not game_over:
            legal_moves = list(state.legal_moves)
            if not legal_moves:
                if state.is_checkmate():
                    if state.turn:
                        return -1
                    else:
                        return 1
                else:
                    return 0
            move = random.choice(legal_moves)
            state.push(move)
            game_over = state.is_game_over()
        #print(state)
        if state.result() == "1-0":
            return 1
        elif state.result() == "0-1":
            return -1
        else:
            return 0
