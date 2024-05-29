""" UUID-compatible Typed IDs with prefixes.

    \b
        user_nnv5rr3rfk3hgry6xrygr
        └──┘ └───────────────────┘
        type    uuid (base58)

    First generate the Types using generate(...), then use them
    like so:

    >>> from uuid_extensions import uuid7
    >>> from typeid import generate
    >>> typeids = generate("sk", "pk", "user", "apikey")
    >>> assert str(typeids.SkId(uuid7().hex)).startswith("sk_")
    >>> assert str(typeids.PkId(uuid7().hex)).startswith("pk_")
    >>> assert str(typeids.UserId(uuid7().hex)).startswith("user_")
    >>> assert str(typeids.ApikeyId(uuid7().hex)).startswith("apikey_")
    >>> assert (typeids.UserId("user_nnv5rr3rfk3hgry6xrygr").hex
    ...    == "0664c4135ed83faabd4bc0dc33839c9f")
    >>> extra_types = generate("admin", suffix="IdUseWithCare")
    >>> assert str(extra_types.AdminIdUseWithCare(uuid7().hex)).startswith("admin_")
"""

from typing import Optional, Callable
from base58 import b58encode, b58decode
from uuid import UUID


class BaseId(UUID):
    """BaseID implementation that does the lifting of a UUID into a typed UUID
    and formats it more nicely.

    :param _prefix: The internal _prefix is filled in the generate() method
    """

    #: This class variable will be filled in by type() later own
    _prefix: str = ""
    _generator: Optional[Callable] = None
    _encode = staticmethod(b58encode)
    _decode = staticmethod(b58decode)

    def __init__(self, id: Optional[UUID | str | bytes] = None) -> None:
        if id is None and callable(self._generator):
            generator = getattr(self, "_generator")
            id = generator()

        if isinstance(id, UUID):
            # Load from a UUID using the hex representation
            super().__init__(id.hex)

        elif isinstance(id, bytes) and len(id) == 16:
            # forward the hex content of a bytes array
            super().__init__(id.hex())

        elif isinstance(id, str):
            # Load from string
            # NOTE: we need to make a distinction if it starts with our prefix
            # or not

            if id.startswith(f"{self._prefix}_"):
                # uses our prefix
                prefix_free_id = id[len(self._prefix) + 1 :]
                uid: bytes = self._decode(prefix_free_id.encode("ascii"))
                super().__init__(uid.hex())

            elif "_" in id:
                # does not use our prefix but has a _ in the string!
                found_prefix = id[: id.index("_")]
                raise ValueError(
                    f"Wrong prefix, got {found_prefix}, expected {self._prefix}"
                )

            else:
                # most probably a hex string
                super().__init__(id)
        else:
            raise NotImplementedError(
                "Incorrect argument type. Requries, UUID, hex, bytes or string."
            )

    def __str__(self) -> str:
        """Prefix and base58 encode the id

        :return: encoded and prefixed id as string
        """
        prefix = str(self._prefix)
        id = self._encode(self.bytes).decode("ascii")
        return f"{prefix}_{id}"


class AttrDict(dict):
    """This class enables us to access the return values of generate() as
    attributes."""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def generate(
    *args: str,
    suffix: str = "Id",
    enable_sqla: bool = False,
    generator: Callable = None,
) -> AttrDict:
    """Generate types based on a list of arguments. Each argument will result in
    a new type named after the argument (camel-cased) with the defined suffix at the end.

    :param *args: list of strings for which to generate typed Id classes
    :param suffix: (Id) suffix used in the classes
    :param enable_sqla: (False) If true, also generates classes (suffix "SQLA" to be used for sqlalchemy)
    :param generator: (None) Allows to provide a generator for new instances
    :return: AttributeClass that allows to access new classes through attributes

    Usage
    =====

    >>> from uuid_extensions import uuid7
    >>> from typeid import generate
    >>> typed_ids = generate(
    ...     "user",
    ...     "apikey",
    ...     generator=lambda: uuid7().hex
    ... )
    >>> user_id = str(typed_ids.UserId())
    >>> # user_id = user_nnv5rr3rfk3hgry6xrygr
    >>> u_id_typed = typed_ids.userId("user_nnv5rr3rfk3hgry6xrygr")
    """
    ret = {}
    for _type in args:
        name = f"{_type.capitalize()}{suffix}"
        typeid_class = type(
            name, (BaseId,), dict(_prefix=_type, _generator=staticmethod(generator))
        )
        globals()[name] = typeid_class
        ret[name] = typeid_class

        # If the user wants sqla support, these additional classes will be
        # generated
        if enable_sqla:
            from .sqla import GUID

            sqla_name = f"{name}SQLA"
            sqla_typeid_class = type(
                name, (GUID,), dict(typeid_class=typeid_class, cache_ok=True)
            )
            globals()[sqla_name] = sqla_typeid_class
            ret[sqla_name] = sqla_typeid_class
    return AttrDict(ret)


if __name__ == "__main__":
    import doctest
    from uuid_extensions import uuid7

    generate("sk", "pk", "user", "apikey")
    generate("admin", suffix="IdUseWithCare", generator=lambda: uuid7().hex)

    doctest.testmod()
