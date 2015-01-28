# encoding=utf-8
from django.shortcuts import redirect, render
from tvenc.models import RecordedProgram
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return redirect("list_recorded")

@login_required
def list_recorded(request):
    programs = RecordedProgram.objects.all().order_by("-program__start")
    return render(request, "list_recorded.html", {"programs":programs})
