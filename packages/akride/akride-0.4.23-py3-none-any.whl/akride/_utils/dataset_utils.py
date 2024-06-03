from akride import Constants
from akride.core.enums import DataType
from akride.core.exceptions import ServerError


def get_dataset_type(dataset_type: str) -> DataType:
    return DataType(dataset_type)


def get_primary_table_columns(dataset_type: DataType):
    if dataset_type == DataType.IMAGE:
        return Constants.PRIMARY_TABLE_IMAGE_COLUMNS

    elif dataset_type == DataType.VIDEO:
        return Constants.PRIMARY_TABLE_VIDEO_COLUMNS

    raise ServerError(f"No primary table is defined for '{dataset_type}'")
