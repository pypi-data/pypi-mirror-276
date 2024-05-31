###
# #%L
# NOAA GPD::Pipelines::Noaa Object Data Delivery Pipeline
# %%
# Copyright (C) 2021 Booz Allen
# %%
# All Rights Reserved. You may not copy, reproduce, distribute, publish, display, 
# execute, modify, create derivative works of, transmit, sell or offer for resale, 
# or in any way exploit any part of this solution without Booz Allen Hamilton’s 
# express written permission.
# #L%
###
from krausening.logging import LogManager
from data_delivery_spark_py.test_utils.spark_session_manager import create_standalone_spark_session

"""
Behave test environment setup to configure Spark for unit tests.

GENERATED CODE - DO NOT MODIFY (add your customizations in environment.py).

Originally generated from: templates/data-delivery-pyspark/behave.environment.base.py.vm
"""
logger = LogManager.get_instance().get_logger("Environment")


"""
Generated or model-dependent setup to be executed prior to unit tests.
"""
def initialize(sparkapplication_path = "target/apps/noaa-object-data-delivery-pipeline-test-chart.yaml"):
    create_standalone_spark_session(sparkapplication_path)


"""
Generated or model-dependent setup to be executed after completion of unit tests.
"""
def cleanup():
    pass
