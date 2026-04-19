from collections import namedtuple

Measurement = namedtuple("Measurement", ["date", "result"])

MeasurementsData = namedtuple(
    "MeasurementsData", ["type", "measurement_time", "unit", "job_name", "measurements"]
)
