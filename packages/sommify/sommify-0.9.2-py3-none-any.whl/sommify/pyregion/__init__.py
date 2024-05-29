from collections import namedtuple

from thefuzz import fuzz, process

from .data import regions as data


def flatten(_l: list) -> list:
    return [item for sublist in _l for item in sublist]


# create a namedtuple
Region = namedtuple(
    "Region",
    ["name", "synonyms", "parent", "subregions", "country", "description"],
)


def get_subregions(branch: dict) -> list:
    obj = Region(
        name=branch["name"],
        synonyms=branch.get("synonyms", []),
        parent=branch.get("parent", None),
        subregions=[x["name"] for x in branch.get("subregions", [])],
        country=branch["country"],
        description=branch.get("description", None),
    )

    return [
        obj,
        *flatten(
            [
                get_subregions(
                    {
                        **subbranch,
                        "parent": branch["name"],
                        "country": branch["country"],
                    }
                )
                for subbranch in branch.get("subregions", [])
            ]
        ),
    ]


class ExistingRegions:
    __slots__ = ["regions", "region_tree", "_synonym_to_name"]

    def __init__(self) -> None:
        self.regions = sorted(
            flatten([get_subregions(branch) for branch in data]),
            key=lambda x: x.name,
        )
        self.region_tree = data
        self._synonym_to_name = {}
        for region in self.regions:
            self._synonym_to_name[region.name] = region.name
            for synonym in region.synonyms:
                self._synonym_to_name[synonym] = region.name

    def __getitem__(self, key: str) -> Region:
        return self.regions[key]

    def __len__(self) -> int:
        return len(self.regions)

    def __iter__(self) -> Region:
        yield from self.regions

    def __repr__(self) -> str:
        return f"ExistingRegions({self.regions})"

    def __str__(self) -> str:
        return f"ExistingRegions({self.regions})"

    def get(self, **kwargs) -> Region:
        for region in self.regions:
            if all(getattr(region, key) == value for key, value in kwargs.items()):
                return region

    def flatten_branch(self, branch: dict) -> list:
        return [
            self.get(name=branch["name"]),
            *flatten(
                [
                    self.flatten_branch(subregion)
                    for subregion in branch.get("subregions", [])
                ]
            ),
        ]

    def find_branch(self, name: str, branch: object = None) -> object:
        if branch is None:
            branch = self.region_tree

        for region in branch:
            if region["name"] == name:
                return region

            res = self.find_branch(name, region.get("subregions", []))

            if res is not None:
                return res

        return None

    def get_descendants(self, region: object) -> list:
        branch = self.find_branch(region if isinstance(region, str) else region.name)

        if branch is None:
            return []

        return self.flatten_branch(branch)[1:]

    def search_fuzzy(self, name: str, threshold: int = 82) -> Region:
        name, distance = process.extractOne(
            name, self._synonym_to_name.keys(), scorer=fuzz.QRatio
        )

        if distance < threshold:
            return None

        return self.get(name=self._synonym_to_name[name])

    def find_closest_geo(self, region: str, subset: object = None) -> list:
        """Find geographically closest region to name in subset. Ordering of closeness is:
        0. regions that are children of name
        1. regions that are siblings of name (same parent)
        2. regions that are cousins of name (same grandparent)
        ...
        N. same country
        """

        if isinstance(region, str):
            region = self.get(name=region)

        if subset is None:
            subset = self.regions

        # check regional hierarchy
        current = region
        while current:
            descendants = self.get_descendants(current)
            descendants = [d for d in descendants if d in subset and d != region]
            if len(descendants) > 0:
                return descendants

            current = self.get(name=current.parent)

        # check country
        same_country = [
            r for r in subset if r.country == region.country and r != region
        ]
        if len(same_country) > 0:
            return same_country

        return None


regions = ExistingRegions()
