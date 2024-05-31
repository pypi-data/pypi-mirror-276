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
from ..generated.step.ingest_data_base import IngestDataBase
from krausening.logging import LogManager
from aiops_core_metadata.metadata_model import MetadataModel
from pyspark.sql.dataframe import DataFrame
from aiops_core_filestore.file_store_factory import FileStoreFactory


class IngestData(IngestDataBase):
    """
    Performs the business logic for IngestData.

    GENERATED STUB CODE - PLEASE ***DO*** MODIFY

    Originally generated from: templates/data-delivery-pyspark/synchronous.processor.impl.py.vm
    """

    logger = LogManager.get_instance().get_logger("IngestData")
    file_stores = {}

    def __init__(self):
        """
        TODO: Configure file store(s)
        In order for the factory to set up your file store, you will need to set a couple of environment
        variables through whichever deployment tool(s) you are using, and in the environment.py file for your tests.
        For more information: https://pages.github.boozallencsn.com/sig-aiops/solution-baseline-docs/aissemble/current/file-storage-details.html
        """
        super().__init__("synchronous", self.get_data_action_descriptive_label())
        self.file_stores["objData"] = FileStoreFactory.create_file_store("objData")

    def get_data_action_descriptive_label(self) -> str:
        """
        Provides a descriptive label for the action that can be used for logging (e.g., provenance details).
        """
        # TODO: replace with descriptive label
        return "IngestData"

    def execute_step_impl(self) -> DataFrame:
        """
        This method performs the business logic of this step.
        """
        # TODO: Add your business logic here for this step!
        IngestData.logger.warn(
            "Implement execute_step_impl(..) or remove this pipeline step!"
        )
        s3_bucket = "noaa-gpd"
        s3_path = f"s3a://{s3_bucket}/ingest/"

        inputDataset = self.spark.read.csv(s3_path, header=True, inferSchema=True)

        inputDataset.show()

        return None
