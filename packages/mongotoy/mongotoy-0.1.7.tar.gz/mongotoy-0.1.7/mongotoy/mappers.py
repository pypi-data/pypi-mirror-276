import abc
import dataclasses
import datetime
import decimal
import json
import re
import typing
import uuid
from types import UnionType, NoneType

import bson

from mongotoy import cache, expressions, types, geodata
from mongotoy.errors import ValidationError, ErrorWrapper

if typing.TYPE_CHECKING:
    from mongotoy import documents, fields


__all__ = (
    'MapperOptions',
    'build_mapper',
    'Mapper',
)


@dataclasses.dataclass
class MapperOptions:
    """
    Represents the options for configuring a Mapper instance.
    Attributes:
        nullable (bool): Flag indicating whether the field is nullable. Defaults to False.
        default (Any): Default value for the field. Defaults to expressions.EmptyValue.
        default_factory (Callable[[], Any]): Factory function to generate default values. Defaults to None.
        ref_field (str): Field name to use as a reference. Defaults to None.
        key_name (str): Name of the key when using a reference. Defaults to None.
        lt (Any): Upper bound for the field value.
        lte (Any): Upper bound (inclusive) for the field value.
        gt (Any): Lower bound for the field value.
        gte (Any): Lower bound (inclusive) for the field value.
        min_items (int): Minimum number of items for sequence fields.
        max_items (int): Maximum number of items for sequence fields.
        min_length (int): Minimum length for string fields.
        max_length (int): Maximum length for string fields.
        choices (list[str]): List of allowed choices for string fields.
        regex (re.Pattern): Regular expression for string fields.
        extra (dict): Extra options for customization. Defaults to empty dict.
    """
    nullable: bool = dataclasses.field(default=False)
    default: typing.Any = dataclasses.field(default=expressions.EmptyValue)
    default_factory: typing.Callable[[], typing.Any] = dataclasses.field(default=None)
    ref_field: str = dataclasses.field(default=None)
    key_name: str = dataclasses.field(default=None)
    lt: typing.Any = dataclasses.field(default=None)
    lte: typing.Any = dataclasses.field(default=None)
    gt: typing.Any = dataclasses.field(default=None)
    gte: typing.Any = dataclasses.field(default=None)
    min_items: int = dataclasses.field(default=None)
    max_items: int = dataclasses.field(default=None)
    min_length: int = dataclasses.field(default=None)
    max_length: int = dataclasses.field(default=None)
    choices: list[str] = dataclasses.field(default=None)
    regex: re.Pattern = dataclasses.field(default=None)
    extra: dict = dataclasses.field(default_factory=dict)

    def get_default_value(self) -> typing.Any:
        """Return the default value."""
        return self.default_factory() if self.default_factory else self.default


def build_mapper(mapper_bind: typing.Type, options: MapperOptions) -> 'Mapper':
    """
    Build a data mapper based on annotations.

    Args:
        mapper_bind (Type): Type annotation for the mapper.
       options (FieldOptions, RefFieldOptions): Additional information about the mapper.

    Returns:
        Mapper: The constructed data mapper.

    Raises:
        TypeError: If the mapper type is not recognized.
    """
    from mongotoy import documents

    # Simple type annotation
    if not typing.get_args(mapper_bind):
        # Extract mapper_bind from ForwardRef
        if isinstance(mapper_bind, typing.ForwardRef):
            mapper_bind = getattr(mapper_bind, '__forward_arg__')

        # Create mappers for forwarded types
        if isinstance(mapper_bind, str):
            # Create ReferencedDocumentMapper
            if options.ref_field:
                return ReferencedDocumentMapper(
                    document_cls=mapper_bind,
                    options=options
                )
            # Create EmbeddedDocumentMapper
            return EmbeddedDocumentMapper(
                document_cls=mapper_bind,
                options=options
            )

        # Create ReferencedDocumentMapper
        if issubclass(mapper_bind, documents.Document):
            return ReferencedDocumentMapper(
                document_cls=mapper_bind,
                options=options
            )

        # Create EmbeddedDocumentMapper
        if issubclass(mapper_bind, documents.EmbeddedDocument):
            return EmbeddedDocumentMapper(
                document_cls=mapper_bind,
                options=options
            )

        # Create mappers for other types
        mapper_cls = cache.mappers.get_type(mapper_bind)
        if not mapper_cls:
            raise TypeError(f'Data mapper not found for type {mapper_bind}')

        return mapper_cls(options)

    # Get type origin and arguments
    type_origin = typing.get_origin(mapper_bind)
    type_args = typing.get_args(mapper_bind)
    mapper_bind = type_args[0]

    # Check for nullable type
    if type_origin in (typing.Union, UnionType) and len(type_args) > 1 and type_args[1] is NoneType:
        options.nullable = True
        return build_mapper(mapper_bind, options)

    # Create sequence mapper
    if type_origin in (list, tuple, set):
        mapper_cls = cache.mappers.get_type(type_origin)
        return mapper_cls(
            mapper=build_mapper(mapper_bind, options),
            options=options
        )

    raise TypeError(
        f'Invalid outer annotation {type_origin}, allowed are [{list, tuple, set}, {typing.Optional}]'
    )


