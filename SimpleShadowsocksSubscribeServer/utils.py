class AcceptType:
    def __init__(self, mime_type: str, weight: float = 1):
        self.mime_type = mime_type
        self.weight = weight

    def __ge__(self, other):
        if self.weight > other.weight:
            return True
        if self.weight == other.weight and self.mime_type > other.mime_type:
            return True
        return False

    def __le__(self, other):
        if self.weight > other.weight:
            return False
        if self.weight == other.weight and self.mime_type > other.mime_type:
            return False
        return True
