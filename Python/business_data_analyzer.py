"""Analyze a sample business sales dataset. Requires pandas and matplotlib."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).with_name('sample_sales.csv')


def main():
    if not DATA_FILE.exists():
        sample = pd.DataFrame([
            {'date': '2026-10-01', 'category': 'Food', 'product': 'Sandwich', 'quantity': 12, 'unit_price': 8.5},
            {'date': '2026-10-02', 'category': 'Drinks', 'product': 'Coffee', 'quantity': 25, 'unit_price': 3.5},
            {'date': '2026-10-03', 'category': 'Food', 'product': 'Salad', 'quantity': 9, 'unit_price': 11},
            {'date': '2026-10-04', 'category': 'Supplies', 'product': 'Notebook', 'quantity': 15, 'unit_price': 4},
            {'date': '2026-10-05', 'category': 'Drinks', 'product': 'Tea', 'quantity': 18, 'unit_price': 2.75},
        ])
        sample.to_csv(DATA_FILE, index=False)
        print(f'Created sample dataset: {DATA_FILE.name}')

    sales = pd.read_csv(DATA_FILE)
    required = {'date', 'category', 'product', 'quantity', 'unit_price'}
    if not required.issubset(sales.columns):
        raise ValueError(f'CSV must contain columns: {sorted(required)}')
    sales['quantity'] = pd.to_numeric(sales['quantity'], errors='raise')
    sales['unit_price'] = pd.to_numeric(sales['unit_price'], errors='raise')
    sales['revenue'] = sales['quantity'] * sales['unit_price']
    by_category = sales.groupby('category')['revenue'].sum().sort_values(ascending=False)
    by_product = sales.groupby('product')['revenue'].sum().sort_values(ascending=False)

    print('\n=== BUSINESS SALES REPORT ===')
    print(f'Total revenue: ${sales["revenue"].sum():,.2f}')
    print(f'Units sold: {sales["quantity"].sum():,.0f}')
    print('\nRevenue by category:')
    print(by_category.to_string())
    print(f'\nTop product: {by_product.index[0]} (${by_product.iloc[0]:,.2f})')

    ax = by_category.plot(kind='bar', title='Revenue by Category', ylabel='Revenue ($)', rot=0)
    ax.figure.tight_layout()
    output = Path(__file__).with_name('sales_by_category.png')
    ax.figure.savefig(output)
    plt.close(ax.figure)
    print(f'\nSaved chart: {output.name}')


if __name__ == '__main__':
    main()
