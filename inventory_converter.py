import csv
from pathlib import Path

from utils import save_deckbox_to_moxfield


PLST_SOURCE = Path('plst_cardlist.csv')


def convert(source_path: Path|str, save_path: Path|str) -> None:
    if isinstance(source_path, str):
        source_path = Path(source_path)
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    
    if isinstance(save_path, str):
        save_path = Path(save_path)
    if save_path.exists():
        raise FileExistsError(save_path)
    
    with source_path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [line for line in reader]

    save_deckbox_to_moxfield(save_path, data)
    

if __name__ == '__main__':
    folder = Path('temp')
    source_path = folder / 'deckbox_tradelist_260108.csv'
    save_path = folder / 'converted_tradelist.csv'
    convert(source_path, save_path)