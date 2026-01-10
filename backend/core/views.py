from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Backend is running successfully",
        "documentation": "/api/",
        "admin": "/admin/"
    })
