from .models import *

def determine_policy_for_user(user):
    quotation_info = QuotationInfo.objects.get(user=user)

    contribution_amount = quotation_info.contribution_amount

    # Determine policy based on contribution amount
    policy = determine_policy_based_on_contribution(contribution_amount)

    return policy

def determine_policy_based_on_contribution(contribution_amount):
    # Fetch policies from the database based on contribution amount
    policies = Policy.objects.filter(lower_limit__lte=contribution_amount, upper_limit__gte=contribution_amount).order_by('upper_limit')

    """
    Policy.objects.filter(...): This line queries the Policy model.
    lower_limit__lte=contribution_amount: This filters policies where the lower_limit is less than or equal to the user's contribution amount. This ensures that the user's contribution amount falls within the lower and upper limits of the policies.
    upper_limit__gte=contribution_amount: This further filters policies where the upper_limit is greater than or equal to the user's contribution amount. This ensures that the user's contribution amount falls within the lower and upper limits of the policies.
    .order_by('upper_limit'): This orders the filtered policies by their upper_limit in ascending order.

    """

    # Check if any policy matches the contribution amount
    if policies.exists():
        # Return the policy with the lowest upper limit greater than or equal to the contribution amount
        return policies.first()
    else:
        # Handle the case where no policy matches the contribution amount
        # You might return a default policy, raise an exception, or return None and handle it in the calling code
        return None

