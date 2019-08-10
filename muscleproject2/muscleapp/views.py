from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import WorkoutModel, DietModel, BodyModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your views here.


# 会員登録設定
def signupfunc(request):
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


# ログイン設定
def loginfunc(request):
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


# ログアウト設定
def logoutfunc(request):
    logout(request)
    return redirect('login')

# ホーム画面設定
@login_required
def homefunc(request):
    # 日付を変更した場合
    if request.method == 'POST':
        changed_date = request.POST['date']
        login_name = request.user.get_username()
        workout_data = WorkoutModel.objects.filter(author=login_name, date__icontains=changed_date).all()
        diet_data = DietModel.objects.filter(author=login_name, date__icontains=changed_date).all()
        body_data = BodyModel.objects.filter(author=login_name, date__icontains=changed_date).all()
        for data in body_data:
            user = get_user_model()
            user_data = user.objects.get(username=data.author)
            data.maintenance_calorie = round(user_data.workoutdegree * (13.4 * data.weight + 4.8 * user_data.height -
                                                                        5.68 * user_data.age + 88.4), 1)
            data.cutting_calorie = data.maintenance_calorie - 500
            data.increasing_calorie = data.maintenance_calorie + 250
            data.save()
        return render(request, 'home.html',
                      {'workout_data': workout_data, 'diet_data': diet_data,
                       'body_data': body_data})
    # GETで今日の日付のデータを表示
    else:
        now = timezone.localtime(timezone.now())
        login_name = request.user.get_username()
        workout_data = WorkoutModel.objects.filter(author=login_name, date__icontains=now.date()).all()
        diet_data = DietModel.objects.filter(author=login_name, date__icontains=now.date()).all()
        body_data = BodyModel.objects.filter(author=login_name, date__icontains=now.date()).all()
        for data in body_data:
            user = get_user_model()
            user_data = user.objects.get(username=data.author)
            data.maintenance_calorie = round(user_data.workoutdegree * (13.4 * data.weight + 4.8 * user_data.height -
                                                                        5.68 * user_data.age + 88.4), 1)
            data.cutting_calorie = data.maintenance_calorie - 500
            data.increasing_calorie = data.maintenance_calorie + 250
            data.save()
        return render(request, 'home.html',
                  {'workout_data': workout_data, 'diet_data': diet_data,
                   'body_data': body_data})


# タイムラインで筋トレデータを表示
@login_required
def timeline_workoutfunc(request):
    workout_data = WorkoutModel.objects.order_by('-date').all()
    return render(request, 'timeline_workout.html', {'workout_data': workout_data})


# タイムラインで食事データを表示
@login_required
def timeline_dietfunc(request):
    diet_data = DietModel.objects.order_by('-date').all()
    return render(request, 'timeline_diet.html', {'diet_data': diet_data})


# タイムラインで身体データを表示
@login_required
def timeline_bodyfunc(request):
    body_data = BodyModel.objects.order_by('-date').all()
    for data in body_data:
        user = get_user_model()
        user_data = user.objects.get(username=data.author)
        # ハリスベネティクト方程式で基礎代謝を算出
        # 運動強度依存定数を掛けることでメンテナンスカロリーを算出
        data.maintenance_calorie = round(user_data.workoutdegree * (13.4 * data.weight + 4.8 * user_data.height -
                                                                    5.68 * user_data.age + 88.4), 1)
        # 減量期・増量期のカロリーは目安
        data.cutting_calorie = data.maintenance_calorie - 500
        data.increasing_calorie = data.maintenance_calorie + 250
        data.save()
    return render(request, 'timeline_body.html', {'body_data': body_data})


# 筋トレデータ作成
class CreateWorkout(CreateView):
    template_name = 'workout_create.html'
    model = WorkoutModel
    fields = ('name', 'weight', 'reps', 'set', 'author')
    success_url = reverse_lazy('home')


# 食事データ作成
class CreateDiet(CreateView):
    template_name = 'diet_create.html'
    model = DietModel
    fields = ('calorie', 'name', 'protein', 'carb', 'fat', 'author')
    success_url = reverse_lazy('home')


# 身体データ作成
class CreateBody(CreateView):
    template_name = 'body_create.html'
    model = BodyModel
    fields = ('weight', 'percent_body_fat', 'muscle_mass', 'author')
    success_url = reverse_lazy('home')


# 筋トレデータ削除
class DeleteWorkout(DeleteView):
    template_name = 'delete.html'
    model = WorkoutModel
    success_url = reverse_lazy('home')


# 食事データ削除
class DeleteDiet(DeleteView):
    template_name = 'delete.html'
    model = DietModel
    success_url = reverse_lazy('home')


# 身体データ削除
class DeleteBody(DeleteView):
    template_name = 'delete.html'
    model = BodyModel
    success_url = reverse_lazy('home')


# 筋トレデータ編集
class UpdateWorkout(UpdateView):
    template_name = 'workout_update.html'
    model = WorkoutModel
    fields = ('name', 'weight', 'reps', 'set')
    success_url = reverse_lazy('home')


# 食事データ編集
class UpdateDiet(UpdateView):
    template_name = 'diet_update.html'
    model = DietModel
    fields = ('calorie', 'name', 'protein', 'carb', 'fat')
    success_url = reverse_lazy('home')


# 身体データ編集
class UpdateBody(UpdateView):
    template_name = 'body_update.html'
    model = BodyModel
    fields = ('weight', 'percent_body_fat', 'muscle_mass')
    success_url = reverse_lazy('home')


# 日付変更画面を表示
@login_required
def home_change_datefunc(request):
    return render(request, 'change_date.html')



