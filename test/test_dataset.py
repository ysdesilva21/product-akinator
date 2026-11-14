from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / 'data' / 'product_akinator_100.csv'
df = pd.read_csv(DATA)
FEATURES = list(df.columns[3:])

def test_dimensions():
    assert df.shape == (100, 31)
    assert len(FEATURES) == 28

def test_categories():
    assert df['category'].nunique() == 10
    assert (df.groupby('category').size() == 10).all()

def test_integrity():
    assert not df.isna().any().any()
    assert df['product_id'].is_unique
    assert df['product_name'].is_unique
    assert set(df['product_id']) == set(range(1, 101))

def test_binary_features():
    assert df[FEATURES].isin([0, 1]).all().all()

def test_question_patterns_unique():
    collisions = df[df.duplicated(subset=FEATURES, keep=False)]
    assert collisions.empty, ('Indistinguishable products: ' + ', '.join(collisions['product_name']))
