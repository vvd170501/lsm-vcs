def splitlines(s: str) -> list[str]:
    res = s.splitlines(keepends=True)
    return [''] if res == [] else res
