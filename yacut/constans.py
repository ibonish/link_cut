import string

MAX_LENGTH_LONG = 2000
LENGTH_SHORT = 6
MAX_LENGTH_SHORT = 16
CHARS = string.ascii_letters + string.digits
RE_PATTERN = fr'^[{CHARS}]*$'
SHORT_EXIST = 'Предложенный вариант короткой ссылки уже существует.'
UNCORRECT = 'Указано недопустимое имя для короткой ссылки'
REDIRECT_FUNC = 'short_link_url'
