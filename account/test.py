# from rest_framework.test import APIClient, APITestCase,APIRequestFactory
# from .views import ClientRegister ,ClientLogin
# from django.urls import reverse,reverse_lazy
# from rest_framework import status
# from .models import Client

# class TestRegsterClient(APITestCase):
#     def setUp(self) -> None:
#         self.factory = APIRequestFactory()
#         self.view = ClientRegister.as_view()
#         self.url = reverse_lazy('register')
#         self.data={
#             'username': 'test',
#             'email': 'test@example.com',
#             'password':'test',
#             'phone_number':'332676327'
#         }
#     def test_clientRegister(self):
#         request = self.factory.post(self.url,self.data)
#         response  = self.view(request)

#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)

#     # def test_exist_usernemae(self):
#     #     existing_user = Client


# class TestLoginView(APITestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = Client.objects.create_user(
#             username='test',
#             email='s@gmail.com',
#             password='password'
#         )

#         self.url = reverse('login')

#     def test_login_successful(self):
#         response = self.client.post(self.url, {
#             'username': 'test',
#             'password': 'password'
#         })
#         self.assertEqual(response.status_code, 200)
        
#         self.assertIn('access', response.data)
        
#         self.assertIn('refresh', response.data)

# class TestPermission(APITestCase):

#     def settings(self):
#         self.client = APIClient()
#         self.user = Client.objects.create_user(
#             username='test',
#             email='s@gmail.com',
#             password='password'
#         )

#         self.url = reverse('login')


#     # def test_login_unsuccessful(self):
#     #     response = self.client.post(self.url, {
#     #         'username': 'test',
#     #         'password': 'invalidpassword'
#     #     })
#     #     self.assertEqual(response.status_code, 400)
#     #     print(response.data['detail'])


# # class TestClentLogin(APITestCase):
# #     def setUp(self) -> None:
# #         self.client = APIClient()
# #         self.user = Client.objects.create_user(
# #             username='testuser',
# #             email='test@example.com', 
# #             password='test'
# #         )

# #         self.url = reverse('login')

# #     def test_login_successful(self):
# #         print(self.user)
# #         response = self.client.post(self.url, {
# #             'username': 'testuser',
# #             'password': 'test'
# #         })
# #         self.assertEqual(response.status_code, 200)
        
# #         self.assertIn('access', response.data)
        
# #         self.assertIn('refresh', response.data)
#     # def test_client_login(self):
#     #     print(self.user)
#     #     response = self.client.post(self.url,{
#     #         'username':self.user.username,
#     #         'password':'test'
#     #     })
#     #     self.assertEqual(response.status_code, 200)
        
#     #     self.assertIn('access', response.data)
        
#     #     self.assertIn('refresh', response.data)

