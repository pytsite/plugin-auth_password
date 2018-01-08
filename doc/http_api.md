# PytSite Auth Password Plugin HTTP API


## POST auth/access-token/password

### Parameters

- *required* **str** `login`: user's login.
- *required* **str** `password`: user's password.

### Response Format

Is fully identical to response format of [POST auth/access-token](https://github.com/pytsite/plugin-auth_http_api/blob/master/doc/ru/http_api.md#post-authaccess-tokendriver)

### Examples

Request:

```
curl -X POST \
-d login='vasya@pupkeen.com' \
-d password='Very5tr0ngP@ssw0rd' \
https://test.com/api/3/auth/access-token/password
```


Response:

```
{
    "token": "e51081bc4632d8c2a31ac5bd8080af1b",
    "user_uid": "586aa6a0523af53799474d0d",
    "ttl": 86400,
    "created": "2017-01-25T14:04:35+0200",
    "expires": "2017-01-26T14:04:35+0200"
}
```


## POST auth/sign-in/password

Alias for **POST auth/access-token/password**.