from builtins import bytes
from datetime import datetime
from math import floor

html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;"
    }


class Util:

    @classmethod
    def transform_to_string(cls, dt_time):
        if dt_time and type(dt_time) is datetime:
            return dt_time.strftime("%b %d, %Y, %H:%M %p UTC%z")
        return dt_time

    @classmethod
    def convert_seconds(cls, seconds):
        if not isinstance(seconds, float) and not isinstance(seconds, int):
            return seconds

        seconds = int(seconds)
        output = ''

        days = floor(seconds / (3600 * 24))
        output += cls.__append_to_time(days, 'days')

        seconds -= days * 3600 * 24
        hours = floor(seconds / 3600)
        output += cls.__append_to_time(hours, 'hours')

        seconds -= hours * 3600
        minutes = floor(seconds / 60)
        output += cls.__append_to_time(minutes, 'minutes')

        return output.strip()

    @classmethod
    def __append_to_time(cls, time, append_str):
        if time:
            return ' ' + str(time) + ' ' + append_str
        return ''

    @classmethod
    def html_escape(cls, text):
        return "".join(html_escape_table.get(c, c) for c in text)

    @classmethod
    def transform_message(cls, text):
        if text:
            if type(text) is bytes:
                text = cls.decode_bytes_to_string(text)
            if type(text) is tuple:
                text = " ".join(text)
        return text

    @classmethod
    def transform_failure_output(cls, text):
        if text:
            if type(text) is bytes:
                text = cls.decode_bytes_to_string(text)
            if type(text) is tuple:
                text = " ".join(text)
            text = cls.html_escape(text)
            text = text.replace("\\n", '&#10;')
            text = text.replace("\\t", '&#9;')
            text = text.replace("\t", '&#9;')
            return text.replace("\n", '&#10;')
        return text

    @classmethod
    def decode_bytes_to_string(cls, bytes, encoding='utf8'):
        if bytes:
            return bytes.decode(encoding=encoding, errors='ignore') # default: 'utf-8'
        return str(bytes)
