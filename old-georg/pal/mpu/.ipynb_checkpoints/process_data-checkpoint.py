from pathlib import Path
import pandas as pd


def process(path: Path):
    data = pd.read_csv(path)

    data


if __name__ == '__main__':
    root = Path(__file__).parent
    process(root / 'good.csv')