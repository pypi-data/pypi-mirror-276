"""Vistenum derived classes should use the Member class defined here when
defining members. The Member class implements membership functionality by
through the descriptor protocol. Instances may contain an inner object.
This object is stored at the attribute 'inner'. Please note, that this
object is optional and is ignored by the derived class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, TYPE_CHECKING

from vistutils.fields import EmptyField
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  from vistenum import MetaVistenum


class Member:
  """Vistenum derived classes should use the Member class defined here when
  defining members. The Member class implements membership functionality by
  through the descriptor protocol. Instances may contain an inner object.
  This object is stored at the attribute 'inner'. Please note, that this
  object is optional and is ignored by the derived class. """

  __inner_object__ = None
  __field_name__ = None
  __field_owner__ = None

  inner = EmptyField()
  name = EmptyField()

  @name.GET
  def _getFieldName(self) -> str:
    """Getter-function for the field name."""
    return self.__field_name__

  @name.SET
  def _setFieldName(self, *_) -> Never:
    """Illegal setter-function for the field name."""
    e = """The field name is read-only. """
    raise TypeError(e)

  @inner.GET
  def _getInnerObject(self) -> object:
    """Getter-function for the inner object."""
    return self.__inner_object__

  @inner.SET
  def _setInnerObject(self, innerObject: object) -> None:
    """Setter-function for the inner object."""
    if self.__inner_object__ is not None:
      e = """The inner object of member: '%s' is already set to: '%s', but
      was attempted to be set to: '%s'. """
      name = self.name
      existing = self.__inner_object__.__str__()
      newObject = innerObject.__str__()
      raise TypeError(monoSpace(e % (name, existing, newObject)))
    self.__inner_object__ = innerObject

  def __init__(self, *args, **kwargs) -> None:
    if args and kwargs:
      self.__inner_object__ = (args, kwargs)
    elif args:
      if len(args) == 1:
        self.__inner_object__ = args[0]
      else:
        self.__inner_object__ = [*args, ]
    elif kwargs:
      self.__inner_object__ = {**kwargs, }
    else:
      pass

  def __set_name__(self, enumClass: MetaVistenum, name: str) -> None:
    if enumClass.__class__.__name__ != 'MetaVistenum':
      e = typeMsg('enumClass', enumClass, MetaVistenum)
      raise TypeError(e)
    self.__field_name__ = name
    self.__field_owner__ = enumClass

  def __get__(self, _, enumClass: MetaVistenum) -> Member:
    if not issubclass(enumClass, self.__field_owner__):
      e = """The instance does not belong to the owner class: '%s'."""
      raise RuntimeError(monoSpace(e % self.__field_owner__.__name__))
    return self

  def __str__(self, ) -> str:
    """Returns the owner name and the field name"""
    clsName = self.__field_owner__.__name__
    return '%s.%s' % (clsName, self.name)

  def __repr__(self, ) -> str:
    """Returns the owner name and the field name"""
    clsName = self.__field_owner__.__name__
    return '%s(%s)' % (clsName, self.name)

  def __eq__(self, other: object) -> bool:
    """Returns True if the other object is a member of the enum."""
    if TYPE_CHECKING:
      assert isinstance(self.name, str)
    if isinstance(other, Member):
      return True if self is other else False
    if isinstance(other, str):
      return True if self.name.lower() == other.lower() else False
    return True if self.inner == other else False
