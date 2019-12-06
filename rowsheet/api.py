from django.http import JsonResponse

def handle(request):
    return JsonResponse({
        "message": "This API Hasn't been implemented yet.",
    })