class MapperMeta(abc.ABCMeta):
    """
    Metaclass for Mapper classes.

    This metaclass is responsible for creating Mapper classes and registering them in the mapper cache.

    """

    def __new__(mcls, name, bases, namespace, **kwargs):
        """
        Create a new Mapper class.

        Args:
            name (str): Name of the class.
            bases: Base classes.
            namespace: Namespace dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            Mapper: The newly created Mapper class.

        """
        _cls = super().__new__(mcls, name, bases, namespace)
        _cls.__bind__ = kwargs.get('bind', _cls)
        cache.mappers.add_type(_cls.__bind__, _cls)

        return _cls


class Mapper(abc.ABC, metaclass=MapperMeta):
    """
    Abstract base class for data mappers.

    This class defines the interface for data mappers and provides basic functionality for validation and dumping.

    Args:
        options (MapperOptions): Mapper configuration params.

    """

    if typing.TYPE_CHECKING:
        __bind__: typing.Type

    def __init__(self, options: MapperOptions):
        self._options = options

    @property
    def options(self) -> MapperOptions:
        return self._options

    def __call__(self, value) -> typing.Any:
        """
        Maps and validate the value.

        Args:
            value (Any): The value to be validated.

        Raises:
            ValueError: If the value is invalid.

        Returns:
            Any: The validated value.

        """
        # Get default value
        if value is expressions.EmptyValue:
            value = self.options.get_default_value()
            if value is expressions.EmptyValue:
                return value

        try:
            # Check nullability
            if value is None:
                if not self.options.nullable:
                    raise ValueError('Null value not allowed')
                return value

            # Validate value
            value = self.validate_value(value)

        except (TypeError, ValueError) as e:
            raise ValidationError(ErrorWrapper(e)) from None

        return value

    @abc.abstractmethod
    def validate_value(self, value) -> typing.Any:
        """
        Abstract value validator to be implemented in child mappers.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        """
        raise NotImplementedError

    def dump_dict(self, value, **options) -> typing.Any:
        """
        Dump the value to be in a dictionary.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the value to valid JSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the value to valid BSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value


class ComparableMapper(Mapper):
    """
    Base mapper for data types supporting the following comparators:
    - lt (less than)
    - lte (less than or equal to)
    - gt (greater than)
    - gte (greater than or equal to)
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the input value against the specified comparators.
        Args:
            value: The value to be validated.
        Returns:
            The validated value.
        Raises:
            TypeError: If the input value is not of the expected data type.
            ValueError: If the value does not meet the specified comparator conditions.
        """
        if not isinstance(value, self.__bind__):
            raise TypeError(f'Invalid data type {type(value)}, expected {self.__bind__}')

        # Validate comparators
        if self.options.lt is not None:
            if value >= self.options.lt:
                raise ValueError(
                    f'Invalid value {value}, required lt={self.options.lt}'
                )
        if self.options.lte is not None:
            if value > self.options.lte:
                raise ValueError(
                    f'Invalid value {value}, required lte={self.options.lte}'
                )
        if self.options.gt is not None:
            if value <= self.options.gt:
                raise ValueError(
                    f'Invalid value {value}, required gt={self.options.gt}'
                )
        if self.options.gte is not None:
            if value < self.options.gte:
                raise ValueError(
                    f'Invalid value {value}, required gte={self.options.gte}'
                )

        return value


class SequenceMapper(Mapper):
    """
    Base mapper for handling sequence of elements.
    """

    def __init__(self, mapper: Mapper, options: MapperOptions):
        """
        Initialize the SequenceMapper.

        Args:
            mapper (Mapper): The mapper for the list items.
            options (MapperOptions): Mapper configuration params.

        """
        self._mapper = mapper
        # SequenceMapper must be at least an empty sequence, not an EmptyValue for ReferencedDocumentMapper
        if options.default is expressions.EmptyValue and isinstance(self.unwrap(), ReferencedDocumentMapper):
            options.default = self.__bind__()
        super().__init__(options)

    @property
    def mapper(self) -> Mapper:
        """
        Get the mapper for the list items.

        Returns:
            Mapper: The mapper for the list items.

        """
        return self._mapper

    def unwrap(self) -> Mapper:
        """Get the innermost mapper that isn't a SequenceMapper"""
        mapper_ = self.mapper
        while isinstance(mapper_, SequenceMapper):
            mapper_ = mapper_.mapper
        return mapper_

    # noinspection PyTypeChecker
    def validate_value(self, value) -> typing.Any:
        """
        Validate the list value.

        Args:
            value: The list value to be validated.

        Returns:
            Any: The validated list value.

        Raises:
            ValidationError: If validation fails.

        """
        if not isinstance(value, self.__bind__):
            raise TypeError(f'Invalid data type {type(value)}, required is {self.__bind__}')

        # Validate length
        if self.options.min_items is not None:
            if len(value) < self.options.min_items:
                raise ValueError(
                    f'Invalid length {len(value)}, required min_items={self.options.min_items}'
                )
        if self.options.max_items is not None:
            if len(value) > self.options.max_items:
                raise ValueError(
                    f'Invalid length {len(value)}, required max_items={self.options.max_items}'
                )

        new_value = []
        val_errors = []

        for i, val in enumerate(value):
            try:
                new_value.append(self.mapper(val))
            except ValidationError as e:
                val_errors.extend([ErrorWrapper(err, loc=(str(i),)) for err in e.errors])

        if val_errors:
            raise ValidationError(*val_errors)

        return self.__bind__(new_value)

    def dump_dict(self, value, **options) -> typing.Any:
        """
        Dump the list value to be in a dictionary.

        Args:
            value: The list value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped list value.

        """
        return self.__bind__((self.mapper.dump_dict(i, **options) for i in value))

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the list value to JSON.

        Args:
            value: The list value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped list value.

        """
        return [self.mapper.dump_json(i, **options) for i in value]

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the list value to BSON.

        Args:
            value: The list value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped list value.

        """
        return [self.mapper.dump_bson(i, **options) for i in value]


