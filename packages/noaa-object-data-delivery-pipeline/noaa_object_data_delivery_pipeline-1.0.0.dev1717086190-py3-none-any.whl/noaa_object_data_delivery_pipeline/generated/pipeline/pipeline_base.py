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

class PipelineBase:
    """
    Performs pipeline level process for NoaaObjectDataDeliveryPipeline.

    GENERATED CODE - DO NOT MODIFY

    Generated from: templates/pipeline.base.py.vm
    """

    _instance = None
    logger = LogManager.get_instance().get_logger('PipelineBase')


    def __new__(cls):
        """
        Create a singleton class for pipeline level process
        """
        if cls._instance is None:
            print("Creating the PipelineBase")
            cls._instance = super(PipelineBase, cls).__new__(cls)
        return cls._instance






