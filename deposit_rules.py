import json
import os

# Load deposit product rules from JSON file
def load_deposit_products():
    with open('deposit_products.json', 'r') as file:
        return json.load(file)

deposit_products = load_deposit_products()

# Validate the term in days for the selected product
def validate_term(product_code, term_days, deposit_age):
    product = deposit_products.get(product_code)
    if not product:
        raise ValueError(f"Invalid product code: {product_code}")

    valid_terms = product.get("valid_terms")
    if term_days < 2 or (valid_terms and term_days not in valid_terms):
        raise ValueError(
            f"Invalid term: {term_days} days. Valid terms for {product['name']} are: {', '.join(map(str, valid_terms))} days."
        )

    if deposit_age < 2 or deposit_age > term_days:
        raise ValueError(
            f"Invalid deposit age: {deposit_age} days. It must be between 2 and {term_days} days."
        )

# Calculate the interest rate for a deposit
def calculate_interest_rate(product_code, principal, term_days, deposit_age, prime_rate, margin_rate, digital_bonus):
    product = deposit_products.get(product_code)
    if not product:
        raise ValueError(f"Invalid product code: {product_code}")

    interest_formula = product.get("interest_formula")
    tiers = product.get("tiers")

    # Check for tiered bonuses
    bonus = 0.0
    if tiers:
        for tier in tiers:
            if tier["amount_min"] <= principal and (tier["amount_max"] is None or principal <= tier["amount_max"]):
                bonus = tier["bonus"]
                break

    # Calculate the interest rate based on the formula
    try:
        base_rate = prime_rate - float(interest_formula.split('-')[-1].strip())
    except Exception:
        raise ValueError(f"Invalid interest formula for product: {product_code}")

    total_rate = base_rate + bonus + margin_rate + digital_bonus

    # Compound interest calculation for daily deposit
    if product_code == "5071/5":
        return calculate_compound_interest(principal, total_rate, min(deposit_age, term_days))

    # Simple interest for other products
    accrued_interest = principal * (total_rate / 100) * (deposit_age / 365)
    return accrued_interest

# Compound interest calculation
def calculate_compound_interest(principal, rate, days):
    daily_rate = rate / 100 / 365
    total_amount = principal * ((1 + daily_rate) ** days)
    return total_amount - principal