# noinspection PyUnresolvedReferences
class EmbeddedDocumentMapper(Mapper):
    """
    Mapper for embedded documents.

    Attributes:
        document_cls (Type['documents.BaseDocument'] | str): The class or name of the embedded document.
        options (MapperOptions): Mapper configuration params.

    """

    def __init__(
        self,
        document_cls: typing.Type['documents.BaseDocument'] | str,
        options: MapperOptions
    ):
        self._document_cls = document_cls
        super().__init__(options)

    @property
    def document_cls(self) -> typing.Type['documents.EmbeddedDocument']:
        """
        Get the class of the embedded document.

        Returns:
            Type['documents.BaseDocument']: The class of the embedded document.

        """
        from mongotoy import documents
        return documents.get_embedded_document_cls(self._document_cls)

    def validate_value(self, value) -> typing.Any:
        """
        Validate the embedded document value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if isinstance(value, dict):
            value = self.document_cls(**value)
        if not isinstance(value, self.document_cls):
            raise TypeError(f'Invalid data type {type(value)}, required is {self.document_cls}')
        return value

    def dump_dict(self, value, **options) -> typing.Any:
        """
        Dump the embedded document value to a dictionary.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value.dump_dict(**options)

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the embedded document value to JSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value.dump_json(**options)

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the embedded document value to BSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value.dump_bson(**options)


