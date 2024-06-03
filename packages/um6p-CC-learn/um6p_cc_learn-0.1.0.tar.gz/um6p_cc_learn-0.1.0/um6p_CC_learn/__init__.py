# mini_sklearn/__init__.py

# Define version
__version__ = "0.1"

import numpy as np
import scipy.linalg


# Import necessary submodules
from . import base
from . import datasets
from . import preprocessing
from . import feature_selection
from . import decomposition
from . import feature_extraction
from . import metrics
from . import model_selection
from . import linear_model
from . import tree
from . import ensemble
from . import neural_network
from . import pipeline
from . import naive_bayes
from . import utils
