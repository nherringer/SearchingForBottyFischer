from ChessPiece import ChessPiece
from BoardSquare import BoardSquare
from ChessBoard import ChessBoard
from GeneralDicts import GeneralDicts
import copy

class Player:
    def __init__(self,color,CB):
        self.color = color
        if self.color == "White":
            self.turn = True
        elif self.color =="Black":
            self.turn = False
        else:
            print("eRrOr!")
        self.color_num = self.Color_Num[self.color]
        self.Set_Count = {"P": 8,
                        "B": 2,
                        "N": 2,
                        "R": 2,
                        "Q": 1,
                        "K": 1}
        if self.turn:               
            self.Set_Start = {"P": ['a2','b2','c2','d2','e2','f2','g2','h2'],
                            "B": ['c1','f1'],
                            "N": ['b1','g1'],
                            "R": ['a1','h1'],
                            "Q": ['d1'],
                            "K": ['e1']}
        else:                
            self.Set_Start = {"P": ['a7','b7','c7','d7','e7','f7','g7','h7'],
                            "B": ['c8','f8'],
                            "N": ['b8','g8'],
                            "R": ['a8','h8'],
                            "Q": ['d8'],
                            "K": ['e8']}
        #print(f"CB.Board: {CB.Board}\n")
        # print(f"(CB.Board[(self.Set_Start['P'])[2]].occupant_uID: {CB.Board[(self.Set_Start['P'])[2]].occupant_uID}\n")
        self.Piece_Set = {f"{CB.Board[self.Set_Start[k][n]].occupant_uID}": ChessPiece(k,self.color,self.Set_Start[k][n],{CB.Board[self.Set_Start[k][n]].occupant_uID}) for k,v in self.Set_Count.items() for n in range(v) }
        self.Capture_Count = {"P": 0,
                        "B": 0,
                        "N": 0,
                        "R": 0,
                        "Q": 0,
                        "K": 0}
        self.Captured_uIDs = []
        


    def gen_pseudolegal_moves(self,c,CB):
        possible_moves = {}
        for piece_key, piece_obj in self.Piece_Set.items():
            #print(f'po.start_sq: {piece_obj.start_sq}\npo.value: {piece_obj.value}\n')
            # Pawn Moves
            # if piece_obj.current_sq == 'e5':
            #     print(f'po: {piece_obj}\npo.value: {piece_obj.value}\nc: {c}\n')
            if piece_obj.value*c > 0:
                possible_moves[piece_obj.current_sq] = piece_obj.piece_movement(CB)

        possible_moves = {k: v for k,v in possible_moves.items() if v is not None}

        return possible_moves
    
    def check_legality(self,c,possible_moves,CB):        
        legal_moves = {}
        # Gen list of all opponent piece
        lm_bts_vals = {}
        for start_sq,moves in possible_moves.items():
            lms_per_piece = []
            # if start_sq == "e5":
            #     print(f'checking legality for piece at {start_sq} with moves: {moves}\n')
            for move in moves:
                tmp_CB = copy.deepcopy(CB)
                tmp_CB.Board.update({f'{move}': BoardSquare(f'{move}', CB.Board[f'{start_sq}'].occupant_id, tmp_CB.Board[f'{move}'].sq_potential-1,CB.Board[f'{start_sq}'].occupant_uID)})
                tmp_CB.Board.update({f'{start_sq}': BoardSquare(f'{start_sq}', 0, tmp_CB.Board[f'{start_sq}'].sq_potential+1, 0)})
                if not self.is_King_in_check(self.color_num,tmp_CB):
                    lms_per_piece.append(move)
                    #print(f'piece: {piece}\nmove: {move}\nself.CB_threat_and_supports: {self.board_threat_and_supports}\ntmp_board_threat_and_supports: {tmp_board_threat_and_supports}\nbts_diff: {bts_diff}\n')
            if lms_per_piece:
                legal_moves[f'{start_sq}'] = lms_per_piece
                #print(f'tmp_board_threat_and_supports: {tmp_board_threat_and_supports}')
                #print(f'summed_bts_vals: {summed_bts_vals}')
        #print(f'CHECK_LEGALITY   lm: {legal_moves}\n lm_bts_vals: {lm_bts_vals}\n')
        
        return legal_moves

    def is_King_in_check(self,c,CB):
        #print(f'board: {board}\n')
        rev_board = {o.occupant_id: sq for sq,o in CB.Board.items()}
        king_pos = rev_board[6*c]
        opponent_moves = self.gen_pseudolegal_moves(-c,CB)
        in_check = False
        for k,vlist in opponent_moves.items():
            if king_pos in vlist:
                in_check = True
                break
        return in_check
    
    def value_from_capture(self,legal_moves,CB):
        
        lm_vals = copy.deepcopy(legal_moves)
        
        for piece,moves in legal_moves.items():
            piece_moves = []
            for move in moves:
                piece_moves.append(CB.ID_Values[CB.Board[move].occupant_id*-self.color_num])
                #print(f'piece_val: {CB.Board[move].occupant_id*-self.color_num}\n')
            lm_vals[piece] = piece_moves
            #print(f'piece: {piece}\n moves: {moves}\npiece_moves: {piece_moves}\n')
        return lm_vals

    def value_from_offense_control(self,legal_moves,CB):
    
        lm_vals = copy.deepcopy(legal_moves)
        for piece,moves in legal_moves.items():
            summed_move_vals = []
            for move in moves:
                move_vals = []
                tmp_CB = copy.deepcopy(CB)
                tmp_CB.Board.update({f'{move}': BoardSquare(f'{move}', CB.Board[f'{piece}'].occupant_id, tmp_CB.Board[f'{piece}'].sq_potential - 1, CB.Board[f'{piece}'].occupant_uID)})
                tmp_CB.Board.update({f'{piece}': BoardSquare(f'{piece}', 0, CB.Board[f'{piece}'].sq_potential + 1, 0)})
                pm_from_move = self.gen_pseudolegal_moves(self.color_num,tmp_CB)
                lm_from_move = self.check_legality(self.color_num,pm_from_move,tmp_CB)                                
                #print(f'Ocontrol lm_bts" {lm_bts_vals}')
                for p,mset in lm_from_move.items():                    
                    move_val = 0
                    for m in mset:
                        if tmp_CB.Board[m].occupant_id == 0:
                            move_val += 0.05
                        elif tmp_CB.Board[m].occupant_id*self.color_num < 0:                           
                            move_val += 0.5*tmp_CB.ID_Values[tmp_CB.Board[m].occupant_id*-self.color_num]*tmp_CB.Board[m].sq_potential
                    move_vals.append(move_val)
                #print(f'lm_bts_vals: {lm_bts_vals.values()}')
                #summed_bts_vals.append(sum([int(v) for v in lm_bts_vals.values()]))
                summed_move_vals.append(sum(move_vals))  
            lm_vals[piece] = summed_move_vals
            #bts_vals[piece] = summed_bts_vals
        return lm_vals#, bts_vals

    def pick_move(self,picked_key,legal_moves,lm_vals,CB):
        max_val = max(lm_vals[picked_key])
        max_val_ind = lm_vals[picked_key].index(max_val)
        move = legal_moves[picked_key][max_val_ind]
        #print(f'max_val: {max_val}\npiece_start: {picked_key}\npiece_end: {move}\n')
        occupant_id = CB.Board[picked_key].occupant_id
        print(f'{self.color} plays {CB.Piece_ID_Inv[abs(occupant_id)]}{picked_key} to {move}')
        CB.BoardsRunningList[CB.turn_number] = copy.deepcopy(CB.Board)
        self.run_updates(picked_key,move,CB)


    def run_updates(self,sq_start,sq_end,CB):

        ouID = str(CB.Board[sq_start].occupant_uID)
        ouID_prev = CB.Board[sq_end].occupant_uID
        oID_prev = CB.Board[sq_end].occupant_id
        CB.Board.update({f'{sq_end}': BoardSquare(f'{sq_end}', CB.Board[sq_start].occupant_id, CB.Board[f'{sq_start}'].sq_potential, int(ouID))})
        CB.Board.update({f'{sq_start}': BoardSquare(f'{sq_start}', 0, CB.Board[f'{sq_start}'].sq_potential, 0)})
        CB.Board[sq_end].occupant_uID_prev = ouID_prev
        if ouID_prev != 0:
            self.Captured_uIDs.append(str(ouID_prev))
            # Remove captured piece from other player's Piece_Set
            print(f'Captured piece uID: {ouID_prev}\n')
       #print(f'self.Piece_Set: {self.Piece_Set[str(ouID)]}\n')
        #print(f'self.Piece_Set.keys: {self.Piece_Set.keys()}\nouID: {ouID}\n')
        self.Piece_Set[ouID].previous_sq = self.Piece_Set[ouID].current_sq
        self.Piece_Set[ouID].current_sq = sq_end

        CB.turn_number += 1

        #CB.BoardsRunningList[CB.turn_number] = copy.deepcopy(CB.Board)
       
        # self.current_sq = sq_start
        # self.previous_sq = sq_start