# noinspection PyUnresolvedReferences
class ReferencedDocumentMapper(EmbeddedDocumentMapper):
    """
    Mapper for referenced documents.

    Attributes:
        document_cls (Type['documents.BaseDocument'] | str): The class or name of the referenced document.
        options (MapperOptions): Mapper configuration params.
    """

    def __init__(
        self,
        document_cls: typing.Type['documents.BaseDocument'] | str,
        options: MapperOptions
    ):
        if not options.ref_field:
            options.ref_field = 'id'
        super().__init__(document_cls, options)

    @property
    def document_cls(self) -> typing.Type['documents.Document']:
        """
        Get the class of the referenced document.

        Returns:
            Type['documents.BaseDocument']: The class of the referenced document.

        """
        from mongotoy import documents
        return documents.get_document_cls(self._document_cls)

    @property
    def ref_field(self) -> 'fields.Field':
        """
        Get the reference field.

        Returns:
            Field: The reference field.

        """
        from mongotoy import documents
        return documents.get_document_field(self.document_cls, field_name=self.options.ref_field)

    def validate_value(self, value) -> typing.Any:
        """
        Validate the referenced document value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            ValueError: If validation fails due to missing referenced field value.
        """
        value = super().validate_value(value)
        if getattr(value, self.ref_field.name) is expressions.EmptyValue:
            raise ValueError(
                f'Referenced field {self.document_cls.__name__}.{self.ref_field.name} value required'
            )
        return value

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the value to BSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return getattr(value, self.ref_field.name)


class StrMapper(Mapper, bind=str):
    """
    Mapper for handling string values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the string value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not isinstance(value, str):
            raise TypeError(f'Invalid data type {type(value)}, required is {str}')

        # Validation options
        if self.options.min_length is not None:
            if len(value) < self.options.min_length:
                raise ValueError(
                    f'Invalid length {len(value)}, required min_length={self.options.min_length}'
                )
        if self.options.max_length is not None:
            if len(value) > self.options.max_length:
                raise ValueError(
                    f'Invalid length {len(value)}, required max_length={self.options.max_length}'
                )
        if self.options.choices:
            if value not in self.options.choices:
                raise ValueError(
                    f'Invalid value {value}, required choices={self.options.choices}'
                )
        if self.options.regex:
            if not self.options.regex.fullmatch(value):
                raise ValueError(f'Invalid value {value}, required regex={self.options.regex.pattern}')

        return value


class IntMapper(ComparableMapper, bind=int):
    """
    Mapper for handling integer values.
    """


class FloatMapper(ComparableMapper, bind=float):
    """
    Mapper for handling float values.
    """


class DecimalMapper(ComparableMapper, bind=decimal.Decimal):
    """
    Mapper for handling decimal values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the decimal value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if isinstance(value, bson.Decimal128):
            value = value.to_decimal()
        value = super().validate_value(value)
        # Ensure decimal limits for MongoDB
        # https://www.mongodb.com/docs/upcoming/release-notes/3.4/#decimal-type
        ctx = decimal.Context(prec=34)
        return ctx.create_decimal(value)

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the decimal value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return float(value)

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the decimal value to BSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return bson.Decimal128(value)


class BoolMapper(Mapper, bind=bool):
    """
    Mapper for handling boolean values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the boolean value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not isinstance(value, bool):
            raise TypeError(f'Invalid data type {type(value)}, required is {bool}')
        return value


class BinaryMapper(Mapper, bind=bytes):
    """
    Mapper for handling binary values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the binary value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not isinstance(value, bytes):
            raise TypeError(f'Invalid data type {type(value)}, required is {bytes}')
        return value

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the binary value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        import base64
        return base64.b64encode(value).decode()


class UUIDMapper(Mapper, bind=uuid.UUID):
    """
    Mapper for handling UUID values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the UUID value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not isinstance(value, uuid.UUID):
            raise TypeError(f'Invalid data type {type(value)}, required is {uuid.UUID}')
        return value

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the UUID value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return str(value)

    def dump_bson(self, value, **options) -> typing.Any:
        if self.options.extra.get('dump_bson_as_str', False):
            return str(value)
        return value


class DateTimeMapper(ComparableMapper, bind=datetime.datetime):
    """
    Mapper for handling datetime values.
    """

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the datetime value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value.isoformat()


class DateMapper(ComparableMapper, bind=datetime.date):
    """
    Mapper for handling date values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the date value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if isinstance(value, datetime.datetime):
            value = value.date()
        return super().validate_value(value)

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the date value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value.isoformat()

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the date value to BSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return datetime.datetime.combine(date=value, time=datetime.time.min)


