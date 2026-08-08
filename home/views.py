from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from .models import (
    Project, Technology, Profile, BlogPost,
    Education, WorkExperience, ContactMessage,
)
from .forms import ContactForm


def get_profile():
    """Return the single portfolio profile."""
    profile = Profile.objects.first()
    if profile is None:
        raise Profile.DoesNotExist(
            "No Profile found. Create one in the Django admin."
        )
    return profile


def sort_technologies(queryset):
    return sorted(queryset, key=lambda t: (-t.level_score, t.name))


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_profile()
        tech_qs = Technology.objects.filter(is_hidden=False)

        context.update({
            'profile': profile,
            'technologies_by_category': {
                'language': sort_technologies(
                    tech_qs.filter(category='language', is_featured=True)
                ),
                'framework': sort_technologies(
                    tech_qs.filter(category='framework', is_featured=True)
                ),
                'tool': sort_technologies(
                    tech_qs.filter(category='tool', is_featured=True)
                ),
                'database': sort_technologies(
                    tech_qs.filter(category='database', is_featured=True)
                ),
                'other': sort_technologies(
                    tech_qs.filter(category='other', is_featured=True)
                ),
            },
            'featured_projects': profile.projects.filter(
                is_hidden=False, is_featured=True
            )[:3],
            'education': profile.education.all()[:3],
            'recent_posts': profile.blog_posts.filter(status='published')[:3],
        })
        return context


class PortfolioView(ListView):
    model = Project
    template_name = 'pages/portfolio.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        profile = get_profile()
        queryset = profile.projects.filter(is_hidden=False)

        tech = self.request.GET.get('tech')
        if tech:
            queryset = queryset.filter(technologies__name=tech)

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-priority', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['technologies'] = Technology.objects.filter(
            projects__is_hidden=False
        ).distinct().order_by('name')
        context['status_choices'] = Project.STATUS_CHOICES
        context['active_tech'] = self.request.GET.get('tech', '')
        context['active_status'] = self.request.GET.get('status', '')
        context['profile'] = get_profile()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'pages/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Project.objects.filter(is_hidden=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['related_projects'] = Project.objects.filter(
            technologies__in=project.technologies.all(),
            is_hidden=False,
        ).exclude(id=project.id).distinct()[:3]
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_profile()
        tech_qs = Technology.objects.filter(is_hidden=False)

        context.update({
            'profile': profile,
            'education': profile.education.all(),
            'work_experience': profile.work_experience.all(),
            'technologies_by_category': {
                category: sort_technologies(tech_qs.filter(category=category))
                for category, _ in Technology.CATEGORY_CHOICES
            },
        })
        return context


class ContactView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_profile()
        return context

    def form_valid(self, form):
        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data.get('subject', ''),
            message=form.cleaned_data['message'],
        )

        messages.success(
            self.request,
            'Thank you for your message. I will get back to you soon!',
        )

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Message sent successfully!',
            })

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': form.errors})

        return super().form_invalid(form)


class BlogListView(ListView):
    model = BlogPost
    template_name = 'pages/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(technologies__name__icontains=query)
            ).distinct()

        tech = self.request.GET.get('tech')
        if tech:
            queryset = queryset.filter(technologies__name=tech)

        return queryset.order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['technologies'] = Technology.objects.filter(
            blog_posts__status='published'
        ).distinct().order_by('name')
        context['search_query'] = self.request.GET.get('q', '')
        context['active_tech'] = self.request.GET.get('tech', '')
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'pages/blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context.update({
            'related_posts': BlogPost.objects.filter(
                technologies__in=post.technologies.all(),
                status='published',
            ).exclude(id=post.id).distinct()[:3],
            'recent_posts': BlogPost.objects.filter(
                status='published'
            ).exclude(id=post.id)[:5],
        })
        return context


@require_http_methods(["GET"])
def resume_view(request):
    profile = get_profile()
    return render(request, 'pages/resume.html', {'profile': profile})


def keep_alive(request):
    return HttpResponse("Service is running")


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)
