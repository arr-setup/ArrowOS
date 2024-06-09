import json

def split(content: str) -> list[str]:
    return content.split('\n')

def parse(content: list, keys: tuple | None = None) -> list[dict] | dict:
    """
    Parse system params

    a = b -> {'a': 'b'}
    a = 1 -> {'a': '1'}
    """

    if keys is None:
        data = { item.split('=')[0] : '='.join(item.split('=')[1:]) for item in content }
        
        for param, val in data.items():
            data[param] = json.loads(val)
        
        return data
    else:
        return [ dict(zip(keys, item.split('::'))) for item in content ]