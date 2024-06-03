import typing

from marshmallow import ValidationError, Schema

from . import TargetNameType
from .exceptions import SchemaValidationException
from .ValidatorABS import ValidatorABS
from ..logger import app_core_logger


TP = typing.TypeVar('TP', bound=dict)
TR = typing.TypeVar('TR', bound=dict)


class ValidatorMarshmallow(ValidatorABS, typing.Generic[TR]):
    schema: Schema

    @typing.overload
    def validate(self, payload: typing.List[TP]) -> typing.List[TR]: ...

    @typing.overload
    def validate(self, payload: TP) -> TR: ...

    def validate(self, payload: typing.Union[dict, list]) -> typing.Union[dict, list]:
        try:
            return self.schema.load(payload)
        except ValidationError as ex:
            raise self.errors_mapper(ex.messages)

    def errors_mapper(self, errors) -> SchemaValidationException:
        errors_list = []
        for key, value in errors.items():
            try:
                # Custom validators
                if key == '_schema':
                    key = ''
                if isinstance(value, list):
                    errors_list.append(self.validation_error(','.join(value), [key]))
                elif isinstance(value, dict):
                    for i, error_data_object in value.items():
                        if isinstance(error_data_object, list):
                            for err_text in error_data_object:
                                errors_list.append(self.validation_error(err_text, [str(key), str(i)]))
                        elif isinstance(error_data_object, dict):
                            for field_name, error_data in error_data_object.items():
                                # Custom validators
                                if field_name == '_schema':
                                    errors_list.append(
                                        self.validation_error(','.join(error_data), [str(key), str(i)])
                                    )
                                else:
                                    errors_list.append(
                                        self.validation_error(','.join(error_data), [str(key), str(i), field_name])
                                    )
                        else:
                            errors_list.append(self.validation_error(str(value), [key]))
                else:
                    errors_list.append(self.validation_error(str(value), [key]))
            except Exception as exc:
                app_core_logger.exception(f'Failed parse validation exception for marshmallow: {exc}')
        return SchemaValidationException(self.target_name, errors_list)

    @classmethod
    def validation_error(cls, message: str, location: typing.List[str]):
        return SchemaValidationException.SchemaValidationItemException(
            message,
            location=location
        )

    def get_schema_fields(self):
        return list(self.schema.fields.keys()) if self.target_name == TargetNameType.PARAMS else []

