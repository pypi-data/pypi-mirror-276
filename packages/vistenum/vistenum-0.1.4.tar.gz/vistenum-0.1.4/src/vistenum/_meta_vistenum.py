"""MetaVistenum provides the metaclass for the 'Vistenum' class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.metas import AbstractMetaclass
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from vistenum import VistenumNamespace, Member


class MetaVistenum(AbstractMetaclass):
  """The metaclass for the 'Vistenum' class."""

  __iter_contents__ = None

  @classmethod
  def __prepare__(mcls,
                  name: str,
                  bases: tuple[type, ...],
                  **kwargs) -> dict[str, type]:
    """An instance of VistenumNamespace is used by classes derived from
    MetaVistenum."""
    return VistenumNamespace(mcls, name, bases, **kwargs)

  def __new__(mcls,
              name: str,
              bases: tuple[type, ...],
              namespace: VistenumNamespace,
              **kwargs) -> type:
    """The 'Vistenum' class is created by the metaclass."""
    return type.__new__(mcls, name, bases, namespace.compile(), **kwargs)

  def __instancecheck__(cls, instance: Member) -> bool:
    """Returns True if the instance is an instance of the Vistenum class."""
    return True if instance in cls else False

  def getMembers(cls, ) -> list[Member]:
    """Returns the members of the enum."""
    if getattr(cls, '__enum_members__', None) is None:
      e = """The enum: '%s' has no members. """
      raise TypeError(e % cls.__name__)
    members = getattr(cls, '__enum_members__')
    if isinstance(members, list):
      for member in members:
        if not isinstance(member, Member):
          e = typeMsg('member', member, Member)
          raise TypeError(e)
      else:
        return members
    e = typeMsg('members', members, list)
    raise TypeError(e)

  def __contains__(cls, other: object) -> bool:
    """Returns True if the other object is a member of the enum."""
    members = cls.getMembers()
    memberNames = [member.name.lower() for member in members]
    innerObjects = [member.inner for member in members]
    if isinstance(other, Member):
      for member in members:
        if other is member:
          return True
        return False
    if isinstance(other, str):
      if other.lower() in memberNames:
        return True
      return False
    if other in innerObjects:
      return True
    return False

  def _recognizeMember(cls, possibleMember: object) -> Member:
    """Returns the member object if the possible member is a member of the
    enum."""
    if possibleMember not in cls:
      e = """The object: '%s' is not recognized as a member of: '%s'!"""
      clsName = cls.__name__
      susName = str(possibleMember)
      raise AttributeError(monoSpace(e % (susName, clsName)))
    if isinstance(possibleMember, Member):
      return possibleMember
    if isinstance(possibleMember, str):
      for member in cls.getMembers():
        if possibleMember.lower() == member.name.lower():
          return member
    for member in cls.getMembers():
      if possibleMember == member.inner:
        return member
    e = """Unexpected discrepancy between membership and recognition!"""
    raise RuntimeError(monoSpace(e))

  def __call__(cls, member: object) -> Member:
    """Returns the member object if the member is a member of the enum."""
    return cls._recognizeMember(member)

  def __getitem__(cls, member: object) -> Member:
    """Returns the member object if the member is a member of the enum."""
    return cls._recognizeMember(member)

  def __iter__(cls, ) -> iter:
    """Iterates over the members of the enum."""
    cls.__iter_contents__ = [*cls.getMembers(), ]
    return cls

  def __next__(cls, ) -> Member:
    """Returns the next member of the enum."""
    try:
      return cls.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __len__(cls, ) -> int:
    """Returns the number of members in the enum."""
    return len(cls.getMembers())

  def __str__(cls, ) -> str:
    """String representation returns the name of the class"""
    return cls.__name__

  def __repr__(cls, ) -> str:
    """Representation returns the name of the class"""
    return cls.__name__
