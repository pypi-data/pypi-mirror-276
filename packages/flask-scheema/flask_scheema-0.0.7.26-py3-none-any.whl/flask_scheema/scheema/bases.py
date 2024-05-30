import validators
from flask import request
from marshmallow import fields, Schema, missing, post_dump, ValidationError
from marshmallow.validate import Length
from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Float,
    Date,
    DateTime,
    Time,
    Text,
    Numeric,
    BigInteger,
    LargeBinary,
    Enum,
    ARRAY,
    Interval,
)
from sqlalchemy.dialects.postgresql import JSON, JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import class_mapper, RelationshipProperty, ColumnProperty

from flask_scheema.api.utils import endpoint_namer, convert_case
from flask_scheema.logging import logger
from flask_scheema.scheema.utils import (
    get_openapi_meta_data,
    get_input_output_from_model_or_make,
    find_matching_relations,
    _get_relation_use_list_and_type,
)
from flask_scheema.utilities import get_config_or_model_meta

type_mapping = {
    # Basic types
    Integer: fields.Int,
    String: fields.Str,
    Text: fields.Str,
    Boolean: fields.Bool,
    Float: fields.Float,
    Date: fields.Date,
    DateTime: fields.DateTime,
    Time: fields.Time,
    JSON: fields.Raw,
    JSONB: fields.Raw,
    Numeric: fields.Decimal,
    BigInteger: fields.Int,
    # Additional types
    LargeBinary: fields.Str,
    Enum: fields.Str,
    ARRAY: fields.List,
    Interval: fields.TimeDelta,
    # Python built-in types
    str: fields.Str,
    int: fields.Int,
    bool: fields.Bool,
    float: fields.Float,
    dict: fields.Dict,
    list: fields.List,
}

class Base(Schema):
    @classmethod
    def get_model(cls):
        """
        Get the SQLAlchemy model associated with the schema.
        Returns:
            The SQLAlchemy model associated with the schema.
        """

        # Check if model is None
        meta = getattr(cls, "Meta")
        model = None

        if meta:
            model = getattr(meta, "model", None)
        return model

class DeleteSchema(Base):
    complete = fields.Boolean(required=True, default=False)


def validate_by_type(validator_type: str, value, field, message=None):

    if field.nullable and value is None:
        return True

    if validator_type == "email":
        validation = validators.email(value)
    elif validator_type == "url":
        validation = validators.url(value)
    elif validator_type == "ipv4":
        validation = validators.ip_address.ipv4(value)
    elif validator_type == "ipv6":
        validation = validators.ip_address.ipv6(value)
    elif validator_type == "mac":
        validation = validators.mac_address(value)
    elif validator_type == "slug":
        validation = validators.slug(value)
    elif validator_type == "uuid":
        validation = validators.uuid(value)
    elif validator_type == "card":
        validation = validators.card.card_number(value)
    elif validator_type == "country_code":
        validation = validators.country_code(value)
    elif validator_type == "domain":
        validation = validators.domain(value)
    elif validator_type == "md5":
        validation = validators.md5(value)
    elif validator_type == "sha1":
        validation = validators.sha1(value)
    elif validator_type == "sha256":
        validation = validators.sha256(value)
    elif validator_type == "sha512":
        validation = validators.sha512(value)
    elif validator_type == "mac":
        validation = validators.mac_address(value)
    elif validator_type == "uuid":
        validation = validators.uuid(value)

    if not validation:
        raise ValidationError(message or f"Invalid {validator_type}")
    else:
        return True

