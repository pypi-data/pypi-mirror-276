'''
Train test validation split function
'''

#pylint: disable=too-many-arguments
#pylint: disable=too-many-locals

from sklearn.model_selection import train_test_split


def train_validation_test_split(
        data,
        col_stratify,
        train_percent=0.7,
        validate_percent=0.15,
        test_percent=0.15,
        random_state=2024
        ):
    """
    Splits a Pandas dataframe into three subsets (train, val, and test).
    Function uses train_test_split (from sklearn) and stratify to receive
    the same ratio response (y, target) in each splits.

    Parameters
    ----------
    data: pd.DataFrame
        Data to split
    col_stratify: str
        Name of column target
    train_percent: float (0,1)
        Percent of train data
    validate_percent: float (0,1)
        Percent of validate data
    test_percent: float (0,1)
        Percent of test data
    random_state: int, None
    
    WARNING:
        Sum of train_percent, validate_percent and test_percent have to be equal 1.0.

    Returns
        data_train, data_val, data_test : Dataframes containing the three splits.
        y_train, y_val, y_test : Series with target variables
    """

    if train_percent + validate_percent + test_percent != 1.0:
        raise ValueError('Sum of train, validate and test is not 1.0')

    if col_stratify not in data.columns:
        raise ValueError(f'{col_stratify} is not a column in the dataframe')

    y = data[[col_stratify]]

    # Split original dataframe into train and temp dataframes.
    data_train, data_temp, y_train, y_temp = train_test_split(
        data,
        y,
        stratify=y,
        test_size=(
            1.0 - train_percent
            ),
        random_state=random_state
        )
    # Split the temp dataframe into val and test dataframes.
    test_to_split = test_percent / (validate_percent + test_percent)
    data_val, data_test, y_val, y_test = train_test_split(
        data_temp,
        y_temp,
        stratify=y_temp,
        test_size=test_to_split,
        random_state=random_state
        )

    assert len(data) == len(data_train) + len(data_val) + len(data_test), \
        "Length of X is different than sum of x_train + x_test + x_val"
    assert len(y) == len(y_train) + len(y_val) + len(y_test), \
        "Length of y is different than sum of y_train + y_test + y_val"
    assert len(data_train) == len(y_train), "Length of data_train is different than y_train"
    assert len(data_val) == len(y_val), "Length of data_val is different than y_val"
    assert len(data_test) == len(y_test), "Length of data_test is different than y_test"

    return data_train.drop(col_stratify, axis=1), data_val.drop(col_stratify, axis=1), \
        data_test.drop(col_stratify, axis=1), y_train, y_val, y_test
