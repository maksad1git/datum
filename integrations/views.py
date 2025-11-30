from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import ImportJob, ExportJob, Backup
from .forms import ImportJobForm, ExportJobForm, BackupForm


# ============================================================================
# ImportJob Views
# ============================================================================

class ImportJobListView(LoginRequiredMixin, ListView):
    model = ImportJob
    template_name = 'integrations/importjob_list.html'
    context_object_name = 'importjobs'
    paginate_by = 25

    def get_queryset(self):
        return ImportJob.objects.select_related('created_by')


class ImportJobDetailView(LoginRequiredMixin, DetailView):
    model = ImportJob
    template_name = 'integrations/importjob_detail.html'
    context_object_name = 'importjob'

    def get_queryset(self):
        return ImportJob.objects.select_related('created_by')


class ImportJobCreateView(LoginRequiredMixin, CreateView):
    model = ImportJob
    template_name = 'integrations/importjob_form.html'
    form_class = ImportJobForm
    success_url = reverse_lazy('integrations:importjob_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Import Job "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class ImportJobUpdateView(LoginRequiredMixin, UpdateView):
    model = ImportJob
    template_name = 'integrations/importjob_form.html'
    form_class = ImportJobForm
    success_url = reverse_lazy('integrations:importjob_list')

    def form_valid(self, form):
        messages.success(self.request, f'Import Job "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class ImportJobDeleteView(LoginRequiredMixin, DeleteView):
    model = ImportJob
    template_name = 'integrations/importjob_confirm_delete.html'
    success_url = reverse_lazy('integrations:importjob_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Import Job "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# ExportJob Views
# ============================================================================

class ExportJobListView(LoginRequiredMixin, ListView):
    model = ExportJob
    template_name = 'integrations/exportjob_list.html'
    context_object_name = 'exportjobs'
    paginate_by = 25

    def get_queryset(self):
        return ExportJob.objects.select_related('created_by')


class ExportJobDetailView(LoginRequiredMixin, DetailView):
    model = ExportJob
    template_name = 'integrations/exportjob_detail.html'
    context_object_name = 'exportjob'

    def get_queryset(self):
        return ExportJob.objects.select_related('created_by')


class ExportJobCreateView(LoginRequiredMixin, CreateView):
    model = ExportJob
    template_name = 'integrations/exportjob_form.html'
    form_class = ExportJobForm
    success_url = reverse_lazy('integrations:exportjob_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Export Job "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class ExportJobUpdateView(LoginRequiredMixin, UpdateView):
    model = ExportJob
    template_name = 'integrations/exportjob_form.html'
    form_class = ExportJobForm
    success_url = reverse_lazy('integrations:exportjob_list')

    def form_valid(self, form):
        messages.success(self.request, f'Export Job "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class ExportJobDeleteView(LoginRequiredMixin, DeleteView):
    model = ExportJob
    template_name = 'integrations/exportjob_confirm_delete.html'
    success_url = reverse_lazy('integrations:exportjob_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Export Job "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Backup Views
# ============================================================================

class BackupListView(LoginRequiredMixin, ListView):
    model = Backup
    template_name = 'integrations/backup_list.html'
    context_object_name = 'backups'
    paginate_by = 25

    def get_queryset(self):
        return Backup.objects.select_related('created_by', 'restored_by')


class BackupDetailView(LoginRequiredMixin, DetailView):
    model = Backup
    template_name = 'integrations/backup_detail.html'
    context_object_name = 'backup'

    def get_queryset(self):
        return Backup.objects.select_related('created_by', 'restored_by')


class BackupCreateView(LoginRequiredMixin, CreateView):
    model = Backup
    template_name = 'integrations/backup_form.html'
    form_class = BackupForm
    success_url = reverse_lazy('integrations:backup_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Backup "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class BackupUpdateView(LoginRequiredMixin, UpdateView):
    model = Backup
    template_name = 'integrations/backup_form.html'
    form_class = BackupForm
    success_url = reverse_lazy('integrations:backup_list')

    def form_valid(self, form):
        messages.success(self.request, f'Backup "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class BackupDeleteView(LoginRequiredMixin, DeleteView):
    model = Backup
    template_name = 'integrations/backup_confirm_delete.html'
    success_url = reverse_lazy('integrations:backup_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Backup "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)
