import csv
from pathlib import Path

from utils import save_deckbox_to_moxfield

PLST_SOURCE = Path('plst_cardlist.csv')

def match_trade(wishlist_path: Path|str, tradelist_path: Path|str, save_path: Path|str) -> None:
    if isinstance(wishlist_path, str):
        wishlist_path = Path(wishlist_path)
    if not wishlist_path.exists():
        raise FileNotFoundError(wishlist_path)
    
    if isinstance(tradelist_path, str):
        tradelist_path = Path(tradelist_path)
    if not tradelist_path.exists():
        raise FileNotFoundError(tradelist_path)
    
    if isinstance(save_path, str):
        save_path = Path(save_path)
    if save_path.exists():
        raise FileExistsError(save_path)
    
    wishlist: list[dict[str, int|str]] = []
    with wishlist_path.open('r', encoding='utf-8') as file:
        for line in file.readlines():
            split_line = line.split()
            if '*' in split_line[-1]:
                split_line.pop()
            
            count, *name = split_line[:-2]
            name = ' '.join(name)
            card = {'Count': count, 'Name': name}
            wishlist.append(card)

    with tradelist_path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        tradelist = [line for line in reader]
    
    trade_gen = lambda name : (card for card in tradelist
                               if card['Name'] == name)
    
    trades = []
    for wish in wishlist:
        availables = list(trade_gen(wish['Name']))
        if availables:
            total_count = sum([int(trade['Tradelist Count']) for trade in availables])
            print(wish['Name'], wish['Count'], '/', total_count)
        trades.extend(availables)
    
    save_deckbox_to_moxfield(save_path, trades)


if __name__ == '__main__':
    folder = Path('temp')
    wishlist_path = folder / 'wishlist.txt'
    tradelist_path = folder / 'deckbox_tradelist_260314.csv'
    save_path = folder / 'matching_trades.csv'
    match_trade(wishlist_path, tradelist_path, save_path)