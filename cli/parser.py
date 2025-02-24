# main method, load json file to dict

import json
from collections import defaultdict

from typing import Dict, Any, List, Set, Tuple


def load_json_file(file_path) -> Any:
    with open(file_path, 'r') as file:
        return json.load(file)

class Stat:
    def __init__(self):
        self.count = 0
        self.values = []

    def add_count(self):
        self.count += 1

    def add_value(self, value):
        self.count += 1
        self.values.append(value)

    def __str__(self):
        if len(self.values) == 0:
            return f'{self.count}'
        else:
            return f'{self.count}, {len(set(self.values))}, {len(set(self.values)) / self.count * 100:.2f}%'

def parse_general_paths(element: Any, prefix: str, unique_paths: Set[str], statistic: Dict[str, Stat]) -> None:
    unique_paths.add(prefix)
    # if object is a List
    if isinstance(element, List):
        statistic[prefix].add_count()
        next_prefix = prefix + '.[]'
        for item in element:
            parse_general_paths(item, next_prefix, unique_paths, statistic)
    # if object is a Dict
    elif isinstance(element, Dict):
        statistic[prefix].add_count()
        for key, value in element.items():
            # append key to unique_prefix copy
            next_prefix = prefix + '.' + key
            parse_general_paths(value, next_prefix, unique_paths, statistic)
    # if object is a primitive
    else:
        statistic[prefix].add_value(element)

def parse_short_paths(element: Any, parent: List[str], unique_paths: Set[str], statistic: Dict[str, Stat]) -> None:
    path = '.'.join(parent)
    unique_paths.add(path)
    if isinstance(element, List):
        statistic[path].add_count()
        for item in element:
            parse_short_paths(item, parent, unique_paths, statistic)
    elif isinstance(element, Dict):
        statistic[path].add_count()
        for key, value in element.items():
            next_parent = [parent[-1], key]
            parse_short_paths(value, next_parent, unique_paths, statistic)
    else:
        statistic[path].add_value(element)

def main(file_path: str):
    data = load_json_file(file_path)
    paths = set()
    statistic = defaultdict(Stat)
    # parse_general_paths(data, '', paths, statistic)
    parse_short_paths(data, ['root'], paths, statistic)
    for path in sorted(paths):
        print(path, statistic.get(path))


if __name__ == '__main__':
    main('sample1.json')
