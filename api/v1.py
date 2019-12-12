from django.http import JsonResponse

def api_test(**args):
    print(args)
    return JsonResponse({ "data": "response from python api_test(**args)", "args": args }, status=200)

def test_get(**args):
    return JsonResponse({ "data": "response from python test_get(**args)" }, status=200)

def dump_args(**args):
    return JsonResponse({ "data": "response from python dump_args(**args)" }, status=200)

#-------------------------------------------------------------------------------
# ACCOUNTS
#-------------------------------------------------------------------------------

def set_phone_number(**args):
    return JsonResponse({ "data": "response from python set_phone_number(**args)" }, status=200)

def verify(**args):
    return JsonResponse({ "data": "response from python verify(**args)" }, status=200)

def profile(**args):
    return JsonResponse({ "data": "response from python profile(**args)" }, status=200)

def set_profile(**args):
    return JsonResponse({ "data": "response from python set_profile(**args)" }, status=200)

def trusted_contacts(**args):
    return JsonResponse({ "data": "response from python trusted_contacts(**args)" }, status=200)

def add_trusted_contact(**args):
    return JsonResponse({ "data": "response from python add_trusted_contact(**args)" }, status=200)

def remove_trusted_contact(**args):
    return JsonResponse({ "data": "response from python remove_trusted_contact(**args)" }, status=200)

def past_rides(**args):
    return JsonResponse({ "data": "response from python past_rides(**args)" }, status=200)

#-------------------------------------------------------------------------------
# SESSION
#-------------------------------------------------------------------------------

def log_out(**args):
    return JsonResponse({ "data": "response from python log_out(**args)" }, status=200)

def unregister(**args):
    return JsonResponse({ "data": "response from python unregister(**args)" }, status=200)

#-------------------------------------------------------------------------------
# PAYMENTS 
#-------------------------------------------------------------------------------

def set_paypal(**args):
    return JsonResponse({ "data": "response from python set_paypal(**args)" }, status=200)

def set_apple_pay(**args):
    return JsonResponse({ "data": "response from python set_apple_pay(**args)" }, status=200)

def set_credit_card(**args):
    return JsonResponse({ "data": "response from python set_credit_card(**args)" }, status=200)

def set_email_address(**args):
    return JsonResponse({ "data": "response from python set_email_address(**args)" }, status=200)

def add_tax_reciept_request(**args):
    return JsonResponse({ "data": "response from python add_tax_reciept_request(**args)" }, status=200)

def add_one_time_donation(**args):
    return JsonResponse({ "data": "response from python add_one_time_donation(**args)" }, status=200)

def add_paypal_donation(**args):
    return JsonResponse({ "data": "response from python add_paypal_donation(**args)" }, status=200)

def add_credit_card_donation(**args):
    return JsonResponse({ "data": "response from python add_credit_card_donation(**args)" }, status=200)

#-------------------------------------------------------------------------------
# SETTINGS
#-------------------------------------------------------------------------------

def settings(**args):
    return JsonResponse({ "data": "response from python settings(**args)" }, status=200)

def set_accessibility_requirement(**args):
    return JsonResponse({ "data": "response from python set_accessibility_requirement(**args)" }, status=200)

def unset_accessibility_requirement(**args):
    return JsonResponse({ "data": "response from python unset_accessibility_requirement(**args)" }, status=200)

#-------------------------------------------------------------------------------
# LOGGING
#-------------------------------------------------------------------------------

def error(**args):
    return JsonResponse({ "data": "response from python error(**args)" }, status=200)

def emercency_assistance_opened(**args):
    return JsonResponse({ "data": "response from python emercency_assistance_opened(**args)" }, status=200)

def emergency_assistance_called(**args):
    return JsonResponse({ "data": "response from python emergency_assistance_called(**args)" }, status=200)

#-------------------------------------------------------------------------------
# RIDESHARE
#-------------------------------------------------------------------------------

def flight_checks(**args):
    return JsonResponse({ "data": "response from python flight_checks(**args)" }, status=200)

def bookmark_locations(**args):
    return JsonResponse({ "data": "response from python bookmark_locations(**args)" }, status=200)

def search_location(**args):
    print(args)
    return {
        "data": "Query result was " + str(args.get("query"))
    }

def ride_status(**args):
    return JsonResponse({ "data": "response from python ride_status(**args)" }, status=200)

def current_location_availibility(**args):
    return JsonResponse({ "data": "response from python current_location_availibility(**args)" }, status=200)

def ride_cost_estimate(**args):
    return JsonResponse({ "data": "response from python ride_cost_estimate(**args)" }, status=200)

def create_ride_request(**args):
    return JsonResponse({ "data": "response from python create_ride_request(**args)" }, status=200)

def cancel_ride_request(**args):
    return JsonResponse({ "data": "response from python cancel_ride_request(**args)" }, status=200)

def set_verification_code(**args):
    return JsonResponse({ "data": "response from python set_verification_code(**args)" }, status=200)

def confirm_verification_code(**args):
    return JsonResponse({ "data": "response from python confirm_verification_code(**args)" }, status=200)

def set_a_driver_tip(**args):
    return JsonResponse({ "data": "response from python set_a_driver_tip(**args)" }, status=200)

def set_pickup_note(**args):
    return JsonResponse({ "data": "response from python set_pickup_note(**args)" }, status=200)

def set_ride_feedback(**args):
    return JsonResponse({ "data": "response from python set_ride_feedback(**args)" }, status=200)

def set_ride_rating(**args):
    return JsonResponse({ "data": "response from python set_ride_rating(**args)" }, status=200)

def add_driver_message(**args):
    return JsonResponse({ "data": "response from python add_driver_message(**args)" }, status=200)
