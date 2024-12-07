"""Views of PagesApp."""
from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'PagesApp/about.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['is_admin'] = self.request.user.groups.filter(
            name__in=['admin']
        ).exists()

        return context


class RulesView(TemplateView):
    template_name = 'PagesApp/rules.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['is_admin'] = self.request.user.groups.filter(
            name__in=['admin']
        ).exists()

        return context


class IndexView(TemplateView):
    template_name = 'PagesApp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['is_admin'] = self.request.user.groups.filter(
            name__in=['admin']
        ).exists()

        return context


def page_403(request, reason=""):
    """Custom 403 page."""
    return render(request, 'PagesApp/403csrf.html', status=403)


def page_404(request, exception):
    """Custom 404 page."""
    return render(request, 'PagesApp/404.html', status=404)


def page_500(request):
    """Custom 500 page."""
    return render(request, 'PagesApp/500.html', status=500)
