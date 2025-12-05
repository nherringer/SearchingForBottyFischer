class BoardSquare:
    def __init__(self,sq_id,sq_potential,occupant_uID):
        self.sq_id = sq_id
        self.column = sq_id[0]
        self.row = int(sq_id[1])
        self.occupant_uID = occupant_uID
        self.occupant_uID_prev = occupant_uID
        self.sq_potential = sq_potential
    
    def update_BS(self,new_occupant_uID=None,new_sq_potential=None):
        if new_occupant_uID is not None:
            self.occupant_uID_prev = self.occupant_uID
            self.occupant_uID = new_occupant_uID
        if new_sq_potential is not None:
            self.sq_potential = new_sq_potential