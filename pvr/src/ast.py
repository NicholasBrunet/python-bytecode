import ast

def from_source(source: str) -> ast.Module:
    try:
        ast_module = ast.parse(source, mode='exec')
    except SyntaxError as e:
        pass
    return ast_module
    #     error_line = e.text.rstrip('\n') if e.text else ""
        
    #     start = e.offset - 1 if e.offset else 0
    #     end = getattr(e, 'end_offset', e.offset) - 1 if getattr(e, 'end_offset', None) else start + 1
        
    #     caret_count = max(1, end - start)
    #     padding = " " * start
    #     carets = "^" * caret_count

    #     raise CompilerError(
    # f"""\n
    # File "<unknown>", line {e.lineno}
    #     {error_line}
    #     {padding}{carets}
    # SyntaxError: {e.msg}
    # """)