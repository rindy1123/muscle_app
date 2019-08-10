from django.urls import path
from .views import homefunc, loginfunc, signupfunc, CreateWorkout, CreateDiet,\
    CreateBody, logoutfunc, DeleteWorkout, DeleteDiet, DeleteBody, UpdateWorkout,\
    UpdateDiet, UpdateBody, home_change_datefunc, timeline_workoutfunc,\
    timeline_dietfunc, timeline_bodyfunc

urlpatterns = [
    path('', loginfunc, name='login'),
    path('home/', homefunc, name='home'),
    path('signup/', signupfunc, name='signup'),
    path('workout_create/', CreateWorkout.as_view(), name='workout_create'),
    path('diet_create/', CreateDiet.as_view(), name='diet_create'),
    path('body_create/', CreateBody.as_view(), name='body_create'),
    path('logout/', logoutfunc, name='logout'),
    path('workout_delete/<int:pk>', DeleteWorkout.as_view(), name='workout_delete'),
    path('diet_delete/<int:pk>', DeleteDiet.as_view(), name='diet_delete'),
    path('body_delete/<int:pk>', DeleteBody.as_view(), name='body_delete'),
    path('workout_update/<int:pk>', UpdateWorkout.as_view(), name='workout_update'),
    path('diet_update/<int:pk>', UpdateDiet.as_view(), name='diet_update'),
    path('body_update/<int:pk>', UpdateBody.as_view(), name='body_update'),
    path('change_date/', home_change_datefunc, name='change_date'),
    path('timeline/workout/', timeline_workoutfunc, name='timeline_workout'),
    path('timeline/diet/', timeline_dietfunc, name='timeline_diet'),
    path('timeline/body/', timeline_bodyfunc, name='timeline_body'),

]
