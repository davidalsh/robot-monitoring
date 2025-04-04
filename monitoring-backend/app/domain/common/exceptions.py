from typing import Optional


class DomainException(Exception):
    message = "Domain exception"
    code = "domain-exception"
    status_code = 500

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message


class DetailNotFound(DomainException):
    message = "Oops! Not found..."
    code = "detail-not-found"
    status_code = 404


class ImpossibleAction(DomainException):
    message = "Bad request. Impossible action"
    code = "bad-request-impossible-action"
    status_code = 400
