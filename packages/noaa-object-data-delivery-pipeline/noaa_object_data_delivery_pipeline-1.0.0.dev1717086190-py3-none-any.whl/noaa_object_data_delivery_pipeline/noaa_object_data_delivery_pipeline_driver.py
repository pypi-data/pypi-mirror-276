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
from noaa_object_data_delivery_pipeline.step.ingest_data import IngestData
from krausening.logging import LogManager

"""
Driver to run the NoaaObjectDataDeliveryPipeline.

GENERATED STUB CODE - PLEASE ***DO*** MODIFY

Originally generated from: templates/data-delivery-pyspark/pipeline.driver.py.vm 
"""

logger = LogManager.get_instance().get_logger("NoaaObjectDataDeliveryPipeline")


if __name__ == "__main__":
    logger.info("STARTED: NoaaObjectDataDeliveryPipeline driver")

    # TODO: Execute steps in desired order and handle any inbound and outbound types
    ingest_data = IngestData().execute_step()
