from django.shortcuts import redirect, render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from .models import Car, Favorite, TestDriveRequest
from .serializers import CarSerializer, FavoriteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['price', 'range_km', 'year', 'drive_type']
    search_fields = ['model', 'brand__name']
    ordering_fields = ['price', 'range_km', 'power_kw']

    @action(detail=True, methods=['get', 'post'])
    def toggle_favorite(self, request, pk=None):
        # 1. Перевірка на аноніма (для DRF)
        if not request.user.is_authenticated:
            # Якщо це звичайний запит через браузер, перенаправляємо
            return redirect('login') 
        
        car = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, car=car)
        
        if not created:
            favorite.delete()
            
        return redirect('catalog')


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@login_required # Дозволяємо тільки залогіненим
def toggle_favorite(request, pk):
    # 1. Якщо юзер не залогінився — відправляємо його на логін
    if not request.user.is_authenticated:
        return redirect('login') 

    car = get_object_or_404(Car, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, car=car)
    
    if not created:
        favorite.delete()
        
    return redirect('catalog')

@login_required
def profile_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('car')
    test_drives = TestDriveRequest.objects.filter(user=request.user)
    
    return render(request, 'cars/profile.html', {
        'favorites': favorites,
        'test_drives': test_drives
    })

def index_view(request):
    return render(request, 'cars/index.html')

def catalog_view(request):
    car_list = Car.objects.all().order_by('-id')
    paginator = Paginator(car_list, 6) # 6 машин на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cars = Car.objects.all()
    fav_ids = []
    if request.user.is_authenticated:
        # Отримуємо ID всіх машин, які цей юзер лайкнув
        fav_ids = Favorite.objects.filter(user=request.user).values_list('car_id', flat=True)
    
    return render(request, 'cars/catalog.html', {'page_obj': page_obj})

def car_detail_view(request, pk):
    car = get_object_or_404(Car, pk=pk)
    specs = [
        ("Запас ходу", car.range_km, "км"),
        ("Батарея", car.battery_capacity, "кВт·год"),
        ("Потужність", car.power_kw, "кВт"),
        ("0-100 км/год", car.acceleration_0_100, "сек"),
    ]
    return render(request, 'cars/car_detail.html', {'car': car, 'specs': specs})

def add_to_compare(request, pk):
    compare_list = request.session.get('compare_list', [])
    if pk not in compare_list:
        compare_list.append(pk)
        # Тримаємо в списку тільки останні 2 обрані машини
        if len(compare_list) > 2:
            compare_list.pop(0)
    request.session['compare_list'] = compare_list
    return redirect('catalog')

def compare_view(request):
    compare_ids = request.session.get('compare_list', [])
    cars = Car.objects.filter(id__in=compare_ids)
    return render(request, 'cars/compare.html', {'cars': cars})

def clear_compare_view(request):
    if 'compare_list' in request.session:
        del request.session['compare_list']
    return redirect('catalog')

def test_drive_view(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        TestDriveRequest.objects.create(
            car=car,
            user=request.user if request.user.is_authenticated else None, # Прив'язуємо юзера
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            preferred_date=request.POST.get('date')
        )
        messages.success(request, f"Заявку на {car.model} прийнято!")
        return redirect('car_detail', pk=pk)
        
    return render(request, 'cars/test_drive.html', {'car': car})

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація успішна! Ласкаво просимо.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'cars/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"З поверненням, {user.username}!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'cars/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

