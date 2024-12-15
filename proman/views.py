
from django.conf import settings
import os
from django.http import Http404, FileResponse

def private_files_view(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    raise Http404