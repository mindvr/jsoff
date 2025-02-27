import json
from typing import Any, List, Dict


def load_json_file(file_path) -> Any:
    with open(file_path, 'r') as file:
        return json.load(file)


def dict_comparator(input: Dict[str, Any], keys: List[str]):
    def compare(a: Dict[str, Any], b: Dict[str, Any]) -> int:
        for key in keys:
            if a[key] < b[key]:
                return -1
            elif a[key] > b[key]:
                return 1
        return 0

    return compare


def sort_list(element: List[Any], keys: List[str]) -> List[Any]:
    dicts = []
    lists = []
    primitives = []
    for item in element:
        if isinstance(item, Dict):
            dicts.append(item)
        elif isinstance(item, List):
            lists.append(item)
        else:
            primitives.append(item)
    for key in reversed(keys):
        dicts.sort(key=lambda x: x.get(key, ''))
    primitives.sort()
    return dicts + primitives + lists


def sort_dict(element: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    # first fields in fields order, then the rest alphabetically
    reordered = {}
    for field in fields:
        if field in element:
            reordered[field] = element[field]
    rest = sorted({k: k for k in element.keys() if k not in fields})
    for field in rest:
        reordered[field] = element[field]
    return reordered


def rec_sort(element: Any, parent: List[str], schema: Dict) -> Any:
    if isinstance(element, List):
        keys = schema.get(parent[-1], {}).get('pk', [])
        items = sort_list(element, keys)
        return [rec_sort(item, parent, schema) for item in items]
    elif isinstance(element, Dict):
        fields = schema.get(parent[-1], {}).get('fields', [])
        item = sort_dict(element, fields)
        for key, value in item.items():
            next_parent = parent + [key]
            item[key] = rec_sort(value, next_parent, schema)
        return item
    else:
        return element

def main(input_file: str, schema_file: str, output_file: str = None):
    schema = load_json_file(schema_file)
    object = load_json_file(input_file)
    sorted = rec_sort(object, ['root'], schema)
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(sorted, f, indent=2)
    else:
        print(json.dumps(sorted, indent=2))


if __name__ == '__main__':
    main("sample2.json", "schema2.json", "sample2_sorted.json")
