import pyspark.sql.functions as F
from pyspark.sql.types import ArrayType
from pyspark.sql.types import StringType


def identity(df):
    return df


def myFilter(df, col, filter_value):

    df = df.filter(df[col] == filter_value)
    return df


#def mydroper_udf(df):
#    F.udf(mydroperonArrayOfString, ArrayType(StringType()))


def mydroper(df):
    return df.dropna(thresh=15)