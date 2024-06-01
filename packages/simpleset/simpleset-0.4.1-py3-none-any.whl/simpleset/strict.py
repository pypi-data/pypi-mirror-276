from collections.abc    import Mapping

from simpleset.constant import Constant as Base
from simpleset.error    import Error


StrictnessError = Error.define_family(
    "StrictnessError",
    "MixedFormsError",
    "SparseAttributesError",
)


class StrictMixin:


    # override to enforce strictness
    @classmethod
    def populate( cls, *args, **kwargs ):

        # detect mixing Form 1 with 2 or 3
        if args and kwargs:
            raise StrictnessError.MixedFormsError(
                "cannot mix args (Form 1) and kwargs (Forms 2 or 3) in definition"
            )

        if kwargs:

            last_form = None
            last_attr = None

            # detect mixing Forms 2 and 3
            for cname, payload in kwargs.items():
                item_form = 3 if isinstance( payload, Mapping ) else 2
                if last_form and last_form != item_form:
                    raise StrictnessError.MixedFormsError(
                        "cannot mix Forms 2 and 3 in definition kwargs"
                    )
                last_form = item_form

            if last_form == 3:
                # detect sparse attributes
                for cname, payload in kwargs.items():
                    item_attr = list( payload.keys() )
                    if last_attr and last_attr != item_attr:
                        raise StrictnessError.SparseAttributesError(
                            "must specify the same set of attributes for all instances"
                        )
                    last_attr = item_attr

        return super().populate( *args, **kwargs )


class Constant( StrictMixin, Base ):
    pass
