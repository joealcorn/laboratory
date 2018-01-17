class LaboratoryException(Exception):
    def __init__(self, message, *a, **kw):
        self.message = message
        super(LaboratoryException, self).__init__(*a, **kw)


class MismatchException(LaboratoryException):
    pass
