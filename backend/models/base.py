from typing import Dict

class Base:
    def __init__(self) -> None:
        pass

    def to_dict(self) -> Dict:
        return vars(self)
