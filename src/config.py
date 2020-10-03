class Rate():
    def __init__(self, expected, rate="GB/s"):
        self.expected = expected
        self.rate = rate

    def __repr__(self):
        return f"{self.expected} {self.rate}"


class Config():
    expected_download = Rate(100)
    expected_upload = Rate(100)
