import FinanceDataReader as fdr

listing = fdr.StockListing('KRX')

listing[['Code','Name']].to_csv(
    'stocks.csv',
    index=False,
    encoding='utf-8-sig'
)

print("완료")