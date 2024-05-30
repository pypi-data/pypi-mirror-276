# pratlib/preprocessing/dimensionality_reduction.py
from pyspark.ml.feature import PCA as SparkPCA

class PCA:
    def __init__(self, **kwargs):
        self.pca = SparkPCA(**kwargs)

    def fit(self, df, input_col, output_col):
        self.pca.setInputCol(input_col).setOutputCol(output_col)
        self.model = self.pca.fit(df)
        return self

    def transform(self, df):
        return self.model.transform(df)
