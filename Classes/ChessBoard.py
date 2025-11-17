class ChessBoard:
    def __init__(self):
        self.board = {}
        self.board_prior = {}
        self.Piece_ID = {'E': 0,
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
                           6: 10}
        self.ID_Values_Inv = {v: k for k,v in self.ID_Values.items()}
        self.Piece_Values = {"E": 0,
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
        self.board_threat_and_supports = {}
        self.tmp_bts = {}
        self.terminal_row_order = ['rook','knight','bishop','queen','king','bishop','knight','rook']
        self.game_start()
#         self.terminal_row_support = [0, 1, 1, 1, 1, 1, 1, 0]
#         self.pawn_row_support = [1, 1, 1, 4, 4, 1, 1, 1]
#         self.after_pawn_row_support = [1, 2, 3, 2, 2, 3, 2, 1]
        
    def game_start(self):
        self.board.update({f'{l}1': self.pieceID[self.terminal_row_order[p]] for p,l in enumerate(self.letters)})
        self.board.update({f'{l}2': self.pieceID['pawn'] for l in self.letters})
        self.board.update({f'{l}{n}': self.pieceID['empty'] for l in self.letters for n in self.numbers[2:6]})
        self.board.update({f'{l}7': self.pieceID['pawn']*-1 for l in self.letters})
        self.board.update({f'{l}8': self.pieceID[self.terminal_row_order[p]]*-1 for p,l in enumerate(self.letters)})
        self.board_prior = copy.deepcopy(self.board)
        
#         self.board_threat_and_supports.update({f'{l}1': self.terminal_row_support[p] for p,l in enumerate(self.letters)})
#         self.board_threat_and_supports.update({f'{l}2': self.pawn_row_support[p] for p,l in enumerate(self.letters)})
#         self.board_threat_and_supports.update({f'{l}3': self.after_pawn_row_support[p] for p,l in enumerate(self.letters)})
#         self.board_threat_and_supports.update({f'{l}{n}': 0 for l in self.letters for n in [4,5]})
#         self.board_threat_and_supports.update({f'{l}4': self.after_pawn_row_support[p]*-1 for p,l in enumerate(self.letters)})
#         self.board_threat_and_supports.update({f'{l}7': self.pawn_row_support[p]*-1 for p,l in enumerate(self.letters)})
#         self.board_threat_and_supports.update({f'{l}8': self.terminal_row_support[p]*-1 for p,l in enumerate(self.letters)})
        self.board_threat_and_supports.update({f'{l}{n}': 0 for l in self.letters for n in self.numbers})

    def visualize_board(self):
        print(f'Turn Number: {self.turn_number}')
        print("    ---------------------------------")
        for n in reversed(self.numbers):
            print(f"{n}   "
                 f"| {self.pieceSymbol[self.pieceName[abs(self.board[f'a{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board[f'b{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board[f'c{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board[f'd{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board[f'e{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board[f'f{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board[f'g{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board[f'h{n}'])]]} |")
            print("    ---------------------------------")
        print("                                     ")
        print("      a   b   c   d   e   f   g   h")
        
    def visualize_board_prior(self):
        print(f'Turn Number: {self.turn_number-1}')
        print("    ---------------------------------")
        for n in reversed(self.numbers):
            print(f"{n}   "
                 f"| {self.pieceSymbol[self.pieceName[abs(self.board_prior[f'a{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board_prior[f'b{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board_prior[f'c{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board_prior[f'd{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board_prior[f'e{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board_prior[f'f{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board_prior[f'g{n}'])]]} |"\
                 f" {self.pieceSymbol[self.pieceName[abs(self.board_prior[f'h{n}'])]]} |")
            print("    ---------------------------------")
        print("                                     ")
        print("      a   b   c   d   e   f   g   h")


    