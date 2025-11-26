import copy
from GeneralDicts import GeneralDicts
class ChessPiece:
    def __init__(self,piece_type,color,start_sq,occupant_uID):
        self.piece_type = piece_type
        self.color_name = color
        self.occupant_uID = occupant_uID
        self.color_num = self.Color_Num[color]
    
        # "Piece": Refers to the one letter representation of a piecetype
        # "ID": Refers to a unique numerical ID for each piecetype
        # "Value": Refers to the value for each piecetype
        self.value = self.Piece_ID[self.piece_type]*self.color_num
        self.start_sq = start_sq
        self.current_sq = start_sq
        self.previous_sq = start_sq
        self.opponent_in_check = False
        self.self_in_check = False
        self.Legal_Moves = {}
    
    def piece_movement(self,CB,ptype=None):
        if ptype is None:
            ptype = self.piece_type
        l = self.current_sq[0]
        n = int(self.current_sq[1])
        l_n = self.Let_Num[l]
        c = self.color_num
        if ptype == "P":
            moves = []
            # Move forward 1
            if CB.Board[f'{l}{n+c}'].occupant_id == 0:
                moves.append(f'{l}{n+c}')
                # Move forward 2
                if CB.Board[f'{l}{n+2*c}'].occupant_id == 0 and (n*c == 2 or n*c == -7):
                    moves.append(f'{l}{n+2*c}')
            

            # Capture left diagonal
            if (1 <= l_n-c <=8):
                if CB.Board[f'{self.Num_Let[l_n-c]}{n+c}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[l_n-c]}{n+c}')
                
            # Capture right diagonal
            if (1 <= l_n+c <=8):
                if CB.Board[f'{self.Num_Let[l_n+c]}{n+c}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[l_n+c]}{n+c}')

            # En Passant (add later)
            if moves:    
                return moves

        elif ptype == "B":
            moves = []
            # Upper right
            temp_ln = l_n + c
            temp_n = n + c
            while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                
                if CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id == 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{temp_n}')
                elif CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{temp_n}')
                    break
                elif CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id*c > 0:
                    break
                temp_ln += c
                temp_n += c
            # Upper left
            temp_ln = l_n - c
            temp_n = n + c
            while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                
                if CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id == 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{temp_n}')
                elif CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{temp_n}')
                    break
                elif CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id*c > 0:
                    break
                temp_ln -= c
                temp_n += c
            # Lower right
            temp_ln = l_n + c
            temp_n = n - c
            while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                
                if CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id == 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{temp_n}')
                elif CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{temp_n}')
                    break
                elif CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id*c > 0:
                    break
                temp_ln += c
                temp_n -= c
            # Lower left
            temp_ln = l_n - c
            temp_n = n - c
            while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                
                if CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id == 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{temp_n}')
                elif CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{temp_n}')
                    break
                elif CB.Board[f'{self.Num_Let[temp_ln]}{temp_n}'].occupant_id*c > 0:
                    break
                temp_ln -= c
                temp_n -= c
            if moves:
                return moves
        elif ptype == "N":
            moves = []
            # Up/Down, right/Left
            for i in [1,-1]:
                for j in [2,-2]:
                    if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                        
                        if CB.Board[f'{self.Num_Let[l_n+i]}{n+j}'].occupant_id*c <= 0:
                            moves.append(f'{self.Num_Let[l_n+i]}{n+j}')
            # Right/Left, up,down
            for i in [2,-2]:
                for j in [1,-1]:
                    if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                        
                        if CB.Board[f'{self.Num_Let[l_n+i]}{n+j}'].occupant_id*c <= 0:
                            moves.append(f'{self.Num_Let[l_n+i]}{n+j}')
            if moves:
                return moves
        elif ptype == "R":

            moves = []
            # Right
            temp_ln = l_n + c
            while (1 <= temp_ln <=8):
                
                if CB.Board[f'{self.Num_Let[temp_ln]}{n}'].occupant_id == 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{n}')
                elif CB.Board[f'{self.Num_Let[temp_ln]}{n}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{n}')
                    break
                elif CB.Board[f'{self.Num_Let[temp_ln]}{n}'].occupant_id*c > 0:
                    break
                temp_ln += c
            # Left
            temp_ln = l_n - c
            while (1 <= temp_ln <=8):
                
                if CB.Board[f'{self.Num_Let[temp_ln]}{n}'].occupant_id == 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{n}')
                elif CB.Board[f'{self.Num_Let[temp_ln]}{n}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[temp_ln]}{n}')
                    break
                elif CB.Board[f'{self.Num_Let[temp_ln]}{n}'].occupant_id*c > 0:
                    break
                temp_ln -= c
            # Up
            temp_n = n + c
            while (1 <= temp_n <=8):
                
                if CB.Board[f'{self.Num_Let[l_n]}{temp_n}'].occupant_id == 0:
                    moves.append(f'{self.Num_Let[l_n]}{temp_n}')
                elif CB.Board[f'{self.Num_Let[l_n]}{temp_n}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[l_n]}{temp_n}')
                    break
                elif CB.Board[f'{self.Num_Let[l_n]}{temp_n}'].occupant_id*c > 0:
                    break
                temp_n += c
            # Down
            temp_n = n - c
            while (1 <= temp_n <=8):
                
                if CB.Board[f'{self.Num_Let[l_n]}{temp_n}'].occupant_id == 0:
                    moves.append(f'{self.Num_Let[l_n]}{temp_n}')
                elif CB.Board[f'{self.Num_Let[l_n]}{temp_n}'].occupant_id*c < 0:
                    moves.append(f'{self.Num_Let[l_n]}{temp_n}')
                    break
                elif CB.Board[f'{self.Num_Let[l_n]}{temp_n}'].occupant_id*c > 0:
                    break
                temp_n -= c
            if moves:
                return moves
        elif ptype == "Q":
            moves = []
            b_moves = self.piece_movement(CB,"B")
            if b_moves:
                moves.append(b_moves)
            r_moves = self.piece_movement(CB,"R")
            if r_moves:
                moves.append(r_moves)
            moves_flat = [move for movelist in moves for move in movelist]
            if moves_flat:
                return moves_flat
        elif ptype == "K":
                moves = []
                for i in [1,0,-1]:
                    for j in [1,0,-1]:
                        if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                            
                            if CB.Board[f'{self.Num_Let[l_n+i]}{n+j}'].occupant_id*c <= 0:
                                moves.append(f'{self.Num_Let[l_n+i]}{n+j}')
                if moves:
                    return moves