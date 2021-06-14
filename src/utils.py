import datetime
from client_exception import BadRequestException

class Utils():
    @staticmethod
    def to_iso_zulu(input_date):
        # TODO: Verify if current timezone is already UTC, so that we don`have problems
        if input_date is None:
            return None
        return input_date.replace(microsecond=0).replace(tzinfo=datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
    
    @staticmethod
    def string_to_bool(input_string):
        if input_string is None:
            return False
        elif input_string.lower() == "false":
            return False
        elif input_string.lower() == "true":
            return True
        else:
            raise BadRequestException('Invalid boolean value', 'String "' + input_string + '" is not a valid boolean.')
    