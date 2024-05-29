# DataGen-kuma
DataGen-kuma is a library for generating test data.   
It creates similar data with the same schema based on a Pandas DataFrame.

# How It Works
DataGen-kuma takes a DataFrame as input and generates random test data.   
Internally, it generates statistical metrics for each data type to facilitate data generation.   
Using these metrics, it produces similar data appropriate for each data type.

## Data Classification and Generation
- Numeric: Numeric data. Generates random values using Kernel Density Estimation (KDE) technique. The kernel density function uses gaussian_kde from scipy.stats.
- Category: Categorical data. Measures the frequency of each value and generates values according to these frequencies.
- Datetime: Date data following the ISO-8601 standard. Converts to Pandas Timestamps and generates random values within the given date range.
- Boolean: Boolean data. Measures the frequency of each value and generates values according to these frequencies.
- ETC: All other data types not mentioned above. Generates data by randomly sampling from the given values with replacement.

# Usage
Assuming you have a Pandas DataFrame named df.   
This example generates 100,000 rows of data.   
The generated object allows access to each row through iteration.

```python
from datagen_kuma.datagen import DataGen

datagen = DataGen(df=df, count=100_000)
for idx, row in datagen:
    print(idx, row)
```

To retrieve the generated DataFrame, use the following:
```python
generated_df = datagen.dataframe
```