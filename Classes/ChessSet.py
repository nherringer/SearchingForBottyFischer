import copy
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
import GeneralDicts
from Player import Player

class ChessSet:
    def __init__(self):
        # Set up chess board and pieces
        self.CB = ChessBoard()
        self.turn_number = 0
        self.CB.game_start()
        self.Piece_Set_32 = {n: ChessPiece(n) for n in range(1,33) }
        # Set up players
        self.player1 = Player("White",self.CB,self.Piece_Set_32)
        self.player2 = Player("Black",self.CB,self.Piece_Set_32)
        self.CB.visualize_board()

    def play(self,num_moves):
        #print(f"value_list: {GeneralDicts.value_list}\n")
        
        for m in range(num_moves):
            if m % 2 == 0:
                pm, pm_pressure = self.player1.gen_pseudolegal_moves(self.player1.color_num,self.CB)
                lm, lm_pressure = self.player1.check_legality(self.player1.color_num,pm,pm_pressure,self.CB)
                
                pm_opp, pm_opp_presure = self.player1.gen_pseudolegal_moves(-self.player1.color_num,self.CB)
                lm_opp, lm_opp_pressure = self.player1.check_legality(-self.player1.color_num,pm_opp,pm_opp_presure,self.CB)

                lm_vals_capture = self.player1.value_from_capture(lm,self.CB)
                lm_vals_Ocontrol = self.player1.value_from_offense_control(lm,self.CB)
                print(f"White lm_pressure:, {lm_pressure}\n")
                lm_vals = {k: [float(lm_vals_capture[k][i]) + float(lm_vals_Ocontrol[k][i]) for i in range(len(lm_vals_capture[k]))] for k in lm_vals_capture.keys()}                        
                max_val_piece = max(lm_vals, key= lambda k: max(lm_vals[k]))
                self.player1.pick_move(max_val_piece,lm,lm_vals,self.CB)
                # if self.player1.Captured_uIDs:
                #     if self.player1.Captured_uIDs[-1] in self.player2.Piece_Set_16.keys():
                #         del self.player2.Piece_Set_16[self.player1.Captured_uIDs[-1]]

            else:
                pm, pm_pressure = self.player2.gen_pseudolegal_moves(self.player2.color_num,self.CB)
                lm, lm_pressure = self.player2.check_legality(self.player2.color_num,pm,pm_pressure,self.CB)

                pm_opp, pm_opp_pressure = self.player2.gen_pseudolegal_moves(self.player2.color_num,self.CB)
                lm_opp, lm_opp_pressure = self.player2.check_legality(self.player2.color_num,pm_opp,pm_opp_pressure,self.CB)
                lm_vals_capture = self.player2.value_from_capture(lm,self.CB)
                lm_vals_Ocontrol = self.player2.value_from_offense_control(lm,self.CB)
                print(f"Black lm_pressure:, {lm_pressure}\n")            
                lm_vals = {k: [float(lm_vals_capture[k][i]) + float(lm_vals_Ocontrol[k][i]) for i in range(len(lm_vals_capture[k]))] for k in lm_vals_capture.keys()}                        
                max_val_piece = max(lm_vals, key= lambda k: max(lm_vals[k]))
                self.player2.pick_move(max_val_piece,lm,lm_vals,self.CB)
                # if self.player2.Captured_uIDs:
                #     if self.player2.Captured_uIDs[-1] in self.player1.Piece_Set_16.keys():
                #         del self.player1.Piece_Set_16[self.player2.Captured_uIDs[-1]]
            
            self.CB.visualize_board()
            print("\n\n\n\n\n")



