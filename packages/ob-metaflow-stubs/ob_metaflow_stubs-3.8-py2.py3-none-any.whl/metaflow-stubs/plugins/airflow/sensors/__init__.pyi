##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.0.1+ob(v1)                                                    #
# Generated on 2024-05-30T17:28:59.772285                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.airflow.sensors.base_sensor

class ExternalTaskSensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def serialize_operator_args(self):
        ...
    def validate(self):
        ...
    ...

class S3KeySensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    def validate(self):
        ...
    ...

SUPPORTED_SENSORS: list

