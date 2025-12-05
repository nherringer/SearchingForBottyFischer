from BoardSquare import BoardSquare
import GeneralDicts

class ChessBoard:
    '''Class to represent the chess board and its state.'''
    def __init__(self):
        self.whose_turn = "White"
        self.color_num = GeneralDicts.Color_Num[self.whose_turn]
        self.Board = {}
        self.BoardsRunningList = {}
        self.turn_number = 0
        self.terminal_row_order = ['R','N','B','Q','K','B','N','R']
        self.mid_rows_nums = [4,5]
        self.terminal_row_support = [0, 1, 1, 1, 1, 1, 1, 0]
        self.pawn_row_support = [1, 1, 1, 4, 4, 1, 1, 1]
        self.after_pawn_row_support = [1, 2, 3, 2, 2, 3, 2, 1]
        
    def game_start(self):
        self.Board.update({f'{l}1': BoardSquare(f'{l}1', self.terminal_row_support[p],p+1) for p,l in enumerate(GeneralDicts.Let_Num.keys())})
        self.Board.update({f'{l}2': BoardSquare(f'{l}2', self.pawn_row_support[p],p+9) for p,l in enumerate(GeneralDicts.Let_Num.keys())})
        self.Board.update({f'{l}3': BoardSquare(f'{l}3', self.after_pawn_row_support[p],0) for p,l in enumerate(GeneralDicts.Let_Num.keys())})
        self.Board.update({f'{l}{p}': BoardSquare(f'{l}{p}', 0, 0) for l in GeneralDicts.Let_Num.keys() for p in self.mid_rows_nums})
        self.Board.update({f'{l}6': BoardSquare(f'{l}6', self.after_pawn_row_support[p]*GeneralDicts.Color_Num["Black"],0) for p,l in enumerate(GeneralDicts.Let_Num.keys())})
        self.Board.update({f'{l}7': BoardSquare(f'{l}7', self.pawn_row_support[p]*GeneralDicts.Color_Num["Black"],p+17) for p,l in enumerate(GeneralDicts.Let_Num.keys())})
        self.Board.update({f'{l}8': BoardSquare(f'{l}8', self.terminal_row_support[p]*GeneralDicts.Color_Num["Black"],p+25) for p,l in enumerate(GeneralDicts.Let_Num.keys())})


    def visualize_board(self):
        print(f'Turn Number: {self.turn_number}')
        print("    ---------------------------------")
        for n in reversed(range(1,9)):
            print(f"{n}   "
                 f"| {GeneralDicts.uID_props[self.Board[f'a{n}'].occupant_uID]['piece_type']} |"\
                 f" {GeneralDicts.uID_props[self.Board[f'b{n}'].occupant_uID]['piece_type']} |"\
                 f" {GeneralDicts.uID_props[self.Board[f'c{n}'].occupant_uID]['piece_type']} |"\
                 f" {GeneralDicts.uID_props[self.Board[f'd{n}'].occupant_uID]['piece_type']} |"\
                 f" {GeneralDicts.uID_props[self.Board[f'e{n}'].occupant_uID]['piece_type']} |"\
                 f" {GeneralDicts.uID_props[self.Board[f'f{n}'].occupant_uID]['piece_type']} |"\
                 f" {GeneralDicts.uID_props[self.Board[f'g{n}'].occupant_uID]['piece_type']} |"\
                 f" {GeneralDicts.uID_props[self.Board[f'h{n}'].occupant_uID]['piece_type']} |"\
            )
            print("    ---------------------------------")
        print("                                     ")
        print("      a   b   c   d   e   f   g   h")
