import csv
from pathlib import Path


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
        fieldnames = list(reader.fieldnames)
        data = [line for line in reader]

    plst_loaded = False
    fieldnames.remove('Edition')

    with save_path.open('w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames, lineterminator='\n')
        writer.writeheader()
        for entry in data:
            if entry['Edition'] == 'The List':
                if not plst_loaded:
                    with PLST_SOURCE.open('r', encoding = 'utf-8') as file:
                        reader = csv.DictReader(file)
                        plst = {line['Name']: line['CN'] for line in reader}
                    plst_loaded = True
                entry['Edition Code'] = 'PLST'
                entry['Card Number'] = plst[entry['Name']]
                entry = {key: entry[key] for key in fieldnames}
                writer.writerow(entry)
    

if __name__ == '__main__':
    folder = Path('temp')
    source_path = folder / 'deckbox_tradelist_260105.csv'
    save_path = folder / 'converted_tradelist.csv'
    convert(source_path, save_path)