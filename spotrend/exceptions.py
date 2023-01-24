
class SpotrendAuthError(Exception):
    """
    This exception would be raised when there is an issue 
    with authenticating with the Spotify API, 
    such as an invalid access token or client ID.
    """
    pass


class SpotrendRequestError(Exception):
    """
    This exception would be raised when there is an issue 
    with making a request to the Spotify API, such as a network 
    error or invalid endpoint.
    """
    pass


class SpotrendPermissionError(Exception):
    """
    This exception would be raised when the user does not 
    have sufficient permissions to perform the requested action, 
    such as trying to modify a playlist they do not own.
    """
    pass


class SpotrendNotFoundError(Exception):
    """
    This exception would be raised when the requested 
    resource is not found, such as a track or album that does not exist.
    """
    pass


class SpotrendInvalidDataError(Exception):
    """
    This exception would be raised when the data passed 
    to the API is invalid, such as an invalid track URI or playlist name.
    """
    pass


class SpotrendQuotaError(Exception):
    """
    This exception would be raised when the user has reached their rate limit for the day.
    """
    pass


class SpotrendServerError(Exception):
    """
    This exception would be raised when there is an issue on Spotify server side.
    """
    pass


__all__ = [
    SpotrendAuthError,
    SpotrendRequestError,
    SpotrendPermissionError,
    SpotrendInvalidDataError,
    SpotrendServerError,
    SpotrendQuotaError,
    SpotrendNotFoundError,
]