class AutoScheema(Base):
    class Meta:
        model = None  # Default to None. Override this in subclasses if needed.
        add_hybrid_properties = True
        include_children = True

    def __init__(self, *args, render_nested=True, **kwargs):

        only_fields = kwargs.pop("only", None)

        if not hasattr(self, "depth"):
            self.depth = kwargs.pop("depth", 0)
        if not hasattr(self, "parent"):
            self.parent = kwargs.pop("parent", 0)

        super().__init__(*args, **kwargs)
        self.context = {"current_depth": 0}  # Initialize an empty context dictionary
        self.render_nested = render_nested  # Save the parameter to the instance
        if hasattr(self.Meta, "model"):

            schema_case = get_config_or_model_meta(
                "API_SCHEMA_CASE", model=self.get_model(), default="camel"
            )
            logger.debug(
                1,
                f"Creating to mallow object |{convert_case(self.__class__.__name__, schema_case)}|",
            )

            try:
                self.__name__ = convert_case(self.get_model().__name__, schema_case)
            except:
                pass


            self.model = self.Meta.model

            self.generate_fields()
            self.dump_fields.update(self.fields)
            self.load_fields.update(self.fields)

        if only_fields:
            self._apply_only(only_fields)

    @post_dump
    def post_dump(self, data, **kwargs):
        post_dump_function = get_config_or_model_meta(
            "API_POST_DUMP_CALLBACK",
            model=self.get_model(),
            method=request.method,
            default=None,
        )
        if post_dump_function:
            return post_dump_function(data, **kwargs)
        return data

    def _apply_only(self, only_fields):
        # Your custom logic here.
        # For example:
        self.fields = {key: self.fields[key] for key in only_fields}
        self.dump_fields = {key: self.dump_fields[key] for key in only_fields}
        self.load_fields = {key: self.load_fields[key] for key in only_fields}

    def generate_fields(self):
        """
        Automatically add fields for each column and relationship in the SQLAlchemy model.
        Also adds fields for hybrid properties.
        Returns:
            None
        """

        model = self.get_model()

        if model is None:
            print("Warning: self.Meta.model is None. Skipping field generation.")
            return

        mapper = class_mapper(model)
        for attribute, mapper_property in mapper.all_orm_descriptors.items():

            original_attribute = attribute
            field_case = get_config_or_model_meta(
                "API_FIELD_CASE", model=model, default="snake_case"
            )
            attribute = convert_case(attribute, field_case)

            ignore_underscore = get_config_or_model_meta(
                "API_IGNORE_UNDERSCORE_ATTRIBUTES", model=model, default=True
            )

            allow_hybrid = get_config_or_model_meta(
                "API_DUMP_HYBRID_PROPERTIES", model=model, default=True
            )

            add_relations = get_config_or_model_meta(
                "API_ADD_RELATIONS", model=model, default=True
            )

            is_underscore = attribute.startswith("_")
            if (not ignore_underscore and is_underscore) or not is_underscore:
                # relations
                if isinstance(mapper_property, RelationshipProperty) and add_relations:
                    self.add_relationship_field(
                        attribute, original_attribute, mapper_property
                    )
                elif (
                    hasattr(mapper_property, "property")
                    and mapper_property.property._is_relationship
                ) and add_relations:
                    logger.debug(
                        4,
                        f"Adding to mallow object |{self.__class__.__name__}| relationship field +{mapper_property}+",
                    )
                    self.add_relationship_field(
                        attribute, original_attribute, mapper_property
                    )
                # columns
                elif hasattr(mapper_property, "property") and isinstance(
                    mapper_property.property, ColumnProperty
                ):
                    logger.debug(
                        4,
                        f"Adding to mallow object |{self.__class__.__name__}| column field +{mapper_property}+",
                    )
                    self.add_column_field(
                        attribute, original_attribute, mapper_property
                    )
                elif hasattr(mapper_property, "columns"):
                    logger.debug(
                        4,
                        f"Adding to mallow object |{self.__class__.__name__}| column field +{mapper_property}+",
                    )
                    self.add_column_field(
                        attribute, original_attribute, mapper_property.columns[0].type
                    )
                # hybrid properties
                elif isinstance(mapper_property, hybrid_property) and allow_hybrid:
                    logger.debug(
                        4,
                        f"Adding to mallow object |{self.__class__.__name__}| hybrid property field +{mapper_property.__name__}+",
                    )
                    self.add_hybrid_property_field(
                        attribute,
                        original_attribute,
                        mapper_property.__annotations__.get("return"),
                    )

    def add_hybrid_property_field(self, attribute, original_attribute, field_type):
        """
        Automatically add a field for a given hybrid property in the SQLAlchemy model.

        Args:
            attribute (str): The name of the attribute to add to the schema.
            original_attribute (str): The original attribute name from the SQLAlchemy model.
            field_type (str): The type of the hybrid property.

        Returns:
            None
        """

        # Skip attributes that start with an underscore
        ignore_underscore = get_config_or_model_meta(
            key="API_IGNORE_UNDERSCORE_ATTRIBUTE", model=self.get_model(), default=True
        )

        if ignore_underscore and attribute.startswith("_"):
            return

        # You might need to determine the appropriate field type differently.
        if field_type:
            field_type = type_mapping.get(field_type, fields.Str)
        else:
            field_type = fields.Str

        # Initialize field arguments
        field_args = {}

        # Check if there is a setter method for the hybrid property
        hybrid_property_obj = getattr(self.Meta.model, original_attribute, None)
        if not hasattr(hybrid_property_obj, "fset") or hybrid_property_obj.fset is None:
            field_args["dump_only"] = True  # No setter, so set it to dump only

        # Add the field to the Marshmallow schema
        self.fields[original_attribute] = field_type(data_key=attribute, **field_args)

        # Update additional attributes like you did in add_column_field
        self.fields[original_attribute].parent = self
        self.fields[original_attribute].name = attribute
        # Assuming `get_openapi_meta_data` is a function you've defined
        self.fields[original_attribute].metadata.update(
            get_openapi_meta_data(self.fields[original_attribute])
        )

    def add_column_field(self, attribute, original_attribute, mapper):
        """
        Automatically add a field for a given column in the SQLAlchemy model, using the column type to determine the
        Marshmallow field type. The function will ignore any attributes that start with an underscore.

        Args:
            attribute (str): The name of the attribute to add to the schema.
            original_attribute (str): The original attribute name from the SQLAlchemy model.
            mapper: SQLAlchemy mapper property object.

        Returns:
            None
        """

        column_type = mapper.property.columns[0].type

        # Skip attributes that start with an underscore
        model = self.get_model()

        if attribute.startswith("_") and get_config_or_model_meta(
            "API_IGNORE_UNDERSCORE_ATTRIBUTES", model, default=True
        ):
            return

        # Determine the Marshmallow field type based on the SQLAlchemy column type
        field_type = type_mapping.get(type(column_type))
        if field_type is None:
            return

        # Collect additional field attributes from the SQLAlchemy column
        field_args = {}
        column = self.model.__table__.columns.get(original_attribute)
        is_pk = False
        if column is not None:
            if not column.nullable and (
                not column.primary_key
                and column.autoincrement
                and column.default is None
            ):
                field_args["required"] = True
            if column.default is not None:
                field_args["default"] = (
                    column.default.arg if not callable(column.default.arg) else None
                )
            if hasattr(column_type, "length"):
                field_args["validate"] = Length(max=column_type.length)
            if column.unique or column.primary_key:
                # You can add more logic here to handle unique validation
                field_args["unique"] = True
            is_pk = column.primary_key
            # Add the field to the Marshmallow schema

        self.fields[original_attribute] = field_type(data_key=attribute, **field_args)

        # mark the field as dump_only if it is an auto incrementing primary key
        if mapper.autoincrement is True or mapper.default:
            self.fields[original_attribute].dump_only = True

        self.fields[original_attribute].dump_default = missing
        # this is set
        if is_pk:
            self.fields[original_attribute].metadata["is_pk"] = is_pk

        self.fields[original_attribute].parent = self
        self.fields[original_attribute].name = attribute
        self.fields[original_attribute].metadata.update(
            get_openapi_meta_data(self.fields[original_attribute])
        )

        field = getattr(self.model, attribute)
        info = getattr(field, "info", None)
        if info:
            validator = info.get("validator")
            validator_message = info.get("validator_message")
            if validator:
                self.fields[original_attribute].validate = (
                    lambda value: validate_by_type(validator, value, field, validator_message)
                )


    def add_relationship_field(
        self, attribute, original_attribute, relationship_property
    ):
        """
        Automatically add a field for a given relationship in the SQLAlchemy model.
        Args:
            attribute (str): The name of the attribute to add to the schema.
            original_attribute (str): The original attribute name from the SQLAlchemy model.
            relationship_property (RelationshipProperty): The SQLAlchemy relationship property object.

        Returns:

        """
        _, rel_type = _get_relation_use_list_and_type(relationship_property)
        model = self.get_model()
        serialization_type = get_config_or_model_meta(
            "API_SERIALIZATION_TYPE", model=model, default="hybrid"
        )
        nested_schema = get_input_output_from_model_or_make(
            relationship_property.mapper.class_
        )[1]
        matching = find_matching_relations(self.Meta.model, nested_schema.Meta.model)[0]

        if (
            serialization_type == "json"
            or (rel_type[-3:] == "ONE" and serialization_type == "hybrid")
        ) and self.depth <= 1:

            # If within allowed depth, serialize fully
            logger.debug(
                3,
                f"Serialization type is `{serialization_type} - Serializing -{nested_schema.__name__}- relations to JSON`",
            )
            # nested_schema.depth = self.depth + 1
            # nested_schema.parent = self
            schema_case = get_config_or_model_meta(
                "API_SCHEMA_CASE", model=self.get_model(), default="camel"
            )
            logger.debug(
                1,
                f"Creating to mallow object |{convert_case(self.__class__.__name__, schema_case)}|",
            )
            model = nested_schema.get_model() if hasattr(nested_schema, "get_model") else nested_schema
            nested_schema.__name__ = convert_case(model.__name__, schema_case)

            if rel_type[-3:] == "ONE":
                self.fields[original_attribute] = fields.Nested(
                    nested_schema,
                    data_key=attribute,
                    attribute=attribute,
                    dump_only=True,
                    many=False,
                )
            else:
                self.fields[original_attribute] = fields.Nested(
                    nested_schema,
                    many=True,
                    data_key=attribute,
                    attribute=attribute,
                    dump_only=True,
                )

        elif serialization_type == "url" or (
            rel_type[-4:] == "MANY" and serialization_type == "hybrid"
        ):
            logger.debug(
                3,
                f"Serialization type is `{serialization_type} - Serializing -{nested_schema.__name__}- relations to URL`",
            )

            def serialize_to_url(obj):
                # Your logic here

                nested_model = nested_schema.get_model() if hasattr(nested_schema, "get_model") else None
                namer = get_config_or_model_meta(
                    "API_ENDPOINT_NAMER", model=nested_model, default=endpoint_namer
                )
                if hasattr(obj, namer(nested_model) + "_to_url"):
                    return getattr(obj, namer(nested_model) + "_to_url")()
                elif hasattr(obj, matching[0] + "to_url"):
                    return obj.to_url()
                return None

            self.fields[original_attribute] = fields.Function(
                serialize_to_url, data_key=attribute
            )

        if self.fields.get(original_attribute):
            self.fields[original_attribute].parent = self
            self.fields[original_attribute].name = attribute
            self.fields[original_attribute].metadata.update(
                get_openapi_meta_data(self.fields[original_attribute])
            )

    def _make_not_required(self):
        """Makes all fields optional except the primary key."""
        from flask_scheema.api.utils import get_primary_keys

        primary_key_field = get_primary_keys(self.Meta.model)
        for field_name, field_obj in self.fields.items():
            if field_name != primary_key_field:
                field_obj.required = False

    # def _update_instance(self, loaded_data):
    #     """Updates an existing SQLAlchemy model instance."""
    #     from flask_scheema.api.utils import get_primary_keys
    #     primary_key_column = get_primary_keys(self.Meta.model)
    #     primary_key_value = loaded_data.get(primary_key_column)
    #
    #     if primary_key_value is None:
    #         raise ValidationError(
    #             f"Primary key {primary_key_column} must be present for {request.method} operations.")
    #
    #     session = self.Meta.model.get_session()
    #     instance = session.query(self.Meta.model).first()
    #
    #     if instance is None:
    #         raise ValidationError(f"Resource with primary key {primary_key_value} not found.")
    #
    #     for key, value in loaded_data.items():
    #         setattr(instance, key, value)
    #
    #     return instance

    def dump(self, obj, *args, **kwargs):
        """Custom serialization for SQLAlchemy model instances."""
        kwargs.setdefault("many", isinstance(obj, list))
        return super().dump(obj, *args, **kwargs)

    def load(self, data, *args, **kwargs):
        """Custom deserialization for SQLAlchemy model instances."""
        output_as_dict = kwargs.pop("output_as_dict", False)
        is_update = request.method in ["PATCH"]

        if hasattr(self.Meta, "model") and self.Meta.model:
            if is_update:
                self._make_not_required()

            loaded_data = super().load(data, *args, **kwargs)

            # if is_update:
            #     return self._update_instance(loaded_data)

            if not output_as_dict:
                return self.Meta.model(**loaded_data)

        return loaded_data
