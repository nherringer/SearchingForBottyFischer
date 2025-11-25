import copy
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from Player import Player

class ChessSet:
    def __init__(self):
        self.CB = ChessBoard()
        self.turn_number = 0
        self.CB.game_start()
        self.player1 = Player("White",self.CB)
        self.player2 = Player("Black",self.CB)

    def play(self,num_moves):
        self.CB.visualize_board()
        
        for m in range(num_moves):
            for k in self.CB.Board.keys():
                self.CB.Board[k].sq_potential = 0
            if m % 2 == 0:
                pm = self.player1.gen_pseudolegal_moves(self.player1.color_num,self.CB)
                #print(f'Player 1 pseudolegal moves: {pm}\n')
                lm = self.player1.check_legality(self.player1.color_num,pm,self.CB)
                for moves in lm.values():
                    for move in moves:
                        self.CB.Board[move].sq_potential += 1
                pm_opp = self.player1.gen_pseudolegal_moves(-self.player1.color_num,self.CB)
                #print(f'Player 1 pseudolegal moves: {pm}\n')
                lm_opp = self.player1.check_legality(-self.player1.color_num,pm_opp,self.CB)
                for moves in lm_opp.values():
                    for move in moves:
                        self.CB.Board[move].sq_potential -= 1
                #print(f'pm: {pm}\nlm: {lm}\nself.turn_number: {self.turn_number}\n')
                #print(f'player 1 piece set: {self.player1.Piece_Set.values()}\n')
                lm_vals_capture = self.player1.value_from_capture(lm,self.CB)
                #print(f'lm_vals_capture: {lm_vals_capture}\n')
                lm_vals_Ocontrol = self.player1.value_from_offense_control(lm,self.CB)
                #print(f'lm_vals_Ocontrol: {lm_vals_Ocontrol}\n')
                lm_vals = {k: [float(lm_vals_capture[k][i]) + float(lm_vals_Ocontrol[k][i]) for i in range(len(lm_vals_capture[k]))] for k in lm_vals_capture.keys()}                        
                #print(f'lm_vals: {lm_vals}\nlm_bts_vals: {lm_bts_vals}\n')
                max_val_piece = max(lm_vals, key= lambda k: max(lm_vals[k]))
                self.player1.pick_move(max_val_piece,lm,lm_vals,self.CB)
                if self.player1.Captured_uIDs:
                    if self.player1.Captured_uIDs[-1] in self.player2.Piece_Set.keys():
                        del self.player2.Piece_Set[self.player1.Captured_uIDs[-1]]
                # for key in self.player2.Piece_Set.keys():
                #     if key in self.player1.Captured_uIDs:
                #         del self.player2.Piece_Set[key]

            else:
                pm = self.player2.gen_pseudolegal_moves(self.player2.color_num,self.CB)
                #print(f'Player 2 pseudolegal moves: {pm}\n')
                lm = self.player2.check_legality(self.player2.color_num,pm,self.CB)
                for moves in lm.values():
                    for move in moves:
                        self.CB.Board[move].sq_potential += 1
                pm_opp = self.player2.gen_pseudolegal_moves(self.player2.color_num,self.CB)
                #print(f'Player 2 pseudolegal moves: {pm}\n')
                lm_opp = self.player2.check_legality(self.player2.color_num,pm_opp,self.CB)
                for moves in lm_opp.values():
                    for move in moves:
                        self.CB.Board[move].sq_potential += 1
                #print(f'pm: {pm}\nlm: {lm}\nself.turn_number: {self.CB.turn_number}\n')
                lm_vals_capture = self.player2.value_from_capture(lm,self.CB)
                #print(f'lm_vals_capture: {lm_vals_capture}\n')
                lm_vals_Ocontrol = self.player2.value_from_offense_control(lm,self.CB)            
                #print(f'lm_vals_Ocontrol: {lm_vals_Ocontrol}\n')
                lm_vals = {k: [float(lm_vals_capture[k][i]) + float(lm_vals_Ocontrol[k][i]) for i in range(len(lm_vals_capture[k]))] for k in lm_vals_capture.keys()}                        
                #print(f'lm_vals: {lm_vals}\nlm_bts_vals: {lm_bts_vals}\n')
                max_val_piece = max(lm_vals, key= lambda k: max(lm_vals[k]))
                self.player2.pick_move(max_val_piece,lm,lm_vals,self.CB)
                if self.player2.Captured_uIDs:
                    if self.player2.Captured_uIDs[-1] in self.player1.Piece_Set.keys():
                        del self.player1.Piece_Set[self.player2.Captured_uIDs[-1]]
                # for key in self.player1.Piece_Set.keys():
                #     print(f'Checking p1 key: {key}\n self.player1.Piece_Set.keys(): {self.player1.Piece_Set.keys()}\n self.player2.Captured_uIDs: {self.player2.Captured_uIDs}\n')
                #     if key in self.player2.Captured_uIDs:
                #         del self.player1.Piece_Set[key]
                #         print(f'p1k: {self.player1.Piece_Set.keys()}')
            
            self.CB.visualize_board()
            print("\n\n\n\n\n")