class TimeMapper(ComparableMapper, bind=datetime.time):
    """
    Mapper for handling time values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the time value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if isinstance(value, datetime.datetime):
            value = value.time()
        return super().validate_value(value)

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the time value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return value.isoformat()

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the time value to BSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return datetime.datetime.combine(date=datetime.datetime.min, time=value)


class ListMapper(SequenceMapper, bind=list):
    """
    Mapper for handling lists.

    Inherits from ManyMapper and specifies 'list' as the binding type.

    """


class TupleMapper(SequenceMapper, bind=tuple):
    """
    Mapper for handling tuples.

    Inherits from ManyMapper and specifies 'tuple' as the binding type.

    """
    def validate_value(self, value) -> typing.Any:
        if isinstance(value, list):
            value = tuple(value)
        return super().validate_value(value)


class SetMapper(SequenceMapper, bind=set):
    """
    Mapper for handling sets.

    Inherits from ManyMapper and specifies 'set' as the binding type.

    """

    def validate_value(self, value) -> typing.Any:
        if isinstance(value, list):
            value = set(value)
        return super().validate_value(value)

    def dump_json(self, value, **options) -> typing.Any:
        return list(value)

    def dump_bson(self, value, **options) -> typing.Any:
        return list(value)


class ObjectIdMapper(Mapper, bind=bson.ObjectId):
    """
    Mapper for handling BSON ObjectId values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the ObjectId value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not bson.ObjectId.is_valid(value):
            raise TypeError(f'Invalid data type {type(value)}, required is {bson.ObjectId}')
        return bson.ObjectId(value)

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the ObjectId value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return str(value)


class Int64Mapper(Mapper, bind=bson.Int64):
    """
    Mapper for handling BSON Int64 values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the Int64 value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not isinstance(value, bson.Int64):
            raise TypeError(f'Invalid data type {type(value)}, required is {bson.Int64}')
        return value

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the Int64 value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return int(value)


class Decimal128Mapper(Mapper, bind=bson.Decimal128):
    """
    Mapper for handling BSON Decimal128 values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the Decimal128 value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not isinstance(value, bson.Decimal128):
            raise TypeError(f'Invalid data type {type(value)}, required is {bson.Decimal128}')
        return value

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the Decimal128 value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return float(value.to_decimal())


class RegexMapper(Mapper, bind=bson.Regex):
    """
    Mapper for handling BSON Regex values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the Regex value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not isinstance(value, bson.Regex):
            value = bson.Regex.from_native(value)
        return value

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the Regex value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return f'{value.pattern}'


class CodeMapper(Mapper, bind=bson.Code):
    """
    Mapper for handling BSON Code values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the Code value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If validation fails due to incorrect data type.

        """
        if not isinstance(value, bson.Code):
            raise TypeError(f'Invalid data type {type(value)}, required is {bson.Code}')
        return value

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the Decimal128 value to a JSON-serializable format.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return str(value)


class ConstrainedStrMapper(StrMapper):
    """
    Mapper for handling constrained string values.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the string value.

        Args:
            value: The value to be validated.

        Returns:
            Any: The validated value.

        """
        return str(self.__bind__(super().validate_value(value)))

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the string value to JSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return str(value)

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the string value to BSON.

        Args:
            value: The value to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped value.

        """
        return str(value)


class IpV4Mapper(ConstrainedStrMapper, bind=types.IPv4):
    """
    Mapper for handling IPv4 addresses.
    """


class IpV6Mapper(ConstrainedStrMapper, bind=types.IPv6):
    """
    Mapper for handling IPv6 addresses.
    """


class PortMapper(ConstrainedStrMapper, bind=types.Port):
    """
    Mapper for handling port numbers.
    """


class MacMapper(ConstrainedStrMapper, bind=types.Mac):
    """
    Mapper for handling MAC addresses.
    """


class PhoneMapper(ConstrainedStrMapper, bind=types.Phone):
    """
    Mapper for handling phone numbers.
    """


class EmailMapper(ConstrainedStrMapper, bind=types.Email):
    """
    Mapper for handling email addresses.
    """


class CardMapper(ConstrainedStrMapper, bind=types.CardNumber):
    """
    Mapper for handling card numbers.
    """


class SsnMapper(ConstrainedStrMapper, bind=types.Ssn):
    """
    Mapper for handling social security numbers.
    """


