from core.file_reader import PythonFileReader

def main():
    reader = PythonFileReader("input.py")
    is_valid, error = reader.validate()
    if not is_valid:
        print(f"Error: {error}")
    else:
        lines, error = reader.read_lines()
        if error:
            print(f"Error: {error}")
        else:
            print(f"Read {lines} lines")

if __name__ == '__main__':
    main()