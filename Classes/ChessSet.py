import copy

class ChessSet:
    def __init__(self):
        self.board = ChessBoard()
        self.player1 = Player("White")
        self.player2 = Player("Black")
        self.turn_number = 0

    def play(self,num_moves):
        self.visualize_board()
        for _ in range(num_moves):
            pm = self.gen_pseudolegal_moves(self.side_to_move,self.board,self.board_threat_and_supports)
            lm,lm_bts_vals = self.check_legality(self.side_to_move,pm,self.board)
            print(f'play_lm_bts_vals: {lm_bts_vals}\n')
            #print(f'lm: {lm}\nlm_bts_vals: {lm_bts_vals}\n')
            lm_vals_capture = self.value_from_capture(lm,self.board)
            lm_vals_Ocontrol = self.value_from_offense_control(lm,self.board,self.board_threat_and_supports)            
            lm_vals = {k: [float(lm_vals_capture[k][i]) + float(lm_vals_Ocontrol[k][i]) + float(lm_bts_vals[k][i]) for i in range(len(lm_vals_capture[k]))] for k in lm_vals_capture.keys()}                        
            #print(f'lm_vals: {lm_vals}\nlm_bts_vals: {lm_bts_vals}\n')
            max_val_piece = max(lm_vals, key= lambda k: max(lm_vals[k]))
            self.picked_move(max_val_piece,lm,lm_vals)
            self.visualize_board()
            print("\n\n\n\n\n")



