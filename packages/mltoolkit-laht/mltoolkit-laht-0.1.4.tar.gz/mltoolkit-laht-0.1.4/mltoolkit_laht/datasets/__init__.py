import pandas as pd
import importlib.resources as pkg_resources


def load_banking_reviews_data():
    # Ensure this matches the path to your data file within the package
    with pkg_resources.open_text(
        "mltoolkit_laht.data", "BankReviews.csv", encoding="ISO-8859-1"
    ) as file:
        return pd.read_csv(file)
