from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView

from ..auth.decorators import management_only
from .forms import TournamentCreateForm
from .models import Tournament


class TournamentListView(ListView):
    model = Tournament
    template_name = "tournaments/previous.html"
    paginate_by = 10
    ordering = ["-start_time"]

    def get_queryset(self):
        return Tournament.objects.finished().order_by(*self.ordering)


def detail(request, tournament_id=None):
    t = Tournament.objects.in_progress()
    t = t[0] if t.exists() else None

    if tournament_id is not None:
        t = get_object_or_404(Tournament, id=tournament_id)

    players = list(enumerate(sorted(t.players.all(), key=lambda x: -x.ranking))) if t is not None else None

    page_obj = None
    if players is not None:
        paginator = Paginator(players, 15)
        page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, "tournaments/detail.html", {"tournament": t, "players": players, "page_obj": page_obj})


@management_only
def create(request):
    if request.method == "POST":
        form = TournamentCreateForm(request.POST)
        if form.is_valid():
            t = form.save()
            messages.success(
                request,
                f"Successfully created tournament! Tournament is scheduled to run at {t.start_time}",
                extra_tags="success",
            )
        else:
            for errors in form.errors.get_json_data().values():
                for error in errors:
                    messages.error(request, error["message"], extra_tags="danger")
    return render(
        request,
        "tournaments/create.html",
        {
            "form": TournamentCreateForm(),
            "in_progress": Tournament.objects.in_progress(),
            "future": Tournament.objects.future(),
        },
    )


@management_only
def management(request, tournament_id=None):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    return HttpResponse(tournament)
