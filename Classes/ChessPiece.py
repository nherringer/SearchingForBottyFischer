class ChessPiece:
    def __init__(self,piece_type,color,start_sq):
        self.piece_type = piece_type
        self.Color_Num = {"White": 1,
                        "Black": -1}
        self.color_name = color
        self.color_num = self.Color_Num[color]
        # "Piece": Refers to the one letter representation of a piecetype
        # "ID": Refers to a unique numerical ID for each piecetype
        # "Value": Refers to the value for each piecetype
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
        self.start_sq = start_sq
        self.current_sq = self.start_sq
        self.previous_sq = self.start_sq
        self.potential_sq = self.start_sq
        self.opponent_in_check = False
        self.self_in_check = False
        self.Legal_Moves = {}
    
    def piece_movement(self,board):
        l = self.current_sq[0]
        n = int(self.current_sq[1])
        l_n = self.Let_Num[l]
        match self.piece_type:
            case "P":
                moves = []
                # Move forward 1
                if board[f'{l}{n+self.color_num}'] == 0:
                    moves.append(f'{l}{n+self.color_num}')
                    # Move forward 2
                    if board[f'{l}{n+2*self.color_num}'] == 0 and (n*self.color_num == 2 or n*self.color_num == -7):
                        moves.append(f'{l}{n+2*self.color_num}')
                

                # Capture left diagonal
                if (1 <= l_n-c <=8):
                    board_threat_and_supports[f'{self.numLet[l_n-c]}{n+c}'] += board[f'{self.numLet[l_n-c]}{n+c}']*c
                    if board[f'{self.numLet[l_n-c]}{n+c}']*c < 0:
                        moves.append(f'{self.numLet[l_n-c]}{n+c}')
                    
                # Capture right diagonal
                if (1 <= l_n+c <=8):
                    board_threat_and_supports[f'{self.numLet[l_n+c]}{n+c}'] += board[f'{self.numLet[l_n+c]}{n+c}']*c
                    if board[f'{self.numLet[l_n+c]}{n+c}']*c < 0:
                        moves.append(f'{self.numLet[l_n+c]}{n+c}')

                # En Passant (add later)
                if moves:    
                    return moves
            case "B":
                bishop_moves(self,sq,c,board,board_threat_and_supports):
                l = sq[0]
                n = int(sq[1])
                l_n = self.letNum[l]
                moves = []
                # Upper right
                temp_ln = l_n + c
                temp_n = n + c
                while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                    board_threat_and_supports[f'{self.numLet[temp_ln]}{temp_n}'] += board[f'{self.numLet[temp_ln]}{temp_n}']*c
                    if board[f'{self.numLet[temp_ln]}{temp_n}'] == 0:
                        moves.append(f'{self.numLet[temp_ln]}{temp_n}')
                    elif board[f'{self.numLet[temp_ln]}{temp_n}']*c < 0:
                        moves.append(f'{self.numLet[temp_ln]}{temp_n}')
                        break
                    elif board[f'{self.numLet[temp_ln]}{temp_n}']*c > 0:
                        break
                    temp_ln += c
                    temp_n += c
                # Upper left
                temp_ln = l_n - c
                temp_n = n + c
                while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                    board_threat_and_supports[f'{self.numLet[temp_ln]}{temp_n}'] += board[f'{self.numLet[temp_ln]}{temp_n}']*c
                    if board[f'{self.numLet[temp_ln]}{temp_n}'] == 0:
                        moves.append(f'{self.numLet[temp_ln]}{temp_n}')
                    elif board[f'{self.numLet[temp_ln]}{temp_n}']*c < 0:
                        moves.append(f'{self.numLet[temp_ln]}{temp_n}')
                        break
                    elif board[f'{self.numLet[temp_ln]}{temp_n}']*c > 0:
                        break
                    temp_ln -= c
                    temp_n += c
                # Lower right
                temp_ln = l_n + c
                temp_n = n - c
                while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                    board_threat_and_supports[f'{self.numLet[temp_ln]}{temp_n}'] += board[f'{self.numLet[temp_ln]}{temp_n}']*c
                    if board[f'{self.numLet[temp_ln]}{temp_n}'] == 0:
                        moves.append(f'{self.numLet[temp_ln]}{temp_n}')
                    elif board[f'{self.numLet[temp_ln]}{temp_n}']*c < 0:
                        moves.append(f'{self.numLet[temp_ln]}{temp_n}')
                        break
                    elif board[f'{self.numLet[temp_ln]}{temp_n}']*c > 0:
                        break
                    temp_ln += c
                    temp_n -= c
                # Lower left
                temp_ln = l_n - c
                temp_n = n - c
                while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                    board_threat_and_supports[f'{self.numLet[temp_ln]}{temp_n}'] += board[f'{self.numLet[temp_ln]}{temp_n}']*c
                    if board[f'{self.numLet[temp_ln]}{temp_n}'] == 0:
                        moves.append(f'{self.numLet[temp_ln]}{temp_n}')
                    elif board[f'{self.numLet[temp_ln]}{temp_n}']*c < 0:
                        moves.append(f'{self.numLet[temp_ln]}{temp_n}')
                        break
                    elif board[f'{self.numLet[temp_ln]}{temp_n}']*c > 0:
                        break
                    temp_ln -= c
                    temp_n -= c
                if moves:
                    return moves
            case "N":
                knight_moves(self,sq,c,board,board_threat_and_supports):
                        l = sq[0]
                        n = int(sq[1])
                        l_n = self.letNum[l]
                        moves = []
                        # Up/Down, right/Left
                        for i in [1,-1]:
                            for j in [2,-2]:
                                if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                                    board_threat_and_supports[f'{self.numLet[l_n+i]}{n+j}'] += board[f'{self.numLet[l_n+i]}{n+j}']*c
                                    if board[f'{self.numLet[l_n+i]}{n+j}']*c <= 0:
                                        moves.append(f'{self.numLet[l_n+i]}{n+j}')
                        # Right/Left, up,down
                        for i in [2,-2]:
                            for j in [1,-1]:
                                if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                                    board_threat_and_supports[f'{self.numLet[l_n+i]}{n+j}'] += board[f'{self.numLet[l_n+i]}{n+j}']*c
                                    if board[f'{self.numLet[l_n+i]}{n+j}']*c <= 0:
                                        moves.append(f'{self.numLet[l_n+i]}{n+j}')
                        if moves:
                            return moves
            case "R":
                rook_moves(self,sq,c,board,board_threat_and_supports):
                        l = sq[0]
                        n = int(sq[1])
                        l_n = self.letNum[l]
                        moves = []
                        # Right
                        temp_ln = l_n + c
                        while (1 <= temp_ln <=8):
                            board_threat_and_supports[f'{self.numLet[temp_ln]}{n}'] += board[f'{self.numLet[temp_ln]}{n}']*c
                            if board[f'{self.numLet[temp_ln]}{n}'] == 0:
                                moves.append(f'{self.numLet[temp_ln]}{n}')
                            elif board[f'{self.numLet[temp_ln]}{n}']*c < 0:
                                moves.append(f'{self.numLet[temp_ln]}{n}')
                                break
                            elif board[f'{self.numLet[temp_ln]}{n}']*c > 0:
                                break
                            temp_ln += c
                        # Left
                        temp_ln = l_n - c
                        while (1 <= temp_ln <=8):
                            board_threat_and_supports[f'{self.numLet[temp_ln]}{n}'] += board[f'{self.numLet[temp_ln]}{n}']*c
                            if board[f'{self.numLet[temp_ln]}{n}'] == 0:
                                moves.append(f'{self.numLet[temp_ln]}{n}')
                            elif board[f'{self.numLet[temp_ln]}{n}']*c < 0:
                                moves.append(f'{self.numLet[temp_ln]}{n}')
                                break
                            elif board[f'{self.numLet[temp_ln]}{n}']*c > 0:
                                break
                            temp_ln -= c
                        # Up
                        temp_n = n + c
                        while (1 <= temp_n <=8):
                            board_threat_and_supports[f'{self.numLet[l_n]}{temp_n}'] += board[f'{self.numLet[l_n]}{temp_n}']*c
                            if board[f'{self.numLet[l_n]}{temp_n}'] == 0:
                                moves.append(f'{self.numLet[l_n]}{temp_n}')
                            elif board[f'{self.numLet[l_n]}{temp_n}']*c < 0:
                                moves.append(f'{self.numLet[l_n]}{temp_n}')
                                break
                            elif board[f'{self.numLet[l_n]}{temp_n}']*c > 0:
                                break
                            temp_n += c
                        # Down
                        temp_n = n - c
                        while (1 <= temp_n <=8):
                            board_threat_and_supports[f'{self.numLet[l_n]}{temp_n}'] += board[f'{self.numLet[l_n]}{temp_n}']*c
                            if board[f'{self.numLet[l_n]}{temp_n}'] == 0:
                                moves.append(f'{self.numLet[l_n]}{temp_n}')
                            elif board[f'{self.numLet[l_n]}{temp_n}']*c < 0:
                                moves.append(f'{self.numLet[l_n]}{temp_n}')
                                break
                            elif board[f'{self.numLet[l_n]}{temp_n}']*c > 0:
                                break
                            temp_n -= c
                        if moves:
                            return moves
            case "Q":
                queen_moves(self,sq,c,board,board_threat_and_supports):
                        moves = []
                        b_moves = self.bishop_moves(sq,c,board,board_threat_and_supports)
                        if b_moves:
                            moves.append(b_moves)
                        r_moves = self.rook_moves(sq,c,board,board_threat_and_supports)
                        if r_moves:
                            moves.append(r_moves)
                        moves_flat = [move for movelist in moves for move in movelist]
                        if moves_flat:
                            return moves_flat
            case "K":
                king_moves(self,sq,c,board,board_threat_and_supports):
                    l = sq[0]
                    n = int(sq[1])
                    l_n = self.letNum[l]
                    moves = []
                    for i in [1,0,-1]:
                        for j in [1,0,-1]:
                            if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                                board_threat_and_supports[f'{self.numLet[l_n+i]}{n+j}'] += board[f'{self.numLet[l_n+i]}{n+j}']*c
                                if board[f'{self.numLet[l_n+i]}{n+j}']*c <= 0:
                                    moves.append(f'{self.numLet[l_n+i]}{n+j}')
                    if moves:
                        return moves