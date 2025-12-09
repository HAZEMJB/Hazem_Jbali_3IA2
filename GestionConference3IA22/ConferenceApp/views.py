from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Conference
from .forms import ConferenceForm


# Liste des conférences
class ConferenceList(ListView):
    model = Conference
    context_object_name = "liste"
    template_name = "conferences/liste.html"


# Détails d'une conférence
class ConferenceDetails(DetailView):
    model = Conference
    context_object_name = "conference"
    template_name = "conferences/details.html"


# Création d'une nouvelle conférence
class ConferenceCreate(CreateView):
    model = Conference
    form_class = ConferenceForm
    template_name = "conferences/form.html"
    success_url = reverse_lazy("liste_conferences")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer une nouvelle conférence"
        context["btn"] = "Enregistrer"
        return context



# Modification d'une conférence existante
class ConferenceUpdate(UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = "conferences/form.html"
    success_url = reverse_lazy("liste_conferences")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Modifier la conférence"
        context["btn"] = "Mettre à jour"
        return context


# Suppression d'une conférence
class ConferenceDelete(DeleteView):
    model = Conference
    template_name = "conferences/delete_confirm.html"
    success_url = reverse_lazy("liste_conferences")
