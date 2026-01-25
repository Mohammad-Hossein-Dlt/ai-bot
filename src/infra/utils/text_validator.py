import re
import string

# MARKDOWN_CHARS = "_*~`#->[](){|}@&"
MARKDOWN_CHARS = "_*~`#->[](){|}@&"

allowed_punctuation = ''.join(c for c in string.punctuation if c not in MARKDOWN_CHARS)


def is_valid_text(text):
    pattern = fr'^[\u0600-\u06FF\uFB8A-\uFBFCa-zA-Z0-9\u0660-\u0669\u06F0-\u06F9\s{re.escape(allowed_punctuation)}]+$'
    return bool(re.match(pattern, text))

