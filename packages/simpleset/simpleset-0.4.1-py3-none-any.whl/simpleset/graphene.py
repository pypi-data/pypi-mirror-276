from functools import cache
from graphene import Enum

from simpleset.constant import Constant as Base


class GrapheneMixin:


    _graphene_name_attr  = "cname"
    _graphene_value_attr = "cname"
    _graphene_desc_attr  = "cname_pretty"


    def as_graphene_tuple( self ):
        return (
            self.getattr_inclusive( self._graphene_name_attr  ),
            self.getattr_inclusive( self._graphene_value_attr ),
            self.getattr_inclusive( self._graphene_desc_attr  )
        )


    @classmethod
    @cache
    def graphene( cls, name=None, filter=None ):
        name         = name or cls.__name__
        items        = []
        descriptions = {}

        for obj in cls.filter( filter ):
            n, v, d = obj.as_graphene_tuple()
            items.append( ( n, v ) )
            descriptions[ n ] = d

        def map_to_description( graphene_enum ):
            return descriptions[ graphene_enum.name ] if graphene_enum else cls.__doc__

        return Enum( name, items, description=map_to_description )


    @classmethod
    def graphene_config( cls, name=None, value=None, desc=None ):
        if name:
            cls._graphene_name_attr  = name
        if value:
            cls._graphene_value_attr = value
        if desc:
            cls._graphene_desc_attr  = desc
        return cls


class Constant( GrapheneMixin, Base ):
    pass
