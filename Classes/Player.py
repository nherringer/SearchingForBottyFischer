class Player:
    def __init__(self,color):
        self.color = color
        self.Set_Count = {"P": 8,
                        "B": 2,
                        "N": 2,
                        "R": 2,
                        "Q": 1,
                        "K": 1}
        self.Capture_Count = {"P": 0,
                        "B": 0,
                        "N": 0,
                        "R": 0,
                        "Q": 0,
                        "K": 0}
        if self.color == "White":
            self.turn = True
        elif self.color =="Black":
            self.turn = False
        else:
            print("eRrOr!")

    def gen_pseudolegal_moves(self,c,board,board_threat_and_supports):     
        pieces_on_board = []
        for sq,pID in board.items():
            if pID*c>=0:
                pieces_on_board.append([sq,pID])

        possible_moves = {}
        for sq,pID in pieces_on_board:
            # Pawn Moves
            if pID*c == 1:
                possible_moves[sq] = self.pawn_moves(sq,c,board,board_threat_and_supports)
            elif pID*c == 2:
                possible_moves[sq] = self.bishop_moves(sq,c,board,board_threat_and_supports)
            elif pID*c == 3:
                possible_moves[sq] = self.knight_moves(sq,c,board,board_threat_and_supports)
            elif pID*c == 4:
                possible_moves[sq] = self.rook_moves(sq,c,board,board_threat_and_supports)
            elif pID*c == 5:
                possible_moves[sq] = self.queen_moves(sq,c,board,board_threat_and_supports)
            elif pID*c == 6:
                possible_moves[sq] = self.king_moves(sq,c,board,board_threat_and_supports)
        possible_moves = {k: v for k,v in possible_moves.items() if v is not None}

        return possible_moves
    
    def check_legality(self,c,possible_moves,board):        
        legal_moves = {}
        # Gen list of all opponent piece
        lm_bts_vals = {}
        for piece,moves in possible_moves.items():
            lms_per_piece = []
            summed_bts_vals = []
            for move in moves:
                tmp_board = copy.deepcopy(board)
                tmp_board.update({f'{move}': board[f'{piece}']})
                tmp_board.update({f'{piece}': 0})
                self.tmp_bts = copy.deepcopy(self.board_threat_and_supports)
                if not self.is_King_in_check(self.side_to_move,tmp_board):
                    lms_per_piece.append(move)
                    bts_diff = {k:(self.board_threat_and_supports[k] - self.tmp_bts[k])*-c for k in moves}
                    #print(f'piece: {piece}\nmove: {move}\nself.board_threat_and_supports: {self.board_threat_and_supports}\ntmp_board_threat_and_supports: {tmp_board_threat_and_supports}\nbts_diff: {bts_diff}\n')
                    summed_bts_vals.append(bts_diff[move])
                    if piece == 'f3' and move == 'f6':
                        print(bts_diff[move])
                        #print(f'board_threat_and_supports[key]: {board_threat_and_supports[move]}\nself.tmp_bts[key]: {self.tmp_bts[move]}')
                        #print(f'piece: {piece}\nmove: {move}\nself.bts: {self.board_threat_and_supports[piece]}\nself.tmp_bts: {self.tmp_bts[piece]}')
            if lms_per_piece:
                legal_moves[f'{piece}'] = lms_per_piece
                #print(f'tmp_board_threat_and_supports: {tmp_board_threat_and_supports}')
                #print(f'summed_bts_vals: {summed_bts_vals}')
                lm_bts_vals[f'{piece}'] = summed_bts_vals
        #print(f'CHECK_LEGALITY   lm: {legal_moves}\n lm_bts_vals: {lm_bts_vals}\n')
        
        return legal_moves,lm_bts_vals

    def is_King_in_check(self,c,board):
        rev_board = {v: k for k,v in board.items()}
        king_pos = rev_board[6*c]
        opponent_moves = self.gen_pseudolegal_moves(-c,board,self.tmp_bts)
        in_check = False
        for k,vlist in opponent_moves.items():
            if king_pos in vlist:
                in_check = True
                break
        return in_check
    
    def value_from_capture(self,legal_moves,board):
        
        lm_vals = copy.deepcopy(legal_moves)
        
        for piece,moves in legal_moves.items():
            piece_moves = []
            for move in moves:
                piece_moves.append(self.pieceValues[board[move]*-self.side_to_move])
            lm_vals[piece] = piece_moves
        return lm_vals

        def value_from_offense_control(self,legal_moves,board,board_threat_and_supports):
        
        lm_vals = copy.deepcopy(legal_moves)
        bts_vals = {}
        for piece,moves in legal_moves.items():
            summed_move_vals = []
            summed_bts_vals = []
            for move in moves:
                move_vals = []
                tmp_board = copy.deepcopy(board)
                tmp_board.update({f'{move}': board[f'{piece}']})
                tmp_board.update({f'{piece}': 0})
                tmp_board_bts = copy.deepcopy(board_threat_and_supports)
                pm_from_move = self.gen_pseudolegal_moves(self.side_to_move,tmp_board,tmp_board_bts)
                lm_from_move,lm_bts_vals = self.check_legality(self.side_to_move,pm_from_move,tmp_board)                                
                #print(f'Ocontrol lm_bts" {lm_bts_vals}')
                for p,mset in lm_from_move.items():                    
                    move_val = 0
                    for m in mset:
                        if tmp_board[m] == 0:
                            move_val += 0.05
                        elif tmp_board[m]*self.side_to_move > 0:
                            move_val += 0.2*self.pieceValues[tmp_board[m]*self.side_to_move]
                        elif tmp_board[m]*self.side_to_move < 0:                           
                            move_val += 0.1*self.pieceValues[tmp_board[m]*-self.side_to_move]
                    move_vals.append(move_val)
                #print(f'lm_bts_vals: {lm_bts_vals.values()}')
                #summed_bts_vals.append(sum([int(v) for v in lm_bts_vals.values()]))
                summed_move_vals.append(sum(move_vals))  
            lm_vals[piece] = summed_move_vals
            #bts_vals[piece] = summed_bts_vals
        return lm_vals#, bts_vals

        def pick_move(self,picked_key,legal_moves,lm_vals):
        if self.side_to_move == 1:
            color = 'White'
        elif self.side_to_move == -1:
            color = 'Black'
        max_val = max(lm_vals[picked_key])
        max_val_ind = lm_vals[picked_key].index(max_val)
        move = legal_moves[picked_key][max_val_ind]
        #print(f'max_val: {max_val}\npiece_start: {picked_key}\npiece_end: {move}\n')
        print(f'{color} plays {self.pieceSymbol[self.pieceName[abs(self.board[picked_key])]]}{picked_key} to {move}')
        self.board_prior = copy.deepcopy(self.board)
        self.board.update({f'{move}': self.board[f'{picked_key}']})
        self.board.update({f'{picked_key}': 0})
        self.side_to_move = -self.side_to_move
        self.turn_number += 1
        self.board_threat_and_supports.update({k: 0 for k in self.board_threat_and_supports.keys()})

    