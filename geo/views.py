from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import GlobalMarket, Country, Region, Channel, Outlet
from .forms import GlobalMarketForm, CountryForm, RegionForm, ChannelForm, OutletForm
from core.validation import OutletValidator


# ============================================================================
# GlobalMarket Views
# ============================================================================

class GlobalMarketListView(LoginRequiredMixin, ListView):
    model = GlobalMarket
    template_name = 'geo/globalmarket_list.html'
    context_object_name = 'globalmarkets'
    paginate_by = 25


class GlobalMarketDetailView(LoginRequiredMixin, DetailView):
    model = GlobalMarket
    template_name = 'geo/globalmarket_detail.html'
    context_object_name = 'globalmarket'

    def get_queryset(self):
        return GlobalMarket.objects.prefetch_related('countries')


class GlobalMarketCreateView(LoginRequiredMixin, CreateView):
    model = GlobalMarket
    template_name = 'geo/globalmarket_form.html'
    form_class = GlobalMarketForm
    success_url = reverse_lazy('geo:globalmarket_list')

    def form_valid(self, form):
        messages.success(self.request, f'Global Market "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class GlobalMarketUpdateView(LoginRequiredMixin, UpdateView):
    model = GlobalMarket
    template_name = 'geo/globalmarket_form.html'
    form_class = GlobalMarketForm
    success_url = reverse_lazy('geo:globalmarket_list')

    def form_valid(self, form):
        messages.success(self.request, f'Global Market "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class GlobalMarketDeleteView(LoginRequiredMixin, DeleteView):
    model = GlobalMarket
    template_name = 'geo/globalmarket_confirm_delete.html'
    success_url = reverse_lazy('geo:globalmarket_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Global Market "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Country Views
# ============================================================================

class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'geo/country_list.html'
    context_object_name = 'countries'
    paginate_by = 25

    def get_queryset(self):
        return Country.objects.select_related('global_market')


class CountryDetailView(LoginRequiredMixin, DetailView):
    model = Country
    template_name = 'geo/country_detail.html'
    context_object_name = 'country'

    def get_queryset(self):
        return Country.objects.select_related('global_market').prefetch_related('regions')


class CountryCreateView(LoginRequiredMixin, CreateView):
    model = Country
    template_name = 'geo/country_form.html'
    form_class = CountryForm
    success_url = reverse_lazy('geo:country_list')

    def form_valid(self, form):
        messages.success(self.request, f'Country "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class CountryUpdateView(LoginRequiredMixin, UpdateView):
    model = Country
    template_name = 'geo/country_form.html'
    form_class = CountryForm
    success_url = reverse_lazy('geo:country_list')

    def form_valid(self, form):
        messages.success(self.request, f'Country "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    model = Country
    template_name = 'geo/country_confirm_delete.html'
    success_url = reverse_lazy('geo:country_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Country "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Region Views
# ============================================================================

class RegionListView(LoginRequiredMixin, ListView):
    model = Region
    template_name = 'geo/region_list.html'
    context_object_name = 'regions'
    paginate_by = 25

    def get_queryset(self):
        return Region.objects.select_related('country', 'country__global_market')


class RegionDetailView(LoginRequiredMixin, DetailView):
    model = Region
    template_name = 'geo/region_detail.html'
    context_object_name = 'region'

    def get_queryset(self):
        return Region.objects.select_related('country', 'country__global_market').prefetch_related('channels')


class RegionCreateView(LoginRequiredMixin, CreateView):
    model = Region
    template_name = 'geo/region_form.html'
    form_class = RegionForm
    success_url = reverse_lazy('geo:region_list')

    def form_valid(self, form):
        messages.success(self.request, f'Region "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class RegionUpdateView(LoginRequiredMixin, UpdateView):
    model = Region
    template_name = 'geo/region_form.html'
    form_class = RegionForm
    success_url = reverse_lazy('geo:region_list')

    def form_valid(self, form):
        messages.success(self.request, f'Region "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class RegionDeleteView(LoginRequiredMixin, DeleteView):
    model = Region
    template_name = 'geo/region_confirm_delete.html'
    success_url = reverse_lazy('geo:region_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Region "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Channel Views
# ============================================================================

class ChannelListView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = 'geo/channel_list.html'
    context_object_name = 'channels'
    paginate_by = 25

    def get_queryset(self):
        return Channel.objects.select_related('region', 'region__country')


class ChannelDetailView(LoginRequiredMixin, DetailView):
    model = Channel
    template_name = 'geo/channel_detail.html'
    context_object_name = 'channel'

    def get_queryset(self):
        return Channel.objects.select_related('region', 'region__country').prefetch_related('outlets')


class ChannelCreateView(LoginRequiredMixin, CreateView):
    model = Channel
    template_name = 'geo/channel_form.html'
    form_class = ChannelForm
    success_url = reverse_lazy('geo:channel_list')

    def form_valid(self, form):
        messages.success(self.request, f'Channel "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class ChannelUpdateView(LoginRequiredMixin, UpdateView):
    model = Channel
    template_name = 'geo/channel_form.html'
    form_class = ChannelForm
    success_url = reverse_lazy('geo:channel_list')

    def form_valid(self, form):
        messages.success(self.request, f'Channel "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class ChannelDeleteView(LoginRequiredMixin, DeleteView):
    model = Channel
    template_name = 'geo/channel_confirm_delete.html'
    success_url = reverse_lazy('geo:channel_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Channel "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Outlet Views
# ============================================================================

class OutletListView(LoginRequiredMixin, ListView):
    model = Outlet
    template_name = 'geo/outlet_list.html'
    context_object_name = 'outlets'
    paginate_by = 25

    def get_queryset(self):
        return Outlet.objects.select_related('channel', 'channel__region', 'channel__region__country')


class OutletDetailView(LoginRequiredMixin, DetailView):
    model = Outlet
    template_name = 'geo/outlet_detail.html'
    context_object_name = 'outlet'

    def get_queryset(self):
        return Outlet.objects.select_related('channel', 'channel__region', 'channel__region__country')


class OutletCreateView(LoginRequiredMixin, CreateView):
    model = Outlet
    template_name = 'geo/outlet_form.html'
    form_class = OutletForm
    success_url = reverse_lazy('geo:outlet_list')

    def form_valid(self, form):
        # Run validation before saving
        validator = OutletValidator()
        is_valid, validation_messages = validator.validate(form.instance)

        # Display validation messages
        for msg in validation_messages:
            if msg.level == 'error':
                messages.error(self.request, f"{msg.field}: {msg.message}")
            elif msg.level == 'warning':
                messages.warning(self.request, f"{msg.field}: {msg.message}")
            elif msg.level == 'info':
                messages.info(self.request, f"{msg.field}: {msg.message}")

        # If there are errors, return to form
        if not is_valid:
            return self.form_invalid(form)

        messages.success(self.request, f'Точка продаж "{form.instance.name}" создана успешно.')
        return super().form_valid(form)


class OutletUpdateView(LoginRequiredMixin, UpdateView):
    model = Outlet
    template_name = 'geo/outlet_form.html'
    form_class = OutletForm
    success_url = reverse_lazy('geo:outlet_list')

    def form_valid(self, form):
        # Run validation before saving
        validator = OutletValidator()
        is_valid, validation_messages = validator.validate(form.instance)

        # Display validation messages
        for msg in validation_messages:
            if msg.level == 'error':
                messages.error(self.request, f"{msg.field}: {msg.message}")
            elif msg.level == 'warning':
                messages.warning(self.request, f"{msg.field}: {msg.message}")
            elif msg.level == 'info':
                messages.info(self.request, f"{msg.field}: {msg.message}")

        # If there are errors, return to form
        if not is_valid:
            return self.form_invalid(form)

        messages.success(self.request, f'Точка продаж "{form.instance.name}" обновлена успешно.')
        return super().form_valid(form)


class OutletDeleteView(LoginRequiredMixin, DeleteView):
    model = Outlet
    template_name = 'geo/outlet_confirm_delete.html'
    success_url = reverse_lazy('geo:outlet_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Outlet "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


class OutletQuickAddView(LoginRequiredMixin, CreateView):
    """
    Mobile-optimized quick outlet registration for field staff.
    Minimal form with photo upload (GPS removed for simplicity).
    """
    model = Outlet
    template_name = 'geo/outlet_quick_add.html'
    fields = ['name', 'address', 'contact_phone', 'channel', 'photo']
    success_url = reverse_lazy('visits:my_visits')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all channels for dropdown (sorted by region)
        context['channels'] = Channel.objects.select_related('region', 'region__country').all()
        return context

    def form_valid(self, form):
        # Auto-generate code from name if empty
        if not form.instance.code:
            import re
            name_slug = re.sub(r'[^\w\s-]', '', form.instance.name.lower())
            name_slug = re.sub(r'[-\s]+', '_', name_slug)
            form.instance.code = name_slug[:50]

        # Set status to pending review
        form.instance.status = Outlet.STATUS_INACTIVE
        form.instance.settings = {'pending_approval': True, 'created_by_field_staff': True}

        messages.success(
            self.request,
            f'Магазин "{form.instance.name}" добавлен! Визит можно начинать после модерации.'
        )
        return super().form_valid(form)
