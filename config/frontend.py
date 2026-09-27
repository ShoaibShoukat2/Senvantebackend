from pathlib import Path

from django.http import FileResponse, Http404, HttpResponse

DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"


def spa(request, path=""):
    dist = DIST.resolve()
    index = dist / "index.html"
    if not index.is_file():
        return HttpResponse(
            "The website build is missing. From the frontend folder, run npm run build.",
            status=503,
            content_type="text/plain",
        )

    if path:
        target = (dist / path).resolve()
        try:
            target.relative_to(dist)
        except ValueError:
            raise Http404
        if target.is_file():
            return FileResponse(target.open("rb"))
        if "." in Path(path).name:
            raise Http404

    return FileResponse(index.open("rb"))
