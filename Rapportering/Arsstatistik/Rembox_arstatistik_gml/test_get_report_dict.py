import pandas as pd
from src.get import get_report_dict


def test_get_report_dict_should_return_a_dict_with_a_dataframe_for_each_hospital():
    # Arrange
    expected_keys = sorted(["Lycksele", "Skellefteå"])
    study_data = {}
    report_df = pd.DataFrame()

    # Act
    result = get_report_dict(study_data_dictionary=study_data, report_dataframe=report_df)
    actual_keys = sorted(list(result.keys()))

    # Assert
    assert actual_keys == expected_keys
