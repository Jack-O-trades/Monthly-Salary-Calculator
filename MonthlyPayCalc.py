#`Imports the necessary components from the decimal module 
# It ensures precise financial calculations, avoiding floating-point errors.`
from decimal import Decimal, getcontext, ROUND_HALF_UP

# Set precision for financial calculations to 10 significant digits
getcontext().prec = 10

class LoanCalculator:
    """A precise loan calculator using Decimal for financial accuracy"""

    def __init__(self, principal, annual_rate, years):
        """
        Initialize loan calculator
        Args:
            principal: Loan amount as string or Decimal
            annual_rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
            years: Loan term in years
        """
        # Convert inputs to Decimal for precision
        self.principal = Decimal(str(principal))
        self.annual_rate = Decimal(str(annual_rate))
        self.years = int(years)
        
        # Calculate monthly rate (annual rate / 12)
        self.monthly_rate = self.annual_rate / Decimal('12')
        # Calculate total number of payments (years * 12)
        self.total_payments = self.years * 12

    def calculate_monthly_payment(self):
        """Calculate monthly payment using precise decimal arithmetic"""
        
        # Handle the special case where the annual interest rate is zero
        if self.annual_rate == 0:
            # Simple division for interest-free loan
            return self.principal / Decimal(str(self.total_payments))

        # Monthly payment formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        r = self.monthly_rate
        n = Decimal(str(self.total_payments))
        
        # Calculate (1+r)^n, a key factor in the formula
        factor = (Decimal('1') + r) ** n
        
        # Apply the full formula
        monthly_payment = self.principal * (r * factor) / (factor - Decimal('1'))
        
        # Round the result to two decimal places (cents) using half-up rounding
        return monthly_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def generate_amortization_schedule(self):
        """Generate first few payments of the amortization schedule (up to 12 payments)"""
        
        # Get the required monthly payment
        monthly_payment = self.calculate_monthly_payment()
        balance = self.principal
        schedule = []
        
        # Loop through payments, up to 12 or the total number of payments
        for payment_num in range(1, min(13, self.total_payments + 1)):
            # Calculate interest for the period: Interest = Balance * Monthly Rate
            interest_payment = (balance * self.monthly_rate).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Calculate principal paid: Principal = Monthly Payment - Interest Payment
            principal_payment = monthly_payment - interest_payment

            # Update remaining loan balance
            balance -= principal_payment
            
            # Store payment details
            schedule.append({
                'payment': payment_num,
                'monthly_payment': monthly_payment,
                'interest': interest_payment,
                'principal': principal_payment,
                # Round balance for display
                'balance': balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            })
            
        return schedule

    def total_interest_paid(self):
        """Calculate total interest over the life of the loan"""
        
        monthly_payment = self.calculate_monthly_payment()
        # Total amount paid = Monthly Payment * Total Payments
        total_paid = monthly_payment * Decimal(str(self.total_payments))
        
        # Total Interest = Total Paid - Principal
        # Quantize (round) the result to two decimal places
        return (total_paid - self.principal).quantize(Decimal('0.01'))

# Example usage
print("=== Loan Calculator Application ===")

# Define loan scenarios
loans = [
    {"principal": "250000", "rate": "0.045", "years": 30, "description": "30-year mortgage"},
    {"principal": "25000", "rate": "0.0675", "years": 5, "description": "5-year car loan"},
    {"principal": "50000", "rate": "0", "years": 10, "description": "Interest-free loan"}
]

for loan_data in loans:
    print(f"\n{loan_data['description']}:")
    print("-" * 50)
    
    # Instantiate the calculator
    calc = LoanCalculator(
        loan_data["principal"],
        loan_data["rate"],
        loan_data["years"]
    )

    # Calculate key metrics
    monthly = calc.calculate_monthly_payment()
    total_interest = calc.total_interest_paid()
    
    # Print summary
    print(f"Loan Amount: ${calc.principal:,}")
    print(f"Monthly Payment: ${monthly}")
    print(f"Total Interest: ${total_interest:,}")
    # Total Cost = Principal + Total Interest
    print(f"Total Cost: ${calc.principal + total_interest:,}")

    # Generate and display the first few payments
    schedule = calc.generate_amortization_schedule()
    print(f"\nFirst 3 Payments:")
    
    # Print table header
    print(f"{'Pmt':<3} {'Payment':<10} {'Interest':<10} {'Principal':<10} {'Balance' :<10}")
    print("-" * 50)
    
    # Loop through and print the first 3 payment entries
    for payment in schedule[:3]:
        print(f"{payment['payment']:<3} "
              f"${payment['monthly_payment']:<9} "
              f"${payment['interest']:<9} "
              f"${payment['principal']:<9} "
              f"${payment['balance']:<11,}")