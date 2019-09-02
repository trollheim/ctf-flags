import requests

# data to be sent to api
data = {'login': 'admin',
                 'password':'W5UVa54FaZ5Ux==k%2bbT$XF@a%rsua3dQk^WPXPGLkZb_gucK+_BCvk#+w8Z9Jc'}

# sending post request and saving response as response object
r = requests.post(url="http://localhost:8080/login" , data = data)

# TODO : handle result