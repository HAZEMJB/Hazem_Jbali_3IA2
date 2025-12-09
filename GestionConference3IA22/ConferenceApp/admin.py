from django.contrib import admin
from .models import Conference, Submission

# Personnalisation du site admin
admin.site.site_header = "Gestion des conférences"
admin.site.site_title = "Gestion des conférences 25/26"
admin.site.index_title = "Bienvenue dans Django App Conference"


# Inline pour les soumissions liées à une conférence
class SubmissionInline(admin.StackedInline):
    model = Submission
    extra = 1
    readonly_fields = ('submission_date',)
    can_delete = False


@admin.register(Conference)
class AdminConferenceModel(admin.ModelAdmin):
    list_display = ('name', 'theme', 'start_date', 'end_date', 'location', 'A')
    ordering = ('-start_date',)
    list_filter = ('theme', 'start_date')
    search_fields = ('name', 'description', 'location')
    date_hierarchy = 'start_date'

    fieldsets = (
        ("Informations générales", {
            'fields': ('conference_id', 'name', 'theme', 'description')
        }),
        ("Informations logistiques", {
            'fields': ('start_date', 'location', 'end_date')
        })
    )
    readonly_fields = ('conference_id',)

    def A(self, objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date - objet.start_date).days
        return "RAS"
    A.short_description = "Durée (en jours)"

    inlines = [SubmissionInline]


# Actions personnalisées
@admin.action(description="Marquer les soumissions comme payées")
def mark_as_payed(modeladmin, req, queryset):
    queryset.update(payed=True)


@admin.action(description="Marquer comme acceptées")
def mark_as_accepted(m, rq, q):
    q.update(status="accepted")


# Admin Submission
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "status","user", "payed", "submission_date")
    fieldsets = (
        ("Informations générales", {
            "fields": ("title", "abstract", "keywords")
        }),
        ("Document", {
            "fields": ("paper", "user", "conference")
        }),
        ("Statut", {
            "fields": ("status", "payed")
        })
    )
    actions = [mark_as_payed, mark_as_accepted]
