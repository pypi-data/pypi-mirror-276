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
from ...step.abstract_data_action_impl import AbstractDataActionImpl

class AbstractPipelineStep(AbstractDataActionImpl):
    """
    Performs common step configurationbased on the pipeline.

    GENERATED CODE - DO NOT MODIFY (Add your customization in your step implementation classes)

    Generated from: templates/data-delivery-pyspark/abstract.pipeline.step.py.vm
    """

    def __init__(self, subject, action):
        super().__init__(subject, action)
