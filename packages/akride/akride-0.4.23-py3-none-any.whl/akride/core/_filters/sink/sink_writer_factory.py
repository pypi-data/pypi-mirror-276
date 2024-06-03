import akridata_akrimanager_v2 as am
import akridata_dsp as dsp

from akride.core._filters.sink.image_sink_writer_filter import (
    ImageSinkWriterFilter,
)
from akride.core._filters.sink.models import SinkWriterFilterInput
from akride.core._filters.sink.video_sink_writer_filter import (
    VideoSinkWriterFilter,
)
from akride.core.enums import DataType
from akride.core.exceptions import ServerError


class SinkWriterFilterFactory:
    @staticmethod
    def get_sink_writer(
        filter_input: SinkWriterFilterInput,
        workflow_api: am.WorkflowsApi,
        dsp_dataset_api: dsp.DatasetApi,
        ccs_api: am.CcsApi,
        data_type: DataType.IMAGE,
    ):
        if data_type == DataType.IMAGE:
            return ImageSinkWriterFilter(
                filter_input=filter_input,
                workflow_api=workflow_api,
                dsp_dataset_api=dsp_dataset_api,
                ccs_api=ccs_api,
            )
        elif data_type == DataType.VIDEO:
            return VideoSinkWriterFilter(
                filter_input=filter_input,
                workflow_api=workflow_api,
                dsp_dataset_api=dsp_dataset_api,
                ccs_api=ccs_api,
            )

        raise ServerError(
            f"Sink writer for data type {data_type} " f"is not defined!"
        )
