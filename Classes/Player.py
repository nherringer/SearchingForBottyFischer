from ChessPiece import ChessPiece
from BoardSquare import BoardSquare
from ChessBoard import ChessBoard
import GeneralDicts
import itertools
import copy

class Player:
    '''Class to represent a chess player.'''
    def __init__(self,color_name,CB,PS32):
        self.color_name = color_name
        self.PS32 = PS32
        if self.color_name == "White":
            self.turn = True
        elif self.color_name =="Black":
            self.turn = False
        else:
            print("eRrOr!")
        self.color_num = GeneralDicts.Color_Num[self.color_name]
        self.Capture_Count = {"P": 0,
                        "B": 0,
                        "N": 0,
                        "R": 0,
                        "Q": 0,
                        "K": 0}
        self.Captured_uIDs = []

    def gen_pseudolegal_moves(self,c,CB):
        '''Generate all movememnt patterns for all pieces of color c on the given ChessBoard CB.'''
        possible_moves = {}
        move_pressure = {}
        for piece_key, piece_obj in self.PS32.items():
            if piece_obj.color_num == c:
                result = piece_obj.piece_movement(CB)
                if not result:
                    continue
                raw_moves, raw_pressure = result
                flat_moves = list(self.flatten_list_recursive(raw_moves))
                #print(f"flat moves for piece at {piece_obj.current_sq}: {flat_moves}\n")
                flat_pressure = list(self.flatten_list_recursive(raw_pressure))
                possible_moves[piece_obj.current_sq] = flat_moves
                move_pressure[piece_obj.current_sq] = flat_pressure


        possible_moves = {k: v for k,v in possible_moves.items() if v is not None}
        move_pressure = {k: v for k,v in move_pressure.items() if v is not None}

        return possible_moves, move_pressure

    def flatten_list_recursive(self,nested_list):
        for item in nested_list:
            if isinstance(item, list):
                # If the item is a list, recursively call the function
                # and chain the results
                yield from self.flatten_list_recursive(item)
            else:
                # If the item is not a list, yield it directly
                yield item
    
    def check_legality(self,c,possible_moves,move_pressure,CB):        
        '''Check the legality of the given possible moves for color c on the given ChessBoard CB.'''
        legal_moves = {}
        # Gen list of all opponent piece
        lm_bts_vals = {}
        for start_sq,moves in possible_moves.items():
            lms_per_piece = []
            for move in moves:
                tmp_CB = copy.deepcopy(CB)
                tmp_CB.Board.update({f'{move}': BoardSquare(f'{move}', tmp_CB.Board[f'{move}'].sq_potential-1,CB.Board[f'{start_sq}'].occupant_uID)})
                tmp_CB.Board.update({f'{start_sq}': BoardSquare(f'{start_sq}', tmp_CB.Board[f'{start_sq}'].sq_potential+1, 0)})
                if not self.is_King_in_check(c,tmp_CB):
                    lms_per_piece.append(move)
            if lms_per_piece:
                legal_moves[f'{start_sq}'] = lms_per_piece
                lm_bts_vals[f'{start_sq}'] = move_pressure[start_sq]
        
        return legal_moves, lm_bts_vals

    def is_King_in_check(self,c,CB):
        '''Check if the king of color c is in check on the given ChessBoard CB.'''
        # rev_board = {o.occupant_uID: sq for sq,o in CB.Board.items() if o.occupant_uID != 0}
        # if 5 not in rev_board.keys():
        #     print(f'Board: ')  # Debugging line
        king_pos =  self.PS32[5 if c == 1 else 29].current_sq
        opponent_moves, opponent_pressure = self.gen_pseudolegal_moves(-c,CB)
        in_check = False
        for k,vlist in opponent_moves.items():
            if king_pos in vlist:
                in_check = True
                break
        return in_check
    
    def value_from_capture(self,legal_moves,CB):
        '''Calculate the value of moves based on captures for the given legal moves on the ChessBoard CB.'''
        lm_vals = copy.deepcopy(legal_moves)
        for piece,moves in legal_moves.items():
            piece_moves = []
            for move in moves:
                piece_moves.append(GeneralDicts.uID_props[CB.Board[move].occupant_uID]["value"])
            lm_vals[piece] = piece_moves
        return lm_vals

    def value_from_offense_control(self,legal_moves,CB):
        '''Calculate the value of moves based on offensive control for the given legal moves on the ChessBoard CB.'''
        lm_vals = copy.deepcopy(legal_moves)
        for piece,moves in legal_moves.items():
            summed_move_vals = []
            for move in moves:
                move_vals = []
                tmp_CB = copy.deepcopy(CB)
                tmp_CB.Board.update({f'{move}': BoardSquare(f'{move}', tmp_CB.Board[f'{move}'].sq_potential - 1, CB.Board[f'{piece}'].occupant_uID)})
                tmp_CB.Board.update({f'{piece}': BoardSquare(f'{piece}', tmp_CB.Board[f'{piece}'].sq_potential + 1, 0)})
                pm_from_move, pm_from_move_pressure = self.gen_pseudolegal_moves(self.color_num,tmp_CB)
                lm_from_move, lm_from_move_pressure = self.check_legality(self.color_num,pm_from_move,pm_from_move_pressure,tmp_CB)                                
                for p,mset in lm_from_move.items():                    
                    move_val = 0
                    for m in mset:
                        if tmp_CB.Board[m].occupant_uID == 0:
                            move_val += 0.05
                        else:                          
                            move_val += 0.5*GeneralDicts.uID_props[tmp_CB.Board[m].occupant_uID]["value"]*tmp_CB.Board[m].sq_potential
                    move_vals.append(move_val)
                summed_move_vals.append(sum(move_vals))  
            lm_vals[piece] = summed_move_vals
        return lm_vals

    def pick_move(self,sq_start,legal_moves,lm_vals,CB):
        '''Pick the best move for the piece identified by picked_key based on the given legal moves and their values on the ChessBoard CB.'''
        max_val = max(lm_vals[sq_start])
        max_val_ind = lm_vals[sq_start].index(max_val)
        sq_end = legal_moves[sq_start][max_val_ind]

        #print(f'{self.color} plays {CB.Piece_ID_Inv[abs(occupant_id)]}{sq_start} to {move}')
        CB.BoardsRunningList[CB.turn_number] = copy.deepcopy(CB.Board)
        self.run_updates(sq_start,sq_end,CB)


    def run_updates(self,sq_start,sq_end,CB):
        '''Update the board and piece positions after a move from sq_start to sq_end on the given ChessBoard CB.'''
        # print("DEBUG run_updates:")
        # print("  sq_start:", sq_start)
        # print("  sq_end:", sq_end)
        # print("  ouID:", CB.Board[sq_start].occupant_uID)
        # print("  Board[sq_start]:", CB.Board[sq_start].__dict__)

        ouID = copy.deepcopy(CB.Board[sq_start].occupant_uID)
        ouID_sq_end = copy.deepcopy(CB.Board[sq_end].occupant_uID)
        CB.Board[sq_end].update_BS(new_occupant_uID=ouID)
        CB.Board[sq_start].update_BS(new_occupant_uID=0)
        if ouID_sq_end != 0:
            self.Captured_uIDs.append(ouID_sq_end)
            del self.PS32[ouID_sq_end]
        print(f'Player {self.color_name} moves piece uID {ouID} from {sq_start} to {sq_end}')
        self.PS32[ouID].update_CP(sq_end)
        CB.turn_number += 1