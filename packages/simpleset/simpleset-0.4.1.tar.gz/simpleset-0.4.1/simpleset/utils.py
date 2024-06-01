# non-data descriptor  (https://github.com/dssg/dickens/blob/2.0.0/src/descriptors.py)
class classproperty:

    def __init__( self, func ):
        self.__func__ = func

    def __get__( self, instance, cls=None ):
        if cls is None:
            cls = type( instance )

        return self.__func__( cls )
