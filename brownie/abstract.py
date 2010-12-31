# coding: utf-8
"""
    brownie.abstract
    ~~~~~~~~~~~~~~~~

    Utilities to deal with abstract base classes.

    .. versionadded:: 0.2

    :copyright: 2010 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
try:
    from abc import ABCMeta
except ImportError:
    class ABCMeta(type):
        """Dummy :class:`abc.ABCMeta` implementation which does nothing."""

        def register(self, subclass):
            pass


class VirtualSubclassMeta(type):
    """
    A metaclass which allows you to easily define abstract super classes,
    simply inherit from this metaclass and set the
    :attr:`virtual_superclasses` attribute to an iterable.
    """
    def __init__(self, name, bases, attributes):
        type.__init__(self, name, bases, attributes)
        def register_superclasses(superclasses):
            for cls in superclasses:
                if isinstance(cls, ABCMeta):
                    cls.register(self)
                if hasattr(cls, 'virtual_superclasses'):
                    register_superclasses(cls.virtual_superclasses)
        register_superclasses(attributes.get('virtual_superclasses', ()))