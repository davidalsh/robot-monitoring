
class DomainException(Exception):
    message = "Domain exception"
    code = "domain-exception"


class DetailNotFound(DomainException):
    message = "Oops! Not found..."
    code = "detail-not-found"
