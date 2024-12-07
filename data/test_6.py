def has_lambda_expression(content: str) -> bool:
    """
    Check if a line contains lambda expressions.
    Ignores lambda mentions in strings and comments.
    """
    pos = 0
    while True:
        pos = content.find('lambda', pos)
        if pos == -1:
            return False
            
        # Check if found lambda is the actual keyword
        if pos > 0 and content[pos-1].isalnum():
            pos += 1
            continue
            
        next_char_pos = pos + 6
        if next_char_pos < len(content) and content[next_char_pos].isalnum():
            pos += 1
            continue
            
        # Check if lambda is in string or comment
        if not StringAnalyzer.is_in_string(content, pos):
            # Check if it's in a comment
            line_start = content.rfind('\n', 0, pos)
            if line_start == -1:
                line_start = 0
            comment_pos = content.find('#', line_start, pos)
            if comment_pos == -1:
                return True
        pos += 1
    return False

lambda_express = ""