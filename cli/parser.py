# main method, load json file to dict

import json
import sys
from collections import defaultdict

from typing import Dict, Any, List, Set


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

    def to_dict(self):
        return {
            'count': self.count,
            'unique': len(set(self.values)),
            'ratio': f'{len(set(self.values)) / self.count * 100:.2f}'
        }


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

def find_pk_fields(parent_stats: Dict[str, Dict]) -> List[str]:
    pk_fields = []
    for field, stats in parent_stats.items():
        if (float(stats['ratio']) == 100.0 and
            stats['count'] > 1):
            pk_fields.append((field, stats['count']))

    # Sort desc by count
    pk_fields.sort(key=lambda x: x[1], reverse=True)
    return [field for field, _ in pk_fields]

def get_all_fields(parent_stats: Dict[str, Dict], pk_fields: List[str]) -> List[str]:
    # Start with PK fields
    all_fields = pk_fields.copy()

    # Add remaining fields alphabetically
    remaining = sorted(set(parent_stats.keys()) - set(pk_fields))
    all_fields.extend(remaining)

    return all_fields

def transform_statistics(statistic: Dict[str, Stat]) -> Dict[str, Dict]:
    # First, group by parent
    transformed = defaultdict(dict)
    for path, stat in statistic.items():
        if '.' in path:
            parent, prop = path.rsplit('.', 1)
            transformed[parent][prop] = stat.to_dict()

    # Then add pk and fields
    result = {}
    for parent, stats in transformed.items():
        result[parent] = {
            'pk': find_pk_fields(stats),
            'fields': get_all_fields(stats, find_pk_fields(stats)),
            'stats': stats
        }

    return result

def main(input_file: str, output_file: str = None):
    data = load_json_file(input_file)
    paths = set()
    statistic = defaultdict(Stat)
    parse_short_paths(data, ['root'], paths, statistic)

    transformed = transform_statistics(statistic)

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(transformed, f, indent=2)
    else:
        print(json.dumps(transformed, indent=2))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("sample2.json")
