from app.domain.schemas import Cell

class GameError(Exception):
    pass


class InvalidMoveError(GameError):
    pass


class CellOccupiedError(InvalidMoveError):
    def __init__(self, x: int, y: int, cell: Cell):
        super().__init__(f"Position x={x}, y={y} is already occupied by '{cell}'")
