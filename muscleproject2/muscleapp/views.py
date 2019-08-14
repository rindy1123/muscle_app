from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import WorkoutModel, DietModel, BodyModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
# Create your views here.


def signupfunc(request):
    """会員登録設定"""
    if request.method == 'POST':
        user = get_user_model()  # 独自のユーザーモデルを取得
        requested_name = request.POST['username']
        requested_pass = request.POST['password']
        requested_email = request.POST['email']
        requested_age = request.POST['age']
        requested_height = request.POST['height']
        requested_workout_degree = request.POST['workoutdegree']
        user.objects.create_user(requested_name, requested_email, requested_pass,
                                 age=requested_age, height=requested_height, workoutdegree=requested_workout_degree)
        return redirect('login')
    else:
        return render(request, 'signup.html')


def loginfunc(request):
    """ログイン設定"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '該当するユーザーが存在しません'})
    else:
        return render(request, 'login.html')


def logoutfunc(request):
    """ログアウト設定"""
    logout(request)
    return redirect('login')


def get_data(name, date):
    """三つのデータを取得"""
    workout_data = WorkoutModel.objects.filter(author=name, date__icontains=date).all()
    diet_data = DietModel.objects.filter(author=name, date__icontains=date).all()
    body_data = BodyModel.objects.filter(author=name, date__icontains=date).all()
    return {'workout_data': workout_data, 'diet_data': diet_data, 'body_data': body_data}


def save_calorie_data(body_data):
    """
    ハリスベネディクト方程式で基礎代謝を算出

    運動強度依存定数を掛けることでメンテナンスカロリーを算出

    メンテナンスカロリーを基準に減量期・増量期のカロリーを算出
    """
    user = get_user_model()
    for data in body_data:
        user_data = user.objects.get(username=data.author)
        data.maintenance_calorie = round(user_data.workoutdegree * (13.4 * data.weight + 4.8 * user_data.height -
                                                                    5.68 * user_data.age + 88.4), 1)
        # 減量期・増量期のカロリーは目安
        data.cutting_calorie = data.maintenance_calorie - 500
        data.increasing_calorie = data.maintenance_calorie + 250
        data.save()


@login_required
def homefunc(request):
    """
    ホーム画面設定

    日付を変更した場合(POST)と直接ホーム画面に訪問した場合(GET)
    """
    # 日付を変更した場合
    if request.method == 'POST':
        changed_date = request.POST['date']
        login_name = request.user.get_username()
        dict_data = get_data(login_name, changed_date)
        save_calorie_data(dict_data['body_data'])
        return render(request, 'home.html', dict_data)
    # GETで今日の日付のデータを表示
    else:
        today = timezone.localtime(timezone.now()).date()
        login_name = request.user.get_username()
        dict_data = get_data(login_name, today)
        save_calorie_data(dict_data['body_data'])
        return render(request, 'home.html', dict_data)


@login_required
def timeline_workoutfunc(request):
    """タイムラインで筋トレデータを表示"""
    workout = WorkoutModel.objects.order_by('-date').all()
    paginator = Paginator(workout, 5)
    page = request.GET.get('page')
    workout_data = paginator.get_page(page)
    return render(request, 'timeline_workout.html', {'workout_data': workout_data})


@login_required
def timeline_dietfunc(request):
    """タイムラインで食事データを表示"""
    diet = DietModel.objects.order_by('-date').all()
    paginator = Paginator(diet, 5)
    page = request.GET.get('page')
    diet_data = paginator.get_page(page)
    return render(request, 'timeline_diet.html', {'diet_data': diet_data})


@login_required
def timeline_bodyfunc(request):
    """タイムラインで身体データを表示"""
    body = BodyModel.objects.order_by('-date').all()
    paginator = Paginator(body, 5)
    page = request.GET.get('page')
    body_data = paginator.get_page(page)
    return render(request, 'timeline_body.html', {'body_data': body_data})


class CreateWorkout(CreateView):
    """筋トレデータ作成"""
    template_name = 'workout_create.html'
    model = WorkoutModel
    fields = ('name', 'weight', 'reps', 'set', 'author')
    success_url = reverse_lazy('home')


class CreateDiet(CreateView):
    """食事データ作成"""
    template_name = 'diet_create.html'
    model = DietModel
    fields = ('calorie', 'name', 'protein', 'carb', 'fat', 'author')
    success_url = reverse_lazy('home')


class CreateBody(CreateView):
    """身体データ作成"""
    template_name = 'body_create.html'
    model = BodyModel
    fields = ('weight', 'percent_body_fat', 'muscle_mass', 'author')
    success_url = reverse_lazy('home')


class DeleteWorkout(DeleteView):
    """筋トレデータ削除"""
    template_name = 'delete.html'
    model = WorkoutModel
    success_url = reverse_lazy('home')


class DeleteDiet(DeleteView):
    """食事データ削除"""
    template_name = 'delete.html'
    model = DietModel
    success_url = reverse_lazy('home')


class DeleteBody(DeleteView):
    """身体データ削除"""
    template_name = 'delete.html'
    model = BodyModel
    success_url = reverse_lazy('home')


class UpdateWorkout(UpdateView):
    """筋トレデータ編集"""
    template_name = 'workout_update.html'
    model = WorkoutModel
    fields = ('name', 'weight', 'reps', 'set')
    success_url = reverse_lazy('home')


class UpdateDiet(UpdateView):
    """食事データ編集"""
    template_name = 'diet_update.html'
    model = DietModel
    fields = ('calorie', 'name', 'protein', 'carb', 'fat')
    success_url = reverse_lazy('home')


class UpdateBody(UpdateView):
    """身体データ編集"""
    template_name = 'body_update.html'
    model = BodyModel
    fields = ('weight', 'percent_body_fat', 'muscle_mass')
    success_url = reverse_lazy('home')


@login_required
def home_change_datefunc(request):
    """日付変更画面を表示"""
    return render(request, 'change_date.html')



