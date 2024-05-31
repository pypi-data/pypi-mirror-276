# mltoolkit-laht 0.1.4

This is a Python library for data science and machine learning tasks. It provides utilities for data processing, modeling, and visualization.

## Installation

To install this package, clone the repository and run the setup script:

```
git clone https://github.com/lehidalgo/mltoolkit-laht
cd mltoolkit-laht
pip install .
```

## Usage

Here is a basic example of how to use this toolkit:

```python
import pandas as pd
from mltoolkit_laht import data_processing as dp
from mltoolkit_laht.datasets import load_banking_reviews_data

# ============================== Load Data ==============================
data_reader = dp.DataSource(data=load_banking_reviews_data())

# ============================== Data Preprocessing ==============================
BankReviews = data_reader.load_data()
BankReviews["Date"] = pd.to_datetime(BankReviews["Date"], format="%d-%m-%Y")
BankReviews["Year"] = BankReviews["Date"].dt.year
BankReviews["text_length"] = BankReviews.Reviews.apply(lambda x: len(x))

# ============================== Data Exploration ==============================
data_reader.show_df_info(num_rows=100)
```

Full example in Tutorials directory.

## Testing

To run the tests, use the following command:

```
python -m unittest discover tests
```

## Dependencies

This package requires the following Python libraries, which are listed in the `requirements.txt` file:

- numpy
- pandas
- scikit-learn
- matplotlib

Please make sure to install these dependencies before using this toolkit.

## Contributing

Contributions are welcome! Please submit a pull request or create an issue to propose changes or additions.
