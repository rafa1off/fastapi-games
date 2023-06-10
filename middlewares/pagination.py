from configs.exceptions import BadRequest


def pagination(limit: int = 5, page: int = 1):
    if limit >= 0 and page >= 1:
        skip = limit * (page - 1)
        page_data = {"limit": limit, "skip": skip}
        return page_data
    else:
        raise BadRequest(
            detail="Limit must be greater or equal to 0"
            " and page greater or equal to 1"
        )
