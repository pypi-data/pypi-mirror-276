"""The BaseEnum class is derived from MetaVistenum. When creating new
enumerations, subclass BaseEnum rather than setting the metaclass keyword
argument to MetaVistenum. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistenum import MetaVistenum


class BaseEnum(metaclass=MetaVistenum):
  """The BaseEnum class is derived from MetaVistenum. When creating new
  enumerations, subclass BaseEnum rather than setting the metaclass keyword
  argument to MetaVistenum. """
  pass
