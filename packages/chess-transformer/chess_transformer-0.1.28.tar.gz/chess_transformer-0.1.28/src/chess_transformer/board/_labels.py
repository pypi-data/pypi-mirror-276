from typing import Sequence, TypeAlias
import chess

piece_symbols = [None, 'P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
symbol_ids = { symbol: i for i, symbol in enumerate(piece_symbols) }

def piece_id_at(board: chess.Board, square: chess.Square) -> int:
  piece = board.piece_at(square)
  return symbol_ids[piece and piece.symbol()]

Label: TypeAlias = Sequence[int]

def encode_board(board: chess.Board) -> Label:
  return [piece_id_at(board, square) for square in chess.SQUARES]

def decode_board(pred: Sequence[int]) -> chess.Board:
  board = chess.Board()
  for square, piece_id in zip(chess.SQUARES, pred):
    symbol = piece_symbols[piece_id]
    board.set_piece_at(square, symbol and chess.Piece.from_symbol(symbol))
  return board

def labels(sans: Sequence[str]) -> Sequence[Label]:
  output = []
  board = chess.Board()
  for san in sans:
    output.append(encode_board(board))
    board.push_san(san)

  return output