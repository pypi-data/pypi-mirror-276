# -*- coding: utf-8 -*-
################################################################################
#     dataset_encoder for AutoML systems 
#     Python v3.10+
#     Created by dmforit
#     Licensed under Apache License v2
################################################################################
# Version
from .__version__ import __version__
from .categorical_encoder import CategoricalEncoder
from .circular_encoder import CircularEncoder
from .datetime_encoder import DateTimeEncoder
from .numerical_encoder import NumericalEncoder
from .encoder import Encoder
################################################################################
if __name__ == "__main__":
    module_type = 'Running'
else:
    module_type = 'Imported'
version_number = __version__
print("%s dataset_encoder %s" %(module_type, version_number))
################################################################################