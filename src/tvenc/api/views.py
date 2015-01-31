# encoding=utf-8
import datetime
import json
from django.http.response import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from tvenc.models import RecordedProgram
from django.shortcuts import get_object_or_404
from tvenc.api.forms import GetNewJobForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST"])
def get_newjob(request):

    form = GetNewJobForm(request.POST)
    if not form.is_valid():
        return HttpResponse(json.dumps(form.errors), content_type="application/json", status=400)


    try:
        recorded_program = RecordedProgram.objects.filter(status=RecordedProgram.STATUS_NEW)[0]
    except IndexError:
        raise Http404

    recorded_program.status = RecordedProgram.STATUS_ENCODING
    recorded_program.start_encode = datetime.datetime.now()
    recorded_program.worker = form.cleaned_data["worker"]
    recorded_program.save()

    url = "/recorded{0}/{1}".format(recorded_program.server.mountpoint, recorded_program.filename)

    data = {
            "id":recorded_program.id,
            "filename":recorded_program.filename,
            "url":url,
            }
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
@require_http_methods(["POST"])
def update_status(request, id):
    recorded_program = get_object_or_404(RecordedProgram, id=id, status=RecordedProgram.STATUS_ENCODING)
    result = request.POST.get("result", None)

    if not result:
        return HttpResponse("Invalid option 'result'", status=400)

    recorded_program.end_encode = datetime.datetime.now()
    if result == "ok":
        recorded_program.status = RecordedProgram.STATUS_ENCODED
    elif result == "cancel":
        recorded_program.status = RecordedProgram.STATUS_NEW
        recorded_program.worker = ""
    else:
        recorded_program.status = RecordedProgram.STATUS_ENCODE_ERROR
    recorded_program.save()

    return HttpResponse("OK")




