from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Company

class CompanyListView(ListView):
    model = Company
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Company.objects.filter(name__icontains=query)
        return Company.objects.all()

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/company_detail.html'

class CompanyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Company
    fields = ['name', 'logo', 'website', 'description', 'location', 'industry', 'min_cgpa', 'required_skills', 'recruitment_drive_date', 'ctc_range', 'active_hiring']
    template_name = 'companies/company_form.html'
    success_url = reverse_lazy('company_list')

    def test_func(self):
        return self.request.user.role == 'ADMIN'

class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    fields = ['name', 'logo', 'description', 'location', 'active_hiring', 'recruitment_drive_date']
    template_name = 'companies/company_form.html'
    success_url = reverse_lazy('company_list')

    def test_func(self):
        return self.request.user.role == 'ADMIN'
