from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Picture, Category


class PictureList(ListView):
    model = Picture
    context_object_name = 'picture_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class CategoryList(ListView):
    model = Picture

    def get_queryset(self):
        category_list_type = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Picture.objects.filter(category=category_list_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context


class PictureOwnerList(LoginRequiredMixin, ListView):
    model = Picture
    template_name = "pictures/my_picture_list.html"
    context_object_name = 'pics_list'

    def get_queryset(self):
        return Picture.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context


class PictureDetail(DetailView):
    model = Picture
    context_object_name = "pic"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if Picture.objects.filter(user=self.request.user).exists():
                context["download"] = True
        return context


class PictureCreate(LoginRequiredMixin, CreateView):
    model = Picture
    fields = ['title', 'picture', 'description', 'category']
    success_url = reverse_lazy('pics_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PictureUpdate(LoginRequiredMixin, UpdateView):
    model = Picture
    fields = ['title', 'picture', 'description', 'category']
    success_url = reverse_lazy('pics_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            raise Http404("U can't rewrite чужое")
        return super().dispatch(request, *args, **kwargs)




class PictureDelete(LoginRequiredMixin, DeleteView):
    model = Picture
    success_url = reverse_lazy('pics_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            raise Http404("U can't  delete чужое ")
        return super().dispatch(request, *args, **kwargs)
