"""
Module containing exceptions for use with the Ronda class.
"""

class RondaFinishedError(Exception):
    """Error raised when trying to perform an action that can only
    be done if the ronda is still ongoing.
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = "The current ronda is finished."
        super(RondaFinishedError, self).__init__(msg)

class RondaNotFinishedError(Exception):
    """Error raised when trying to perform an action that can only
    be done once the ronda is finished.
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = "The current ronda is not yet finished."
        super(RondaNotFinishedError, self).__init__(msg)
