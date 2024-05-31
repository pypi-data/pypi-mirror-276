from .constants import COLOR_MAPPING, RESET_CODE, CURSOR_UP, CLEAR

class ColorMeta(type):
    def __getattr__(cls, name):
        def apply_color(text):
            color_code = COLOR_MAPPING.get(name.lower(), "")
            return print('{color_code}{text}{RESET_CODE}'.format(
                color_code=color_code,
                text=text,
                RESET_CODE=RESET_CODE
            ))
        return apply_color

class crint(metaclass=ColorMeta):
    @staticmethod
    def unprint(lines=1):
        print((CURSOR_UP + CLEAR)*lines, end="")
