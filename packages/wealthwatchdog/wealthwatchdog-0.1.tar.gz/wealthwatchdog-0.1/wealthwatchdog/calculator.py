def calculate_savings(initial_amount, monthly_income, monthly_expenses):
    savings_per_month = monthly_income - monthly_expenses
    total_savings = initial_amount + (savings_per_month * 12)
    return total_savings
