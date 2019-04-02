# The Command Enumeration represents all of the valid commands, and includes a
# method for finding the closest matching Command instance based on a string
# input.

from enum import Enum

class Command(Enum):
    TO = "TO"
    REP = "REP"
    THISIS = "THISIS"
    INVALID = None

    # CLOSEST_MATCH takes a string representation of a command and returns the
    # closest matching Command, or Command.INVALID if the raw_command is really
    # far off.
    def closest_match(self, raw_command):
        assert isinstance(raw_command, str)

        score_dictionary = {
            "TO": 0,
            "REP": 0,
            "THISIS": 0
        }

        for key in score_dictionary:
            score_dictionary[key] -= abs(len(self.value) - len(raw_command))
            score_dictionary[key] += self._letters_in_common(raw_command)
        
        return _command_with_highest_score(score_dictionary)
        # Return the entry with the highest score. If there is a tie, return INVALID. If no commands have a positive score, return INVALID.

    # Return the Command with the highest score in the provided score
    # dictionary. If any scores tie for top or no scores are above 0, return INVALID.
    def _command_with_highest_score(self, score_dictionary):
        best_match = Command.INVALID.value
        for key in score_dictionary:
            if best_match is Command.INVALID.value or score_dictionary[key] > score_dictionary[best_match]:
                best_match = key
            elif score_dictionary[key] == score_dictionary[best_match]:
                return Command.INVALID

        return Command(best_match)

    # _letters_in_common counts how many of the characters in this Command are
    # also present in the raw_command. Duplicate characters in the Command will
    # be matched to the same character in raw_command, since this only adds a
    # single point in the case of THISIS, which does not affect the overall
    # score calculation.
    def _letters_in_common(self, raw_command):
        assert isinstance(raw_command, str)

        # Guard against INVALID Command case
        if self.value is None:
            return 0

        self_index = 0
        letters_in_common = 0
        
        for self_character in self.value:
            for raw_command_character in raw_command:
                if self_character == raw_command_character:
                    letters_in_common += 1
                    break

        return letters_in_common
