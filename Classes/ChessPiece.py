import copy
import GeneralDicts
from collections import Counter
class ChessPiece:
    '''Class to represent individual chess pieces.'''
    def __init__(self,uID):
        self.uID = uID
        self.piece_type = GeneralDicts.uID_props[uID]["piece_type"] 
        self.color_name = GeneralDicts.uID_props[uID]["color_name"]
        self.color_num = GeneralDicts.uID_props[uID]["color_num"]
        self.value = GeneralDicts.uID_props[uID]["value"]
        self.start_sq = GeneralDicts.uID_props[uID]["start_sq"]
        self.current_sq = GeneralDicts.uID_props[uID]["start_sq"]
        self.previous_sq = GeneralDicts.uID_props[uID]["start_sq"]
        self.checking_king = False
        self.Legal_Moves = {}
    
    def update_CP(self,new_current_sq=None):
        '''Update the ChessPiece's current square and previous square.'''
        if new_current_sq is not None:
            self.previous_sq = self.current_sq
            self.current_sq = new_current_sq

    def piece_movement(self,CB,ptype=None):
        pressure_sqs = {}
        moves = []
        '''Generate all movement patterns for the piece on the given ChessBoard.'''
        if ptype is None:
            ptype = self.piece_type
        l = self.current_sq[0]
        n = int(self.current_sq[1])
        l_n = GeneralDicts.Let_Num[l]
        c = self.color_num
        #print(f'self.uID: {self.uID}\nocc_uID: {CB.Board[f"{l}{n}"].occupant_uID}\nptype: {ptype}\nself.value: {self.value}\nuID_props value: {GeneralDicts.uID_props[CB.Board[f"{l}{n}"].occupant_uID]["value"]}\n')
        # if (1 <= l_n-c <=8) and (1 <= l_n-c <=8):
        #     ouid = CB.Board[f'{GeneralDicts.Num_Let[l_n-c]}{n+c}'].occupant_uID
        #     print(ouid)
        #     print(GeneralDicts.uID_props[ouid]["value"])
        if ptype == "P":

            # Move forward 1
            if CB.Board[f'{l}{n+c}'].occupant_uID == 0:
                moves.append(f'{l}{n+c}')
                # Move forward 2
                if CB.Board[f'{l}{n+2*c}'].occupant_uID == 0 and (n*c == 2 or n*c == -7):
                    moves.append(f'{l}{n+2*c}')
            

            # Capture left diagonal
            if (1 <= l_n-c <=8):
                pressure_sqs[f'{GeneralDicts.Num_Let[l_n-c]}{n+c}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n-c]}{n+c}'].occupant_uID]["value"]*c < 0:
                    #print(GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n-c]}{n+c}'].occupant_uID]["value"])
                    moves.append(f'{GeneralDicts.Num_Let[l_n-c]}{n+c}')
                
            # Capture right diagonal
            if (1 <= l_n+c <=8):
                pressure_sqs[f'{GeneralDicts.Num_Let[l_n+c]}{n+c}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n+c]}{n+c}'].occupant_uID]["value"]*c < 0:
                    #print(GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n+c]}{n+c}'].occupant_uID]["value"])
                    moves.append(f'{GeneralDicts.Num_Let[l_n+c]}{n+c}')

            # En Passant (add later)
            if moves:
                #print(f"ouID: {CB.Board[f'{GeneralDicts.Num_Let[l_n]}{n}'].occupant_uID}\nptype: {ptype}\n")
                return moves,pressure_sqs

        elif ptype == "B":

            # Upper right
            temp_ln = l_n + c
            temp_n = n + c
            while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                #print(GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c)
                #print(moves)
                pressure_sqs[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"] == 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}')
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c < 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}')
                    break
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c > 0:
                    break
                temp_ln += c
                temp_n += c
                #print(moves)
            # Upper left
            temp_ln = l_n - c
            temp_n = n + c
            while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                pressure_sqs[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"] == 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}')
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c < 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}')
                    break
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c > 0:
                    break
                temp_ln -= c
                temp_n += c
            # Lower right
            temp_ln = l_n + c
            temp_n = n - c
            while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                pressure_sqs[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"] == 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}')
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c < 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}')
                    break
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c > 0:
                    break
                temp_ln += c
                temp_n -= c
            # Lower left
            temp_ln = l_n - c
            temp_n = n - c
            while (1 <= temp_ln <=8) and (1 <= temp_n <=8):
                pressure_sqs[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"] == 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}')
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c < 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}')
                    break
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{temp_n}'].occupant_uID]["value"]*c > 0:
                    break
                temp_ln -= c
                temp_n -= c
            if moves:
                return moves, pressure_sqs
        elif ptype == "N":

            # Up/Down, right/Left
            for i in [1,-1]:
                for j in [2,-2]:
                    if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                        pressure_sqs[f'{GeneralDicts.Num_Let[l_n+i]}{n+j}'] = 1
                        if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n+i]}{n+j}'].occupant_uID]["value"]*c <= 0:
                            moves.append(f'{GeneralDicts.Num_Let[l_n+i]}{n+j}')
            # Right/Left, up,down
            for i in [2,-2]:
                for j in [1,-1]:
                    if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                        pressure_sqs[f'{GeneralDicts.Num_Let[l_n+i]}{n+j}'] = 1
                        if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n+i]}{n+j}'].occupant_uID]["value"]*c <= 0:
                            moves.append(f'{GeneralDicts.Num_Let[l_n+i]}{n+j}')
            if moves:
                return moves, pressure_sqs
        elif ptype == "R":
            
            
            # Right
            temp_ln = l_n + c            
            
            while (1 <= temp_ln <=8):
                #print(GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{n}'].occupant_uID]["value"]*c)

                pressure_sqs[f'{GeneralDicts.Num_Let[temp_ln]}{n}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{n}'].occupant_uID]["value"] == 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{n}')
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{n}'].occupant_uID]["value"]*c < 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{n}')
                    break
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{n}'].occupant_uID]["value"]*c > 0:
                    break
                temp_ln += c
            # Left

            temp_ln = l_n - c
            while (1 <= temp_ln <=8):
                #print(GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{n}'].occupant_uID]["value"]*c)

                pressure_sqs[f'{GeneralDicts.Num_Let[temp_ln]}{n}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{n}'].occupant_uID]["value"] == 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{n}')
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{n}'].occupant_uID]["value"]*c < 0:
                    moves.append(f'{GeneralDicts.Num_Let[temp_ln]}{n}')
                    break
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[temp_ln]}{n}'].occupant_uID]["value"]*c > 0:
                    break
                temp_ln -= c
            # Up
            temp_n = n + c
            while (1 <= temp_n <=8):
                #print(GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'].occupant_uID]["value"]*c)

                pressure_sqs[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'].occupant_uID]["value"] == 0:
                    moves.append(f'{GeneralDicts.Num_Let[l_n]}{temp_n}')
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'].occupant_uID]["value"]*c < 0:
                    moves.append(f'{GeneralDicts.Num_Let[l_n]}{temp_n}')
                    break
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'].occupant_uID]["value"]*c > 0:
                    break
                temp_n += c
            # Down
            temp_n = n - c
            while (1 <= temp_n <=8):
                #print(GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'].occupant_uID]["value"]*c)

                pressure_sqs[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'] = 1
                if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'].occupant_uID]["value"] == 0:
                    moves.append(f'{GeneralDicts.Num_Let[l_n]}{temp_n}')
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'].occupant_uID]["value"]*c < 0:
                    moves.append(f'{GeneralDicts.Num_Let[l_n]}{temp_n}')
                    break
                elif GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n]}{temp_n}'].occupant_uID]["value"]*c > 0:
                    break
                temp_n -= c
            #print(moves)
            if moves:
                return moves, pressure_sqs
        elif ptype == "Q":
            #print(f'uID: {self.uID} at {self.current_sq} generating Q moves')
            b_movement = self.piece_movement(CB,ptype="B")
            #print(f'b_moves: {b_movement}')
            if b_movement:
                #print(f'b_moves: {b_moves}')
                b_moves, pressure_sqs_b = b_movement
                moves.append(b_moves)
            r_movement = self.piece_movement(CB,ptype="R")
            #print(f'r_moves: {r_movement}\n\n')
            if r_movement:
                #print(f'r_moves: {r_moves}')
                r_moves, pressure_sqs_r = r_movement
                moves.append(r_moves)
            moves_flat = [move for movelist in moves for move in movelist]
            if moves_flat and r_movement:
                pressure_sqs = pressure_sqs_r 
                if b_movement:
                    pressure_sqs = Counter(pressure_sqs_r) + Counter(pressure_sqs_b)
                return moves_flat, pressure_sqs
            #pressure_sqs = pressure_sqs_b + pressure_sqs_r
        elif ptype == "K":

                for i in [1,0,-1]:
                    for j in [1,0,-1]:
                        if (1 <= l_n+i <=8) and (1 <= n+j <=8):
                            pressure_sqs[f'{GeneralDicts.Num_Let[l_n+i]}{n+j}'] = 1
                            if GeneralDicts.uID_props[CB.Board[f'{GeneralDicts.Num_Let[l_n+i]}{n+j}'].occupant_uID]["value"]*c <= 0:
                                moves.append(f'{GeneralDicts.Num_Let[l_n+i]}{n+j}')
                if moves:
                    return moves, pressure_sqs