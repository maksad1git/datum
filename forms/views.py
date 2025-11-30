from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import FormTemplate
from .forms import FormTemplateForm


# ============================================================================
# FormTemplate Views
# ============================================================================

class FormTemplateListView(LoginRequiredMixin, ListView):
    model = FormTemplate
    template_name = 'forms/formtemplate_list.html'
    context_object_name = 'formtemplates'
    paginate_by = 25

    def get_queryset(self):
        return FormTemplate.objects.select_related('created_by', 'parent_version')


class FormTemplateDetailView(LoginRequiredMixin, DetailView):
    model = FormTemplate
    template_name = 'forms/formtemplate_detail.html'
    context_object_name = 'formtemplate'

    def get_queryset(self):
        return FormTemplate.objects.select_related(
            'created_by', 'parent_version'
        ).prefetch_related('applies_to_channels', 'versions', 'visit_types')


class FormTemplateCreateView(LoginRequiredMixin, CreateView):
    model = FormTemplate
    template_name = 'forms/formtemplate_form.html'
    form_class = FormTemplateForm
    success_url = reverse_lazy('forms:formtemplate_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Form Template "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class FormTemplateUpdateView(LoginRequiredMixin, UpdateView):
    model = FormTemplate
    template_name = 'forms/formtemplate_form.html'
    form_class = FormTemplateForm
    success_url = reverse_lazy('forms:formtemplate_list')

    def form_valid(self, form):
        messages.success(self.request, f'Form Template "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class FormTemplateDeleteView(LoginRequiredMixin, DeleteView):
    model = FormTemplate
    template_name = 'forms/formtemplate_confirm_delete.html'
    success_url = reverse_lazy('forms:formtemplate_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Form Template "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)
