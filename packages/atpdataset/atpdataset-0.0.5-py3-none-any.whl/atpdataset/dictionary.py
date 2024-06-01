import json
from collections import defaultdict
from pathlib import Path

import toml
import yaml


class Dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_json(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = json.dumps(
            dict(self),
            default=str,
            ensure_ascii=False,
            indent=indent,
        )
        if path is not None:
            path = _path_suffix_check(path, suffix=".json")
            _save_string_to_file(ret, path)
        return ret

    def to_yaml(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = yaml.dump(
            dict(self),
            default_flow_style=False,
            allow_unicode=True,
            indent=indent,
        )
        if path is not None:
            _save_string_to_file(ret, path)
        return ret

    def to_toml(self, path: str | Path | None = None) -> str:
        ret = toml.dumps(dict(self))
        if path is not None:
            _save_string_to_file(ret, path)
        return ret


class DictDefault(defaultdict):
    def __init__(self, *args, **kwargs):
        super().__init__(dict, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict(self)

    # def to_defaultdict(self) -> defaultdict:
    #     return defaultdict(self)

    def to_json(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = json.dumps(
            dict(self),
            default=str,
            ensure_ascii=False,
            indent=indent,
        )
        if path is not None:
            path = _path_suffix_check(path, suffix=".json")
            _save_string_to_file(ret, path)
        return ret

    def to_yaml(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = yaml.dump(
            dict(self),
            default_flow_style=False,
            allow_unicode=True,
            indent=indent,
        )
        if path is not None:
            _save_string_to_file(ret, path)
        return ret

    def to_toml(self, path: str | Path | None = None) -> str:
        ret = toml.dumps(dict(self))
        if path is not None:
            _save_string_to_file(ret, path)
        return ret

    def from_json(self, path: str | Path) -> None:
        with open(path, "r", encoding="utf-8") as file:
            self.update(json.load(file))

    def from_yaml(self, path: str | Path) -> None:
        with open(path, "r", encoding="utf-8") as file:
            self.update(yaml.safe_load(file))

    def from_toml(self, path: str | Path) -> None:
        with open(path, "r", encoding="utf-8") as file:
            self.update(toml.load(file))


def _save_string_to_file(string: str, path: str | Path) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(string)

    return


def _path_suffix_check(path: Path | str, suffix: str) -> Path:
    if isinstance(path, str):
        path = Path(path)

    if path.suffix != suffix:
        path = path.with_suffix(suffix)
    return path
