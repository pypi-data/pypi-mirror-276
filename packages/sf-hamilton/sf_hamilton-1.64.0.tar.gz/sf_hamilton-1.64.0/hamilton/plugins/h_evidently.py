import pandas as pd
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report
from evidently.test_preset import DataStabilityTestPreset
from evidently.test_suite import TestSuite
from sklearn import datasets

iris_data = datasets.load_iris(as_frame="auto")
iris_frame = iris_data.frame

data_stability = TestSuite(
    tests=[
        DataStabilityTestPreset(),
    ]
)
data_stability.run(
    current_data=iris_frame.iloc[:60],
    reference_data=iris_frame.iloc[60:],
    column_mapping=None,
)
data_stability
