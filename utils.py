import csv
from pathlib import Path


PLST_SOURCE = Path('assets/plst_cardlist.csv')
FNM_SOURCE = Path('assets/fnm_cardlist.csv')


def get_plst_set_info(cardname: str, cardnumber: str) -> tuple[str, str]:
    with PLST_SOURCE.open('r', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)
        for line in reader:
            if line['Name'] == cardname and cardnumber in line['CN']:
                return line['Set'], line['CN']


def get_fnm_set_info(cardname: str) -> tuple[str, str]:
    with FNM_SOURCE.open('r', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)
        for line in reader:
            if line['Name'] == cardname:
                return line['Set'], line['CN']
            

def save_deckbox_to_moxfield(save_path: Path, card_dicts: list[dict[str, str]]) -> None:
    fieldnames = [
        'Count',
        'Name',
        'Edition Code',
        'Card Number',
        'Condition',
        'Language',
        'Foil'
    ]

    with save_path.open('w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames, lineterminator='\n')
        writer.writeheader()
        for entry in card_dicts:
            entry['Count'] = entry['Tradelist Count']
            if entry['Edition'] == 'The List':
                edition_code, cardnumber = get_plst_set_info(entry['Name'], entry['Card Number'])
                entry['Edition Code'] = edition_code
                entry['Card Number'] = cardnumber
            elif entry['Edition'] == 'Friday Night Magic':
                edition_code, cardnumber = get_fnm_set_info(entry['Name'])
                entry['Edition Code'] = edition_code
                entry['Card Number'] = cardnumber
            entry = {key: entry[key] for key in fieldnames}
            writer.writerow(entry)


def verify_path(path: Path|str, verify_exists: bool = False, verify_available: bool = False) -> Path:
    if isinstance(path, str):
        path = Path(path)
    if verify_exists and not path.exists():
        raise FileNotFoundError(path)
    if verify_available and path.exists():
        raise FileExistsError(path)
    return path