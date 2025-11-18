import copy

class ChessSet:
    def __init__(self):
        self.CB = ChessBoard()
        self.player1 = Player("White")
        self.player2 = Player("Black")
        self.turn_number = 0

    def play(self,num_moves):
        self.CB.Board.visualize_board()
        for m in range(num_moves):
            if m % 2 == 0:
                pm = self.player1.gen_pseudolegal_moves(self.player1.color_num,self.CB.Board)
                lm,lm_bts_vals = self.check_legality(self.player1.color_num,pm,self.CB.Board)
                lm_vals_capture = self.player1.value_from_capture(lm,self.CB.Board)
                self.player1.picked_move(max_val_piece,lm,lm_vals)
            else:
                pm = self.player2.gen_pseudolegal_moves(self.player2.color_num,self.CB.Board)
                lm,lm_bts_vals = self.check_legality(self.player2.color_num,pm,self.CB.Board)
                lm_vals_capture = self.player2.value_from_capture(lm,self.CB.Board)
                self.player2.picked_move(max_val_piece,lm,lm_vals)
            
            self.CB.Board.visualize_board()
            print("\n\n\n\n\n")



