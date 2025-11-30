from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
import json

from .models import VisitType, Visit, Observation, VisitMedia
from .forms import VisitTypeForm, VisitForm, ObservationForm, VisitMediaForm
from core.validation import VisitValidator, ObservationValidator


# ============================================================================
# VisitType Views
# ============================================================================

class VisitTypeListView(LoginRequiredMixin, ListView):
    model = VisitType
    template_name = 'visits/visittype_list.html'
    context_object_name = 'visittypes'
    paginate_by = 25

    def get_queryset(self):
        return VisitType.objects.select_related('form_template')


class VisitTypeDetailView(LoginRequiredMixin, DetailView):
    model = VisitType
    template_name = 'visits/visittype_detail.html'
    context_object_name = 'visittype'

    def get_queryset(self):
        return VisitType.objects.select_related('form_template').prefetch_related('coefficients', 'visits')


class VisitTypeCreateView(LoginRequiredMixin, CreateView):
    model = VisitType
    template_name = 'visits/visittype_form.html'
    form_class = VisitTypeForm
    success_url = reverse_lazy('visits:visittype_list')

    def form_valid(self, form):
        messages.success(self.request, f'Visit Type "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class VisitTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = VisitType
    template_name = 'visits/visittype_form.html'
    form_class = VisitTypeForm
    success_url = reverse_lazy('visits:visittype_list')

    def form_valid(self, form):
        messages.success(self.request, f'Visit Type "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class VisitTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = VisitType
    template_name = 'visits/visittype_confirm_delete.html'
    success_url = reverse_lazy('visits:visittype_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Visit Type "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Visit Views
# ============================================================================

class VisitListView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = 'visits/visit_list.html'
    context_object_name = 'visits'
    paginate_by = 25

    def get_queryset(self):
        queryset = Visit.objects.select_related('visit_type', 'outlet', 'user', 'outlet__channel')
        data_source_type = self.request.GET.get('data_source_type')
        if data_source_type in ['MON', 'EXP', 'AI']:
            queryset = queryset.filter(data_source_type=data_source_type)
        return queryset


class VisitDetailView(LoginRequiredMixin, DetailView):
    model = Visit
    template_name = 'visits/visit_detail.html'
    context_object_name = 'visit'

    def get_queryset(self):
        return Visit.objects.select_related(
            'visit_type', 'outlet', 'user',
            'outlet__channel', 'outlet__channel__region'
        ).prefetch_related('observations', 'media')


class VisitCreateView(LoginRequiredMixin, CreateView):
    model = Visit
    template_name = 'visits/visit_form.html'
    form_class = VisitForm
    success_url = reverse_lazy('visits:visit_list')

    def form_valid(self, form):
        # Run validation before saving
        validator = VisitValidator()
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

        # Store validation messages in session for display after redirect
        if validation_messages:
            self.request.session['validation_messages'] = [msg.to_dict() for msg in validation_messages]

        messages.success(self.request, 'Визит создан успешно.')
        return super().form_valid(form)


class VisitUpdateView(LoginRequiredMixin, UpdateView):
    model = Visit
    template_name = 'visits/visit_form.html'
    form_class = VisitForm
    success_url = reverse_lazy('visits:visit_list')

    def form_valid(self, form):
        # Run validation before saving
        validator = VisitValidator()
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

        messages.success(self.request, 'Визит обновлен успешно.')
        return super().form_valid(form)


class VisitDeleteView(LoginRequiredMixin, DeleteView):
    model = Visit
    template_name = 'visits/visit_confirm_delete.html'
    success_url = reverse_lazy('visits:visit_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Visit deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Observation Views
# ============================================================================

class ObservationListView(LoginRequiredMixin, ListView):
    model = Observation
    template_name = 'visits/observation_list.html'
    context_object_name = 'observations'
    paginate_by = 25

    def get_queryset(self):
        return Observation.objects.select_related('visit', 'coefficient', 'product', 'visit__outlet')


class ObservationDetailView(LoginRequiredMixin, DetailView):
    model = Observation
    template_name = 'visits/observation_detail.html'
    context_object_name = 'observation'

    def get_queryset(self):
        return Observation.objects.select_related(
            'visit', 'coefficient', 'product',
            'visit__outlet', 'visit__visit_type'
        ).prefetch_related('media')


class ObservationCreateView(LoginRequiredMixin, CreateView):
    model = Observation
    template_name = 'visits/observation_form.html'
    form_class = ObservationForm
    success_url = reverse_lazy('visits:observation_list')

    def form_valid(self, form):
        # Run validation before saving
        validator = ObservationValidator()
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

        messages.success(self.request, 'Наблюдение создано успешно.')
        return super().form_valid(form)


class ObservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Observation
    template_name = 'visits/observation_form.html'
    form_class = ObservationForm
    success_url = reverse_lazy('visits:observation_list')

    def form_valid(self, form):
        # Run validation before saving
        validator = ObservationValidator()
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

        messages.success(self.request, 'Наблюдение обновлено успешно.')
        return super().form_valid(form)


class ObservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Observation
    template_name = 'visits/observation_confirm_delete.html'
    success_url = reverse_lazy('visits:observation_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Observation deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# VisitMedia Views
# ============================================================================

class VisitMediaListView(LoginRequiredMixin, ListView):
    model = VisitMedia
    template_name = 'visits/visitmedia_list.html'
    context_object_name = 'media_files'
    paginate_by = 25

    def get_queryset(self):
        return VisitMedia.objects.select_related('visit', 'observation', 'visit__outlet')


class VisitMediaDetailView(LoginRequiredMixin, DetailView):
    model = VisitMedia
    template_name = 'visits/visitmedia_detail.html'
    context_object_name = 'media'

    def get_queryset(self):
        return VisitMedia.objects.select_related('visit', 'observation', 'visit__outlet')


class VisitMediaCreateView(LoginRequiredMixin, CreateView):
    model = VisitMedia
    template_name = 'visits/visitmedia_form.html'
    form_class = VisitMediaForm
    success_url = reverse_lazy('visits:visitmedia_list')

    def form_valid(self, form):
        messages.success(self.request, f'Media file uploaded successfully.')
        return super().form_valid(form)


class VisitMediaUpdateView(LoginRequiredMixin, UpdateView):
    model = VisitMedia
    template_name = 'visits/visitmedia_form.html'
    form_class = VisitMediaForm
    success_url = reverse_lazy('visits:visitmedia_list')

    def form_valid(self, form):
        messages.success(self.request, f'Media file updated successfully.')
        return super().form_valid(form)


class VisitMediaDeleteView(LoginRequiredMixin, DeleteView):
    model = VisitMedia
    template_name = 'visits/visitmedia_confirm_delete.html'
    success_url = reverse_lazy('visits:visitmedia_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Media file deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Интерфейс для тайного покупателя
# ============================================================================

@login_required
def my_visits(request):
    """Мои визиты - простой интерфейс для тайного покупателя"""
    visits = Visit.objects.filter(user=request.user).select_related(
        'visit_type', 'outlet', 'outlet__channel'
    ).order_by('-created_at')

    context = {
        'visits': visits,
    }
    return render(request, 'visits/my_visits.html', context)


def is_mobile(request):
    """Определить мобильное устройство по User-Agent"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone']
    return any(keyword in user_agent for keyword in mobile_keywords)


@login_required
def fill_visit(request, pk):
    """Заполнение визита - упрощённый интерфейс"""
    visit = get_object_or_404(Visit, pk=pk, user=request.user)

    # Загрузить форму из VisitType
    form_template = visit.visit_type.form_template

    if request.method == 'POST':
        # Сохранить данные формы
        form_data = {}

        if form_template and form_template.fields_schema:
            for field in form_template.fields_schema:
                field_name = field.get('field_name')
                field_type = field.get('field_type')

                if field_type == 'image':
                    # Обработать загрузку файла
                    file = request.FILES.get(field_name)
                    if file:
                        # Создать VisitMedia
                        media = VisitMedia.objects.create(
                            visit=visit,
                            media_type='photo',
                            file=file,
                            title=field.get('label', field_name)
                        )
                        form_data[field_name] = f"media_{media.id}"
                elif field_type == 'boolean':
                    form_data[field_name] = request.POST.get(field_name) == 'on'
                else:
                    form_data[field_name] = request.POST.get(field_name, '')

        # Сохранить в Visit.form_data
        visit.form_data = form_data

        # Обновить статус если нужно
        if 'start_visit' in request.POST:
            visit.status = Visit.STATUS_IN_PROGRESS
            visit.start_date = timezone.now()
        elif 'complete_visit' in request.POST:
            visit.status = Visit.STATUS_COMPLETED
            visit.end_date = timezone.now()

        visit.save()

        if visit.status == Visit.STATUS_COMPLETED:
            messages.success(request, 'Визит успешно завершён!')
            return redirect('visits:my_visits')
        else:
            messages.success(request, 'Данные сохранены!')

    # Получить коэффициенты для этого типа визита
    coefficients = visit.visit_type.coefficients.filter(is_active=True)

    # Получить существующие наблюдения
    observations = Observation.objects.filter(visit=visit).select_related('coefficient')
    observations_dict = {obs.coefficient_id: obs for obs in observations}

    # Подготовить коэффициенты с их текущими значениями
    coefficients_with_values = []
    for coef in coefficients:
        obs = observations_dict.get(coef.id)
        coef_data = {
            'id': coef.id,
            'name': coef.name,
            'code': coef.code,
            'description': coef.description,
            'value_type': coef.value_type,
            'unit': coef.unit,
            'current_value': None,
        }

        if obs:
            if coef.value_type == 'numeric':
                coef_data['current_value'] = obs.value_numeric
            elif coef.value_type == 'boolean':
                coef_data['current_value'] = obs.value_boolean
            elif coef.value_type == 'text':
                coef_data['current_value'] = obs.value_text

        coefficients_with_values.append(coef_data)

    # Подготовить поля формы с текущими значениями
    fields_with_values = []
    if form_template and form_template.fields_schema:
        for field in form_template.fields_schema:
            field_data = dict(field)  # Копировать данные поля
            # Получить текущее значение из visit.form_data
            field_id = field.get('id')
            if visit.form_data and field_id in visit.form_data:
                field_data['current_value'] = visit.form_data.get(field_id)
            else:
                field_data['current_value'] = None
            fields_with_values.append(field_data)

    context = {
        'visit': visit,
        'form_template': form_template,
        'fields_with_values': fields_with_values,
        'coefficients': coefficients_with_values,
        'observations_dict': observations_dict,
    }

    # Использовать мобильный шаблон для мобильных устройств
    template = 'visits/fill_visit_mobile.html' if is_mobile(request) else 'visits/fill_visit.html'
    return render(request, template, context)


# ============================================================================
# API для Background Sync
# ============================================================================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
@require_http_methods(["POST"])
def sync_visit_api(request):
    """
    API endpoint для синхронизации визитов из оффлайн режима.
    Используется Service Worker Background Sync API.
    """
    try:
        # Проверить аутентификацию
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)

        # Парсить данные
        data = json.loads(request.body.decode('utf-8'))

        visit_id = data.get('visit_id')
        form_data = data.get('form_data', {})
        observations = data.get('observations', {})
        notes = data.get('notes', '')

        if not visit_id:
            return JsonResponse({
                'success': False,
                'error': 'visit_id is required'
            }, status=400)

        # Получить визит
        try:
            visit = Visit.objects.get(pk=visit_id, user=request.user)
        except Visit.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Visit not found or access denied'
            }, status=404)

        # Обновить данные визита
        if form_data:
            visit.form_data = form_data

        if notes:
            visit.notes = notes

        visit.save()

        # Сохранить наблюдения
        saved_observations = []
        for coef_id, value in observations.items():
            try:
                from coefficients.models import Coefficient
                coefficient = Coefficient.objects.get(pk=int(coef_id))

                # Определить тип значения
                if coefficient.value_type == 'numeric':
                    obs_data = {'value_numeric': float(value) if value else None}
                elif coefficient.value_type == 'boolean':
                    obs_data = {'value_boolean': bool(value)}
                elif coefficient.value_type == 'text':
                    obs_data = {'value_text': str(value)}
                else:
                    continue

                # Создать или обновить наблюдение
                observation, created = Observation.objects.update_or_create(
                    visit=visit,
                    coefficient=coefficient,
                    defaults=obs_data
                )

                saved_observations.append({
                    'coefficient_id': int(coef_id),
                    'created': created
                })
            except Exception as e:
                # Логировать ошибку, но продолжить
                print(f"Error saving observation for coefficient {coef_id}: {e}")
                continue

        return JsonResponse({
            'success': True,
            'visit_id': visit.id,
            'observations_saved': len(saved_observations),
            'synced_at': timezone.now().isoformat()
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ============================================================================
# Начать визит сейчас (Start Visit Now)
# ============================================================================

@login_required
def start_visit_now(request):
    """
    Мобильная стартовая страница для тайного покупателя.
    Выбор канала → магазин → начало визита.
    """
    from geo.models import Outlet, Channel

    # Получить выбранный канал из GET параметров
    selected_channel_id = request.GET.get('channel')

    # Получить все активные каналы (только те, где есть активные магазины)
    channels = Channel.objects.filter(
        outlets__status=Outlet.STATUS_ACTIVE
    ).select_related('region', 'region__country').distinct().order_by('region__country__name', 'region__name', 'name')

    # Получить магазины выбранного канала
    outlets = []
    if selected_channel_id:
        outlets = Outlet.objects.filter(
            channel_id=selected_channel_id,
            status=Outlet.STATUS_ACTIVE
        ).select_related('channel', 'channel__region', 'channel__region__country').order_by('name')

    # Получить типы визитов (FONON и другие)
    visit_types = VisitType.objects.filter(is_active=True)

    context = {
        'channels': channels,
        'outlets': outlets,
        'selected_channel_id': selected_channel_id,
        'visit_types': visit_types,
    }

    return render(request, 'visits/start_visit_now.html', context)


@login_required
def quick_start_visit(request):
    """
    Быстрое создание и начало визита.
    POST endpoint для немедленного начала визита в выбранном магазине.
    """
    if request.method != 'POST':
        return redirect('visits:start_visit_now')

    outlet_id = request.POST.get('outlet_id')
    visit_type_id = request.POST.get('visit_type_id')

    if not outlet_id or not visit_type_id:
        messages.error(request, 'Выберите магазин и тип визита')
        return redirect('visits:start_visit_now')

    try:
        from geo.models import Outlet
        outlet = Outlet.objects.get(pk=outlet_id, status=Outlet.STATUS_ACTIVE)
        visit_type = VisitType.objects.get(pk=visit_type_id, is_active=True)

        # Создать визит и сразу начать его
        visit = Visit.objects.create(
            visit_type=visit_type,
            outlet=outlet,
            user=request.user,
            status=Visit.STATUS_IN_PROGRESS,
            start_date=timezone.now()
        )

        messages.success(request, f'Визит в "{outlet.name}" начат!')
        return redirect('visits:fill_visit', pk=visit.pk)

    except (Outlet.DoesNotExist, VisitType.DoesNotExist):
        messages.error(request, 'Магазин или тип визита не найден')
        return redirect('visits:start_visit_now')
