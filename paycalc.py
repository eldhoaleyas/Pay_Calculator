import sys

def calculate_medicare_levy(taxable_income):
    LOWER_THRESHOLD = 27222.00
    UPPER_THRESHOLD = 34027.00
    
    medicare_levy = 0.0

    if taxable_income <= LOWER_THRESHOLD:
        medicare_levy = 0.0     
    elif taxable_income < UPPER_THRESHOLD:
        # Reduced Levy / Phase-in: 10% of income over the lower threshold
        medicare_levy = 0.10 * (taxable_income - LOWER_THRESHOLD)   
    else:
        # Full Levy: 2.0%
        medicare_levy = 0.02 * taxable_income
        
    return round(medicare_levy, 2)

def calculate_annual_tax(base_taxable_salary):

    tax_payable = 0.0
    taxable_income = base_taxable_salary 

    if taxable_income <= 18200:
        tax_payable = 0.0
    elif taxable_income <= 45000:
        tax_payable = 0.16 * (taxable_income - 18200)
    elif taxable_income <= 135000:
        tax_payable = 4288.00 + 0.30 * (taxable_income - 45000)
    elif taxable_income <= 190000:
        tax_payable = 31288.00 + 0.37 * (taxable_income - 135000)
    else: 
        tax_payable = 51638.00 + 0.45 * (taxable_income - 190000)
    
    medicare_levy = calculate_medicare_levy(base_taxable_salary)
    
    total_tax_and_levy = round(tax_payable + medicare_levy, 2)
    
    return {
        "income_tax": round(tax_payable, 2),
        "medicare_levy": medicare_levy,
        "total_deduction": total_tax_and_levy
    }

def calculate_pay_breakdown():
    try:
        annual_input = float(input("Please enter the TOTAL annual salary: $"))
    except ValueError:
        print("Invalid input. Please enter a numerical value for the salary.")
        sys.exit()
        
    # Check Superannuation Status (Standard SGC for 2024/2025 is 11%)
    standard_super_rate = 0.11
    super_rate_used = standard_super_rate
    
    super_included_input = input("Is the entered salary INCLUSIVE of superannuation (Total Package)? (yes/no): ").lower().strip()
    
    if super_included_input == 'yes':
        try:
            super_rate_input = input(f"What is the superannuation percentage? (Enter '11' for the standard {standard_super_rate*100:.0f}%): ")
            super_rate_used = float(super_rate_input) / 100 if super_rate_input else standard_super_rate
        except ValueError:
            super_rate_used = standard_super_rate
        base_taxable_salary = annual_input / (1 + super_rate_used)
        super_component = annual_input - base_taxable_salary
    else: # Assumes EXCLUSIVE of super
        base_taxable_salary = annual_input
        try:
            super_rate_input = input(f"What is the superannuation percentage? (Enter '11' for the standard {standard_super_rate*100:.0f}%): ")
            super_rate_used = float(super_rate_input) / 100 if super_rate_input else standard_super_rate
        except ValueError:
            super_rate_used = standard_super_rate
        super_contribution = base_taxable_salary * super_rate_used
        super_component = super_contribution

    tax_results = calculate_annual_tax(base_taxable_salary)
       
    annual_tax_deduction = tax_results["total_deduction"]
    net_annual_pay = base_taxable_salary - annual_tax_deduction

    # Gross Figures
    pay_monthly_gross = base_taxable_salary / 12
    pay_fortnightly_gross = base_taxable_salary / 26
    pay_weekly_gross = base_taxable_salary / 52
    pay_daily_gross = base_taxable_salary / 260
    pay_hourly_gross = pay_daily_gross / 8
    # Net Figures
    net_monthly_pay = net_annual_pay / 12
    net_fortnightly_pay = net_annual_pay / 26
    net_weekly_pay = net_annual_pay / 52
    net_daily_pay = net_annual_pay / 260
    net_hourly_pay = net_daily_pay / 8  
    
    print("\n=======================================================")
    print(f"** Taxable Base Salary: ${base_taxable_salary:,.2f} **")
    print(f"Superannuation Component ({super_rate_used*100:.2f}%): ${super_component:,.2f} (Employer Contribution)")
    print("=======================================================")

    print("\n--- ANNUAL DEDUCTIONS (Estimated) ---")
    print(f"1. Income Tax (PAYG): ${tax_results['income_tax']:,.2f}")
    print(f"2. Medicare Levy:     ${tax_results['medicare_levy']:,.2f}")
    print(f"Total Deduction:      ${annual_tax_deduction:,.2f}")

    print("\n--- NET PAY BREAKDOWN (Estimated Take-Home) ---")
    print(f"Annual:     ${net_annual_pay:,.2f}")
    print(f"Monthly:    ${net_monthly_pay:,.2f}")
    print(f"Fortnightly:${net_fortnightly_pay:,.2f}")
    print(f"Weekly:     ${net_weekly_pay:,.2f}")
    print(f"Daily:      ${net_daily_pay:,.2f}")
    print(f"Hourly:     ${net_hourly_pay:,.2f}")

    print("\n--- GROSS PAY BREAKDOWN (For Reference) ---")
    print(f"Annual:     ${base_taxable_salary:,.2f}")
    print(f"Monthly:    ${pay_monthly_gross:,.2f}")
    print(f"Fortnightly:${pay_fortnightly_gross:,.2f}")
    print(f"Weekly:     ${pay_weekly_gross:,.2f}")
    print(f"Daily:      ${pay_daily_gross:,.2f}")
    print(f"Hourly:     ${pay_hourly_gross:,.2f}")
    
    print("\n*NOTE: This is an ESTIMATE based on general assumptions (Australian resident, claiming tax-free threshold). It excludes HECS/HELP repayments, private health insurance (MLS), and other individual tax offsets.")

if __name__ == "__main__":
    calculate_pay_breakdown()