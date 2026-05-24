import polars as pl

# To get the version of Polars
print(pl.__version__)

data={
    "ID":100,
    "Name":"Prem",
    "Age":40
      }

print(data)
print(type(data))

data_df=pl.DataFrame(data)
print(data_df)

print(type(data_df))