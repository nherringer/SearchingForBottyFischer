Color_Num = {"White": 1,
            "Black": -1}
Color_Num_Inv = {v: k for k,v in Color_Num.items()}
Piece_ID = {' ': 0,
            'P': 1,
            'B': 2,
            'N': 3,
            'R': 4,
            'Q': 5,
            'K': 6}
Piece_ID_Inv = {v: k for k,v in Piece_ID.items()}
ID_Values = {0: 0,
            1: 1,
            2: 3,
            3: 3,
            4: 5,
            5: 9,
            6: 40}
ID_Values_Inv = {v: k for k,v in ID_Values.items()}
Piece_Values = {" ": 0,
                "P": 1,
                "N": 3,
                "B": 3,
                "R": 5,
                "Q": 9,
                "K": 40}
Piece_Values_Inv = {v: k for k,v in Piece_Values.items()}
Let_Num = {'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 7,
            'h': 8}
Num_Let = {v: k for k,v in Let_Num.items()}
back_ranks_piecetypes = ['R','N','B','Q','K','B','N','R']
piece_type_list = back_ranks_piecetypes + ['P']*16 + back_ranks_piecetypes
color_num_list = [1]*16 + [-1]*16
value_list = [ID_Values[Piece_ID[pt]] * cn for pt, cn in zip(piece_type_list, color_num_list)]
white_squares = [f"{Num_Let[i%8+1]}{i//8+1}" for i in range(16)]
# Black back rank + pawns
black_squares = [f"{Num_Let[i%8+1]}{8 - (i//8)}" for i in range(16)]

# Now swap 17-24 and 25-32 to match piece ordering
black_pawns = black_squares[8:]   # 25–32 in original list
black_back = black_squares[:8]    # 17–24 in original list

start_sq_list = white_squares + black_pawns + black_back
uID_props = {n: {"piece_type": piece_type_list[n-1],
                 "color_name": Color_Num_Inv[color_num_list[n-1]],
                 "color_num": color_num_list[n-1],
                 "value": value_list[n-1],
                 "start_sq": start_sq_list[n-1]} for n in range(1,33)}
uID_props.update({0: {"piece_type": ' ',
                     "color_name": 'None',
                     "color_num": 0,
                     "value": 0,
                     "start_sq": 'None'}})  