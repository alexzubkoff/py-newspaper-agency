from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RedactorCreationForm, RedactorExperienceUpdateForm, NewspaperForm
from django.db.models import Q

from newspaper.models import Redactor, Newspaper, Topic


@login_required
def index(request):
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "newspaper/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "newspaper/topic_list.html"
    paginate_by = 5


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newspaper:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 5
    queryset = Newspaper.objects.select_related("topic")


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspaper:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorExperienceUpdateForm
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("")


@login_required
def toggle_assign_to_newspaper(request, pk):
    redactor = Redactor.objects.get(id=request.user.id)
    if (
        Newspaper.objects.get(id=pk) in Redactor.newspapers.all()
    ):  # probably could check if Newspaper exists
        redactor.newspapers.remove(pk)
    else:
        redactor.newspapers.add(pk)
    return HttpResponseRedirect(reverse_lazy("newspaper:newspaper-detail", args=[pk]))


def newspapers_search(request):
    search_newspaper = request.GET.get("search")
    if search_newspaper:
        newspaper_list = Newspaper.objects.filter(
            Q(title__icontains=search_newspaper)
            | Q(published_date__contains=search_newspaper)
        )
    else:
        newspaper_list = Newspaper.objects.all().order_by("title")

    context = {
        "newspaper_list": newspaper_list
    }
    return render(request, "newspaper/newspaper_list.html", context=context)


def redactors_search(request):
    redactors_searching = request.GET.get("search")
    if redactors_searching:
        redactor_list = Redactor.objects.filter(
            Q(username__icontains=redactors_searching)
        )
    else:
        redactor_list = Redactor.objects.all().order_by("username")

    context = {
        "redactor_list": redactor_list
    }
    return render(request, "newspaper/redactor_list.html", context=context)


def topics_search(request):
    topics_searching = request.GET.get("search")
    if topics_searching:
        topic_list = Topic.objects.filter(
            Q(name__icontains=topics_searching)
        )
    else:
        topic_list = Topic.objects.all().order_by("name")

    context = {
        "topic_list": topic_list
    }
    return render(request, "newspaper/topic_list.html", context=context)
