#Basic REST-API Server documentation

NOTE: Token validity for authentication is valid for 30 minutes. If a "no token" message appears after you have made a 
request, you have to return to the /login endpoint to get a new token. 

##Admin

### Login
```bash
curl -X GET \
  http://127.0.0.1:5000/login \
  -H 'Authorization: Basic QWRtaW46MTIzNDU=' \
  -H 'cache-control: no-cache'
```
Response: 
```JSON
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlZTgwZjQ3OC1hMDEwLTQxMTAtOTFiYy02YzQ3ODIzMzlhYWIiLCJleHAiOjE1NDk1MzIxMTd9.5FKR0RlJ0ajjhu-JDypr0nx140KySJ8ke5G8MuPRTvY"
}
```

Using this token, we can then request for subsequent information.

###To request user information (as admin):
```bash
curl -X GET \
  http://127.0.0.1:5000/user \
  -H 'Authorization: Basic QWRtaW46MTIzNDU=' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlZTgwZjQ3OC1hMDEwLTQxMTAtOTFiYy02YzQ3ODIzMzlhYWIiLCJleHAiOjE1NDk1MzMwNjB9.Oji01y3v8RpTOQM7ShQycIjfsG9-ivHRcA50srgEveA'
```

Here is the result:
```json
{
    "users": [
        {
            "admin": true,
            "has_quota": false,
            "name": "Admin",
            "password": "sha256$QDZzslGq$ef8087b2022480f31f91dbe64a9b5d967f4b8edc7efc2730d4e68c6564b7000e",
            "public_id": "ee80f478-a010-4110-91bc-6c4782339aab",
            "quota": null,
            "resource_count": 1
        },
        {
            "admin": false,
            "has_quota": false,
            "name": "David",
            "password": "sha256$KcU1C8j2$a372c9b5a3842f44087ac68a0424475d11835abd58e6d4255a6831e0ba8d244b",
            "public_id": "1edcd425-7f2c-472a-8815-0e52b45d722a",
            "quota": null,
            "resource_count": 1
        }
    ]
}
```

###Request all resources (Admin)
```bash
curl -X GET \
  http://127.0.0.1:5000/resource \
  -H 'Authorization: Basic QWRtaW46MTIzNDU=' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlZTgwZjQ3OC1hMDEwLTQxMTAtOTFiYy02YzQ3ODIzMzlhYWIiLCJleHAiOjE1NDk1MzMwNjB9.Oji01y3v8RpTOQM7ShQycIjfsG9-ivHRcA50srgEveA'
```
Response:
```json
{
    "resources": [
        {
            "id": 3,
            "text": "resource #2",
            "user_id": 1
        }
    ]
}
```

### Add resource 
```bash
curl -X POST \
  http://127.0.0.1:5000/resource \
  -H 'Authorization: Basic QWRtaW46MTIzNDU=' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 549d37e7-7c84-4319-8365-acc5c452fdf6' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlZTgwZjQ3OC1hMDEwLTQxMTAtOTFiYy02YzQ3ODIzMzlhYWIiLCJleHAiOjE1NDk1MzMwNjB9.Oji01y3v8RpTOQM7ShQycIjfsG9-ivHRcA50srgEveA' \
  -d '{"text" : "Creating new resource"}'
```

To check, we make a call to list the resources: 
```bash
curl -X GET \
  http://127.0.0.1:5000/resource \
  -H 'Authorization: Basic QWRtaW46MTIzNDU=' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 718e8186-a6ab-439b-ada4-5f3480fc2ce7' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlZTgwZjQ3OC1hMDEwLTQxMTAtOTFiYy02YzQ3ODIzMzlhYWIiLCJleHAiOjE1NDk1MzMwNjB9.Oji01y3v8RpTOQM7ShQycIjfsG9-ivHRcA50srgEveA'
```
Here is the result, after adding a new resource!
```json
{
    "resources": [
        {
            "id": 3,
            "text": "resource #2",
            "user_id": 1
        },
        {
            "id": 4,
            "text": "Creating new resource",
            "user_id": 1
        }
    ]
}
```

### Deleting a resource 
```bash
curl -X DELETE \
  http://127.0.0.1:5000/resource/3 \
  -H 'Authorization: Basic QWRtaW46MTIzNDU=' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 86e0fc53-e637-4acf-9d71-4cbce8fadeac' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlZTgwZjQ3OC1hMDEwLTQxMTAtOTFiYy02YzQ3ODIzMzlhYWIiLCJleHAiOjE1NDk1MzUwNTh9.MxoZOXJJBKOG0u38t2o4nRC7gOqY56b2yOPgSXBhiLo'
```
Result:
```json
{
    "message": "Resource deleted by user"
}
```

