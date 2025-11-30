from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Role, User
from .forms import RoleForm, UserForm


# Role Views
class RoleListView(LoginRequiredMixin, ListView):
    model = Role
    template_name = 'users/role_list.html'
    context_object_name = 'object_list'
    paginate_by = 20


class RoleDetailView(LoginRequiredMixin, DetailView):
    model = Role
    template_name = 'users/role_detail.html'


class RoleCreateView(LoginRequiredMixin, CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'users/role_form.html'
    success_url = reverse_lazy('users:role_list')

    def form_valid(self, form):
        messages.success(self.request, 'Роль успешно создана!')
        return super().form_valid(form)


class RoleUpdateView(LoginRequiredMixin, UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'users/role_form.html'
    success_url = reverse_lazy('users:role_list')

    def form_valid(self, form):
        messages.success(self.request, 'Роль успешно обновлена!')
        return super().form_valid(form)


class RoleDeleteView(LoginRequiredMixin, DeleteView):
    model = Role
    template_name = 'users/role_confirm_delete.html'
    success_url = reverse_lazy('users:role_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Роль успешно удалена!')
        return super().delete(request, *args, **kwargs)


# User Views
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.select_related('role').all()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно создан!')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно обновлен!')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Пользователь успешно удален!')
        return super().delete(request, *args, **kwargs)
