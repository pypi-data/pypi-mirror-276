import json
import re
from collections import namedtuple

from thefuzz import fuzz, process

from .data import grapes as data

grape_to_object = {}


def format_name(name: str) -> str:
    return name.lower().replace("i̇", "i").title()


for o in data:
    name = format_name(o["name"])
    grape_to_object[name] = {**o, "name": name}

# named tuple


Grape = namedtuple("Grape", ["name", "synonyms", "description", "color", "numeric"])


# create a generator of grapes
class ExistingGrapes:
    __slots__ = ["grapes", "_synonym_to_name"]

    def __init__(self) -> None:
        self.grapes = []
        self._synonym_to_name = {}
        for name in grape_to_object:
            grape = Grape(
                name=name,
                synonyms=grape_to_object[name].get("synonyms", []),
                description=grape_to_object[name].get("description", None),
                color=grape_to_object[name].get("color", None),
                numeric=list(grape_to_object.keys()).index(name),
            )
            self.grapes.append(grape)
            self._synonym_to_name[name] = name
            for synonym in grape.synonyms:
                if re.search(r"\d", synonym) or re.search(r"×", synonym):
                    continue
                self._synonym_to_name[synonym] = name

    def __iter__(self) -> Grape:
        yield from self.grapes

    def __getitem__(self, index: int) -> Grape:
        return self.grapes[index]

    def __len__(self) -> int:
        return len(self.grapes)

    def __repr__(self) -> str:
        return f"ExistingGrapes({len(self.grapes)})"

    def __str__(self) -> str:
        return f"ExistingGrapes({len(self.grapes)})"

    def get(self, **kwargs) -> Grape:
        for grape in self.grapes:
            if all(getattr(grape, k) == v for k, v in kwargs.items()):
                return grape

    def search_fuzzy(self, grape: str, threshold: int = 82) -> Grape:
        name, distance = process.extractOne(
            grape, self._synonym_to_name.keys(), scorer=fuzz.QRatio
        )
        if distance > threshold:
            return self.get(name=self._synonym_to_name[name])
        else:
            return None


grapes = ExistingGrapes()
