import os
import base64
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rowsheet import APIRequest
from rowsheet.APISpec import APISpec

api_spec = APISpec(os.path.join(settings.BASE_DIR, "api"))

def parse_auth_bearer(auth_header):
    if auth_header is None:
        return None

    # Remove "Basic " to isolate credentials.
    encoded_credentials = auth_header.split(' ')[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')

    # Remove the square brackets around username.
    bearer = decoded_credentials[0][1:-1]
    return bearer

def assert_range(value, min_val, max_val):
    if max_val is not None:
        if value > max_val:
            raise ValueError("Value too large (max %s)" % max_val)
    if min_val is not None:
        if value < min_val:
            raise ValueError("Value too small (min %s)" % min_val)

@csrf_exempt
def handle(request, version, service, module, command):

    api_version = api_spec.spec.get(version)
    if api_version is None:
        return JsonResponse({"error": "Unknown API version."}, status=404)
    api_service = api_version.get("services").get(service)
    if api_service is None:
        return JsonResponse({"error": "Unknown API service."}, status=404)
    api_module = api_service.get("modules").get(module)
    if api_module is None:
        return JsonResponse({"error": "Unknown API module."}, status=404)
    api_command = api_module.get("commands").get(command)
    if api_command is None:
        return JsonResponse({"error": "Unknown API command."}, status=404)
    if request.method != api_command.get("method"):
        return JsonResponse({"error":
            "Invalid http method, should be '%s'" % api_command.get("method")},status=400)
    if request.method == "GET":
        raw_args = { key : val for key, val in request.GET.items()}
    if request.method == "POST":
        raw_args = { key : val for key, val in request.POST.items()}
    args = {}
    if api_command.get("params") is not None:
        params = api_command.get("params")
        errors = {}
        for param_name, param in api_command.get("params").items():
            raw_param = raw_args.get(param_name)
            if raw_param is None:
                if param.get("required") == True:
                    if raw_param is None:
                        errors[param_name] = "Parameter required."
                else:
                    args[param_name] = param.get("default")
            else:
                if param.get("type") is not None:
                    param_type = param.get("type")
                    if param_type == "str":
                        try:
                            args[param_name] = str(raw_param)
                        except Exception:
                            errors[param_name] = "Invalid string."
                    else:
                        if param_type == "int":
                            try:
                                value = int(raw_param)
                                assert_range(value, param.get("min"), params.get("max"))
                                args[param_name] = value
                            except Exception as ex:
                                errors[param_name] = "Invalid integer: " + str(ex)
                            except ValueError as ex:
                                errors[param_name] = str(ex)
                        if param_type == "bool":
                            try:
                                if raw_param.lower() in ["0","false","f"]:
                                    args[param_name] = False
                                elif raw_param.lower() in ["1","true","t"]:
                                    args[param_name] = True
                                else:
                                    raise Exception("Invalid bool.")
                            except Exception as ex:
                                errors[param_name] = "Invalid bool."
                        if param_type == "float":
                            try:
                                value = float(raw_param)
                                assert_range(value, param.get("min"), params.get("max"))
                                args[param_name] = value
                            except Exception as ex:
                                errors[param_name] = "Invalid bool."
                            except ValueError as ex:
                                errors[param_name] = str(ex)
                        if param_type == "price":
                            try:
                                value = round(float(raw_param), 2)
                                assert_range(value, param.get("min"), params.get("max"))
                                args[param_name] = value
                            except Exception as ex:
                                errors[param_name] = "Invalid price."
                            except ValueError as ex:
                                errors[param_name] = str(ex)
        if errors != {}:
            return JsonResponse({"error": "Bad request parameters", "errors": errors}, status=400)

    auth_header = request.headers.get('Authorization')
    bearer_token = parse_auth_bearer(auth_header)
    session_valid = request.session.exists(bearer_token)

    if session_valid == False:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    import importlib
    module = importlib.import_module("api.v1")
    method = getattr(module, command)

    return method(**args)
