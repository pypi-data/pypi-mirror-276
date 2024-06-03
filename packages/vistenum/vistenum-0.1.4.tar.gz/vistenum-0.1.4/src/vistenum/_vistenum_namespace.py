"""VistenumNamespace provides the namespace object used by the MetaVistenum
metaclass. It is instantiated by MetaVistenum when a new class is derived
from it or when a derived class is subclassed. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, TYPE_CHECKING

from vistutils.metas import BaseNamespace
from vistutils.parse import maybe
from vistutils.text import monoSpace

from vistenum import Member

if TYPE_CHECKING:
  from vistenum import MetaVistenum


class VistenumNamespace(BaseNamespace):
  """VistenumNamespace provides the namespace object used by the MetaVistenum
  metaclass. It is instantiated by MetaVistenum when a new class is derived
  from it or when a derived class is subclassed. """

  __enum_members__ = None

  def compile(self) -> dict:
    """Enum members must be instances of the Member class. """
    out = BaseNamespace.compile(self, )
    members = maybe(self.__enum_members__, [])
    return {**out, **dict(__enum_members__=members)}

  def __setitem__(self, key: str, val: object) -> None:
    """Instances of Member receive special treatment. """
    if isinstance(val, Member):
      existing = maybe(self.__enum_members__, [])
      self.__enum_members__ = [*existing, val]
    BaseNamespace.__setitem__(self, key, val)
