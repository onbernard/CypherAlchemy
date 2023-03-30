from typing import (
    Dict,
    List
)
import string
import random

from pydantic import BaseModel


def random_str(length: int = 8) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class Node(BaseModel):
    @property
    def label(self) -> str:
        return self.__class__.__name__

    @property
    def properties(self) -> Dict:
        return self.dict()

    @classmethod
    def property_keys(cls) -> List:
        return list(cls.schema()["properties"].keys())

    @classmethod
    def match(cls, **properties):
        if not all(k in cls.property_keys() for k in properties.keys()):
            raise ValueError("Properties in match statement must match class properties")
        outp = f"(n{random_str()}:{cls.__name__}"
        if properties:
            outp += " {" + ", ".join(f"{k}: {v}" for k,v in properties.items()) + "}"
        outp += ")"
        return outp


class Edge(BaseModel):
    nfrom: Node
    nto: Node

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def properties(self):
        return self.dict(exclude={"nfrom", "nto"})

    @classmethod
    def property_keys(cls) -> List:
        return list(k for k in cls.schema()["properties"].keys() if k not in ("nfrom", "nto"))

    @classmethod
    def match(cls, **properties):
        if not all(k in cls.property_keys() for k in properties.keys()):
            raise ValueError("Properties in match statement must match class properties")
        outp = f"[r{random_str()}:{cls.__name__}"
        if properties:
            outp += " {" + ", ".join(f"{k}: {v}" for k,v in properties.items()) + "}"
        outp += "]"
        return outp