### Setting a quota
Before: 
```json
{
    "users": [
        {
            "admin": true,
            "has_quota": false,
            "name": "Admin",
            "password": "sha256$QDZzslGq$ef8087b2022480f31f91dbe64a9b5d967f4b8edc7efc2730d4e68c6564b7000e",
            "public_id": "ee80f478-a010-4110-91bc-6c4782339aab",
            "quota": null,
            "resource_count": 1
        },
        {
            "admin": false,
            "has_quota": false,
            "name": "David",
            "password": "sha256$KcU1C8j2$a372c9b5a3842f44087ac68a0424475d11835abd58e6d4255a6831e0ba8d244b",
            "public_id": "1edcd425-7f2c-472a-8815-0e52b45d722a",
            "quota": null,
            "resource_count": 1
        }
    ]
}
```

Execute:
```bash
curl -X PUT \
  http://127.0.0.1:5000/user/setquota/1edcd425-7f2c-472a-8815-0e52b45d722a \
  -H 'Authorization: Basic QWRtaW46MTIzNDU=' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: b252589a-d67c-4818-8de7-67133d86ca47' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlZTgwZjQ3OC1hMDEwLTQxMTAtOTFiYy02YzQ3ODIzMzlhYWIiLCJleHAiOjE1NDk1MzUwNTh9.MxoZOXJJBKOG0u38t2o4nRC7gOqY56b2yOPgSXBhiLo' \
  -d '{"quota":"2"}'
```
Result:
```json
{
    "message": "Quota set!"
}
```
Final State (send request to list users again):
```json
{
    "users": [
        {
            "admin": true,
            "has_quota": false,
            "name": "Admin",
            "password": "sha256$QDZzslGq$ef8087b2022480f31f91dbe64a9b5d967f4b8edc7efc2730d4e68c6564b7000e",
            "public_id": "ee80f478-a010-4110-91bc-6c4782339aab",
            "quota": null,
            "resource_count": 1
        },
        {
            "admin": false,
            "has_quota": true,
            "name": "David",
            "password": "sha256$KcU1C8j2$a372c9b5a3842f44087ac68a0424475d11835abd58e6d4255a6831e0ba8d244b",
            "public_id": "1edcd425-7f2c-472a-8815-0e52b45d722a",
            "quota": 2,
            "resource_count": 1
        }
    ]
}
```
###Create new User
```bash
curl -X POST \
  http://127.0.0.1:5000/user \
  -H 'Authorization: Basic QWRtaW46MTIzNDU=' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 475cd10b-d7eb-4cee-a620-0a858fd4aa1e' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlZTgwZjQ3OC1hMDEwLTQxMTAtOTFiYy02YzQ3ODIzMzlhYWIiLCJleHAiOjE1NDk1MzUwNTh9.MxoZOXJJBKOG0u38t2o4nRC7gOqY56b2yOPgSXBhiLo' \
  -d '{"name":"User", "password":"password"}'
```

Response:
```json
{
    "message": "New user created!"
}
```
After listing users, we get:
```json
{
    "users": [
        {
            "admin": true,
            "has_quota": false,
            "name": "Admin",
            "password": "sha256$QDZzslGq$ef8087b2022480f31f91dbe64a9b5d967f4b8edc7efc2730d4e68c6564b7000e",
            "public_id": "ee80f478-a010-4110-91bc-6c4782339aab",
            "quota": null,
            "resource_count": 1
        },
        {
            "admin": false,
            "has_quota": true,
            "name": "David",
            "password": "sha256$KcU1C8j2$a372c9b5a3842f44087ac68a0424475d11835abd58e6d4255a6831e0ba8d244b",
            "public_id": "1edcd425-7f2c-472a-8815-0e52b45d722a",
            "quota": 2,
            "resource_count": 1
        },
        {
            "admin": false,
            "has_quota": false,
            "name": "User",
            "password": "sha256$AapcvHzE$bf56d058069844c79ce15470a66b92d52df0daeace436d967bcc89f6600de046",
            "public_id": "7cdf6521-c4cc-4697-8bb0-6f3134fa4147",
            "quota": null,
            "resource_count": 0
        }
    ]
}
```

