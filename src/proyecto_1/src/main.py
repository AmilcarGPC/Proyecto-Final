# main.py
import argparse
from pathlib import Path
from colorama import init, Fore, Style
from core.contadores.analizador import AnalizadorCodigo, ExcepcionAnalizador

def get_filename_from_path(filepath: str) -> str:
    return Path(filepath).name

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Python file analyzer - counts physical and logical lines of code"
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the Python file to analizar"
    )
    return parser.parse_args()

def print_results(result):
    print(f"{Fore.GREEN}File processed successfully!{Style.RESET_ALL}")
    print(f"Physical lines: {result.lineas_fisicas}")
    print(f"Logical lines: {result.lineas_logicas}")
    print(f"{Fore.GREEN}Metrics saved to storage.{Style.RESET_ALL}")

def main() -> None:
    init()
    args = parse_arguments()
    filepath = args.filepath
    filename = get_filename_from_path(filepath)
    
    try:
        analizador = AnalizadorCodigo()
        result = analizador.analizar_archivo(filepath, filename)
        print_results(result)
    
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{filepath}' not found{Style.RESET_ALL}")
    except ExcepcionAnalizador as e:
        print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()