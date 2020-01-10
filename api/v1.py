from django.http import JsonResponse
from django.conf import settings as _settings
import googlemaps

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
    user = args["request_user"]

    from rideshare.models import AppUser
    from rideshare.models import Pronoun

    acct_list = AppUser.objects.filter(
        django_account = user
    )
    acct = None
    if acct_list.count() == 0:
        AppUser.objects.create(
            django_account = user,
            username = " ".join([
                user.first_name,
                user.last_name,
            ]),
            pronoun = Pronoun(id=3),
        )
        acct = AppUser.objects.get(
            django_account = user
        )
    else:
        acct = acct_list.first()

    pronouns = {
        res.key: res.display_name for res in Pronoun.objects.all()
    }

    return JsonResponse({
        "profile": {
            "username": acct.username,
            "pronouns": acct.pronoun.key,
            # @TODO "accessibility": "ACCESSIBILITY",
        },
        "options": {
            "pronouns": pronouns,
        },
    }, status=200)

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

def reverse_geocode(**args):
    print(args)
    gmaps = googlemaps.Client(key=_settings.GOOGLE_MAPS_API_KEY)
    location = (args.get("lat"), args.get("lng"))
    result = gmaps.reverse_geocode(location)
    return {
        "formatted_address": result[0]["formatted_address"],
        "place_id": result[0]["place_id"],
    }

def search_suggestions(**args):
    try:
        gmaps = googlemaps.Client(key=_settings.GOOGLE_MAPS_API_KEY)
        location = (args.get("lat"), args.get("lng"))
        query = args.get("query")
        if query is None:
            return []
        if query == "":
            return []
        resp = gmaps.places_autocomplete(
                query, location=location, types='address',
                radius=(1650 * 50), strict_bounds=True)
        import pprint as pp
        pp.pprint(resp);
        addresses = [{
            "address": item.get("description"),
            "place_id": item.get("place_id"),
        } for item in resp]
        return addresses 
    except Exception as ex:
        print("EX:")
        print(str(ex))
        return {}

def location_detail(**args):
    try:
        gmaps = googlemaps.Client(key=_settings.GOOGLE_MAPS_API_KEY)
        resp = gmaps.place(args.get("place_id"))
        import pprint as pp
        pp.pprint(resp)
        result = resp.get("result")
        return {
            "address": result.get("formatted_address"),
            "icon": result.get("icon"),
            "name": result.get("name"),
            "place_id": result.get("place_id"),
            "geometry": result.get("geometry"),
        }
    except Exception as ex:
        print("EX:")
        print(str(ex))
        return {}

def search_location(**args):
    try:
        gmaps = googlemaps.Client(key=_settings.GOOGLE_MAPS_API_KEY)
        location = (args.get("lat"), args.get("lng"))
        resp = gmaps.places_nearby(location,
                keyword=args.get("query"), rank_by="distance")
        api_result = []
        for item in resp["results"]:
            api_result.append({
                "address": item.get("vicinity"),
                "name": item.get("name"),
                "geometry": item.get("geometry"),
                "icon": item.get("icon"),
                "open_now": item.get("opening_hours").get("open_now") if item.get("opening_hours") is not None else None,
                "rating": item.get("rating"),
                "total_reviews": item.get("user_ratings_total"),
                "place_id": item.get("place_id"),
                "types": item.get("types"),
                "price_level": item.get("price_level"),
            })
        import pprint as pp
        pp.pprint(api_result)
        return api_result
    except Exception as ex:
        print("EX:")
        print(str(ex))
        return {}
        """
        result = gmaps.find_place(args.get("query"), "textquery", fields=[
            "formatted_address",
            "geometry",
            "icon",
            "name",
            "permanently_closed",
            "photos",
            "place_id",
            "plus_code",
            "types",
            ],
            location_bias= "point:%s,%s" % (
                args.get("lat"),
                args.get("lng"),
            )
        )
        import pprint as pp
        pp.pprint(result)
        """

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
