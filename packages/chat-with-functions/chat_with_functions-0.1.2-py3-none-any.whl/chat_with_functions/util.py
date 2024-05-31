def indent_content(content, indentation: int = 4) -> str:
    """
    Indent the content by the given number of spaces.
    """
    lines = content.split("\n")
    indented_lines = [f"{' ' * indentation}{line}" for line in lines]
    return "\n".join(indented_lines)


def omit(d: dict, *keys):
    res = dict(d)
    for k in keys:
        del res[k]
    return res
