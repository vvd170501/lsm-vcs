def generate_next_string(a: str) -> str | None:
    """Generate next string in lexicographical order among strings
    with characters in ['0', '2']"""
    a = list(a)
    i = len(a) - 1
    while a[i] == '2':
        a[i] = '0'
        i -= 1
    if i == -1:
        return None
    a[i] = '2'
    return ''.join(a)


def generate_middle_string(a: str, b: str) -> str:
    """Generate middle string in lexicographical order assuming that a, b
    consist of '0', '2' except for the last character which is always '1'
    and a < b."""
    if len(a) == len(b):
        if generate_next_string(a[:-1]) == b[:-1]:
            return a[:-1] + '21'
        return generate_next_string(a[:-1]) + '1'
    return ''
