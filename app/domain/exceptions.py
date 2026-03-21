from app.domain.schemas import Cell


class GameError(Exception):
    pass


class InvalidMoveError(GameError):
    pass


class GameNotFoundError(GameError):
    def __init__(self, game_id: str):
        super().__init__(f"Game '{game_id}' not found")


class GameFinishedError(GameError):
    def __init__(self):
        super().__init__("Game is already finished")


class CellOccupiedError(InvalidMoveError):
    def __init__(self, x: int, y: int, cell: Cell):
        super().__init__(f"Position x={x}, y={y} is already occupied by '{cell}'")