class HashtagMapper(ConstrainedStrMapper, bind=types.Hashtag):
    """
    Mapper for handling hashtags.
    """


class DoiMapper(ConstrainedStrMapper, bind=types.Doi):
    """
    Mapper for handling DOI (Digital Object Identifier) numbers.
    """


class UrlMapper(ConstrainedStrMapper, bind=types.Url):
    """
    Mapper for handling URLs.
    """


class VersionMapper(ConstrainedStrMapper, bind=types.Version):
    """
    Mapper for handling version numbers.
    """


class GeometryMapper(Mapper):
    """
    Mapper for handling geometry data.

    This mapper validates and handles geometry data.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the geometry data.

        Args:
            value (Any): The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            TypeError: If the value is not of the expected type.
        """
        if isinstance(value, dict):
            # noinspection PyTypeChecker
            value = geodata.parse_geojson(value, parser=self.__bind__)
        if not isinstance(value, self.__bind__):
            raise TypeError(f'Invalid data type {type(value)}, expected {self.__bind__}')
        return value

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the geometry data to GEO-JSON.

        Args:
            value: The geometry data to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped geometry data.
        """
        return value.dump_json()

    def dump_bson(self, value, **options) -> typing.Any:
        """
        Dump the geometry data to BSON.

        Args:
            value: The geometry data to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped geometry data.
        """
        return self.dump_json(value, **options)


class PointMapper(GeometryMapper, bind=types.Point):
    """
    Mapper class for Point geometry data.
    """


class MultiPointMapper(GeometryMapper, bind=types.MultiPoint):
    """
    Mapper class for MultiPoint geometry data.
    """


class LineStringMapper(GeometryMapper, bind=types.LineString):
    """
    Mapper class for LineString geometry data.
    """


class MultiLineStringMapper(GeometryMapper, bind=types.MultiLineString):
    """
    Mapper class for MultiLineString geometry data.
    """


class PolygonMapper(GeometryMapper, bind=types.Polygon):
    """
    Mapper class for Polygon geometry data.
    """


class MultiPolygonMapper(GeometryMapper, bind=types.MultiPolygon):
    """
    Mapper class for MultiPolygon geometry data.
    """


class JsonMapper(Mapper, bind=types.Json):
    """
    Mapper for handling JSON data.

    This mapper validates and handles JSON data.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the JSON data.

        Args:
            value (Any): The JSON data to be validated.

        Returns:
            Any: The validated JSON data.

        Raises:
            TypeError: If the value is not of the expected type.
            ValueError: If the JSON data is invalid.
        """
        if not isinstance(value, dict):
            raise TypeError(f'Invalid data type {type(value)}, expected {types.Json}')

        # Check if the JSON data is valid
        try:
            json.dumps(value)
        except Exception as e:
            raise ValueError(f'Invalid JSON data: {str(e)}') from None

        return types.Json(value)


class BsonMapper(Mapper, bind=types.Bson):
    """
    Mapper for handling BSON data.

    This mapper validates and handles BSON data.
    """

    def validate_value(self, value) -> typing.Any:
        """
        Validate the BSON data.

        Args:
            value (Any): The BSON data to be validated.

        Returns:
            Any: The validated BSON data.

        Raises:
            TypeError: If the value is not of the expected type.
            ValueError: If the BSON data is invalid.
        """
        if not isinstance(value, dict):
            raise TypeError(f'Invalid data type {type(value)}, expected {types.Bson}')

        # Check if the BSON data is valid
        try:
            bson.encode(value)
        except Exception as e:
            raise ValueError(f'Invalid BSON data: {str(e)}') from None

        return types.Bson(value)

    def dump_json(self, value, **options) -> typing.Any:
        """
        Dump the BSON data to JSON.

        Args:
            value: The BSON data to be dumped.
            **options: Additional options.

        Returns:
            Any: The dumped JSON data.
        """
        from bson import json_util
        # noinspection PyProtectedMember
        return json_util._json_convert(value, json_options=json_util.RELAXED_JSON_OPTIONS)


class FileMapper(ReferencedDocumentMapper, bind=types.File):
    """
    Mapper for handling file references.

    This mapper handles references to files stored in a database.

    Args:
        options (MapperOptions): Mapper configuration params.
    """

    def __init__(self, options: MapperOptions):
        from mongotoy import db
        super().__init__(db.FsObject, options)
