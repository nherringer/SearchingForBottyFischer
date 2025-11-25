from BoardSquare import BoardSquare

class ChessBoard:
    def __init__(self):
        self.whose_turn = "White"
        self.Color_Num = {"White": 1,
                        "Black": -1}
        self.color_num = self.Color_Num[self.whose_turn]
        self.Board = {}
        self.BoardsRunningList = {}
        self.Piece_ID = {' ': 0,
                     'P': 1,
                     'B': 2,
                     'N': 3,
                     'R': 4,
                     'Q': 5,
                     'K': 6}
        self.Piece_ID_Inv = {v: k for k,v in self.Piece_ID.items()}
        self.ID_Values = {0: 0,
                           1: 1,
                           2: 3,
                           3: 3,
                           4: 5,
                           5: 9,
                           6: 40}
        self.ID_Values_Inv = {v: k for k,v in self.ID_Values.items()}
        self.Piece_Values = {" ": 0,
                            "P": 1,
                            "N": 3,
                            "B": 3,
                            "R": 5,
                            "Q": 9,
                            "K": 40}
        self.Piece_Values_Inv = {v: k for k,v in self.Piece_Values.items()}
        self.Let_Num = {'a': 1,
                      'b': 2,
                      'c': 3,
                      'd': 4,
                      'e': 5,
                      'f': 6,
                      'g': 7,
                      'h': 8}
        self.Num_Let = {v: k for k,v in self.Let_Num.items()}

        self.turn_number = 0
        self.terminal_row_order = ['R','N','B','Q','K','B','N','R']
        self.mid_rows_nums = [4,5]
        self.terminal_row_support = [0, 1, 1, 1, 1, 1, 1, 0]
        self.pawn_row_support = [1, 1, 1, 4, 4, 1, 1, 1]
        self.after_pawn_row_support = [1, 2, 3, 2, 2, 3, 2, 1]
        
    def game_start(self):
        self.Board.update({f'{l}1': BoardSquare(f'{l}1', self.Piece_ID[self.terminal_row_order[p]], self.terminal_row_support[p],p+1) for p,l in enumerate(self.Let_Num.keys())})
        self.Board.update({f'{l}2': BoardSquare(f'{l}2', self.Piece_ID['P'], self.pawn_row_support[p],p+9) for p,l in enumerate(self.Let_Num.keys())})
        self.Board.update({f'{l}3': BoardSquare(f'{l}3', self.Piece_ID[' '], self.after_pawn_row_support[p],0) for p,l in enumerate(self.Let_Num.keys())})
        self.Board.update({f'{l}{p}': BoardSquare(f'{l}{p}', self.Piece_ID[' '], 0, 0) for l in self.Let_Num.keys() for p in self.mid_rows_nums})
        self.Board.update({f'{l}6': BoardSquare(f'{l}6', self.Piece_ID[' ']*self.Color_Num["Black"], self.after_pawn_row_support[p]*self.Color_Num["Black"],0) for p,l in enumerate(self.Let_Num.keys())})
        self.Board.update({f'{l}7': BoardSquare(f'{l}7', self.Piece_ID['P']*self.Color_Num["Black"], self.pawn_row_support[p]*self.Color_Num["Black"],p+17) for p,l in enumerate(self.Let_Num.keys())})
        self.Board.update({f'{l}8': BoardSquare(f'{l}8', self.Piece_ID[self.terminal_row_order[p]]*self.Color_Num["Black"], self.terminal_row_support[p]*self.Color_Num["Black"],p+25) for p,l in enumerate(self.Let_Num.keys())})


    def visualize_board(self):
        print(f'Turn Number: {self.turn_number}')
        print("    ---------------------------------")
        for n in reversed(range(1,9)):
            print(f"{n}   "
                 f"| {self.Piece_ID_Inv[abs(self.Board[f'a{n}'].occupant_id)]} |"\
                 f" {self.Piece_ID_Inv[abs(self.Board[f'b{n}'].occupant_id)]} |"\
                 f" {self.Piece_ID_Inv[abs(self.Board[f'c{n}'].occupant_id)]} |"\
                 f" {self.Piece_ID_Inv[abs(self.Board[f'd{n}'].occupant_id)]} |"\
                 f" {self.Piece_ID_Inv[abs(self.Board[f'e{n}'].occupant_id)]} |"\
                 f" {self.Piece_ID_Inv[abs(self.Board[f'f{n}'].occupant_id)]} |"\
                 f" {self.Piece_ID_Inv[abs(self.Board[f'g{n}'].occupant_id)]} |"\
                 f" {self.Piece_ID_Inv[abs(self.Board[f'h{n}'].occupant_id)]} |"\
            )
            print("    ---------------------------------")
        print("                                     ")
        print("      a   b   c   d   e   f   g   h")
        
