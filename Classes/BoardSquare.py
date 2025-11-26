from GeneralDicts import GeneralDicts
class BoardSquare:
    def __init__(self,sq_id,occupant_id,sq_potential,occupant_uID):
        self.sq_id = sq_id
        self.column = sq_id[0]
        self.row = int(sq_id[1])
        self.occupant_id_prev = occupant_id
        self.occupant_id = occupant_id
        self.occupant_id_next = occupant_id
        self.occupant_uID = occupant_uID
        self.occupant_uID_prev = occupant_uID

        self.sq_potential = sq_potential
    