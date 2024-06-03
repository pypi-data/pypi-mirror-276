from typing import List, Optional

from akride import logger
from akride._utils.pipeline.constants import Constants
from akride.core.entities.pipeline import Pipeline
from akride.core.enums import DataType, FeaturizerType
from akride.core.exceptions import UserError


class PipelineHelper:
    FEATURIZER_TYPE_AND_PIPELINE_MAPPING = {
        DataType.IMAGE: {
            FeaturizerType.FULL_IMAGE: (
                Constants.FULL_IMAGE_PIPELINE_INTERNAL_ID
            ),
            FeaturizerType.PATCH: Constants.PATCH_IMAGE_PIPELINE_INTERNAL_ID,
            FeaturizerType.CLIP: Constants.CLIP_IMAGE_PIPELINE_INTERNAL_ID,
        },
        DataType.VIDEO: {
            FeaturizerType.FULL_IMAGE: (
                Constants.FULL_IMAGE_VIDEO_PIPELINE_INTERNAL_ID
            ),
            FeaturizerType.PATCH: Constants.PATCH_VIDEO_PIPELINE_INTERNAL_ID,
            FeaturizerType.CLIP: Constants.CLIP_VIDEO_PIPELINE_INTERNAL_ID,
        },
    }

    @classmethod
    def get_pipeline_internal_id(
        cls,
        featurizer_type: FeaturizerType,
        data_type: DataType = DataType.IMAGE,
    ) -> int:
        featurizer_map_by_datatype = (
            cls.FEATURIZER_TYPE_AND_PIPELINE_MAPPING.get(data_type)
        )
        if not featurizer_map_by_datatype:
            raise ValueError(f"Data type {data_type} is not yet supported!")

        pipeline_internal_id = featurizer_map_by_datatype.get(featurizer_type)

        if not pipeline_internal_id:
            raise ValueError(
                f"Featurizer {featurizer_type} is not yet supported"
            )
        return pipeline_internal_id

    @classmethod
    def get_default_pipeline(
        cls,
        attached_pipelines: List[Pipeline],
        data_type: DataType,
    ) -> Optional[Pipeline]:
        # Find the pipelines from the list of attached pipelines based on the dataset type,
        # if both full/patch pipelines are present, prefer patch
        # pipeline
        patch_image_pipeline: Optional[Pipeline] = None
        full_image_pipeline: Optional[Pipeline] = None

        featurizer_pipeline_map = cls.FEATURIZER_TYPE_AND_PIPELINE_MAPPING.get(
            data_type
        )

        patch_image_pipeline_id = featurizer_pipeline_map.get(
            FeaturizerType.PATCH
        )
        full_image_pipeline_id = featurizer_pipeline_map.get(
            FeaturizerType.FULL_IMAGE
        )

        logger.info(
            f"Patch image pipeline id is {patch_image_pipeline_id},"
            f"Full image pipeline id is {full_image_pipeline_id}"
        )

        for pipeline in attached_pipelines:
            internal_id = pipeline.info.pipeline_internal_id

            logger.info(f"Internal id is {internal_id}")
            if internal_id == patch_image_pipeline_id:
                patch_image_pipeline = pipeline
                break

            if internal_id == full_image_pipeline_id:
                full_image_pipeline = pipeline

        if patch_image_pipeline is None and full_image_pipeline is None:
            raise UserError(
                message="No default pipelines attached to the dataset"
            )

        return (
            patch_image_pipeline
            if patch_image_pipeline
            else full_image_pipeline
        )
