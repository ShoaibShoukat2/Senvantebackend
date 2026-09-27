import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Inquiry


@require_GET
def health(request):
    return JsonResponse({"status": "ok", "service": "senvante-api"})


@csrf_exempt
@require_POST
def create_inquiry(request):
    try:
        payload = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Send a JSON note."}, status=400)

    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    company_name = str(payload.get("company", "")).strip()
    project = str(payload.get("project", "")).strip()
    message = str(payload.get("message", "")).strip()

    errors = {}
    if not name:
        errors["name"] = "Please add your name."
    try:
        validate_email(email)
    except ValidationError:
        errors["email"] = "Use a valid email so we can reply."
    if not project:
        errors["project"] = "Choose a starting point."
    if len(message) < 12:
        errors["message"] = "A sentence or two is enough to begin."

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    inquiry = Inquiry.objects.create(
        name=name[:120],
        email=email[:254],
        company=company_name[:160],
        project=project[:80],
        message=message,
    )
    return JsonResponse(
        {"id": inquiry.id, "detail": "Received. The Senvante team will reply."},
        status=201,
    )
