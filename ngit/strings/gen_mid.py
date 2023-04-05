def generate_next_string(a: str) -> str | None:
    """Generate next string in lexicographical order among strings
    with characters in ['0', '2']"""
    a_mut = list(a)
    i = len(a) - 1
    while i != -1 and a[i] == '2':
        a_mut[i] = '0'
        i -= 1
    if i == -1:
        return None
    a_mut[i] = '2'
    return ''.join(a)


def generate_middle_string(a: str | None, b: str | None) -> str:
    """Generate middle string in lexicographical order assuming that a, b
    consist of '0', '2' except for the last character which is always '1'
    and a < b."""
    if a is None and b is None:
        return '1'
    if a is None:
        assert b is not None  # TODO check
        return b[:-1] + '01'
    if b is None:
        res = generate_next_string(a[:-1])
        if res is None:
            return a[:-1] + '21'
        return res + '1'
    if len(a) == len(b):
        if generate_next_string(a[:-1]) == b[:-1]:
            return a[:-1] + '21'
        return generate_next_string(a[:-1]) + '1'  # type: ignore  # TODO check
    if len(a) < len(b):
        return b[:-1] + '01'
    return a[:-1] + '21'
