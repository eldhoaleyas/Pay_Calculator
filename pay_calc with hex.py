import sys


def calculate_hecs_help_repayment(repayment_income):

    HECS_BRACKETS = [
        (159664, float('inf'), 0.100),
        (150627, 159663, 0.095),
        (142101, 150626, 0.090),
        (134057, 142100, 0.085),
        (126468, 134056, 0.080),
        (119310, 126467, 0.075),
        (112557, 119309, 0.070),
        (106186, 112556, 0.065),
        (100175, 106185, 0.060),
        (94504, 100174, 0.055),
        (89155, 94503, 0.050),
        (84108, 89154, 0.045),
        (79347, 84107, 0.040),
        (74856, 79346, 0.035),
        (70619, 74855, 0.030),
        (66621, 70618, 0.025),
        (62851, 66620, 0.020),
        (54435, 62850, 0.010),
        (0, 54434, 0.000)
    ]
    
    repayment = 0.0
    
    if repayment_income < 54435:
        return 0.0

    for lower, upper, rate in HECS_BRACKETS:
        if repayment_income >= lower:
            repayment = repayment_income * rate
            break
            
    return round(repayment, 2)



def calculate_medicare_levy(taxable_income):
    LOWER_THRESHOLD = 27222.00
    UPPER_THRESHOLD = 34027.00
    
    medicare_levy = 0.0

    if taxable_income <= LOWER_THRESHOLD:
        medicare_levy = 0.0     
    elif taxable_income < UPPER_THRESHOLD:
        medicare_levy = 0.10 * (taxable_income - LOWER_THRESHOLD)   
    else:
        medicare_levy = 0.02 * taxable_income
        
    return round(medicare_levy, 2)


def calculate_annual_tax(base_taxable_salary, has_hecs_debt=False):
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
    hecs_repayment = 0.0
    
    if has_hecs_debt:
        hecs_repayment = calculate_hecs_help_repayment(base_taxable_salary)
    
    total_tax_and_levy = round(tax_payable + medicare_levy + hecs_repayment, 2)
    
    return {
        "income_tax": round(tax_payable, 2),
        "medicare_levy": medicare_levy,
        "hecs_repayment": hecs_repayment,
        "total_deduction": total_tax_and_levy
    }

# --- Main Logic Function ---
def calculate_pay_breakdown():
    try:
        annual_input = float(input("Please enter the TOTAL annual salary: $"))
    except ValueError:
        print("Invalid input. Please enter a numerical value for the salary.")
        sys.exit()
        
    # User inputs for Super and HECS
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

    hecs_input = input("Do you have a HECS/HELP debt? (yes/no): ").lower().strip()
    has_hecs_debt = hecs_input == 'yes'

    tax_results = calculate_annual_tax(base_taxable_salary, has_hecs_debt)
       
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
    
    # --- OUTPUT ---
    print("\n=======================================================")
    print(f"** Taxable Base Salary: ${base_taxable_salary:,.2f} **")
    print(f"Superannuation Component ({super_rate_used*100:.2f}%): ${super_component:,.2f} (Employer Contribution)")
    print("=======================================================")

    print("\n--- ANNUAL DEDUCTIONS (Estimated) ---")
    print(f"1. Income Tax (PAYG): ${tax_results['income_tax']:,.2f}")
    print(f"2. Medicare Levy:     ${tax_results['medicare_levy']:,.2f}")
    if has_hecs_debt:
        print(f"3. HECS/HELP Repay:   ${tax_results['hecs_repayment']:,.2f}")
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
    
    print("\n*NOTE: This is an ESTIMATE based on general assumptions (Australian resident, claiming tax-free threshold). It excludes Medicare Levy Surcharge (MLS), Low-Income Tax Offset (LITO), and other individual tax offsets.")

if __name__ == "__main__":
    calculate_pay_breakdown()