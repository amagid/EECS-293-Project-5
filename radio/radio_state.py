class RadioState:
    def __init__(self, current_section, repeats, partial_address, invalid_count):
        self.current_section = current_section
        self.repeats = repeats
        self.partial_address = partial_address
        self.invalid_count = invalid_count