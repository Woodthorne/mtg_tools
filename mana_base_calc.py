class ManaBaseCalculator:
    def __init__(
        self,
        pips_w: int = 0,
        pips_u: int = 0,
        pips_b: int = 0,
        pips_r: int = 0,
        pips_g: int = 0,
        total_sources: int = 24
    ) -> None:
        self.pips = {
            'w': pips_w,
            'u': pips_u,
            'b': pips_b,
            'r': pips_r,
            'g': pips_g
        }
        self.total_sources = total_sources
        self.sources = self.calculate_mana_sources()
        self.colors: dict[str, str] = {
            'w': 'white',
            'u': 'blue',
            'b': 'black',
            'r': 'red',
            'g': 'green'
        }

    def calculate_mana_sources(self) -> dict[str, float]:
        sources: dict[str, float] = {}
        for color in ['w', 'u', 'b', 'r', 'g']:
            source_count = self.source_count(self.pips[color])
            if source_count:
                sources[color] = source_count
        
        return sources
    
    def calculate_even_mana_sources(self) -> dict[str, int]:
        remaining_sources = self.sources.copy()
        even_sources: dict[str, int] = {}
        for _ in range(self.total_sources):
            neediest_color = max(remaining_sources, key = lambda x: remaining_sources[X])
            if neediest_color not in even_sources.keys():
                even_sources[neediest_color] = 0
            even_sources[neediest_color] += 1
            remaining_sources[neediest_color] -= 1

        return {color: even_sources[color] for color in self.sources.keys()}
    
    def source_count(self, pip_count: int) -> float:
        return pip_count / sum(self.pips.values()) * self.total_sources
    
    def print_sources(self) -> None:
        for color in self.sources:
            print(self.colors[color], ':', '{:.2f}'.format(self.sources[color]))
    
    def print_even_sources(self) -> None:
        even_sources = self.calculate_even_mana_sources()
        for color in even_sources:
            print(self.colors[color], ':', '{:.2f}'.format(even_sources[color]))



if __name__ == '__main__':
    kwargs = dict(
        pips_w = 33,
        pips_u = 24,
        pips_g = 43,
        total_sources = 39
    )
    mbc = ManaBaseCalculator(**kwargs)
    mbc.print_sources()
    print('===================')
    mbc.print_even_sources()
