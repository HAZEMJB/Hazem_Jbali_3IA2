from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView , DetailView , CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def list_conferences(request):
    conferences_list=Conference.objects.all()
    """retour : liste + page """
    return render(request,"conferences/liste.html", {"liste":conferences_list})

class ConferenceList(ListView):
    model=Conference
    context_object_name="liste"
    template_name="conferences/liste.html"

class ConferenceDetails(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="conferences/details.html"

class ConferenceCreate(LoginRequiredMixin,CreateView):
    model= Conference
    template_name ="conferences/form.html"
    #fields = "__all__"
    form_class =ConferenceForm
    success_url = reverse_lazy("liste_conferences")

class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model =Conference
    template_name="conferences/form.html"
    #fields="__all__"
    form_class =ConferenceForm
    success_url=reverse_lazy("liste_conferences")

class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model=Conference
    template_name ="conferences/conference_confirm_delete.html"
    success_url =reverse_lazy("liste_conferences")




# ConferenceApp/views.py
from django.views.generic import ListView, DetailView
from .models import Submission

class ListSubmissions(ListView):
    model = Submission
    context_object_name = 'submissions'
    template_name = 'submissions/list.html'

    def get_queryset(self):
        user = self.request.user
        # Filter submissions for the logged-in user
        return Submission.objects.filter(user=user)
class DetailSubmission(DetailView):
    model = Submission
    context_object_name = 'submission'
    template_name = 'submissions/detail.html'
    pk_url_kwarg = 'submission_id'
from django.http import FileResponse, Http404
import os
from django.conf import settings
from .models import Submission

def download_paper(request, submission_id):
    try:
        submission = Submission.objects.get(submission_id=submission_id)
        file_path = submission.paper.path
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        else:
            raise Http404("File not found.")
    except Submission.DoesNotExist:
        raise Http404("Submission not found.")

from django.contrib import messages


from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Submission

class AddSubmission(CreateView):
    model = Submission
    fields = ["title", "abstract", "keywords", "paper", "conference"]
    template_name = "submissions/add.html"
    success_url = reverse_lazy("list_submissions")

    def form_valid(self, form):
        # Set the current logged-in user
        form.instance.user = self.request.user
        # Set default status
        form.instance.status = "under review"
        response = super().form_valid(form)
        messages.success(self.request, "Submission added successfully and is under review!")
        return response

# ✅ 11. Update submission
class UpdateSubmission(UpdateView):
    model = Submission
    fields = ["title", "abstract", "keywords", "paper"]
    template_name = "submissions/update.html"
    pk_url_kwarg = "submission_id"
    success_url = reverse_lazy("list_submissions")

    def dispatch(self, request, *args, **kwargs):
        submission = self.get_object()
        if submission.status in ["accepted", "rejected"]:
            messages.error(request, "Impossible de modifier une soumission acceptée ou rejetée ❌")
            return redirect("list_submissions")
        if submission.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)