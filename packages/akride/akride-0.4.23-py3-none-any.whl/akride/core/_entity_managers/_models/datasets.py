from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from akride import Constants
from akride.core.enums import DataType
from akride.core.exceptions import InvalidInputError


class CreateDatasetIn(BaseModel):
    dataset_name: str
    dataset_namespace: str = "default"
    data_type: DataType = DataType.IMAGE
    glob_pattern: str = Field(
        validate_default=True, default=Constants.DEFAULT_IMAGE_BLOB_EXPR
    )
    overwrite: bool = False
    sample_frame_rate: float = -1

    @field_validator("sample_frame_rate")
    def validate_frame_rate(cls, v: float, info: ValidationInfo) -> float:
        data_type = info.data.get("data_type")
        sample_frame_rate = v

        if data_type == DataType.IMAGE and sample_frame_rate != -1:
            raise InvalidInputError(
                "Sample frame rate is not applicable " "for image datasets!"
            )

        return v

    @field_validator("glob_pattern")
    def set_glob_pattern(cls, v: str, info: ValidationInfo) -> str:
        data_type = info.data.get("data_type")
        glob_pattern = v

        if (
            data_type == DataType.VIDEO
            and glob_pattern == Constants.DEFAULT_IMAGE_BLOB_EXPR
        ):
            glob_pattern = Constants.DEFAULT_VIDEO_BLOB_EXPR

        return glob_pattern
