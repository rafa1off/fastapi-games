from configs.exceptions import BadRequest


def id_validation(game_id: int) -> int:
    if game_id >= 1:
        id = game_id
        return id
    else:
        raise BadRequest(detail="Id must be greater or equal to 1")
