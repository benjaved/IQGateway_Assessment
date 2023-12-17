import pandas as pd
from types import GeneratorType
from datetime import datetime, timedelta

class NestedCV:
    def __init__(self, k):
        # Initialize the NestedCV object with the number of folds (k)
        self.k = k

    def split(self, data, date_column):
   
        # Get unique dates from the specified date column
        dt=data[date_column].unique()
    
    # Iterate over each fold
        for i in range(self.k):
            # Check if the number of folds is greater than or equal to the number of unique dates
            if(self.k+1>=len(dt)):
                print("The number of folds should be less than the number of dates")
                break
                
            if i==0:
                # For the first iteration, create the first fold
                fold=self.k+1
                fold_size = int(len(dt) / fold) 
                end_date = fold_size + (len(dt)%fold)
                
                # Split the data into training and validation sets based on date
                train_data = data[data["date"]<=dt[end_date-1]]
                valid_data = data[(data["date"]>dt[end_date-1]) & (data["date"]<=dt[(end_date-1)+fold_size])]
                
                # Yield the training and validation sets for the first fold
                yield train_data, valid_data
            else:
                # For subsequent iterations, update the end_date and create the next fold
                end_date=end_date + fold_size

                # Split the data into training and validation sets based on date
                train_data = data[data["date"]<=dt[end_date-1]]
                valid_data = data[(data["date"]>dt[end_date-1]) & (data["date"]<=dt[(end_date-1)+fold_size])]
        
                # Yield the training and validation sets for the current fold
                yield train_data, valid_data


#Unit test skeleton provided in the assignment
if __name__ == "__main__":
    # Creating sample dataset to test
    # Generate date range
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 2, 28)
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    # Creating a sample DataFrame
    data = {
        'date': np.repeat(date_range, 3),  # Repeat each date three times for three groups
        'group_column': np.tile(['Group1', 'Group2', 'Group3'], len(date_range)),
        'value': np.random.randn(len(date_range) * 3)
    }
    data = pd.DataFrame(data)
    data["date"] = pd.to_datetime(data["date"])

    # nested cv
    k = 3
    cv = NestedCV(k)
    splits = cv.split(data, "date")

    # check return type
    assert isinstance(splits, GeneratorType)

    # check return types, shapes, and data leaks
    count = 0
    for train, validate in splits:
        
        # types
        assert isinstance(train, pd.DataFrame)
        assert isinstance(validate, pd.DataFrame)

        # shape
        assert train.shape[1] == validate.shape[1]

        # data leak
        assert train["date"].max() <= validate["date"].min()

        count += 1

    # check number of splits returned
    assert count == k