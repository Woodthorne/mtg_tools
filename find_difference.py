import csv
from collections import defaultdict
from pathlib import Path

from utils import read_deckbox, save_deckbox_to_moxfield, verify_path

def card_name_exists(path: Path, card_name: str):
    with path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for card in reader:
            if card['Name'] == card_name:
                return True
        return False


def find_difference(source_path: Path|str, tradelist_path: Path|str, save_path: Path|str, match_printing: bool = False) -> None:
    source_path = verify_path(source_path, verify_exists = True)
    tradelist_path = verify_path(tradelist_path, verify_exists = True)
    save_path = verify_path(save_path, verify_available = False)
    
    existing_gen = read_deckbox(source_path)
    existing_cards = defaultdict(list)
    for card in iter(existing_gen):
        existing_cards[card['Name']].append((card['Edition Code'], card['Card Number']))
    
    availables = []
    tradelist_gen = read_deckbox(tradelist_path)
    for trade in iter(tradelist_gen):
        if match_printing and (trade['Edition Code'], trade['Card Number']) not in existing_cards[trade['Name']]:
            availables.append(trade)
        elif not match_printing and trade['Name'] not in existing_cards.keys():
            availables.append(trade)
    
    save_deckbox_to_moxfield(save_path, availables)
