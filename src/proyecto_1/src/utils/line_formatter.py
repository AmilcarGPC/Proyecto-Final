# src/utils/line_formatter.py

class LineFormatter:
    MAX_LINE_LENGTH = 80

    @staticmethod
    def format_line(line: str) -> list[str]:
        """Format a line to ensure it doesn't exceed MAX_LINE_LENGTH characters."""
        indent = len(line) - len(line.lstrip())
        indent_str = ' ' * indent
        working_line = line.strip()

        if line.strip().startswith(('from ', 'import ')):
            return LineFormatter._format_import(line, indent_str)

        # If line is within limit, return as is
        if len(line) <= LineFormatter.MAX_LINE_LENGTH:
            return [line]

        # Handle function definitions
        if line.strip().startswith('def ') and '(' in line:
            return LineFormatter._format_function_def(line, indent_str)

        # Handle assignments with constructor calls or long expressions
        if '=' in line:
            return LineFormatter._format_assignment(line, indent_str)

        # Default formatting for other long lines
        return LineFormatter._format_generic(line, indent_str)
    
    @staticmethod
    def _format_import(line: str, indent: str) -> list[str]:
        """Format import statement with multiple items."""
        working_line = line.strip()
        
        # Handle simple imports differently (with backslash)
        if line.strip().startswith('import '):
            items = [item.strip() for item in line[6:].strip().split(',')]
            formatted = []
            current_line = 'import '
            
            for i, item in enumerate(items):
                if not item:  # Skip empty items
                    continue
                if len(current_line + item) <= LineFormatter.MAX_LINE_LENGTH:
                    current_line += (', ' if current_line != 'import ' else '') + item
                else:
                    formatted.append(current_line + ', \\')
                    current_line = indent + item
            
            if current_line:
                formatted.append(current_line)
            return formatted
        
        # Handle from ... import with parentheses
        if '(' in line and ')' in line:
            import_part = line[:line.index('(')]
            items_part = line[line.index('(')+1:line.rindex(')')].strip()
        else:
            import_part = line[:line.index('import') + 6]
            items_part = line[line.index('import') + 6:].strip()
        
        items = [item.strip() for item in items_part.split(',')]
        formatted = [f"{import_part.strip()} ("]
        items_indent = indent + ' ' * 4

        for i, item in enumerate(items):
            if not item:  # Skip empty items
                continue
            if i < len(items) - 1:
                formatted.append(f"{items_indent}{item},")
            else:
                formatted.append(f"{items_indent}{item}")
        
        formatted.append(f"{indent})")
        return formatted

    @staticmethod
    def _format_function_def(line: str, indent: str) -> list[str]:
        """Format function definition with parameters."""
        # Split into function name and parameters
        func_part = line[:line.index('(')]
        params_part = line[line.index('('):].strip('():')
        params = [p.strip() for p in params_part.split(',')]

        # Format function header
        formatted = [f"{func_part}("]
        param_indent = indent + ' ' * 8  # Extra indentation for parameters

        # Add parameters
        for i, param in enumerate(params):
            if i < len(params) - 1:
                formatted.append(f"{param_indent}{param.strip()},")
            elif not param.endswith('):') and not param.endswith(':'):
                formatted.append(f"{param_indent}{param.strip()}):")
            else:
                formatted.append(f"{param_indent}{param.strip()}")

        return formatted

    @staticmethod
    def _format_assignment(line: str, indent: str) -> list[str]:
        """Format assignment statements."""
        left, right = line.split('=', 1)
        if '(' in right and ')' in right:  # Constructor or function call
            # Get constructor/function name and arguments
            func_name = right[:right.index('(')].strip()
            args_str = right[right.index('(')+1:right.rindex(')')].strip()
            latest = right[right.rindex(')'):].strip() if right.rindex(')') < len(right) - 1 else ''
            args = [arg.strip() for arg in args_str.split(',')]

            formatted = [f"{indent}{left.strip()} = {func_name}("]
            arg_indent = indent + ' ' * 4

            # Format each argument
            for i, arg in enumerate(args):
                if i < len(args) - 1:
                    formatted.append(f"{arg_indent}{arg},")
                else:
                    formatted.append(f"{arg_indent}{arg}")
            formatted.append(f"{indent}{latest}")
            return formatted

        return LineFormatter._format_generic(line, indent)

    @staticmethod
    def _format_generic(line: str, indent: str) -> list[str]:
        """Generic formatting for long lines."""
       
        words = line.split()
        current_line = indent
        formatted = []

        for word in words:
            # Check if adding the word would exceed the limit
            if len(current_line) + len(word) + 1 <= LineFormatter.MAX_LINE_LENGTH:
                current_line += (' ' if current_line.strip() else '') + word
            else:
                if current_line.strip():
                    # Add backslash to continue the line
                    formatted.append(current_line + " \\")
                current_line = indent + word

        if current_line.strip():
            # Last line doesn't need backslash
            formatted.append(current_line)
  
        return formatted