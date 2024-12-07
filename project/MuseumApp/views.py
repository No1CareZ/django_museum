"""Views of MuseumApp."""
from django.shortcuts import (
    render, redirect,
    get_object_or_404
)
from django.http import Http404
from django.db.models import Count
from django.views.generic import (
    DetailView, ListView,
    CreateView, DeleteView, UpdateView
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Exposition, Exhibit, User
from .forms import ProfileEditForm
# Create your views here.


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class FloorListView(ListView):

    template_name = 'MuseumApp/floor.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        """Will be loaded 5th.\n"""

        selected_floor = self.kwargs['floor_level']
        user = self.request.user
        possible = user.groups.filter(name__in=['admin']).exists()

        if selected_floor in [-1, 0] and not possible:
            """Acctualy it exist but they are not allowed to visit it.\n"""
            raise Http404(f"Данный этаж ({selected_floor}) не существует")

        if selected_floor not in Exposition.POSITION_CHOICES.keys():
            raise Http404("Данный этаж не существует")

        page_obj = Exposition.objects.filter(
            position=selected_floor,
            on_restoration=False,
            open=True
        ).annotate(exibits_count=Count("exhibit"))

        return page_obj

    def get_context_data(self, *args, **kwargs):
        """Will be loaded 7th. So there is no actual need to check floor\n
         existence second time\n"""

        context = super().get_context_data(*args, **kwargs)

        context['floor_level'] = Exposition.POSITION_CHOICES[
            self.kwargs['floor_level']
        ]
        context['is_admin'] = self.request.user.groups.filter(
            name__in=['admin']
        ).exists()

        return context


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ExpositionListView(ListView):

    template_name = 'MuseumApp/exposition.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        """Will be loaded 5th.\n"""

        user = self.request.user
        possible = user.groups.filter(name__in=['admin']).exists()

        selected_exp = get_object_or_404(
            Exposition,
            pk=self.kwargs['exposition_pk']
        )

        if not selected_exp.open and not possible:
            raise Http404(f"""Данная экспозиция ({selected_exp.pk})
                не существует""")

        page_obj = selected_exp.exhibit.all()

        return page_obj

    def get_context_data(self, *args, **kwargs):
        """Will be loaded 7th. So there is no actual need to check exposition\n
         existence second time\n"""

        context = super().get_context_data(*args, **kwargs)

        selected_exp = get_object_or_404(
            Exposition,
            pk=self.kwargs['exposition_pk']
        )

        context['exposition'] = selected_exp
        context['is_admin'] = self.request.user.groups.filter(
            name__in=['admin']
        ).exists()

        return context


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ExpositionCreationView(CreateView):
    model = Exposition
    fields = [
        "title",
        "description",
        "position",
        "on_restoration",
        "open"
    ]

    def get_context_data(self, **kwargs):

        user = self.request.user
        possible = user.groups.filter(name__in=['admin']).exists()

        if not possible:
            raise Http404("Данная страница не существует")

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return redirect('museum:exposition', exposition_pk=self.object.pk)


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ExpositionUpdateView(UpdateView):
    model = Exposition
    pk_url_kwarg = 'exposition_pk'
    fields = [
        "title",
        "description",
        "position",
        "on_restoration",
        "open"
    ]

    def get_context_data(self, **kwargs):

        user = self.request.user
        possible = user.groups.filter(name__in=['admin']).exists()

        if not possible:
            raise Http404("Данная страница не существует")

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return redirect('museum:exposition', exposition_pk=self.object.pk)


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ExpositionDeleteView(DeleteView):
    model = Exposition
    pk_url_kwarg = 'exposition_pk'
    fields = [
        "title",
        "description",
        "position",
        "on_restoration",
        "open"
    ]

    def get_context_data(self, **kwargs):

        user = self.request.user
        possible = user.groups.filter(name__in=['admin']).exists()

        if not possible:
            raise Http404("Данная страница не существует")

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        floor = self.object.position

        self.object.delete()

        return redirect('museum:floor', floor_level=floor)


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ExhibitView(DetailView):

    model = Exhibit
    template_name = 'MuseumApp/exhibit.html'
    pk_url_kwarg = 'exhibit_pk'

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)

        selected_exh = get_object_or_404(
            Exhibit,
            pk=self.kwargs['exhibit_pk']
        )

        context['exhibit'] = selected_exh
        context['is_admin'] = self.request.user.groups.filter(
            name__in=['admin']
        ).exists()

        return context


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ExhibitCreationView(CreateView):
    model = Exhibit
    fields = [
        "title",
        "description",
        "placement",
        "image"
    ]

    def get_context_data(self, **kwargs):

        user = self.request.user
        possible = user.groups.filter(name__in=['admin']).exists()

        if not possible:
            raise Http404("Данная страница не существует")

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return redirect('museum:exhibit', exhibit_pk=self.object.pk)


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ExhibitUpdateView(UpdateView):
    model = Exhibit
    pk_url_kwarg = 'exhibit_pk'
    fields = [
        "title",
        "description",
        "placement",
        "image"
    ]

    def get_context_data(self, **kwargs):

        user = self.request.user
        possible = user.groups.filter(name__in=['admin']).exists()

        if not possible:
            raise Http404("Данная страница не существует")

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return redirect('museum:exhibit', exhibit_pk=self.object.pk)


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ExhibitDeleteView(DeleteView):
    model = Exhibit
    pk_url_kwarg = 'exhibit_pk'
    fields = [
        "title",
        "description",
        "placement",
        "image"
    ]

    def get_context_data(self, **kwargs):

        user = self.request.user
        possible = user.groups.filter(name__in=['admin']).exists()

        if not possible:
            raise Http404("Данная страница не существует")

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        exposition = self.object.placement

        self.object.delete()

        return redirect('museum:exposition', exposition_pk=exposition.pk)


@method_decorator(login_required(login_url='/auth/login/'), name="dispatch")
class ProfileView(DetailView):
    model = User
    template_name = 'MuseumApp/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)

        context['is_admin'] = context['object'].groups.filter(
            name__in=['admin']
        ).exists()

        return context


@login_required(login_url='/auth/login/')
def edit_profile(request):
    """Profile view."""
    profile = request.user
    form = ProfileEditForm(
        request.POST,
        instance=profile
    )
    context = {
        'profile': profile,
        'form': form,
    }
    if form.is_valid():
        new_info = form.save(commit=False)
        profile.first_name = new_info.first_name
        profile.last_name = new_info.last_name
        profile.email = new_info.email
        profile.username = new_info.username
        profile.save()
        return redirect('museum:profile', profile.username)

    return render(request, 'MuseumApp/user.html', context)
