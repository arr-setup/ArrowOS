def split(content: str) -> list[str]:
    return content.split('\n')

def parse(content: list, keys: tuple) -> list[dict]:
    return [ dict(zip(keys, item.split('::'))) for item in content ]