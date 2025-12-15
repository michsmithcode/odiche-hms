"""

{
    "message": "Login successful.",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1MzM0ODg4LCJpYXQiOjE3NjUzMzEyODgsImp0aSI6ImEwMGU0ODMyMzcwZjQ1NjlhODAxMGRiNjgxNjI3ZjcyIiwidXNlcl9pZCI6Ijc1YjBhNDIwLWM1NWItNDJhYi1hZjJiLTM0ZDRiMzVmZDQ2MyJ9.f7E4gJSNaNgq0xtjss3YiIsXe3sxQQ9s8eaiqZHnGjw",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NTUwNDA4OCwiaWF0IjoxNzY1MzMxMjg4LCJqdGkiOiJjN2NlNTQ3ZWRhZmE0OTNiYTA0NTE1NmY2OWEwMDlmOCIsInVzZXJfaWQiOiI3NWIwYTQyMC1jNTViLTQyYWItYWYyYi0zNGQ0YjM1ZmQ0NjMifQ.q79OHhzIXD7q9GEo9JVHNxC_QU631MFisfLQz6LmTew",
    "user": {
        "email": "testdoctor@gmail.com",
        "role": "Doctor",
        "is_active": true
    }
}

"""

"""
15/12
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1Nzk4MjI0LCJpYXQiOjE3NjU3OTQ2MjQsImp0aSI6ImQ2YjIwNWU4ZGFkNDQ1NDc4MjI0NGQzMjRkMmQ2YTk2IiwidXNlcl9pZCI6Ijc1YjBhNDIwLWM1NWItNDJhYi1hZjJiLTM0ZDRiMzVmZDQ2MyJ9.1a2-_SIXgGgYx9tHi0KW5w6lZ3HNQywM6dGxrmCf2Wo",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NTk2NzQyNCwiaWF0IjoxNzY1Nzk0NjI0LCJqdGkiOiIwYjY4NjE3YmQwODA0YWE5ODY5NGE3YjVmMzFjNzMyYiIsInVzZXJfaWQiOiI3NWIwYTQyMC1jNTViLTQyYWItYWYyYi0zNGQ0YjM1ZmQ0NjMifQ.wWBOgt6fuUI6uBkH8v8D7Ins6N7Gntt3NeLMU9m8b8k"
}
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1Nzc0MzI3LCJpYXQiOjE3NjU3NzA3MjgsImp0aSI6ImMxNTZiMmQ4MGRiMjRjMDZhNzRhYTliZmI3OTgxZjMxIiwidXNlcl9pZCI6Ijc1YjBhNDIwLWM1NWItNDJhYi1hZjJiLTM0ZDRiMzVmZDQ2MyJ9.61IHflfkLWlBcxspVRMYv34IbTTqccvBEkXw2uc9F68",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NTk0MzUyNywiaWF0IjoxNzY1NzcwNzI3LCJqdGkiOiJhMzMyZGIwNjEyODQ0OWU0YjQzN2NiY2IwMDA0YzRlNyIsInVzZXJfaWQiOiI3NWIwYTQyMC1jNTViLTQyYWItYWYyYi0zNGQ0YjM1ZmQ0NjMifQ.b7nUNbnxMQ2bCRu2Qo1jKam-X3KQ4KgZzab5lIyoveY"
}
or
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1NTQyOTIxLCJpYXQiOjE3NjU1MzkzMjEsImp0aSI6IjA4YzY5YWM5NmY3NjRjODk5MTZlOWEwNmFiMzA3Yzk4IiwidXNlcl9pZCI6Ijc1YjBhNDIwLWM1NWItNDJhYi1hZjJiLTM0ZDRiMzVmZDQ2MyJ9.S_gcCKs0dxgMw_cziOcmv0F3a2u3LZF93Wk8HAGi124",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NTcxMjEyMSwiaWF0IjoxNzY1NTM5MzIxLCJqdGkiOiJhZDQ2MTY0OGZlNmM0ZWM0Yjc1M2MzMDY4NWRkYmE1MyIsInVzZXJfaWQiOiI3NWIwYTQyMC1jNTViLTQyYWItYWYyYi0zNGQ0YjM1ZmQ0NjMifQ.OaRXUJKo8SkVvfCYuKi5Ip7Bdo5dIiPN3mzCRDNV10k"
}
{new,
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1Njg0MDA5LCJpYXQiOjE3NjU2ODA0MDksImp0aSI6IjBmZWYxMWNmMGMxMzRjNDY4Mzc0MjYxNmE2YWJlMTUxIiwidXNlcl9pZCI6Ijc1YjBhNDIwLWM1NWItNDJhYi1hZjJiLTM0ZDRiMzVmZDQ2MyJ9.7l4c0TXronvLq2uQO9SfuiUxOHjnBNyA3b8K64zLepY",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NTg1MzIwOSwiaWF0IjoxNzY1NjgwNDA5LCJqdGkiOiJlZmUxZmNkZjRkZDA0OGY1OTkxYjE5MjcxMmUzZWJjMiIsInVzZXJfaWQiOiI3NWIwYTQyMC1jNTViLTQyYWItYWYyYi0zNGQ0YjM1ZmQ0NjMifQ.3ZupQmTRY3uTb6IFplvXNW2kE5z71GFloZqPJNM3Kws"
}
 
 """
""" #first doctor created
"email": "testdoctor@gmail.com",
    "first_name": "test",
    "last_name": "test",
    "role": "doctor",
    "specialization": "general_practitioner",
    "license_number": "MDCM/RN/12345",
    "years_of_experience": 5,
    "qualifications": "MDCM General",
    "bio": null,
    "shift": null,
    "available_time_from": null,
    "available_time_to": null,
    "created_at": "2025-11-28T13:20:38.859124Z"
"""