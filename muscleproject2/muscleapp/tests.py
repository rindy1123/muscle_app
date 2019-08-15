from django.test import TestCase
from django.utils.timezone import localdate
from django.test import Client
from django.urls import reverse
from django.contrib.auth import models

from muscleapp.models import WorkoutModel, DietModel, BodyModel
import sys
import pathlib
from register.models import User

current_dir = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(current_dir) + '/register/models.py')

# Create your tests here.


class GetViewTestCase(TestCase):
    def setUp(self):
        self.workout_object = WorkoutModel.objects.create(
            name='スクワット',
            weight=80,
            reps=10,
            set=3,
            date=localdate(),
            author='A'
        )
        self.diet_object = DietModel.objects.create(
            calorie=100,
            name='白米',
            protein=10,
            carb=30,
            fat=10,
            date=localdate(),
            author='B'
        )
        self.body_object = BodyModel.objects.create(
            weight=80.5,
            percent_body_fat=10,
            muscle_mass=50,
            date=localdate(),
            maintenance_calorie=1700,
            cutting_calorie=1450,
            increasing_calorie=2200,
            author='C'

        )
        self.user = User.objects.create(
            username='Mike',
            age=20,
            height=170,
            email='Mike@gmail.com',
            workoutdegree=1.5,
            is_staff=False,
            password='mike'
        )

    def test_get_workout_data(self):
        actual = WorkoutModel.objects.get(author='A').name
        expected = 'スクワット'
        self.assertEqual(actual, expected)

    def test_get_diet_data(self):
        actual = DietModel.objects.get(author='B').name
        expected = '白米'
        self.assertEqual(actual, expected)

    def test_get_body_data(self):
        actual = BodyModel.objects.get(author='C').weight
        expected = 80.5
        self.assertEqual(actual, expected)

    def test_get_user_model(self):
        actual = User.objects.get(username='Mike').email
        expected = 'Mike@gmail.com'
        self.assertEqual(actual, expected)

    def test_login_page(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        client = Client()
        response = client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        client = Client()
        client.force_login(self.user)
        response = client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_timeline(self):
        client = Client()
        client.force_login(self.user)
        workout_response = client.get('/timeline/workout/')
        self.assertEqual(workout_response.status_code, 200)
        diet_response = client.get('/timeline/diet/')
        self.assertEqual(diet_response.status_code, 200)
        body_response = client.get('/timeline/body/')
        self.assertEqual(body_response.status_code, 200)

    def test_create_page(self):
        client = Client()
        client.force_login(self.user)
        workout_response = client.get('/workout_create/')
        self.assertEqual(workout_response.status_code, 200)
        diet_response = client.get('/diet_create/')
        self.assertEqual(diet_response.status_code, 200)
        body_response = client.get('/body_create/')
        self.assertEqual(body_response.status_code, 200)

    def test_update_page(self):
        client = Client()
        client.force_login(self.user)

        workout_url = reverse('workout_update', args=[1])
        workout_response = client.get(workout_url)
        self.assertEqual(workout_response.status_code, 200)

        diet_url = reverse('diet_update', args=[1])
        diet_response = client.get(diet_url)
        self.assertEqual(diet_response.status_code, 200)

        body_url = reverse('body_update', args=[1])
        body_response = client.get(body_url)
        self.assertEqual(body_response.status_code, 200)

    def test_delete_page(self):
        client = Client()
        client.force_login(self.user)

        workout_url = reverse('workout_delete', args=[1])
        workout_response = client.get(workout_url)
        self.assertEqual(workout_response.status_code, 200)

        diet_url = reverse('diet_delete', args=[1])
        diet_response = client.get(diet_url)
        self.assertEqual(diet_response.status_code, 200)

        body_url = reverse('body_delete', args=[1])
        body_response = client.get(body_url)
        self.assertEqual(body_response.status_code, 200)

    def test_change_date(self):
        client = Client()
        client.force_login(self.user)
        response = client.get('/change_date/')
        self.assertEqual(response.status_code, 200)







