from collections.abc import Mapping
from copy            import deepcopy
from functools       import total_ordering

from simpleset.utils import classproperty


IMMUTABILITY = AttributeError( "instance attributes are immutable" )


# Metaclass for Constant to facilitate class-level magic methods.
# Intended as part of the class API for subclasses of Constant.
# All item-based methods accept strings (cname) or class instances.
class ConstantType( type ):


    def __contains__( self, item ):
        return str( item ) in self._objdir


    def __delattr__( self, name ):
        if "_objdir" in self.__dict__ and name in self.__dict__[ "_objdir" ]:
            raise IMMUTABILITY
        return super().__delattr__( name )


    def __getitem__( self, item ):
        return self._objdir.get( str( item ) )


    def __iter__( self ):
        return iter( self.all )


    def __len__( self ):
        return len( self._objdir )


    def __setattr__( self, name, value ):
        if "_objdir" in self.__dict__ and name in self._objdir:
            raise IMMUTABILITY
        return super().__setattr__( name, value )


@total_ordering
class Constant( metaclass=ConstantType ):


    ##
    ##  Definition API
    ##


    @classmethod
    def define_set( cls, name, *args, **kwargs ):

        # create subclass
        subcls = type(
            name,                   # subclass name
            ( cls, ),               # superclass
            dict( _objdir={} ),     # subclass attributes
        )

        # create subclass instances
        subcls.populate( *args, **kwargs )

        return subcls


    ##
    ##  Class API
    ##


    @classproperty
    def all( cls ):
        return cls._objects


    @classmethod
    def as_cnames( cls, filter=None ):
        return cls.pick( "cname", filter=filter )


    @classmethod
    def as_dicts( cls, *names, filter=None  ):
        return [ obj.as_dict( *names ) for obj in cls.filter( filter ) ]


    @classmethod
    def as_tuples( cls, *names, filter=None  ):
        return [ obj.as_tuple( *names ) for obj in cls.filter( filter ) ]


    @classmethod
    def choices( cls, filter=None ):
        return cls.as_tuples( "cname", "cname_pretty", filter=filter )


    @classmethod
    def filter( cls, filter=None ):
        if filter:
            assert callable( filter )
            return [ obj for obj in cls.all if filter( obj ) ]
        return cls.all


    @classmethod
    def get( cls, **kwargs ):
        results = cls._select( **kwargs )
        if len( results ) != 1:
            raise ValueError( f"select( { kwargs } ) found { len( results ) } results instead of 1" )
        return results[ 0 ]


    @classproperty
    def max_length( cls ):
        if cls.all:
            return max( len( obj ) for obj in cls.all )
        return 0


    @classmethod
    def pick( cls, name, filter=None ):
        return [ obj.getattr_inclusive( name ) for obj in cls.filter( filter ) ]


    # Form 1:  populate( "cname1", ... )
    # Form 2:  populate( cname1=value1, ... )
    # Form 3:  populate( cname1=dict( attr1=val1, ... ), ... )
    #
    # Warning:  Doesn't prevent you from mixing multiple forms in a single call.
    @classmethod
    def populate( cls, *args, **kwargs ):

        if not hasattr( cls, "_objdir" ):
            cls._objdir = {}

        # Form 1
        for cname in args:
            cname = str( cname )
            assert cname.isidentifier()
            cls._create( cname )

        for cname, payload in kwargs.items():
            # Form 3
            if isinstance( payload, Mapping ):
                cls._create( cname, **payload )

            # Form 2
            else:
                cls._create( cname, value=payload )


    @classmethod
    def select( cls, **kwargs ):
        return cls._select( **kwargs )


    ##
    ##  Instance API
    ##


    def __init__( self, cname, **kwargs ):
        self._attrdir = dict( cname=cname )
        self._attrdir.update( **kwargs )


    def __delattr__( self, name ):
        if "_attrdir" in self.__dict__ and name in self.__dict__[ "_attrdir" ]:
            raise IMMUTABILITY
        return super().__delattr__( name )


    def __eq__( self, other ):
        return self.cname == str( other )


    def __getattribute__( self, name ):
        if name == "__dict__":
            return super().__getattribute__( name )

        if "_attrdir" in self.__dict__ and name in self.__dict__[ "_attrdir" ]:
            return deepcopy( self.__dict__[ "_attrdir" ][ name ] )

        return super().__getattribute__( name )


    def __hash__( self ):
        return hash( self.cname )


    def __index__( self ):
        return self.ordinal 


    def __len__( self ):
        return len( self.cname )


    def __lt__( self, other ):
        return self.ordinal < self.__class__[ other ].ordinal


    def __repr__( self ):
        return self.cname


    def __setattr__( self, name, value ):
        if "_attrdir" in self.__dict__ and name in self._attrdir:
            raise IMMUTABILITY
        return super().__setattr__( name, value )


    def __str__( self ):
        return self.cname


    def as_dict( self, *names ):
        if names:
            return { name:self.getattr_inclusive( name ) for name in names }

        return deepcopy( self._attrdir )


    def as_tuple( self, *names ):
        if names:
            return tuple( [ self.getattr_inclusive( name ) for name in names ] )

        if len( self._attrdir ) == 1:   # Form 1
            return ( self.cname, self.ordinal )

        return deepcopy( tuple( self._attrdir.values() ) )


    @property
    def cname_pretty( self ):
        return self.cname.replace( "_", " " ).title()


    def getattr_inclusive( self, name ):
        if name == "cname_pretty":
            return self.cname_pretty

        if name == "ordinal":
            return self.ordinal

        if name in self._attrdir:
            return deepcopy( self._attrdir[ name ] )

        raise AttributeError( f"attribute { name } not found in instance { self.cname }" )


    @property
    def ordinal( self ):
        return self.all.index( self ) + 1


    ##
    ##  PRIVATE
    ##


    @classmethod
    def _create( cls, cname, **kwargs ):

        # create instance
        obj = cls( cname, **kwargs )

        # add instance to class as attribute
        setattr( cls, cname, obj )

        # add instance to class's object directory
        cls._objdir[ cname ] = obj

        return obj


    # Returns True if all kwargs exist and all values match, else False.
    def _is_match( self, **kwargs ):
        for k, v in kwargs.items():
            if not hasattr( self, k ):
                return False
            if getattr( self, k ) != v:
                return False
        return True


    @classproperty
    def _objects( cls ):
        return list( cls._objdir.values() )


    @classmethod
    def _select( cls, **kwargs ):
        return [ obj for obj in cls._objects if obj._is_match( **kwargs ) ]
