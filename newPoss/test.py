import chess
import exp
from exp import MCTS

board = chess.Board()
print(board)
player = MCTS(board)
best_move = player.select_move()
board.push_san(best_move)
print(board)