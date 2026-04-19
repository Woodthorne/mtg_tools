from pathlib import Path

from utils import (
    read_deckbox,
    read_wishlist,
    save_deckbox_to_moxfield,
    verify_path
)


def match_trade(wishlist_path: Path|str, tradelist_path: Path|str, save_path: Path|str, exact_match: bool = False) -> None:
    wishlist_path = verify_path(wishlist_path, verify_exists = True)
    tradelist_path = verify_path(tradelist_path, verify_exists = True)
    save_path = verify_path(save_path, verify_available = True)
    
    trades = []
    wishlist_gen = read_wishlist(wishlist_path)
    for wish in iter(wishlist_gen):
        if exact_match:
            trade_gen = read_deckbox(tradelist_path, wish['Name'], wish['Edition Code'], wish['Card Number'])
        else:
            trade_gen = read_deckbox(tradelist_path, wish['Name'])
        
        total_count = 0
        for trade in iter(trade_gen):
            trade_count = int(trade['Tradelist Count'])
            if trade_count > 0:
                total_count += int(trade['Tradelist Count'])
                trades.append(trade)
        
        if total_count > 0:
            print(wish['Name'], wish['Count'], '/', total_count)
    
    save_deckbox_to_moxfield(save_path, trades)


if __name__ == '__main__':
    folder = Path('temp')
    wishlist_path = folder / 'wishlist.txt'
    tradelist_path = folder / 'deckbox_tradelist_260314.csv'
    save_path = folder / 'matching_trades.csv'
    match_trade(wishlist_path, tradelist_path, save_path)