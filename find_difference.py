import csv
from pathlib import Path

from utils import save_deckbox_to_moxfield, verify_path


def card_name_exists(path: Path, card_name: str):
    with path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for card in reader:
            if card['Name'] == card_name:
                return True
        return False


def find_missing(source_path: Path|str, tradelist_path: Path|str, save_path: Path|str) -> None:
    source_path = verify_path(source_path, verify_exists = True)
    tradelist_path = verify_path(tradelist_path, verify_exists = True)
    save_path = verify_path(save_path, verify_available = True)

    with source_path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        existing_cards = [card['Name'] for card in reader]
    
    availables: list[dict[str, int|str]] = []
    with tradelist_path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for card in reader:
            if card['Name'] not in existing_cards:
                availables.append(card)
    
    save_deckbox_to_moxfield(save_path, availables)


if __name__ == '__main__':
    folder = Path('temp')
    source_path = folder / 'deckbox_inventory_a_260323.csv'
    tradelist_path = folder / 'deckbox_tradelist_260314.csv'
    save_path = folder / 'possible_interests.csv'
    find_missing(source_path, tradelist_path, save_path)