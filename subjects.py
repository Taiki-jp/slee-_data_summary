from dataclasses import astuple, dataclass

class Subjects:
    def __init__(self,
                 name : str,
                 is_valid : False,
                 date : str,) -> None:
        # subject name
        self.name = name
        # whether data is valid or not
        self.is_valid = is_valid
        # date
        self.date = date
    