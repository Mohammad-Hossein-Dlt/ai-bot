import re
from re import Pattern

# request_pattern = re.compile(
#     r'^(?P<name>[A-Za-z0-9_]+)?'
#     r'(?:s:(?P<step>-?[A-Za-z0-9_]+))?'
#     r'(?:p:(?P<page>-?[A-Za-z0-9_]+))?'
#     r'(?:o:(?P<origin>-?[A-Za-z0-9_]+))?'
#     r'(?:i:(?P<index>-?[A-Za-z0-9_]+))?'
#     r'(?:m:(?P<message_id>-?[A-Za-z0-9_]+))?$'
# )

# close_request_pattern = r'^(?:close:(?P<id>-?[A-Za-z0-9_]+))?$'

# def special_request_pattern(name: str) -> Pattern:
#     return re.compile(
#         fr'^{name}([A-Za-z0-9_]+:[A-Za-z0-9_]+)+$',
#     )
    
def request_pattern(
    name: str | None = None,
    **kwargs: str,
) -> Pattern | None:
    
    pattern = ""
    
    if name:
        pattern += fr'^(?P<name>-?{name}+)?'
    
    for alias, name in kwargs.items():        
        pattern += fr"(?:{alias}:(?P<{name}>-?[A-Za-z0-9_]+))?"
        
    if pattern:
        if kwargs:
            pattern += "$"
        return re.compile(pattern)
    
    return None

def request_decoder(encoded: str, pattern: Pattern) -> dict:
    return re.match(pattern, encoded).groupdict()