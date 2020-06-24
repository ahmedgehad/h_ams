import numpy as np


# Calcualte some Custerom Lifetime Value metrics
def basic_clv(df, u_id, invoice_month, revenue, life_span_months):
    # Calculate monthly spend per customer
    monthly_revenue = df.groupby([u_id, invoice_month])[revenue].sum().mean()
    # Calculate average monthly spend
    monthly_revenue = np.mean(monthly_revenue)
    # Define lifespan to specific months period
    lifespan_months = life_span_months
    # Calculate basic CLV
    clv_basic = monthly_revenue * lifespan_months
    # Print basic CLV value
    print('\nAverage basic CLV is {:.1f} $ based on a lifespan of {} months'.format(clv_basic, lifespan_months))


# Granular CLV calculation
def granular_clv(df, u_id, invoice_month, revenue, Conv_ID, life_span_months):
    # Calculate average revenue per invoice
    revenue_per_purchase = df.groupby([Conv_ID])[revenue].mean().mean()
    # Calculate average number of unique invoices per customer per month
    freq = df.groupby([u_id, invoice_month])[Conv_ID].nunique().mean()
    # Define lifespan to specific months period
    lifespan_months = life_span_months
    # Calculate granular CLV
    clv_granular = revenue_per_purchase * freq * lifespan_months
    # Print granular CLV value
    print('\nAverage granular CLV is {:.1f} $ based on a lifespan of {} months'.format(clv_granular, lifespan_months))


# Traditional CLV
def traditional_clv(df, retention_df, u_id, invoice_month, revenue):
    # Calculate monthly spend per customer
    monthly_revenue = df.groupby([u_id, invoice_month])[revenue].sum().mean()
    # Calculate average monthly retention rate
    retention_rate = retention_rate = retention_df.iloc[:, 1:].mean().mean()
    # Calculate average monthly churn rate
    churn_rate = 1 - retention_rate
    # Calculate traditional CLV
    clv_traditional = monthly_revenue * (retention_rate / churn_rate)
    # Print traditional CLV and the retention rate values
    print('\nAverage traditional CLV is {:.1f} $ at {:.1f} % retention_rate'.format(
        clv_traditional, retention_rate * 100))