## User
###Login
```bash
curl -X GET \
  http://127.0.0.1:5000/login \
  -H 'Authorization: Basic VXNlcjpwYXNzd29yZA==' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 9a450943-3084-42b8-bad6-1aebb0cf39c7' \
  -H 'cache-control: no-cache'
```
Response: 
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI3Y2RmNjUyMS1jNGNjLTQ2OTctOGJiMC02ZjMxMzRmYTQxNDciLCJleHAiOjE1NDk1MzY0MjJ9.WjFEZSwR5u4ITCc1rOT2CkiMkUCLnbK79LV51n50HW8"
}
```
This token can be used in subsequent queries.

###Create resource
```bash
curl -X POST \
  http://127.0.0.1:5000/resource \
  -H 'Authorization: Basic VXNlcjpwYXNzd29yZA==' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 09509f63-56e8-48ca-a1ef-fad1c886f7c7' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI3Y2RmNjUyMS1jNGNjLTQ2OTctOGJiMC02ZjMxMzRmYTQxNDciLCJleHAiOjE1NDk1MzY0MjJ9.WjFEZSwR5u4ITCc1rOT2CkiMkUCLnbK79LV51n50HW8' \
  -d '{"text":"newly added resource"}'
```
Response:
```json
{
    "message": "Resource created!"
}
```
Subsequently, when we list all resources, here's what we get:
```json
{
    "resources": [
        {
            "id": 1,
            "text": "resource",
            "user_id": 2
        },
        {
            "id": 4,
            "text": "Creating new resource",
            "user_id": 1
        },
        {
            "id": 5,
            "text": "newly added resource",
            "user_id": 3
        }
    ]
}
```
Note that the user properties also get updated - their resource count increases by 1! This is what we get when the admin
lists all users:
```json
{
    "users": [
        {
            "admin": true,
            "has_quota": false,
            "name": "Admin",
            "password": "sha256$QDZzslGq$ef8087b2022480f31f91dbe64a9b5d967f4b8edc7efc2730d4e68c6564b7000e",
            "public_id": "ee80f478-a010-4110-91bc-6c4782339aab",
            "quota": null,
            "resource_count": 1
        },
        {
            "admin": false,
            "has_quota": true,
            "name": "David",
            "password": "sha256$KcU1C8j2$a372c9b5a3842f44087ac68a0424475d11835abd58e6d4255a6831e0ba8d244b",
            "public_id": "1edcd425-7f2c-472a-8815-0e52b45d722a",
            "quota": 2,
            "resource_count": 1
        },
        {
            "admin": false,
            "has_quota": false,
            "name": "User",
            "password": "sha256$AapcvHzE$bf56d058069844c79ce15470a66b92d52df0daeace436d967bcc89f6600de046",
            "public_id": "7cdf6521-c4cc-4697-8bb0-6f3134fa4147",
            "quota": null,
            "resource_count": 1
        }
    ]
}
```

###Attempting to create when exceeding quota:
Before:
```json
{
    "resources": [
        {
            "id": 1,
            "text": "resource",
            "user_id": 2
        },
        {
            "id": 4,
            "text": "Creating new resource",
            "user_id": 1
        },
        {
            "id": 5,
            "text": "newly added resource",
            "user_id": 3
        }
    ]
}
```
User David (user_id) creates a new resource using the following command:
```bash
curl -X POST \
  http://127.0.0.1:5000/resource \
  -H 'Authorization: Basic RGF2aWQ6MTIz' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 1fb20790-5969-4def-99fb-e181bd18792d' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIxZWRjZDQyNS03ZjJjLTQ3MmEtODgxNS0wZTUyYjQ1ZDcyMmEiLCJleHAiOjE1NDk1NDMyNDN9.QlN0fWG2eDXLQJisyHjSmtWHuK19nmu_e3uVDyya-lw' \
  -d '{"text":"David'\''s 2nd resource"}'
```

The resources are now:
```json
{
    "resources": [
        {
            "id": 1,
            "text": "resource",
            "user_id": 2
        },
        {
            "id": 4,
            "text": "Creating new resource",
            "user_id": 1
        },
        {
            "id": 5,
            "text": "newly added resource",
            "user_id": 3
        },
        {
            "id": 6,
            "text": "David's 2nd resource",
            "user_id": 2
        }
    ]
}
```

Now, user David tries to create another resource (when his quota is set to be 2). When posting the following command:
```bash
curl -X POST \
  http://127.0.0.1:5000/resource \
  -H 'Authorization: Basic RGF2aWQ6MTIz' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 5a73dc8c-7c6a-423d-bd3a-b1298a76e020' \
  -H 'cache-control: no-cache' \
  -H 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIxZWRjZDQyNS03ZjJjLTQ3MmEtODgxNS0wZTUyYjQ1ZDcyMmEiLCJleHAiOjE1NDk1NDMyNDN9.QlN0fWG2eDXLQJisyHjSmtWHuK19nmu_e3uVDyya-lw' \
  -d '{"text":"David'\''s 3rd resource"}'
```

The response is:
```json
{
    "message": "Invalid request: Resource quota reached."
}
```

The server does not allow the user to create any new resources (because the quota has exceeded)