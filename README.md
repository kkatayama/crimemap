# [Web Framework](#Web-Framework)
[https://crimemap.hopto.org](https://crimemap.hopto.org)

Framework is loosely modeled after CRUD: [C]reate [R]ead [U]pdate [D]elete

**Features:**
* [*User Functions*](#User-Functions) &nbsp;&nbsp; - [**`/login`**](#1-login), [**`/logout`**](#2-logout), [**`/register`**](#3-register)
* [*Admin Functions*](#Admin-Functions)            - [**`/createTable`**](#1-createTable), [**`/deleteTable`**](#2-deleteTable)
* [*Core Functions*](#Core-Functions) &nbsp;&nbsp; - [**`/add`**](#1-add), [**`/get`**](#2-get), [**`/edit`**](#3-edit), [**`/delete`**](4-delete)
* [*Extra_Functions*](#Extra-Functions) &nbsp;     - [**`/uploadImageUrl`**](#1-uploadImageUrl)
* Query and URL path parameter support
* Additional [**`filter`**](#notes-on-filter-option) parameter - enables SQLite expressions containing operators 
* In-place column editing with SQLite3 expression support
* [**`/get`**](#2-get), [**`/edit`**](#3-edit), [**`/delete`**](4-delete) supports single and multiple simultaneous table transactions
* Changes made to the **backend.db** database are now automatically updated to the GitHub repo in *real-time*

**Design Constrains:**
* All  **`table_names`** and **`column_names`** are defined with **lowercase** letters
* A column name with suffix **`_id`** reference a **unique item** or a **unique item group**.
* A column name with suffix **`_time`** reference a **unique datetime item**
* All tables must have a **`{ref}_id`** `column` to be used as `PRIMARY KEY`
* All tables must have a **`{ref}_time`** `column` 

**4 User Functions:**
1. [**`/login`**](#1-login) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Login a user
2. [**`/logout`**](#2-logout) &nbsp;&nbsp;&nbsp; - Logout a user
3. [**`/register`**](#3-register) - Register a new user
4. [**`/status`**](#4-status) &nbsp;&nbsp;&nbsp; - Verify signed session cookies

**2 Admin Functions**
1. [**`/createTable`**](#1-createTable) - Create a new `table` 
2. [**`/deleteTable`**](#2-deleteTable) - Delete an existing `table`

**4 Core Functions:**
1. [**`/add`**](#1-add) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Add a *single* entry to a `table`
2. [**`/get`**](#2-get) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Fetch a *single* entry or *multiple* entries from a `table`
3. [**`/edit`**](#3-edit) &nbsp;&nbsp;&nbsp; - Edit a *single* entry or *multiple* entries in a `table`
4. [**`/delete`**](#4-delete) - Delete a *single* entry or *multiple* entries from a `table`

**1 Extra Function**
1. [**`uploadImageUrl`**](#1-uploadImageUrl) - Upload an image to the backend via `image_url`

---

<details><summary>Debugging Tip! (click me to expand)</summary>
<p>

To see all of the available `tables` along with the `column_names` and the `column_types`, make a request to the root path of any `core` or `admin` function:

Request:
```ruby
https://api.crimemap.hopto.org/add
https://api.crimemap.hopto.org/get
https://api.crimemap.hopto.org/edit
https://api.crimemap.hopto.org/delete
https://api.crimemap.hopto.org/createTable
https://api.crimemap.hopto.org/deleteTable
```

Response:
```json
{ "message": "active tables in the database",
  "tables": [
    { "name": "users",
      "type": "table",
      "columns": [
        { "name": "user_id", "type": "INTEGER PRIMARY KEY" },
        { "name": "username", "type": "TEXT NOT NULL" },
        { "name": "password", "type": "TEXT NOT NULL" },
        { "name": "create_time", "type": "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))" }
      ]
    },
    { "name": "oximeter", 
      "type": "table",
      "columns": [
        { "name": "entry_id", "type": "INTEGER PRIMARY KEY" },
        { "name": "user_id", "type": "INTEGER NOT NULL" },
        { "name": "heart_rate", "type": "INTEGER NOT NULL" },
        { "name": "blood_o2", "type": "INTEGER NOT NULL" },
        { "name": "temperature", "type": "DOUBLE NOT NULL" },
        { "name": "entry_time", "type": "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))" }
      ]
    }
  ]
}
```

If you receive an `invalid token` response, then the request you are making does not contain the `session cookie`. <br />
**REQUESTS TO `/login` SHOULD BE DONE AS A `POST` REQUEST** <br />
The `session cookie` is assigned after a successful login. <br />
To get around adding the `session cookie` along with your request, you can simply add the `token` parameter. <br />

PLEASE LET ME KNOW IF YOU WISH TO DISABLE THE SESSION COOKIES AND TOKENS!!! <br />

FOR EXAMPLE:

### You logged in with the `admin` user doing a `GET` request:
Request:
```ruby
/login?username=admin&password=admin
```

Response:
```json
{
  "message": "user login success",
  "user_id": 1,
  "username": "admin",
  "token": "IVA1WTF3UDhOSHVacm1GUk1DRVVaMFE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09"
}
```

### But all of the requests return `invalid token`...?
Request:
```ruby
/add
```

Response:
```json
{
  "message": "invalid token"
}
```

### Simply append the token parameter to all requests
Request:
```ruby
/add?token=IVA1WTF3UDhOSHVacm1GUk1DRVVaMFE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09
```

Response:
```json
{ "message": "active tables in the database",
  "tables": [
    { "name": "users",
      "type": "table",
      "columns": [
        { "name": "user_id", "type": "INTEGER PRIMARY KEY" },
        { "name": "username", "type": "TEXT NOT NULL" },
        { "name": "password", "type": "TEXT NOT NULL" },
        { "name": "create_time", "type": "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))" }
      ]
    },
    { "name": "oximeter", 
      "type": "table",
      "columns": [
        { "name": "entry_id", "type": "INTEGER PRIMARY KEY" },
        { "name": "user_id", "type": "INTEGER NOT NULL" },
        { "name": "heart_rate", "type": "INTEGER NOT NULL" },
        { "name": "blood_o2", "type": "INTEGER NOT NULL" },
        { "name": "temperature", "type": "DOUBLE NOT NULL" },
        { "name": "entry_time", "type": "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))" }
      ]
    }
  ]
}
```

### When using `curl`, add `-b` and `-c` to save and read session cookies
``` ruby
curl -XPOST -b cookie.txt -c cookie.txt 'http://api.crimemap.hopto.org/login' -d '{"username": "admin", "password": "admin"}'
curl -b cookie.txt -c cookie.txt 'http://api.crimemap.hopto.org/get/users'
```
</p>
</details>

---

# [Getting Started](#Getting-Started)
Follow the [Setup Guide](SERVER_SETUP.md) to install and configure the framework. <br />

You can choose to run the server locally or connect with the server all ready running at: <br />
[https://api.crimemap.hopto.org](https://api.crimemap.hopto.org)

To interact with the framework (locally or remote) you will need to first login. <br />

I recommend starting with the [Workflows](#Workflows) provided to get comfortable with using this framework. <br />

## [Workflows](#Workflows):
- [ ] [Workflow 1 - Login](#Workflow-1---Login)
- [ ] [Workflow 2 - Register Users](#Workflow-2---Register-Users)
- [ ] [Workflow 3 - Creating Tables](#Workflow-3---Creating-Tables)
- [ ] [Workflow 4 - Inserting Data](#Workflow-4---Inserting-Data)
- [ ] [Workflow 5 - Requesting Data](#Workflow-5---Requesting-Data)
- [ ] [Workflow 6 - Editing Data](#Workflow-6---Editing-Data)
- [ ] [Workflow 7 - Deleting Data](#Workflow-7---Deleting-Data)

---

# [User Functions](#User-Functions)
The examples listed below will cover the **4 user functions**.<br />
All examples were executed with a **GET** request and can be tested in any browser. <br />
All endpoints support 4 *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

## 1. `/login`
**Login `user`** 
> NOTE: Only logged in users can call functions!
> NOTE: This request shold be a `POST` request.  Even though you can make a `GET` request, doing so may not store your `session cookie`! 

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/login
```
</td><td>

```rexx
return: {"message": "missing parameters"}
```
</td></tr><tr></tr><tr><td>

```jq
/login/<param_name>/<param_value>
```
</td><td>

```rexx
login with url_paths: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/login/param_name=param_value
```
</td><td>

```rexx
login with params: 'param_name=param_value'
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Description </td></tr><tr><td>

```rexx
username
```
</td><td>

```rexx
must match the users table
```
</td></tr><tr></tr><tr><td>

```rexx
password
```
</td><td>

```rexx
passwords are salted and pbkdf2 hmac sha256 hashed with 1000 iterations
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/login`
Request:
```ruby
/login
```

Response:
```json
{
  "message": "missing parameters", 
  "required": [{"username": "TEXT", "password": "TEXT"}], "submitted": [{}]
}
```

Arguments:
```python
username = admin
```

Request:
```ruby
/login/username/admin
```

Response:
```json
{
  "message": "missing parameters",
  "required": [{"username": "TEXT", "password": "TEXT"}],
  "submitted": [{"username": "admin"}]
}
```

Arguments:
```python
username = admin
password = 123
```

Request:
```ruby
/login?username=admin&password=123
```

Response:
```json
{
  "message": "incorrect password",
  "password": "123"
}
```

Arguments:
```python
username = admin
password = admin
```

Request:
```ruby
/login?username=admin&password=admin
```

Response:
```json
{
  "message": "user login success",
  "user_id": 1,
  "username": "admin",
  "token": "IVA1WTF3UDhOSHVacm1GUk1DRVVaMFE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09"
}
```
</details>

---

## [Workflow 1 - Login](#Workflow-1---Login)

<details><summary> (click here to expand) </summary>

### Let's log in as the user `admin`
Arguments:
```python
username = admin
password = admin
```

POST Request:
```ruby
POST(url='https://api.crimemap.hopto.org/login', data={"username": "admin", "password": "admin"})
```

Response:
```json
{
  "message": "user login success",
  "user_id": 1,
  "username": "admin",
  "token": "ITVIMUxRUitCTjdwYUwxbjdESWh3MHc9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09"
}
```

> Note: the `token` is only needed when api requests do not store session cookies.

### Verify session by making a request to `/status`
Request:
```jq
https://api.crimemap.hopto.org/status
```

Response:
```json

{
  "message": "user is logged in with valid session cookie",
  "user_id": "1",
  "cookies": {
    "user_id": "!5H1LQR+BN7paL1n7DIhw0w==?gAWVEQAAAAAAAACMB3VzZXJfaWSUjAExlIaULg=="
  }
}
```

</details>

---

## 2. `/logout`
Terminate a logged in session

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/logout
```
</td><td>

```rexx
delete the user's signed cookie session token
```
</td></tr>
</table>

### Response After Successful [`/logout`](#2-logout)
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
message
```
</td><td>

```rexx
'user logged out'
```
</td></tr><tr></tr><tr><td>

```rexx
user_id
```
</td><td>

```rexx
the user_id that was affiliated with the signed cookie session token 
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)
</summary>

### Investigating the Endpoint `/logout`
Request:
```ruby
/logout
```

Response:
```json
{
  "message": "user logged out",
  "user_id": "1"
}
```

</details>

---

## 3. `/register`
Register a new **`user`** to the `users` table.

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/register
```
</td><td>

```rexx
returns: {"message": "missing parameters", "required params": ["username", "password", "password2"]}
```
</td></tr><tr></tr><tr><td>

```jq
/register/usage
```
</td><td>

```rexx
returns: {"message": "usage_info"}
```
</td></tr><tr></tr><tr><td>

```jq
/register/<param_name>/<param_value>
```
</td><td>

```rexx
register with url_paths: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/register?param_name=param_value
```
</td><td>

```rexx
register with params: 'param_name=param_value'
```
</td></tr>
</table>

### Requirements:
<table>
<tr><td> Parameters </td><td> Description </td></tr><tr><td>

```rexx
username
```
</td><td>

```rexx
must be unique (not exist in users table)
```
</td></tr><tr></tr><tr><td>

```rexx
password
```
</td><td>

```rexx
must match password2
```
</td></tr><tr></tr><tr><td>

```rexx
password2
```
</td><td>

```rexx
must match password
```
</td></tr>
</table>


### Response After Successful [`/register`](#3-register)
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
message
```
</td><td>

```rexx
'new user created'
```
</td></tr><tr></tr><tr><td>

```rexx
user_id
```
</td><td>

```rexx
the {ref}_id for the user generated by PRIMARY_KEY of the users table
```
</td></tr><tr></tr><tr><td>

```rexx
username 
```
</td><td>

```rexx
user supplied paramater
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint `/register`
Request:
```ruby
/register
```

Response:
```json
{"message": "missing parameter", "required params": ["username", "password", "password2"]}
```

---

Request:
```ruby
/register/usage
```

Response:
```json
{
    "message": "usage info: /register",
    "description": "Register a new user to the [users] table",
    "end_points": {
        "/register": {"returns": "missing paramaters"},
        "/register/<param_name>/<param_value>": {
            "url_paths": "register with: \"param_name=param_value\"",
            "example": "/register/username/admin/password/admin",
            "response": {"message": "new user created", "user_id": 2, "username": "teddy"}
        },
        "/register?param_name=param_value": {
            "url_paths": "register with: \"param_name=param_value\"",
            "example": "/register?username=teddy&password=teddy&password2=teddy",
            "response": {"message": "new user created", "user_id": 2, "username": "teddy"}
        },
        "Required": {"Parameters": {"username": "TEXT", "password": "TEXT", "password2": "TEXT"}},
        "Response": {"message": "new user created", "user_id": "INTEGER", "username": "TEXT", "token": "TEXT"}
    }
}
```

---

Request:
```ruby
/register/username/teddy/password/teddy/password2/ted
```

Response:
```json
{"message": "passwords do not match", "password1": "teddy", "password2": "ted"}
```

---

Request:
```ruby
/register/username/teddy/password/teddy/password2/teddy
```

Response:
```json
{"message": "new user created", "user_id": 2, "username": "teddy"}
```

---

Request:
```ruby
/register?username=teddy&password=teddy&password2=teddy
```

Response:
```json
{"message": "user exists", "username": "teddy"}
```

</details>

---

## [Workflow 2 - Register Users](#Workflow-2---Register-Users)

<details><summary> (click here to expand) </summary>

### Let's create a few users by registering them: `alice`, `bob`, `anna`, `steve`
---

Arguments:
```rexx
username = alice
password = alice
password2 = alice
```

Request:
```jq
https://api.crimemap.hopto.org/register/username/alice/password/alice/password2/alice
```

Response:
```json
{"message": "new user created", "user_id": 2, "username": "alice"}
```
---

Arguments:
```rexx
username = bob
password = bob
password2 = bob
```

Request:
```jq
https://api.crimemap.hopto.org/register/username/bob/password/bob/password2/bob
```

Response:
```json
{"message": "new user created", "user_id": 3, "username": "bob"}
```
---

Arguments:
```rexx
username = anna
password = anna
password2 = anna
```

Request:
```jq
https://api.crimemap.hopto.org/register/username/anna/password/anna/password2/anna
```

Response:
```json
{"message": "new user created", "user_id": 4, "username": "anna"}
```
---

Arguments:
```rexx
username = steve
password = steve
password2 = steve
```

Request:
```jq
https://api.crimemap.hopto.org/register/username/steve/password/steve/password2/steve
```

Response:
```json

{
  "message": "new user created",
  "user_id": 5,
  "username": "steve"
}
```

</details>

---

## 4. `/status`
Verify signed cookie sessions

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/status
```
</td><td>

```rexx
Verify the session cookie is signed with a valid token
```
</td></tr>
</table>

### Response After Successful [`/status`](#2-logout)
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
message
```
</td><td>

```rexx
'user is logged in with valid session cookie'
```
</td></tr><tr></tr><tr><td>

```rexx
user_id
```
</td><td>

```rexx
'the user_id of the logged in user with a signed cookie session token' 
```
</td></tr><tr></tr><tr><td>

```rexx
cookies
```
</td><td>

```rexx
'the session token'
```
</td><tr>
</table>

---

# [Admin Functions](#Admin-Functions)
The examples listed below will cover the **2 admin functions**. <br />
All examples shown are executed via a **GET** request and can be tested with any browser. <br />
All endpoints support 4  *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

## 1. `/createTable`
**Create a new `table`**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/createTable
```
</td><td>

```rexx
returns a list of all existing tables in the database
```
</td></tr><tr></tr><tr><td>

```jq
/createTable/usage
```
</td><td>

```rexx
returns a message for how to use this function
```
</td></tr><tr></tr><tr><td>

```jq
/createTable/{table_name}
```
</td><td>

```rexx
debug: returns the required parameters
```
</td></tr><tr></tr><tr><td>

```jq
/createTable/{table_name}/{column_name}/{column_type}
```
</td><td>

```rexx
create a table with columns using path parameters
```
</td></tr><tr></tr><tr><td>

```erlang
/createTable/{table_name}?column_name=column_type
```
</td><td>

```rexx
create a table with columns using query parameters
```
</td></tr>
</table>

### Requirements:
<table>
</td></tr><tr><td> Parameters </td><td> Value </td></tr><tr><td>

```rexx
{ref}_id
```
</td><td>

```rexx
INTEGER - to be used as the PRIMARY_KEY for the table where the ID is automatically created
```
</td></tr><tr></tr><tr><td>

```rexx
{ref}_time
```
</td><td>

```rexx
DATETIME - autogenerated date-timestamp assigned with every table entry transaction 
```
</td></tr><tr></tr><tr><td>

```rexx
column_name 
```
</td><td>

```rexx
categorical reference to data - should only consist of underscore and lowercase letters 
```
</td></tr><tr></tr><tr><td>

```rexx
column_type
```
</td><td>

```rexx
currently impleted data types: INTEGER, DOUBLE, TEXT, DATETIME
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/createTable`
The endpoint for creating a **`table`** with a **`table_name`** is **`/createTable/{table_name}`**. <br />
Making a request to the endpoint without providing **parameters** returns a `missing parameters` message:

Request:
```ruby
/createTable/steps
```

Response:
```json
{
    "message": "missing paramaters",
    "required": [
        {
            "user_id": "INTEGER",
            "{ref}_id": "INTEGER",
            "{ref}_time": "DATETIME",
            "column_name": "column_type",
            "available_types": ["INTEGER", "DOUBLE", "TEXT", "DATETIME"]
        }
    ],
    "available_types": ["INTEGER", "DOUBLE", "TEXT", "DATETIME"],
    "Exception": "\"{ref}_id\" not required when creating \"users\" table",
    "submitted": []
}
```

### Creating the Table `steps`
Arguments:
```python
step_id    = INTEGER
user_id    = INTEGER
step_count = INTEGER
latitude   = DOUBLE
longitude  = DOUBLE
step_time  = DATETIME
```

Request:
```ruby
/createTable/steps/step_id/INTEGER/user_id/INTEGER/step_count/INTEGER/latitude/DOUBLE/longitude/DOUBLE/step_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "steps",
    "columns": [
        "step_id INTEGER PRIMARY KEY",
        "user_id INTEGER NOT NULL",
        "step_count INTEGER NOT NULL",
        "latitude DOUBLE NOT NULL",
        "longitude DOUBLE NOT NULL",
        "step_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
    ]
}
```

### Creating the Table `oximeter`
Arguments:
```python
entry_id    = INTEGER
user_id     = INTEGER
heart_rate  = INTEGER
blood_o2    = INTEGER
temperature = DOUBLE
entry_time  = DATETIME
```

Request:
```ruby
/createTable/oximeter/entry_id/INTEGER/user_id/INTEGER/heart_rate/INTEGER/blood_o2/INTEGER/temperature/DOUBLE/entry_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "oximeter",
    "columns": [
        "entry_id    INTEGER PRIMARY KEY",
        "user_id     INTEGER NOT NULL",
        "heart_rate  INTEGER NOT NULL",
        "blood_o2    INTEGER NOT NULL",
        "temperature DOUBLE NOT NULL",
        "entry_time  DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
    ]
}
```



</details>

---

## [Workflow 3 - Creating Tables](#Workflow-3---Creating-Tables)

<details><summary> (click here to expand) </summary>

### Let's create a few tables!<br />
<table>
<tr><td> Table Name </td><td> Table Description </td><td> Column Names </td></tr><tr><td>

```rexx
user_profiles
```
</td><td>

```css
profiles for the users in the users table
```
</td><td>

```jq
["entry_id", "user_id", "name", "email", "profile_pic", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
incidents
```
</td><td>

```css
incidents scraped from www.crimemapping.com
```
</td><td>

```jq
["entry_id", "tier", "type", "type_img", "description", "location", "latitude", "longitude", "agency", "report_date", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
sex_offenders
```
</td><td>

```css
offenders scraped from sexoffender.dsp.delaware.gov
```
</td><td>

```jq
["entry_id", "tier", "name", "dob", "arrest_description", "arrest_date", "victim_age", "home_address", "home_latitude", "home_longitude", "work_name", "work_address", "work_latitude", "work_longitude", "entry_time"]
```
</td></tr>
</table>

---

### Creating the Table `user_profiles`:
Arguments:
```rexx
user_profiles = entry_id/INTEGER/INTEGER/TEXT/TEXT/TEXT/DATETIME
```

Request:
```jq
https://api.crimemap.hopto.org/createTable/user_profiles/entry_id/INTEGER/user_id/INTEGER/name/TEXT/email/TEXT/profile_pic/TEXT/entry_time/DATETIME
```

Response:
```json
{
  "message": "1 table created",
  "table": "user_profiles",
  "columns": [
    "entry_id INTEGER PRIMARY KEY",
    "user_id INTEGER NOT NULL",
    "name TEXT NOT NULL",
    "email TEXT NOT NULL",
    "profile_pic TEXT NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))"
  ],
}
```

### Creating the Table `incidents`:
Arguments:
```rexx
entry_id = INTEGER
tier = INTEGER
type = TEXT
type_img = TEXT
description = TEXT
location = TEXT
latitude = DOUBLE
longitude = DOUBLE
agency = TEXT
report_date = DATETIME
entry_time = DATETIME
```

Request:
```jq
https://api.crimemap.hopto.org/createTable/incidents/entry_id/INTEGER/tier/INTEGER/type/TEXT/type_img/TEXT/description/TEXT/location/TEXT/latitude/DOUBLE/longitude/DOUBLE/agency/TEXT/report_date/DATETIME/entry_time/DATETIME
```

Response:
```json

{
  "message": "1 table created",
  "table": "incidents",
  "columns": [
    "entry_id INTEGER PRIMARY KEY",
    "tier INTEGER NOT NULL",
    "type TEXT NOT NULL",
    "type_img TEXT NOT NULL",
    "description TEXT NOT NULL",
    "location TEXT NOT NULL",
    "latitude DOUBLE NOT NULL",
    "longitude DOUBLE NOT NULL",
    "agency TEXT NOT NULL",
    "report_date DATETIME NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))"
  ]
}
```

### Creating the Table `sex_offenders`:
Arguments:
```rexx
entry_id = INTEGER
tier = INTEGER
name = TEXT
dob = DATETIME
arrest_description = TEXT
arrest_date = DATETIME
victim_age = TEXT
home_address = TEXT
home_latitude = DOUBLE
home_longitude = DOUBLE
work_name = TEXT
work_address = TEXT
work_latitude = DOUBLE
work_longitude = DOUBLE
entry_time = DATETIME
```

Request:
```jq
https://api.crimemap.hopto.org/createTable/sex_offenders/entry_id/INTEGER/tier/INTEGER/name/TEXT/dob/DATETIME/arrest_description/TEXT/arrest_date/DATETIME/victim_age/TEXT/home_address/TEXT/home_latitude/DOUBLE/home_longitude/DOUBLE/work_name/TEXT/work_address/TEXT/work_latitude/DOUBLE/work_longitude/DOUBLE/entry_time/DATETIME
```

Response:
```json

{
  "message": "1 table created",
  "table": "sex_offenders",
  "columns": [
    "entry_id INTEGER PRIMARY KEY",
    "tier INTEGER NOT NULL",
    "name TEXT NOT NULL",
    "dob DATETIME NOT NULL",
    "arrest_description TEXT NOT NULL",
    "arrest_date DATETIME NOT NULL",
    "victim_age TEXT NOT NULL",
    "home_address TEXT NOT NULL",
    "home_latitude DOUBLE NOT NULL",
    "home_longitude DOUBLE NOT NULL",
    "work_name TEXT NOT NULL",
    "work_address TEXT NOT NULL",
    "work_latitude DOUBLE NOT NULL",
    "work_longitude DOUBLE NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))"
  ]
}
```

</details>

---


## 2. `/deleteTable`
**Delete `table`**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/deleteTable
```
</td><td>

```rexx
returns a list of all existing tables in the database
```
</td></tr><tr></tr><tr><td>

```jq
/deleteTable/usage
```
</td><td>

```rexx
returns a message for how to use this function
```
</td></tr><tr></tr><tr><td>

```jq
/deleteTable/{table_name}
```
</td><td>

```rexx
debug: returns the required parameters
```
</td></tr>
</table>

### Requirements:
<table>
<tr><td> Parameters </td><td> Description </td></tr><tr><td>

```rexx
table_name
```
</td><td>

```rexx
the name of the table you wish to delete
```
</td></tr>
</table>

---

<details>
<summary>Endpoint Background (click here to expand)</summary>



### Investigating the Endpoint: `/deleteTable`
The endpoint for deleting a **`table`** with a **`table_name`** is **`/deleteTable/{table_name}`**.

### Let's Delete the Table `steps`
Request:
```ruby
/deleteTable/steps
```

Response:
```json
{"message": "1 table deleted!", "table": "steps"}
```

Verify the **`steps`**** table no longer exists

Request:
```ruby
/deleteTable
```

Response:
```json
{
    "message": "active tables in the database",
    "tables": [
        {
            "name": "users",
            "type": "table",
            "columns": [
                {"name": "user_id", "type": "INTEGER PRIMARY KEY"},
                {"name": "username", "type": "TEXT NOT NULL"},
                {"name": "password", "type": "TEXT NOT NULL"},
                {"name": "create_time", "type": "DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"}
            ]
        },
        {
            "name": "oximeter",
            "type": "table",
            "columns": [
                {"name": "entry_id", "type": "INTEGER PRIMARY KEY"},
                {"name": "user_id", "type": "INTEGER NOT NULL"},
                {"name": "heart_rate", "type": "INTEGER NOT NULL"},
                {"name": "blood_o2", "type": "INTEGER NOT NULL"},
                {"name": "temperature", "type": "DOUBLE NOT NULL"},
                {"name": "entry_time", "type": "DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"}
            ]
        }
    ]
}
```
</details> 

---

# [Core Functions](#Core-Functions)
All examples shown are executed via a **GET** request and can be tested with any browser. <br />
All endpoints support 4 *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE** <br />

## 1. `/add`
**Add a *single* entry to a `table`**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/add
```
</td><td>

```rexx
returns all tables[] in the database
```
</td></tr><tr></tr><tr><td>

```jq
/add/usage
```
</td><td>

```rexx
returns message: 'usage info'
```
</td></tr><tr></tr><tr><td>

```jq
/add/{table_name}
```
</td><td>

```rexx
returns message: 'missing parameters'
```
</td></tr><tr></tr><tr><td>

```jq
/add/{table_name}/{param_name}/{param_value}
```
</td><td>

```rexx
add entry: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/add/{table_name}?param_name=param_value
```
</td><td>

```rexx
add entry: 'param_name=param_value'
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Exception </td></tr><tr><td>

```rexx
All params not {ref}_id or {ref}_time
```
</td><td>

```rexx
{ref}_id required when not PRIMARY KEY
```
</td></tr>
</table>

### Response After Successful [`/add`](#1-add):
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
user_id
```
</td><td>

```rexx
when entry added to users table
```
</td></tr><tr></tr><tr><td>

```rexx
{ref}_id
```
</td><td>

```rexx
when entry added to any other table
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)
</summary>

### Investigating the Endpoint: `/add`
The endpoint for adding a user to the **`users`** table is **`/add/users`**.
Making a request to the endpoint without providing **parameters** returns a `missing parameters` message:

Request:
```ruby
/add/users
```

Response:
```json
{
  "message": "missing parameters", 
  "required": [{"username": "TEXT", "password": "TEXT"}], 
  "missing": [{"username": "TEXT", "password": "TEXT"}], 
  "submitted": [{}]
}
```

Making a request with only 1 of the 2 **required_parameters** updates the `missing parameters` message:

Request:
```ruby
/add/users/username/alice
```

Response:
```json
{
  "message": "missing parameters",
  "required": [{"username": "TEXT", "password": "TEXT"}],
  "missing": [{"password": "TEXT"}],
  "submitted": [{"username": "alice"}]
}
```

### Adding `alice` to the **`users`** table
To add the user `alice`, we need to provide the **username** and **password** parameters
There are several ways to do this: using **url_parameters**, **query_parameters**, or a combination of both.

**Recommended Method: Using URL_Parameters**
```ruby
/add/users/username/alice/password/alice
```
Response:
```json
{
  "message": "data added to {users}",
  "user_id": 7
}
```

*Alternative Methods: Any of these will work but the format may get confusing when using the other **core functions***
```ruby
/add/users?username=alice&password=alice
/add/users/username/alice?password=alice
/add/users/password=alice?username=alice
```

Attempting to add the existing user `alice` will respond with a `user exists` message:

Request
```ruby
/add/users/username/alice/password/alice
```
Response:
```json
{
  "message": "user exists",
  "username": "alice"
}
```

### Adding `bob` to the **`users`** table
Request:
```ruby
/add/users/username/bob/password/bob
```
Response:
```json
{
  "message": "data added to {users}",
  "user_id": 8
}
```

### Adding sensor data for the user `alice` to the **`oximeter`** table
When we added the user `alice` to the **`users`** table, we were provided with the **`user_id = 7`** 
To get the required parameters for adding an `entry` to the **`oximeter`**, make a request without parameters:

Request:
```ruby
/add/oximeter
```

Response:
```json
{
    "message": "missing parameters",
    "required": [{"user_id": "INTEGER", "heart_rate": "INTEGER", "blood_o2": "INTEGER", "temperature": "DOUBLE"}],
    "missing": [{"user_id": "INTEGER", "heart_rate": "INTEGER", "blood_o2": "INTEGER", "temperature": "DOUBLE"}],
    "submitted": [{}]
}
```

Let's add some sensor data for the user `alice` to the **`oximeter`** table by making the following requests:

Request:
```ruby
/add/oximeter/user_id/7/heart_rate/134/blood_o2/97/temperature/97.6691638391727
/add/oximeter/user_id/7/heart_rate/129/blood_o2/98/temperature/97.45331222228752
/add/oximeter/user_id/7/heart_rate/128/blood_o2/100/temperature/97.35755335543793
/add/oximeter/user_id/7/heart_rate/134/blood_o2/96/temperature/97.03691402965539
/add/oximeter/user_id/7/heart_rate/132/blood_o2/96/temperature/97.78609598543946
/add/oximeter/user_id/7/heart_rate/130/blood_o2/98/temperature/97.262831668111
```

Each request had a unique response:
Response:
```json
{"message": "data added to {oximeter}", "entry_id": 43, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 44, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 45, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 46, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 47, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 48, "user_id": "7"}
```

Now let's add some sensor data for the user `bob` to the **`oximeter`** table by making the following requests:

Request:
```ruby
/add/oximeter/user_id/8/heart_rate/143/blood_o2/97/temperature/97.23579109761334
/add/oximeter/user_id/8/heart_rate/127/blood_o2/97/temperature/97.7532770488335
/add/oximeter/user_id/8/heart_rate/131/blood_o2/95/temperature/97.89202180155488
/add/oximeter/user_id/8/heart_rate/124/blood_o2/95/temperature/97.81020200542864
/add/oximeter/user_id/8/heart_rate/133/blood_o2/95/temperature/101.7115308733577
/add/oximeter/user_id/8/heart_rate/133/blood_o2/100/temperature/103.10357503270177
/add/oximeter/user_id/8/heart_rate/144/blood_o2/98/temperature/103.35133621760384
/add/oximeter/user_id/8/heart_rate/134/blood_o2/98/temperature/102.16442367992002
/add/oximeter/user_id/8/heart_rate/132/blood_o2/98/temperature/101.79215076652413
/add/oximeter/user_id/8/heart_rate/130/blood_o2/99/temperature/102.76488036781804
```

Response:
```json
{"message": "data added to {oximeter}", "entry_id": 49, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 50, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 51, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 52, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 53, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 54, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 55, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 56, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 57, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 58, "user_id": "8"}
```

</details>

---

## [Workflow 4 - Inserting Data](#Workflow-Example-4---Inserting-Data)

<details><summary> (click here to expand) </summary>

### Adding `users` to `user_profiles`
1. For each `user` in the `users` table, upload a `profile_pic` and add to `user_profiles` table

### Adding `incidents` from [www.crimemapping.com](www.crimemapping.com)
2. Describe the `crimemapping.py` script
3. Demo the `crimemapping_to_pandas.py` script
4. Demo a manual entry to the `incidents` table

### Adding `sex_offenders` from [sexoffender.dsp.delaware.gov](sexoffender.dsp.delaware.gov)
5. Describe the `sexoffender.py` script
6. Demo the `sexoffender_to_pandas.py` script
7. Demo a manual entry to the `sex_offenders` table

---

### 4.1 For each `user` in the `users` table, upload a `profile_pic` and add to `user_profiles` table

<details><summary> (click here to expand) </summary>

---
First, let's examine the `users` table:

Request:
```jq
https://api.crimemap.hopto.org/get/users
```

Response:
```json
{
  "message": "found 5 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "756a404bd66b7f081a936fe6fbcf2374de5c6ce018d62f37e664be8df02de03807b51fc4273dc06d12c11f7075369b5e96e2b0fef57037f6711f7e0f07a224af", "create_time": "2022-10-28 09:34:39.683"},
    {"user_id": 2, "username": "alice", "password": "1d5f25f69d22e57f92408247a304ab513e32791505c3f4eb878b732fb87d78c5dab7f5f46766e2fd7f2167f395829fd37feb7e8a773352830f70b5eeeef6d809", "create_time": "2022-11-15 22:52:22.768"},
    {"user_id": 3, "username": "bob", "password": "541803a1dc5e1e822dc34cecfc43bb634c9604bb612e65e1b02ee1a239a2aac5d3605469e24418dc327eb9f66af74ce9fd127ae8b50246e43497e3efce73dfe2", "create_time": "2022-11-15 22:52:23.082"},
    {"user_id": 4, "username": "anna", "password": "584a56a0c3e0b750b3b6ae320efb6004bdb73e5e06c455f1ede9d750ec6a0329c9b7fb0b2c36838728e68fea2327fddbb4cc34a17412dfd24730f4c2cf77cdb1", "create_time": "2022-11-15 22:52:23.185"},
    {"user_id": 5, "username": "steve", "password": "be93fe20d457f6d23539baf51e8c2fb9e38ae9232d8a2ae04e45e60e2c0e019d5cd56a380611046f9c904dfaf47f725b87a6dc1b84c8b9cf4e15b03e8f30ddd6", "create_time": "2022-11-15 22:52:23.343"},
  ],
}
```
---
#### Uploading profile picture for `admin`
Arguments:
```rexx
url = https://www.shutterstock.com/image-vector/user-icon-vector-260nw-393536320.jpg
```

Request:
```erlang
https://api.crimemap.hopto.org/uploadImageUrl?url=https://www.shutterstock.com/image-vector/user-icon-vector-260nw-393536320.jpg
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.shutterstock.com/image-vector/user-icon-vector-260nw-393536320.jpg",
  "full_path": "/static/img/19.jpg",
  "file_name": "19.jpg",
}
```
---
#### Adding `admin` to `user_profiles` table
> Note: `admin` has a `user_id` of `1` in the `users` table

Arguments:
```rexx
user_id = 1
name = Administrator
email = admin@udel.edu
profile_pic = 19.jpg
```

Request:
```jq
https://api.crimemap.hopto.org/add/user_profiles/user_id/1/name/Administrator/email/admin@udel.edu/profile_pic/19.jpg
```

Response:
```json
{
  "message": "data added to <user_profiles>",
  "entry_id": "1",
  "user_id": "1",
}
```
---
#### Uploading profile picture for `alice`
Arguments:
```rexx
url = https://www.w3schools.com/w3images/avatar4.png
```

Request:
```erlang
https://api.crimemap.hopto.org/uploadImageUrl?url=https://www.w3schools.com/w3images/avatar4.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.w3schools.com/w3images/avatar4.png",
  "full_path": "/static/img/20.png",
  "file_name": "20.png",
}
```
#### Adding `alice` to `user_profiles` table
Arguments:
```rexx
user_id = 2
name = Alice Smith
email = alice@udel.edu
profile_pic = 20.png
```

Request:
```jq
https://api.crimemap.hopto.org/add/user_profiles/user_id/2/name/Alice Smith/email/alice@udel.edu/profile_pic/20.png
```

Response:
```json
{
  "message": "data added to <user_profiles>",
  "entry_id": "2",
  "user_id": "2",
}
```
---
#### Uploading profile picture for `bob`
Arguments:
```rexx
url = https://www.w3schools.com/w3images/avatar2.png
```

Request:
```erlang
https://api.crimemap.hopto.org/uploadImageUrl?url=https://www.w3schools.com/w3images/avatar2.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.w3schools.com/w3images/avatar2.png",
  "full_path": "/static/img/21.png",
  "file_name": "21.png",
}
```
#### Adding `bob` to `user_profiles` table
Arguments:
```rexx
user_id = 3
name = Bob Smith
email = bob@udel.edu
profile_pic = 21.png
```

Request:
```jq
https://api.crimemap.hopto.org/add/user_profiles/user_id/3/name/Bob Smith/email/bob@udel.edu/profile_pic/21.png
```

Response:
```json
{
  "message": "data added to <user_profiles>",
  "entry_id": "3",
  "user_id": "3",
}
```
---
#### Uploading profile picture for `anna`
Arguments:
```rexx
url = https://www.w3schools.com/w3images/avatar5.png
```

Request:
```erlang
https://api.crimemap.hopto.org/uploadImageUrl?url=https://www.w3schools.com/w3images/avatar5.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.w3schools.com/w3images/avatar5.png",
  "full_path": "/static/img/22.png",
  "file_name": "22.png",
}
```
#### Adding `anna` to `user_profiles` table
Arguments:
```rexx
user_id = 4
name = Anna Williams
email = anna@udel.edu
profile_pic = 22.png
```

Request:
```jq
https://api.crimemap.hopto.org/add/user_profiles/user_id/4/name/Anna Williams/email/anna@udel.edu/profile_pic/22.png
```

Response:
```json
{
  "message": "data added to <user_profiles>",
  "entry_id": "4",
  "user_id": "4",
}
```
---
#### Uploading profile picture for `steve`
Arguments:
```rexx
url = https://www.w3schools.com/w3images/avatar3.png
```

Request:
```erlang
https://api.crimemap.hopto.org/uploadImageUrl?url=https://www.w3schools.com/w3images/avatar3.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.w3schools.com/w3images/avatar3.png",
  "full_path": "/static/img/23.png",
  "file_name": "23.png",
}
```
#### Adding `steve` to `user_profiles` table
Arguments:
```rexx
user_id = 5
name = Steve Williams
email = steve@udel.edu
profile_pic = 23.png
```

Request:
```jq
https://api.crimemap.hopto.org/add/user_profiles/user_id/5/name/Steve Williams/email/steve@udel.edu/profile_pic/23.png
```

Response:
```json
{
  "message": "data added to <user_profiles>",
  "entry_id": "5",
  "user_id": "5",
}
```

</details>

---

### 4.2 Describe the `crimemapping.py` script
<details><summary> (click here to expand) </summary>

---
The script `scrapers/crimemapping.py` was used to automate the scraping of `crimemapping.com` data. <br />
This data was then uploaded to the `incidents` table. <br />
To use this script, first navigate to the `scrapers` directory:
```rexx
cd scrapers
```

Then use `python3` to run the script. <br />
For example:
```rexx
python3 crimemapping.py --help
```
outputs:
```rexx
usage: crimemapping.py [-h] [--init] [--update]

options:
  -h, --help  show this help message and exit
  --init      scrape and upload entire history of incidents
  --update    scrape and upload latest incidents
```

To scrape and upload the entire history of incidents:
> NOTE: THIS HAS ALL READY BEEN DONE!
> YOU DO NOT NEED TO RUN THIS COMMAND.
> DOING SO ON A NON-EMPTY BACKEND DATABASE WILL RESULT WITH DUPLICATE ENTRIES...

```rexx
python3 crimemapping.py --init
```
outputs:
``` rexx
Processing Incidents... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Uploading Incidents... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

To fetch and upload only the latest incidents:
> NOTE: YOU SHOULD RUN THIS ONCE DAILY

```rexx
python3 crimemapping.py --upload
```
outputs:
``` rexx
Processing Incidents... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
{'tier': 1, 'type': 'Vandalism', 'type_img': '13.svg', 'description': 'LARCENY/SHOPLIFTING', 'location': '200 BLOCK S. MAIN ST', 'latitude': (39.67787000000004,), 'longitude': (-75.76204999999997,), 'agency': 'Newark Police', 'report_date': '2022-11-22 01:57:00'}
Uploading Latest Incidents... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

</details>

### 4.3 Demo the `crimemapping_to_pandas.py` script
<details><summary> (click here to expand) </summary>

---
The script `scrapers/crimemapping_to_pandas.py` demonstrates how to use pandas with the `incidents` table. <br />
To use this script, first navigate to the `scrapers` directory:
```rexx
cd scrapers
```

Then use `python3` to run the script. <br />
For example:
```rexx
python3 crimemapping_to_pandas.py
```
outputs:
```rexx
https://api.crimemap.hopto.org/get/incidents

message: found 753 incident entries

=== FIRST 10 INCIDENTS ===
   entry_id  tier                        type type_img                               description                     location  latitude  longitude                 agency         report_date              entry_time
0         1     1                   Vandalism   13.svg                     LARCENY/FROM BUILDING        100 BLOCK SUBURBAN DR  39.66671  -75.77605          Newark Police 2022-07-01 17:43:00 2022-11-18 18:21:39.315
1         2     1                         DUI    6.svg           POSSESSION OF AN OPEN CONTAINER       200 BLOCK E E. MAIN ST  39.68363  -75.74546          Newark Police 2022-07-01 19:02:00 2022-11-18 18:21:39.438
2         3     1  Drugs / Alcohol Violations    5.svg      DISTURBING THE PEACE/PUBLIC NUISANCE       000 BLOCK PROSPECT AVE  39.68685  -75.75333          Newark Police 2022-07-02 01:33:00 2022-11-18 18:21:39.560
3         4     1                     Weapons   15.svg         LARCENY/FROM VEHICLE/NOT ATTACHED  300 BLOCK CHRISTINA MILL DR  39.66978  -75.77437          Newark Police 2022-07-03 07:17:00 2022-11-18 18:21:39.703
4         5     1                         DUI    6.svg           POSSESSION OF AN OPEN CONTAINER           000 BLOCK BENNY ST  39.67711  -75.74543          Newark Police 2022-07-04 18:34:00 2022-11-18 18:21:39.862
5         6     1  Drugs / Alcohol Violations    5.svg    DISORDERLY CONDUCT/UNRELATED TO LIQUOR         000 BLOCK E. MAIN ST  39.68310  -75.75230          Newark Police 2022-07-05 00:57:00 2022-11-18 18:21:39.959
6         7     1                   Vandalism   13.svg  LARCENY/VEHICLE PARTS/FROM AUTO/ATTACHED        900 BLOCK E CHAPEL ST  39.66115  -75.73585  Delaware State Police 2022-07-05 07:51:00 2022-11-18 18:21:40.084
7         8     1  Drugs / Alcohol Violations    5.svg      DISTURBING THE PEACE/PUBLIC NUISANCE        3100 BLOCK WOOLEN WAY  39.68855  -75.74660          Newark Police 2022-07-05 18:20:00 2022-11-18 18:21:40.199
8         9     1  Drugs / Alcohol Violations    5.svg      DISTURBING THE PEACE/PUBLIC NUISANCE    000 BLOCK NW O DANIEL AVE  39.67424  -75.77022          Newark Police 2022-07-06 20:37:00 2022-11-18 18:21:40.291
9        10     1                   Vandalism   13.svg                     LARCENY/FROM BUILDING      600 BLOCK W OGLETOWN RD  39.68526  -75.73346          Newark Police 2022-07-06 21:19:00 2022-11-18 18:21:40.380
=== LATEST 10 INCIDENTS ===
     entry_id  tier                        type type_img                                       description                 location  latitude  longitude         agency         report_date              entry_time
752       753     1                   Vandalism   13.svg                               LARCENY/SHOPLIFTING     200 BLOCK S. MAIN ST  39.67787  -75.76205  Newark Police 2022-11-22 01:57:00 2022-11-22 18:55:00.542
751       752     1                   Vandalism   13.svg                                  LARCENY/BICYCLES    3300 BLOCK WOOLEN WAY  39.68811  -75.74615  Newark Police 2022-11-21 22:37:00 2022-11-22 18:55:00.455
750       751     1                    Burglary    3.svg  AGGRAVATED ASSAULT/FAMILY OTHER DANGEROUS WEAPON  800 BLOCK S COLLEGE AVE  39.65399  -75.75099  Newark Police 2022-11-21 21:12:00 2022-11-22 18:55:00.366
749       750     1                   Vandalism   13.svg                               LARCENY/SHOPLIFTING  200 BLOCK SW S. MAIN ST  39.67795  -75.76197  Newark Police 2022-11-21 00:31:00 2022-11-22 18:55:00.277
748       749     1                     Weapons   15.svg                 LARCENY/FROM VEHICLE/NOT ATTACHED  300 BLOCK E CANNONS WAY  39.65701  -75.74722  Newark Police 2022-11-20 18:58:00 2022-11-22 18:55:00.179
747       748     1                   Vandalism   13.svg                               LARCENY/SHOPLIFTING  400 BLOCK NEW LONDON RD  39.69415  -75.76453  Newark Police 2022-11-20 15:03:00 2022-11-22 18:55:00.078
746       747     1  Drugs / Alcohol Violations    5.svg              DISTURBING THE PEACE/PUBLIC NUISANCE    000 BLOCK NE BRIAR LA  39.68639  -75.76848  Newark Police 2022-11-20 10:08:00 2022-11-22 18:54:59.977
745       746     1                   Vandalism   13.svg          LARCENY/VEHICLE PARTS/FROM AUTO/ATTACHED  600 BLOCK N COLLEGE AVE  39.65978  -75.75191  Newark Police 2022-11-20 09:38:00 2022-11-22 18:54:59.867
744       745     1                         DUI    6.svg             DISORDERLY CONDUCT/LIQUOR INVOLVEMENT    1200 BLOCK WOOLEN WAY  39.68871  -75.74676  Newark Police 2022-11-20 03:09:00 2022-11-22 18:54:59.756
743       744     1    Vehicle Break-In / Theft   14.svg                           DAMAGE/PRIVATE PROPERTY       100 BLOCK GROVE LA  39.68435  -75.73479  Newark Police 2022-11-19 15:38:00 2022-11-22 18:54:59.643
```

</details>

### 4.4 Demo a manual entry to the `incidents` table
<details><summary> (click here to expand) </summary>

---
To manually add an `incident` entry to the `incidents` table, we use the endpoint `/add/<table_name>` <br/>

Arguments:
```rexx
tier = 1
type = Vandalism
type_img = 13.svg
description = LARCENY/SHOPLIFTING
location = 200 BLOCK S. MAIN ST
latitude = 39.67787000000004
longitude = -75.76204999999997
agency = Newark Police
report_date = 2022-11-22 01:57:00
```

Request:
```erlang
https://api.crimemap.hopto.org/add/incidents?tier=1&type=Vandalism&type_img=13.svg&description=LARCENY/SHOPLIFTING&location=200 BLOCK S. MAIN ST&latitude=39.67787000000004&longitude=-75.76204999999997&agency=Newark
Police&report_date=2022-11-22 01:57:00
```

Response:
```json
{
  "message": "data added to <incidents>",
  "entry_id": "753",
}
```

</details>

### 4.5 Describe the `sexoffender.py` script
<details><summary> (click here to expand) </summary>

---
The script `scrapers/sexoffender.py` was used to automate the scraping of `sexoffender.dsp.delaware.gov` data. <br />
This data was then uploaded to the `sex_offenders` table. <br />
To use this script, first navigate to the `scrapers` directory:
```rexx
cd scrapers
```

Then use `python3` to run the script. <br />
For example:
```rexx
python3 sexoffender.py --help
```
outputs:
```rexx
usage: sexoffender.py [-h] [--init] [--update]

options:
  -h, --help  show this help message and exit
  --init      scrape and upload entire history of sex offenders
  --update    NOT FINISHED YET...
```

To scrape and upload the entire history of sex offenders:
> NOTE: THIS HAS ALL READY BEEN DONE!
> YOU DO NOT NEED TO RUN THIS COMMAND.
> DOING SO ON A NON-EMPTY BACKEND DATABASE WILL RESULT WITH DUPLICATE ENTRIES...

```rexx
python3 sexoffender.py --init
```
outputs:
``` rexx
Processing Sex Offenders... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Uploading Sex Offenders... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

</details>

### 4.6 Demo the `sexoffender_to_pandas.py` script
<details><summary> (click here to expand) </summary>

--
The script `scrapers/sexoffender_to_pandas.py` demonstrates how to use pandas with the `sex_offenders` table. <br />
To use this script, first navigate to the `scrapers` directory:
```rexx
cd scrapers
```

Then use `python3` to run the script. <br />
For example:
```rexx
python3 sexoffender_to_pandas.py
```
outputs:
```rexx
https://api.crimemap.hopto.org/get/sex_offenders

message: found 61 sex_offender entries

=== ARREST INFO ===
   tier               name        dob                                 arrest_description arrest_date victim_age
0     3    MARIO DITOMASSO 1982-12-02  UNLAWFUL SEXUAL INTERCOURSE FIRST DEGREE-VICTI...  1997-08-28     1-11yr
1     2        JAMES BROWN 1983-05-19  UNLAWFUL SEXUAL CONTACT SECOND DEGREE - HAVE S...  1997-08-19     1-11yr
2     3   MOHAMAD ALIAHMED 1980-05-26  Sexual Abuse of a child by a person of trust 1...  2012-01-25    12-15yr
3     2      JOHN HOLTZMAN 1958-03-14  UNLAWFUL SEXUAL INTERCOURSE THIRD DEGREE-WITHO...  1999-02-04    12-15yr
4     2       JUSTIN LOGUE 1981-01-28  UNLAWFUL SEXUAL CONTACT SECOND DEGREE - HAVE S...  1997-06-17     1-11yr
5     2    GEORGE BROOMALL 1944-04-10  SEXUAL SOLICITATION OF A CHILD UNDER 16 YEARS ...  2002-01-28    12-15yr
6     2     ROBERT JACKSON 1953-06-24  UNLAWFUL SEXUAL INTERCOURSE THIRD DEGREE-VICTI...  1995-06-29      18+yr
7     3  RICHARD DESHIELDS 1963-10-14  UNLAWFUL SEXUAL INTERCOURSE FIRST DEGREE-NOT C...  1991-10-17    12-15yr
8     2      BRANDON SMITH 1974-03-27  UNLAWFUL SEXUAL INTERCOURSE THIRD DEGREE-VICTI...  1996-03-20    12-15yr
9     2      DWAYNE KEENAN 1976-07-06  UNLAWFUL SEXUAL CONTACT SECOND DEGREE HAVE SEX...  2009-08-10     1-11yr
=== ADDRESS INFO ===
   tier               name         home_address  home_latitude  home_longitude                      work_name          work_address  work_latitude  work_longitude
0     3    MARIO DITOMASSO    163 SCOTTFIELD DR      39.657723      -75.732460                     Unemployed     163 SCOTTFIELD DR      39.657723      -75.732460
1     2        JAMES BROWN   18601 N Roxbury RD      39.564379      -77.723914                     Unemployed    18601 N Roxbury RD      39.564379      -77.723914
2     3   MOHAMAD ALIAHMED     526 Dougfield RD      39.658525      -75.721554                     JIFFY LUBE        29 Liberty PLZ      39.694874      -75.717293
3     2      JOHN HOLTZMAN         26 Keller RD      39.658764      -75.734228                     Unemployed          26 Keller RD      39.658764      -75.734228
4     2       JUSTIN LOGUE     515 Dougfield RD      39.659278      -75.722871                     Unemployed      515 Dougfield RD      39.659278      -75.722871
5     2    GEORGE BROOMALL          22 KORDA DR      39.663291      -75.733223  CB LAWN SERVICE/SELF EMPLOYED           22 KORDA DR      39.663291      -75.733223
6     2     ROBERT JACKSON         55 MERCER DR      39.665281      -75.730139                   GRUBB LUMBER              200 A ST      39.733824      -75.553151
7     3  RICHARD DESHIELDS       23 Montrose DR      39.665924      -75.723012                 ZACROS AMERICA           220 Lake DR      39.614624      -75.755175
8     2      BRANDON SMITH         23 Mercer DR      39.666791      -75.728523                     Unemployed          23 Mercer DR      39.666791      -75.728523
9     2      DWAYNE KEENAN  41 Martindale Drive      39.667605      -75.724523               BELL NURSERY USA  211 Interchange BLVD      39.662899      -75.777035
```

</details>

### 4.7 Demo a manual entry to the `sex_offenders` table
<details><summary> (click here to expand) </summary>

---
To manually add a `sex_offender` entry to the `sex_offenders` table, we use the endpoint `/add/<table_name>` <br/>

Arguments:
```rexx
tier = 2
name = MATTHEW OGRADY
dob = 1980-09-16 00:00:00
arrest_description = RAPE FOURTH DEGREE SEXUAL INTERCOURSE VICTIM LESS THAN 16 YEARS OLD
arrest_date = 2002-07-08 00:00:00
victim_age = 12-15yr
home_address = 104 N Brownleaf RD
home_latitude = 39.678394
home_longitude = -75.686106
work_name = F.L. GIANNONE ELECTRICAL
work_address = 134 Register DR
work_latitude = 39.695876
work_longitude = -75.746505
```

Request:
```erlang
https://api.crimemap.hopto.org/add/sex_offenders?tier=2&name=MATTHEW OGRADY&dob=1980-09-16 00:00:00&arrest_description=RAPE FOURTH DEGREE SEXUAL INTERCOURSE VICTIM LESS THAN 16 YEARS OLD&arrest_date=2002-07-08
00:00:00&victim_age=12-15yr&home_address=104 N Brownleaf RD&home_latitude=39.678394&home_longitude=-75.686106&work_name=F.L. GIANNONE ELECTRICAL&work_address=134 Register DR&work_latitude=39.695876&work_longitude=-75.746505
```

Response:
```json
{
  "message": "data added to <sex_offenders>",
  "entry_id": "61",
}
```
</details>

</details>

---

# 2. `/get`
**Fetch a *single* entry or *multiple* entries from a `table`**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/get
```
</td><td>

```rexx
returns all tables[] in the database
```
</td></tr><tr></tr><tr><td>

```jq
/get/usage
```
</td><td>

```rexx
returns a message for how to use this function
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}
```
</td><td>

```rexx
returns all entries for the table: {table_name}
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}/{param_name}/{param_value}
```
</td><td>

```rexx
match entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/get/{table_name}?param_name=param_value
```
</td><td>

```rexx
match entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}/filter/{query}
```
</td><td>

```rexx
match entries: 'filter='
```
</td></tr><tr></tr><tr><td>

```erlang
/get/{table_name}?filter=query
```
</td><td>

```rexx
match entries: 'filter='
```
</td></tr>
</table>


### Options:
<table>
<tr><td> Parameters </td><td> Comment </td></tr><tr><td>

```rexx
*None*
```
</td><td>

```rexx
submit no parameters (none required)
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}/key/value
```
</td><td>

```rexx
match is limited to 'column_name == column_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/get/{table_name}?key=value
```
</td><td>

```rexx
match is limited to 'column_name == column_value'
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}/filter/query
```
</td><td>

```rexx
supports expressions, operators, and functions
```
</td></tr><tr></tr><tr><td>

```erlang
/get/{table_name}?filter=query
```
</td><td>

```rexx
supports expressions, operators, and functions
```
</td></tr>
</table>

### Notes on `filter` option:
<table>
<tr><td> Note </td><td> Comment </td></tr><tr><td>

```rexx
keyword
```
</td><td>

```rexx
filter
```
</td></tr><tr></tr><tr><td>

```rexx
QUERY FORMAT
```
</td><td>

```erlang
/get/{table_name}?filter=(param_name > "param_value")
```
</td></tr><tr></tr><tr><td>

```rexx
QUERY EXAMPLE
```
</td><td>

```erlang
/get/users?filter=(user_id = "7" OR username="bob")
```
</td></tr><tr></tr><tr><td>

```rexx
PATH FORMAT
```
</td><td>

```jq
/get/{table_name}/filter/(param_name="param_value" OR param_name="param_value")
```
</td></tr><tr></tr><tr><td>

```rexx
PATH EXAMPLE
```
</td><td>

```jq
/get/users/filter/(username="bob" OR username="alice")
```
</td></tr>
</table>

### Response After Successful [`/get`](#2-get):
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
data = {obj}
```
</td><td>

```rexx
a single object matching the parameters
```
</td></tr><tr></tr><tr><td>

```rexx
data = [{obj}]
```
</td><td>

```rexx
an array of objects matching the parameters
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/get`
The endpoint for getting users from the **`users`** table is **`/get/users`**.


### Let's query the **`users`** table to find the 2 users we created earlier
Examine the **`users`** table
Request:
```ruby
/get/users
```

Response:
```json
{
    "message": "found 8 user entries",
    "data": [
        {"user_id": 1, "username": "user_1", "password": "794001bff7f6ae7ded745c7de77043873b4173fad011d3ee5ba42bea334d99486f38d77f246009a052277d7b56dddd90337d5f18cf7fa065ed287e6b8661a279", "create_time": "2022-04-01 23:09:19.000"},
        {"user_id": 2, "username": "user_2", "password": "828beaa5b092bc374d1a443847ea68f1d83e4991b83c2e95e961ce4817138b7c53c7eb8be731d5bb0c3bfbe7d0335fe3f5ccc1b674d93c89c27d6b644da56875", "create_time": "2022-04-01 23:16:26.000"},
        {"user_id": 3, "username": "user_3", "password": "a3bfdbe9284aecf165cf3fad3ff9c66c3ffa08fe930a2de52094a039062573b00642870e7a304500b1c62a9d0b50d0ffab4a4e08ffc028c86b2f46acae92be74", "create_time": "2022-04-01 23:16:36.000"},
        {"user_id": 4, "username": "user_4", "password": "e820f57e418d387107bfb9e57119e9aa7c3e1db9ef06b1b107c0eb8444b57b69cee1fac48feeb33c7dc34904e0a38e84dd9b6b44fd51078c8359fc272d5af13d", "create_time": "2022-04-01 23:16:41.000"},
        {"user_id": 5, "username": "user_5", "password": "a3cc8fd887edb257f9e630383eb5569d35d2f2600333cd3ff828e5f35edbedbba64bfac5a7da46013a6877934f57d1e3807116205c556aeef83521d6561408fb", "create_time": "2022-04-01 23:16:48.000"},
        {"user_id": 6, "username": "M2band", "password": "30823caee74ca49fd5699c8de172b515f7a00ab04a04d0641107677af5f372c169746ccdf08b3ba1542c0626d73cb5ebcfec762016cab411e06596e4d2211b34", "create_time": "2022-04-03 15:29:41.223"},
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```

We just want our 2 users **`alice`** and **`bob`**, let's try querying with different parameters

Arguments:
``` python
username = alice
```

Request:
```ruby
/get/users/username/alice
```

Response:
```json
{
  "message": "1 user entry found",
  "data": {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"}
}
```

Arguments:
``` python
username = bob
```

Request:
```ruby
/get/users/username/bob
```

Response:
```json
{
    "message": "1 user entry found",
    "data": {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
}
```

Arguments:
``` python
user_id = 7
```

Request:
```ruby
/get/users/user_id/7
```

Response:
```json
{
    "message": "1 user entry found",
    "data": {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"}
}
```

Arguments:
``` python
user_id = 8
```

Request:
```ruby
/get/users/user_id/8
```

Response:
```json
{
    "message": "1 user entry found",
    "data": {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
}
```

### Let's try out the **`filter`** parameter to get just the users: **`alice`** and **`bob`**

Arguments:
``` python
filter = (user_id = 7 OR user_id = 8)
```

Request:
```ruby
/get/users?filter=(user_id = 7 OR user_id = 8)
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```

Arguments: "values" wrapped with double quotations 
``` python
filter = (user_id = "7" OR user_id = "8")
```

Request:
```ruby
/get/users?filter=(user_id = "7" OR user_id = "8")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```

Arguments:
``` python
filter = (user_id > '6' AND user_id < "9")
```

Request:
```ruby
/get/users?filter=(user_id > '6' AND user_id < "9")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```

Arguments:
``` python
filter = (username="bob" OR username="alice")
```

Request:
```ruby
/get/users/filter/(username="bob" OR username="alice")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```
---
### Notes on {filter_string}:
<table>
<tr><td> Note </td><td> Comment </td></tr><tr><td>

```rexx
keyword
```
</td><td>

```rexx
filter
```
</td></tr><tr></tr><tr><td>

```rexx
QUERY FORMAT
```
</td><td>

```erlang
?filter=(param_name > "param_value")
```
</td></tr><tr></tr><tr><td>

```rexx
QUERY EXAMPLE
```
</td><td>

```erlang
/get/users?filter=(user_id = "7" OR username="bob")
```
</td></tr><tr></tr><tr><td>

```rexx
PATH FORMAT
```
</td><td>

```jq
/filter/(param_name="param_value" OR param_name="param_value")
```
</td></tr><tr></tr><tr><td>

```rexx
PATH EXAMPLE
```
</td><td>

```jq
/get/users/filter/(username="bob" OR username="alice")
```
</td></tr></table>

---

### Next, we will query the **`oximeter`** table to retrieve the sensor data for each user: `alice` and `bob`
Oximeter data for just `alice`:

Arguments:
``` python
user_id = 7
```

Request:
```ruby
/get/oximeter/user_id/7
```

Response:
```json
{
    "message": "found 6 oximeter entries",
    "data": [
        {"entry_id": 43, "user_id": 7, "heart_rate": 134, "blood_o2": 97, "temperature": 97.6691638391727, "entry_time": "2022-04-05 12:06:01.397"},
        {"entry_id": 44, "user_id": 7, "heart_rate": 129, "blood_o2": 98, "temperature": 97.45331222228752, "entry_time": "2022-04-05 12:06:01.528"},
        {"entry_id": 45, "user_id": 7, "heart_rate": 128, "blood_o2": 100, "temperature": 97.35755335543793, "entry_time": "2022-04-05 12:06:01.740"},
        {"entry_id": 46, "user_id": 7, "heart_rate": 134, "blood_o2": 96, "temperature": 97.03691402965539, "entry_time": "2022-04-05 12:06:01.994"},
        {"entry_id": 47, "user_id": 7, "heart_rate": 132, "blood_o2": 96, "temperature": 97.78609598543946, "entry_time": "2022-04-05 12:06:02.469"},
        {"entry_id": 48, "user_id": 7, "heart_rate": 130, "blood_o2": 98, "temperature": 97.262831668111, "entry_time": "2022-04-05 12:06:02.669"}
    ]
}
```

Oximeter data for just `bob`:

Arguments:
``` python
user_id = 8
```

Request:
```ruby
/get/oximeter/user_id/8
```

Response:
```json
{
    "message": "found 10 oximeter entries",
    "data": [
        {"entry_id": 49, "user_id": 8, "heart_rate": 143, "blood_o2": 97, "temperature": 97.23579109761334, "entry_time": "2022-04-05 12:16:11.420"},
        {"entry_id": 50, "user_id": 8, "heart_rate": 127, "blood_o2": 97, "temperature": 97.7532770488335, "entry_time": "2022-04-05 12:16:11.592"},
        {"entry_id": 51, "user_id": 8, "heart_rate": 131, "blood_o2": 95, "temperature": 97.89202180155488, "entry_time": "2022-04-05 12:16:11.747"},
        {"entry_id": 52, "user_id": 8, "heart_rate": 124, "blood_o2": 95, "temperature": 97.81020200542864, "entry_time": "2022-04-05 12:16:11.897"},
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"}
    ]
}
```

Oximeter data for users with (**`user_id`** BETWEEN "6" AND "9")

Arguments:
``` python
filter = (user_id BETWEEN "6" AND "9")
```

Request:
```ruby
/get/oximeter/filter/(user_id BETWEEN "6" AND "9")
```

Response:
```json
{
    "message": "found 16 oximeter entries",
    "data": [
        {"entry_id": 43, "user_id": 7, "heart_rate": 134, "blood_o2": 97, "temperature": 97.6691638391727, "entry_time": "2022-04-05 12:06:01.397"},
        {"entry_id": 44, "user_id": 7, "heart_rate": 129, "blood_o2": 98, "temperature": 97.45331222228752, "entry_time": "2022-04-05 12:06:01.528"},
        {"entry_id": 45, "user_id": 7, "heart_rate": 128, "blood_o2": 100, "temperature": 97.35755335543793, "entry_time": "2022-04-05 12:06:01.740"},
        {"entry_id": 46, "user_id": 7, "heart_rate": 134, "blood_o2": 96, "temperature": 97.03691402965539, "entry_time": "2022-04-05 12:06:01.994"},
        {"entry_id": 47, "user_id": 7, "heart_rate": 132, "blood_o2": 96, "temperature": 97.78609598543946, "entry_time": "2022-04-05 12:06:02.469"},
        {"entry_id": 48, "user_id": 7, "heart_rate": 130, "blood_o2": 98, "temperature": 97.262831668111, "entry_time": "2022-04-05 12:06:02.669"},
        {"entry_id": 49, "user_id": 8, "heart_rate": 143, "blood_o2": 97, "temperature": 97.23579109761334, "entry_time": "2022-04-05 12:16:11.420"},
        {"entry_id": 50, "user_id": 8, "heart_rate": 127, "blood_o2": 97, "temperature": 97.7532770488335, "entry_time": "2022-04-05 12:16:11.592"},
        {"entry_id": 51, "user_id": 8, "heart_rate": 131, "blood_o2": 95, "temperature": 97.89202180155488, "entry_time": "2022-04-05 12:16:11.747"},
        {"entry_id": 52, "user_id": 8, "heart_rate": 124, "blood_o2": 95, "temperature": 97.81020200542864, "entry_time": "2022-04-05 12:16:11.897"},
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"}
    ]
}
```

### Test Case: Fever?
Now let's determine who may have been suspected for having a fever.
Using this definition: *Anything above 100.4 F is considered a fever.*

Arguments:
``` python
filter = (temperature > "100.4") GROUP BY user_id
```

Request:
```ruby
/get/oximeter/filter/(temperature > "100.4") GROUP BY user_id
```

Response:
```json
{
    "message": "1 oximeter entry found",
    "data": {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"}
}
```

Only **`bob`** reached temperatures above `100.4 F`

### Test Case: MIN, MAX, Temperature Range?
Let's get the range of temperatures from **MIN** to **MAX**

Arguments:
``` python
filter = (user_id = "8") ORDER BY temperature
```

Request:
```ruby
/get/oximeter/filter/(user_id = "8") ORDER BY temperature
```

Response:
```json
{
    "message": "found 10 oximeter entries",
    "data": [
        {"entry_id": 49, "user_id": 8, "heart_rate": 143, "blood_o2": 97, "temperature": 97.23579109761334, "entry_time": "2022-04-05 12:16:11.420"},
        {"entry_id": 50, "user_id": 8, "heart_rate": 127, "blood_o2": 97, "temperature": 97.7532770488335, "entry_time": "2022-04-05 12:16:11.592"},
        {"entry_id": 52, "user_id": 8, "heart_rate": 124, "blood_o2": 95, "temperature": 97.81020200542864, "entry_time": "2022-04-05 12:16:11.897"},
        {"entry_id": 51, "user_id": 8, "heart_rate": 131, "blood_o2": 95, "temperature": 97.89202180155488, "entry_time": "2022-04-05 12:16:11.747"},
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"}
    ]
}
```

Get **`temperature`** Range of fever

Arguments:
``` python
filter = (temperature > "100.4") ORDER BY temperature
```

Request:
```ruby
/get/oximeter/user_id/8/filter/(temperature > "100.4") ORDER BY temperature
```

Response:
```json
{
    "message": "found 6 oximeter entries",
    "data": [
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"}
    ]
}
```


Get entry with **MIN** **`temperature`** 

Arguments:
``` python
filter = (temperature > "100.4") ORDER BY temperature LIMIT 1
```

Request:
```ruby
/get/oximeter/user_id/8/filter/(temperature > "100.4") ORDER BY temperature LIMIT 1
```

Response:
```json
{
    "message": "1 oximeter entry found",
    "data": {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"}
}
```

Get entry with **MAX** **`temperature`** 

Arguments:
``` python
user_id = 8
filter = (temperature > "100.4") ORDER BY temperature DESC
```

Request:
```ruby
/get/oximeter/user_id/8/filter/(temperature > "100.4") ORDER BY temperature DESC
```

Response:
```json
{
    "message": "found 6 oximeter entries",
    "data": [
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"}
    ]
}
```

Get **MAX**

Arguments:
``` python
user_id = 8
filter = (temperature > "100.4") ORDER BY temperature DESC LIMIT 1
```

Request:
```ruby
/get/oximeter/user_id/8/filter/(temperature > "100.4") ORDER BY temperature DESC LIMIT 1
```

Response
```json
{"message": "1 oximeter entry found", "data": {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"}}
```

### Test Case: Filter users created after a start date but before an end date.

Finding users created after `2022-04-02`
> Note: If you only provide a date but do not specify a time, then time 00:00:00 is assumed.

Arguments:
```python
filter = (create_time > "2022-04-03")
```

Request:
```ruby
/get/users?filter=(create_time > "2022-04-03")
```

Response:
```json
{
    "message": "found 3 user entries",
    "data": [
        {
            "user_id": 6,
            "username": "M2band",
            "password": "30823caee74ca49fd5699c8de172b515f7a00ab04a04d0641107677af5f372c169746ccdf08b3ba1542c0626d73cb5ebcfec762016cab411e06596e4d2211b34",
            "create_time": "2022-04-03 15:29:41.223"
        },
        {
            "user_id": 7,
            "username": "alice@udel.edu",
            "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a",
            "create_time": "2022-04-05 03:25:57.163"
        },
        {
            "user_id": 8,
            "username": "robert@udel.edu",
            "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4",
            "create_time": "2022-04-05 03:41:12.857"
        }
    ]
}
```

Finding users created after `2022-04-03` and before `2022-04-05 03:40:00`

Arguments:
```python
filter = (create_time > "2022-04-03" AND create_time < "2022-04-05 03:40:00")
```

Request:
```ruby
/get/users?filter=(create_time > "2022-04-03" AND create_time < "2022-04-05 03:40:00")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {
            "user_id": 6,
            "username": "M2band",
            "password": "30823caee74ca49fd5699c8de172b515f7a00ab04a04d0641107677af5f372c169746ccdf08b3ba1542c0626d73cb5ebcfec762016cab411e06596e4d2211b34",
            "create_time": "2022-04-03 15:29:41.223"
        },
        {
            "user_id": 7,
            "username": "alice@udel.edu",
            "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a",
            "create_time": "2022-04-05 03:25:57.163"
        }
    ]
}
```
</details>

---

## [Workflow 5 - Requesting Data](#Workflow-5---Requesting-Data)

---

<details><summary> (click here to expand) </summary>

### Investigating the `users` table

#### Let's fetch all users in the `users` table:
Request:
```jq
https://api.crimemap.hopto.org/get/users
```

Response:
```json
{
  "message": "found 5 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "756a404bd66b7f081a936fe6fbcf2374de5c6ce018d62f37e664be8df02de03807b51fc4273dc06d12c11f7075369b5e96e2b0fef57037f6711f7e0f07a224af", "create_time": "2022-10-28 09:34:39.683"},
    {"user_id": 2, "username": "alice", "password": "1d5f25f69d22e57f92408247a304ab513e32791505c3f4eb878b732fb87d78c5dab7f5f46766e2fd7f2167f395829fd37feb7e8a773352830f70b5eeeef6d809", "create_time": "2022-11-15 22:52:22.768"},
    {"user_id": 3, "username": "bob", "password": "541803a1dc5e1e822dc34cecfc43bb634c9604bb612e65e1b02ee1a239a2aac5d3605469e24418dc327eb9f66af74ce9fd127ae8b50246e43497e3efce73dfe2", "create_time": "2022-11-15 22:52:23.082"},
    {"user_id": 4, "username": "anna", "password": "584a56a0c3e0b750b3b6ae320efb6004bdb73e5e06c455f1ede9d750ec6a0329c9b7fb0b2c36838728e68fea2327fddbb4cc34a17412dfd24730f4c2cf77cdb1", "create_time": "2022-11-15 22:52:23.185"},
    {"user_id": 5, "username": "steve", "password": "be93fe20d457f6d23539baf51e8c2fb9e38ae9232d8a2ae04e45e60e2c0e019d5cd56a380611046f9c904dfaf47f725b87a6dc1b84c8b9cf4e15b03e8f30ddd6", "create_time": "2022-11-15 22:52:23.343"},
  ],
}
```

### Investigating the `user_profiles` table

#### Let's fetch all profiles in the `user_profiles` table:
Request:
```jq
https://api.crimemap.hopto.org/get/user_profiles
```

Response:
```json
{
  "message": "found 5 user_profile entries",
  "data": [
    {"entry_id": 1, "user_id": 1, "name": "Administrator", "email": "admin@udel.edu", "profile_pic": "19.jpg", "entry_time": "2022-11-22 20:27:27.766"},
    {"entry_id": 2, "user_id": 2, "name": "Alice Smith", "email": "alice@udel.edu", "profile_pic": "20.png", "entry_time": "2022-11-22 20:41:20.552"},
    {"entry_id": 3, "user_id": 3, "name": "Bob Smith", "email": "bob@udel.edu", "profile_pic": "21.png", "entry_time": "2022-11-22 20:43:00.595"},
    {"entry_id": 4, "user_id": 4, "name": "Anna Williams", "email": "anna@udel.edu", "profile_pic": "22.png", "entry_time": "2022-11-22 20:55:27.737"},
    {"entry_id": 5, "user_id": 5, "name": "Steve Williams", "email": "steve@udel.edu", "profile_pic": "23.png", "entry_time": "2022-11-22 20:56:51.605"},
  ],
}
```

#### Fetch the profile for the user `steve`
> Note: from the `users` table, we know that the user `steve` has a `user_id` of `5`

Arguments:
```rexx
filter = (user_id = 5)
```

Request:
```erlang
https://api.crimemap.hopto.org/get/user_profiles?filter=(user_id = 5)
```

Response:
```json
{
  "message": "1 user_profile entry found",
  "data": [{"entry_id": 5, "user_id": 5, "name": "Steve Williams", "email": "steve@udel.edu", "profile_pic": "23.png", "entry_time": "2022-11-22 20:56:51.605"}],
}
```

Note: the `profile_pic` can be fetched directly: [https://api.crimemap.hopto.org/23.png](https://api.crimemap.hopto.org/23.png) <br />
![https://api.crimemap.hopto.org/23.png](https://api.crimemap.hopto.org/23.png)

### Investigating the `incidents` table

#### Let's fetch the first `10 incidents` in the `incidents` table
Arguments:
```rexx
filter = (entry_id >= 1) LIMIT 10
```

Request:
```erlang
https://api.crimemap.hopto.org/get/incidents?filter=(entry_id >= 1) LIMIT 10
```

Response:
```json
{
  "message": "found 10 incident entries",
  "data": [
    {"entry_id": 1, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/FROM BUILDING", "location": "100 BLOCK SUBURBAN DR", "latitude": 39.66671000000007, "longitude": -75.77604999999994, "agency": "Newark Police", "report_date": "2022-07-01 17:43:00", "entry_time": "2022-11-18 18:21:39.315"},
    {"entry_id": 2, "tier": 1, "type": "DUI", "type_img": "6.svg", "description": "POSSESSION OF AN OPEN CONTAINER", "location": "200 BLOCK E E. MAIN ST", "latitude": 39.68363000000002, "longitude": -75.74546, "agency": "Newark Police", "report_date": "2022-07-01 19:02:00", "entry_time": "2022-11-18 18:21:39.438"},
    {"entry_id": 3, "tier": 1, "type": "Drugs / Alcohol Violations", "type_img": "5.svg", "description": "DISTURBING THE PEACE/PUBLIC NUISANCE", "location": "000 BLOCK PROSPECT AVE", "latitude": 39.686850000000014, "longitude": -75.75332999999995, "agency": "Newark Police", "report_date": "2022-07-02 01:33:00", "entry_time": "2022-11-18 18:21:39.560"},
    {"entry_id": 4, "tier": 1, "type": "Weapons", "type_img": "15.svg", "description": "LARCENY/FROM VEHICLE/NOT ATTACHED", "location": "300 BLOCK CHRISTINA MILL DR", "latitude": 39.669780000000046, "longitude": -75.77436999999996, "agency": "Newark Police", "report_date": "2022-07-03 07:17:00", "entry_time": "2022-11-18 18:21:39.703"},
    {"entry_id": 5, "tier": 1, "type": "DUI", "type_img": "6.svg", "description": "POSSESSION OF AN OPEN CONTAINER", "location": "000 BLOCK BENNY ST", "latitude": 39.677110000000006, "longitude": -75.74542999999993, "agency": "Newark Police", "report_date": "2022-07-04 18:34:00", "entry_time": "2022-11-18 18:21:39.862"},
    {"entry_id": 6, "tier": 1, "type": "Drugs / Alcohol Violations", "type_img": "5.svg", "description": "DISORDERLY CONDUCT/UNRELATED TO LIQUOR", "location": "000 BLOCK E. MAIN ST", "latitude": 39.683099999999996, "longitude": -75.75229999999993, "agency": "Newark Police", "report_date": "2022-07-05 00:57:00", "entry_time": "2022-11-18 18:21:39.959"},
    {"entry_id": 7, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/VEHICLE PARTS/FROM AUTO/ATTACHED", "location": "900 BLOCK E CHAPEL ST", "latitude": 39.6611500000001, "longitude": -75.73584999999993, "agency": "Delaware State Police", "report_date": "2022-07-05 07:51:00", "entry_time": "2022-11-18 18:21:40.084"},
    {"entry_id": 8, "tier": 1, "type": "Drugs / Alcohol Violations", "type_img": "5.svg", "description": "DISTURBING THE PEACE/PUBLIC NUISANCE", "location": "3100 BLOCK WOOLEN WAY", "latitude": 39.68855000000009, "longitude": -75.74659999999993, "agency": "Newark Police", "report_date": "2022-07-05 18:20:00", "entry_time": "2022-11-18 18:21:40.199"},
    {"entry_id": 9, "tier": 1, "type": "Drugs / Alcohol Violations", "type_img": "5.svg", "description": "DISTURBING THE PEACE/PUBLIC NUISANCE", "location": "000 BLOCK NW O DANIEL AVE", "latitude": 39.67424000000003, "longitude": -75.77021999999987, "agency": "Newark Police", "report_date": "2022-07-06 20:37:00", "entry_time": "2022-11-18 18:21:40.291"},
    {"entry_id": 10, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/FROM BUILDING", "location": "600 BLOCK W OGLETOWN RD", "latitude": 39.68526000000007, "longitude": -75.73345999999997, "agency": "Newark Police", "report_date": "2022-07-06 21:19:00", "entry_time": "2022-11-18 18:21:40.380"},
  ],
}
```

We see that the first `10 incidents` were reported in `July`

#### Let's fetch all incidents reported on and after `2022-11-21`
Arguments:
```rexx
filter = (report_date >= "2022-11-21")
```

Request:
```erlang
https://api.crimemap.hopto.org/get/incidents?filter=(report_date >= "2022-11-21")
```

Response:
```json
{
  "message": "found 4 incident entries",
  "data": [
    {"entry_id": 750, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/SHOPLIFTING", "location": "200 BLOCK SW S. MAIN ST", "latitude": 39.67795000000005, "longitude": -75.76196999999992, "agency": "Newark Police", "report_date": "2022-11-21 00:31:00", "entry_time": "2022-11-22 18:55:00.277"},
    {"entry_id": 751, "tier": 1, "type": "Burglary", "type_img": "3.svg", "description": "AGGRAVATED ASSAULT/FAMILY OTHER DANGEROUS WEAPON", "location": "800 BLOCK S COLLEGE AVE", "latitude": 39.653990000000064, "longitude": -75.75098999999993, "agency": "Newark Police", "report_date": "2022-11-21 21:12:00", "entry_time": "2022-11-22 18:55:00.366"},
    {"entry_id": 752, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/BICYCLES", "location": "3300 BLOCK WOOLEN WAY", "latitude": 39.68811000000006, "longitude": -75.74614999900001, "agency": "Newark Police", "report_date": "2022-11-21 22:37:00", "entry_time": "2022-11-22 18:55:00.455"},
    {"entry_id": 753, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/SHOPLIFTING", "location": "200 BLOCK S. MAIN ST", "latitude": 39.67787000000004, "longitude": -75.76204999999997, "agency": "Newark Police", "report_date": "2022-11-22 01:57:00", "entry_time": "2022-11-22 18:55:00.542"},
  ],
}
```

#### Let's fetch all incidents along `Main Street` between `South College Ave` and `Deer Park Tavern`

##### Latitude=39.682800, Longitude-75.756200
![https://api.crimemap.hopto.org/w_main_left.png](https://api.crimemap.hopto.org/w_main_left.png)

##### Latitude=39.683100, Longitude-75.753600
![https://api.crimemap.hopto.org/w_main_right.png](https://api.crimemap.hopto.org/w_main_right.png)

Arguments:
```rexx
filter = (latitude >= 39.682800 AND latitude <= 39.683100 AND longitude >= -75.756200 AND longitude <= -75.753600)
```

Request:
```erlang
https://api.crimemap.hopto.org/get/incidents?filter=(latitude >= 39.682800 AND latitude <= 39.683100 AND longitude >= -75.756200 AND longitude <= -75.753600)
```

Response:
```json
{
  "message": "found 11 incident entries",
  "data": [
    {"entry_id": 69, "tier": 1, "type": "Burglary", "type_img": "3.svg", "description": "AGGRAVATED ASSAULT/NON-FAMILY STRONG-ARM/HANDS/FIST/FEET", "location": "100 BLOCK MAIN ST", "latitude": 39.682960000000044, "longitude": -75.75600999999999, "agency": "Newark Police", "report_date": "2022-08-14 00:51:00", "entry_time": "2022-11-18 18:21:47.446"},
    {"entry_id": 230, "tier": 1, "type": "Vehicle Break-In / Theft", "type_img": "14.svg", "description": "DAMAGE/PRIVATE PROPERTY", "location": "100 BLOCK E MAIN ST", "latitude": 39.682970000000026, "longitude": -75.75581000099999, "agency": "Newark Police", "report_date": "2022-09-15 23:59:00", "entry_time": "2022-11-18 18:22:08.371"},
    {"entry_id": 346, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/VEHICLE PARTS/FROM AUTO/ATTACHED", "location": "100 BLOCK W MAIN ST", "latitude": 39.682980000000015, "longitude": -75.75467999999994, "agency": "Newark Police", "report_date": "2022-09-27 23:10:00", "entry_time": "2022-11-18 18:22:23.256"},
    {"entry_id": 380, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/BICYCLES", "location": "100 BLOCK MAIN ST", "latitude": 39.682970000000026, "longitude": -75.75577999999993, "agency": "Newark Police", "report_date": "2022-10-01 01:05:00", "entry_time": "2022-11-18 18:22:26.921"},
    {"entry_id": 413, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/FROM ALL OTHER YARDS", "location": "W N ST & COLLEGE AVE", "latitude": 39.682990000000075, "longitude": -75.75408, "agency": "Newark Police", "report_date": "2022-10-04 13:38:00", "entry_time": "2022-11-18 18:22:30.688"},
    {"entry_id": 475, "tier": 1, "type": "Burglary", "type_img": "3.svg", "description": "SIMPLE ASSAULT/NON-FAMILY/OTHER ASSAULTS/NON-AGGRAVATED", "location": "100 BLOCK E MAIN ST", "latitude": 39.682980000000015, "longitude": -75.75593999999995, "agency": "Newark Police", "report_date": "2022-10-14 01:23:00", "entry_time": "2022-11-18 18:22:37.452"},
    {"entry_id": 498, "tier": 1, "type": "Drugs / Alcohol Violations", "type_img": "5.svg", "description": "DISORDERLY CONDUCT/UNRELATED TO LIQUOR", "location": "100 BLOCK E MAIN ST", "latitude": 39.682960000000044, "longitude": -75.75530999999995, "agency": "Newark Police", "report_date": "2022-10-15 23:58:00", "entry_time": "2022-11-18 18:22:40.726"},
    {"entry_id": 523, "tier": 1, "type": "Burglary", "type_img": "3.svg", "description": "OFFENSIVE TOUCHING/OTHER ASSAULTS/NON-AGGRAVATED", "location": "E. MAIN ST & W", "latitude": 39.682990000000075, "longitude": -75.7540299999999, "agency": "Newark Police", "report_date": "2022-10-21 02:34:00", "entry_time": "2022-11-18 18:22:44.655"},
    {"entry_id": 533, "tier": 1, "type": "Burglary", "type_img": "3.svg", "description": "OFFENSIVE TOUCHING/OTHER ASSAULTS/NON-AGGRAVATED", "location": "E. MAIN ST & W", "latitude": 39.682960000000044, "longitude": -75.75550000000004, "agency": "Newark Police", "report_date": "2022-10-22 00:01:00", "entry_time": "2022-11-18 18:22:46.076"},
    {"entry_id": 566, "tier": 1, "type": "Vandalism", "type_img": "13.svg", "description": "LARCENY/FROM BUILDING", "location": "100 BLOCK MAIN ST", "latitude": 39.683009999999996, "longitude": -75.75603999999996, "agency": "Newark Police", "report_date": "2022-10-24 12:00:00", "entry_time": "2022-11-18 18:22:50.715"},
    {"entry_id": 616, "tier": 1, "type": "Burglary", "type_img": "3.svg", "description": "AGGRAVATED ASSAULT/NON-FAMILY STRONG-ARM/HANDS/FIST/FEET", "location": "100 BLOCK MAIN ST", "latitude": 39.682970000000026, "longitude": -75.75548999999992, "agency": "Newark Police", "report_date": "2022-10-30 00:57:00", "entry_time": "2022-11-18 18:22:56.623"},
  ],
}
```

### Investigating the `sex_offenders` table

#### Let's fetch all `tier 3` sex offenders where the victim's age is `1-11yr`
Arguments:
```rexx
filter = (tier = 3 AND victim_age = "1-11yr")
```

Request:
```erlang
https://api.crimemap.hopto.org/get/sex_offenders?filter=(tier = 3 AND victim_age = "1-11yr")
```

Response:
```json
{
  "message": "found 4 sex_offender entries",
  "data": [
    {"entry_id": 1, "tier": 3, "name": "MARIO DITOMASSO", "dob": "1982-12-02 00:00:00", "arrest_description": "UNLAWFUL SEXUAL INTERCOURSE FIRST DEGREE-VICTIM < 16 AND NOT SOCIAL COMPANION", "arrest_date": "1997-08-28 00:00:00", "victim_age": "1-11yr", "home_address": "163 SCOTTFIELD DR", "home_latitude": 39.657723, "home_longitude": -75.73246, "work_name": "Unemployed", "work_address": "163 SCOTTFIELD DR", "work_latitude": 39.657723, "work_longitude": -75.73246, "entry_time": "2022-11-22 18:12:27.020"},
    {"entry_id": 22, "tier": 3, "name": "TAMMY CAMPBELL", "dob": "1978-07-26 00:00:00", "arrest_description": "RAPE SECOND DEGREE <16 YEARS BY PERSON IN POSITION OF TRUST, AUTHORITY, SUPERV", "arrest_date": "2007-11-14 00:00:00", "victim_age": "1-11yr", "home_address": "155 Madison DR", "home_latitude": 39.677082, "home_longitude": -75.768674, "work_name": "Unemployed", "work_address": "155 Madison DR", "work_latitude": 39.677082, "work_longitude": -75.768674, "entry_time": "2022-11-22 18:12:29.372"},
    {"entry_id": 34, "tier": 3, "name": "JAMES NORTON", "dob": "1959-08-27 00:00:00", "arrest_description": "UNLAWFUL SEXUAL CONTACT 1ST", "arrest_date": "1995-06-19 00:00:00", "victim_age": "1-11yr", "home_address": "28730 N WOODCREST DR", "home_latitude": 38.658209, "home_longitude": -75.247851, "work_name": "WATERCOLORS PAINTING", "work_address": "21 E SHADY DR", "work_latitude": 39.659054, "work_longitude": -75.707886, "entry_time": "2022-11-22 18:12:30.549"}, 
    {"entry_id": 39, "tier": 3, "name": "PAULRON CLARK", "dob": "1994-06-30 00:00:00", "arrest_description": "RAPE THIRD DEGREE VICTIM <16 DEF AT LEAST 10 YEARS OLDER OR VICT <14 DEF >19YR", "arrest_date": "2015-12-21 00:00:00", "victim_age": "1-11yr", "home_address": "416 S Van BUREN ST", "home_latitude": 39.739736, "home_longitude": -75.565057, "work_name": "LOCAL 199", "work_address": "308 MarkUS CT", "work_latitude": 39.660335, "work_longitude": -75.774232, "entry_time": "2022-11-22 18:12:31.393"},
  ],
}
```

</details>

---

# 3. `/edit`
**Edit a single entry or multiple entries of a table**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/edit
```
</td><td>

```rexx
returns all tables[] in the database
```
</td></tr><tr></tr><tr><td>

```jq
/edit/usage
```
</td><td>

```rexx
returns message: 'usage-info'
```
</td></tr><tr></tr><tr><td>

```jq
/edit/{table_name}
```
</td><td>

```rexx
returns message: 'missing a parameter'
```
</td></tr><tr></tr><tr><td>

```jq
/edit/{table_name}/{param_name}/{param_value}
```
</td><td>

```rexx
edit entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/edit/{table_name}?param_name=param_value
```
</td><td>

```rexx
edit entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/edit/{table_name}/filter/{filter_string}
```
</td><td>

```rexx
edit entries: filter='
```
</td></tr><tr></tr><tr><td>

```erlang
/edit/{table_name}?filter=filter_string
```
</td><td>

```rexx
edit entries: filter='
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Comment </td></tr><tr><td>

```rexx
at least 1 edit parameter
```
</td><td>

```rexx
any parameter not *_id or *_time
```
</td></tr><tr></tr><tr><td>

```rexx
at least 1 reference parameter
```
</td><td>

```rexx
any *_id or *_time parameter or filter
```

</td></tr>
</table>


### Response After Successful [`/edit`](#3-edit):
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
message
```
</td><td>

```rexx
number of edits made
```
</td></tr><tr></tr><tr><td>

```rexx
submitted[]
```
</td><td>

```rexx
the parameters that were submitted
```
</td></tr>
</table>

---

<details><summary>Endpint Background (click here to expand)
</summary>


### Investigating the Endpoint: `/edit`
The endpoint to edit a user from the **`users`** is **`/edit/users`**.
Making a request to the endpoint without providing **parameters** returns a `missing parameters` message:

Request:
```ruby
/edit/users
```

Response:
```json
{
    "message": "missing a parameter to edit",
    "editable": [{"username": "TEXT", "password": "TEXT"}],
    "submitted": [{}]
}
```

Making a request with only an **editable_parameter** updates the `missing parameters` message:

Arguments:
```python
username = bob
```

Request:
```ruby
/edit/users/username/bob
```

Response:
```json
{
    "message": "missing a query parameter",
    "query_params": [{"user_id": "INTEGER", "create_time": "DATETIME", "filter": ""}],
    "submitted": [{"username": "bob"}]
}
```

Making a request with only a **query_parameter** also updates the `missing parameters` message:

Arguments:
```python
user_id = 8
```

Request:
```ruby
/edit/users?user_id=8
```

Response:
```json
{
    "message": "missing a parameter to edit",
    "editable": [{"username": "TEXT", "password": "TEXT"}],
    "submitted": [{"user_id": "8"}, {"filter": ""}]
}

```

### Edit bob's **`username`** from `bob` to `robert`
Arguments:
```python
username = robert
user_id = 8
```

Request:
```ruby
/edit/users/username/robert?user_id=8
```

Response:
```json
{
    "message": "edited 1 user entry",
    "submitted": [{"username": "robert", "user_id": "8"}]
}
```

Check the user to verify the edit

Arguments:
```python
user_id = 8
```

Request:
```ruby
/get/users?user_id=8
```

Response:
```json
{
    "message": "1 user entry found",
    "data": {
        "user_id": 8,
        "username": "robert",
        "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4",
        "create_time": "2022-04-05 03:41:12.857"
    }
}
```

### Appending `@gmail.com` to the **`username`** for both `robert` and `alice`
Arguments:
```python
username = username||"@gmail.com"
filter = (user_id="7" OR user_id="8")
```

Request:
```ruby
/edit/users/username/username||"@gmail.com"?filter=(user_id="7" OR user_id="8")
```

Response:
```json
{
    "message": "edited 2 user entries",
    "submitted": [{
        "filter": "(user_id=\"7\" OR user_id=\"8\")",
        "username": "username||\"@gmail.com\""
    }]
}
```

Verify the edits

Arguments:
```python
filter = (user_id="7" OR user_id="8")
filter = (user_id="7" OR user_id="8")
```

Request:
```ruby
/get/users?filter=(user_id="7" OR user_id="8")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {
            "user_id": 7,
            "username": "alice@gmail.com",
            "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a",
            "create_time": "2022-04-05 03:25:57.163"
        },
        {
            "user_id": 8,
            "username": "robert@gmail.com",
            "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4",
            "create_time": "2022-04-05 03:41:12.857"
        }
    ]
}
```

### Replacing all **`users`** with **`username`** containing `@gmail.com` to `@udel.edu`
Arguments:
```python
username = REPLACE(username, "@gmail.com", "@udel.edu")
filter = (user_id="7" OR user_id="8")
```

Request:
```ruby
/edit/users/username/REPLACE(username, "@gmail.com", "@udel.edu")?filter=(user_id="7" OR user_id="8")
```

Response:
```json
{
    "message": "edited 2 user entries",
    "submitted": [{
        "filter": "(user_id=\"7\" OR user_id=\"8\")",
        "username": "REPLACE(username, \"@gmail.com\", \"@udel.edu\")"
    }]
}
```

Verify the edits

### Converting the **`temperature`** from **`farenheight`** to **`celsius`** for `alice`
> Note: parsing url paths now support fractions :)

Arguments:
```python
temperature = ((5.0/9.0)*(temperature-32.0))
filter = (user_id="7")
```

Request:
```ruby
/edit/oximeter/temperature/(temperature-32.0)*(5.0/9.0)?filter=(user_id="7")
```

Response:
```json
{
    "message": "edited 6 oximeter entries",
    "submitted": [{
        "filter": "(user_id=\"7\")",
        "temperature": "((5.0/9.0)*(temperature-32.0))"
    }]
}
```

Verify the edits

Arguments:
```python
filter = (user_id="7")
```

Request:
```ruby
/get/oximeter?filter=(user_id="7")
```

Response:
```json
{
    "message": "found 6 oximeter entries",
    "data": [
        {"entry_id": 43, "user_id": 7, "heart_rate": 134, "blood_o2": 97, "temperature": 36.48286879954039, "entry_time": "2022-04-05 12:06:01.397"},
        {"entry_id": 44, "user_id": 7, "heart_rate": 129, "blood_o2": 98, "temperature": 36.36295123460418, "entry_time": "2022-04-05 12:06:01.528"},
        {"entry_id": 45, "user_id": 7, "heart_rate": 128, "blood_o2": 100, "temperature": 36.30975186413218, "entry_time": "2022-04-05 12:06:01.740"},
        {"entry_id": 46, "user_id": 7, "heart_rate": 134, "blood_o2": 96, "temperature": 36.13161890536411, "entry_time": "2022-04-05 12:06:01.994"},
        {"entry_id": 47, "user_id": 7, "heart_rate": 132, "blood_o2": 96, "temperature": 36.54783110302192, "entry_time": "2022-04-05 12:06:02.469"},
        {"entry_id": 48, "user_id": 7, "heart_rate": 130, "blood_o2": 98, "temperature": 36.257128704506115, "entry_time": "2022-04-05 12:06:02.669"}
    ]
}
```

</details>

---

## [Workflow 6 - Editing Data](#Workflow-6---Editing-Data)

---

<details><summary> (click here to expand) </summary>

### Executing a User and Profile Edit

#### `anna` wants to edit her `email` in the `user_profiles` table from `anna@udel.edu` to `anna@gmail.com`

#### `anna` would like to change her `password` from `anna` to `Anna1234`

#### Query the `users` table to see all of the current `users`:
Request:
```jq
https://api.crimemap.hopto.org/get/users
```

Response:
```json
{
  "message": "found 5 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "756a404bd66b7f081a936fe6fbcf2374de5c6ce018d62f37e664be8df02de03807b51fc4273dc06d12c11f7075369b5e96e2b0fef57037f6711f7e0f07a224af", "create_time": "2022-10-28 09:34:39.683"},
    {"user_id": 2, "username": "alice", "password": "1d5f25f69d22e57f92408247a304ab513e32791505c3f4eb878b732fb87d78c5dab7f5f46766e2fd7f2167f395829fd37feb7e8a773352830f70b5eeeef6d809", "create_time": "2022-11-15 22:52:22.768"},
    {"user_id": 3, "username": "bob", "password": "541803a1dc5e1e822dc34cecfc43bb634c9604bb612e65e1b02ee1a239a2aac5d3605469e24418dc327eb9f66af74ce9fd127ae8b50246e43497e3efce73dfe2", "create_time": "2022-11-15 22:52:23.082"},
    {"user_id": 4, "username": "anna", "password": "584a56a0c3e0b750b3b6ae320efb6004bdb73e5e06c455f1ede9d750ec6a0329c9b7fb0b2c36838728e68fea2327fddbb4cc34a17412dfd24730f4c2cf77cdb1", "create_time": "2022-11-15 22:52:23.185"},
    {"user_id": 5, "username": "steve", "password": "be93fe20d457f6d23539baf51e8c2fb9e38ae9232d8a2ae04e45e60e2c0e019d5cd56a380611046f9c904dfaf47f725b87a6dc1b84c8b9cf4e15b03e8f30ddd6", "create_time": "2022-11-15 22:52:23.343"},
  ],
}
```

#### Fetch the `user_profile` for `anna`
Arguments:
```rexx
filter = (user_id = 4)
```

Request:
```erlang
https://api.crimemap.hopto.org/get/user_profiles?filter=(user_id = 4)
```

Response:
```json
{
  "message": "1 user_profile entry found",
  "data": [{"entry_id": 4, "user_id": 4, "name": "Anna Williams", "email": "anna@udel.edu", "profile_pic": "22.png", "entry_time": "2022-11-22 20:55:27.737"}],
}
```

#### Changing the `email` for `anna` in the `user_profiles` from `anna@udel.edu` to `anna@gmail.com`:
Arguments:
```rexx
email = anna@gmail.com
filter = (user_id=4)
```

Request:
```erlang
https://api.crimemap.hopto.org/edit/user_profiles/email/anna@gmail.com?filter=(user_id=4)
```

Response:
```json
{
  "message": "edited 1 user_profile entry",
  "submitted": [{"filter": "(user_id=4)", "email": "anna@gmail.com"}],
}
```

#### Verify by fetching the `user_profile` for `anna`
Arguments:
```rexx
filter = (user_id = 4)
```

Request:
```erlang
https://api.crimemap.hopto.org/get/user_profiles?filter=(user_id = 4)
```

Response:
```json
{
  "message": "1 user_profile entry found",
  "data": [{"entry_id": 4, "user_id": 4, "name": "Anna Williams", "email": "anna@gmail.com", "profile_pic": "22.png", "entry_time": "2022-11-22 20:55:27.737"}],
}
```

#### Changing the `password` for `anna` in the `users` table from `anna` to `Anna1234`
Arguments:
```rexx
password = Anna1234
filter = (user_id = 4)
```

Request:
```erlang
https://api.crimemap.hopto.org/edit/users?password=Anna1234&filter=(user_id = 4)
```

Response:
```json
{
  "message": "edited 1 user entry",
  "submitted": [{"filter": "(user_id = 4)", "password": "d5501e6216fc43dd32fd50a86eb306f414d6fee4692217c6303481e86513f1277930e058fc12564a3daa5ef9ba95544c0c0f9dc811c0bb2ee7ea3dd90d79c503"}],
}
```

#### Verify by logging in with the new `password`:
Arguments:
```rexx
username = anna
password = Anna1234
```

Request:
```erlang
https://api.crimemap.hopto.org/login?username=anna&password=Anna1234
```

Response:
```json
{
  "message": "user login success",
  "user_id": "4",
  "username": "anna",
  "token": "IUlhd1k1RFpBajZoS2ZNWEo4R2t3ZXc9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFMGxJYVVMZz09",
}
```

</details>

---


# 4. `/delete`
**Delete a single entry or multiple entries of a table**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/delete
```
</td><td>

```rexx
returns all tables[] in the database
```
</td></tr><tr></tr><tr><td>

```jq
/delete/usage
```
</td><td>

```rexx
returns message: 'usage-info'
```
</td></tr><tr></tr><tr><td>

```jq
/delete/{table_name}
```
</td><td>

```rexx
returns message: 'missing a parameter'
```
</td></tr><tr></tr><tr><td>

```jq
/delete/{table_name}/{param_name}/{param_value}
```
</td><td>

```rexx
delete entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/delete/{table_name}?param_name=param_value
```
</td><td>

```rexx
delete entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/delete/{table_name}/filter/{filter_string}
```
</td><td>

```rexx
delete entries: filter='
```
</td></tr><tr></tr><tr><td>

```erlang
/delete/{table_name}?filter=filter_string
```
</td><td>

```rexx
delete entries: filter='
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Comment </td></tr><tr><td>

```rexx
at least 1 reference parameter
```
</td><td>

```rexx
any *_id or *_time parameter or filter
```
</td></tr>
</table>


### Response After Successful [`/delete`](#4-delete):
<table>
<tr><td> Variable </td><td> Comment </td></tr>
<tr><td>

```rexx
message
```

</td><td>

```rexx
number of deletes made
```

</td></tr><tr></tr><tr><td>

```rexx
submitted[]
```

</td><td>

```rexx
the parameters that were submitted
```

</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/delete`
The endpoint for deleting an entry from the **`oximeter`** table is **`/delete/oximeter`**.
Making a request to the endpoint without providing **parameters** returns a `missing parameters` message:

Request:
```ruby
/delete/oximeter
```

Response:
```json
{
    "message": "missing a query param(s)",
    "query_params": [
        {"entry_id": "INTEGER", "user_id": "INTEGER", "heart_rate": "INTEGER", "blood_o2": "INTEGER", "temperature": "DOUBLE", "entry_time": "DATETIME", "filter": ""}
    ],
    "submitted": [{}]
}
```

### Deleting all entries for `Robert` with **`temperature`** in the fever range
Arguments:
```python
filter = (user_id = "8" AND temperature > "100.4")
```

Request:
```ruby
/delete/oximeter?filter=(user_id = "8" AND temperature > "100.4")
```

Response:
```json
{
    "message": "6 oximeter entries deleted",
    "submitted": [{"filter": "(user_id = \"8\" AND temperature > \"100.4\")"}]
}
```

Verify the deletes

Arguments:
```python
user_id = 8
```

Request:
```ruby
/get/oximeter/user_id/8
```

Response:
```json
{
    "message": "found 4 oximeter entries",
    "data": [
        {"entry_id": 49, "user_id": 8, "heart_rate": 143, "blood_o2": 97, "temperature": 97.23579109761334, "entry_time": "2022-04-05 12:16:11.420"},
        {"entry_id": 50, "user_id": 8, "heart_rate": 127, "blood_o2": 97, "temperature": 97.7532770488335, "entry_time": "2022-04-05 12:16:11.592"},
        {"entry_id": 51, "user_id": 8, "heart_rate": 131, "blood_o2": 95, "temperature": 97.89202180155488, "entry_time": "2022-04-05 12:16:11.747"},
        {"entry_id": 52, "user_id": 8, "heart_rate": 124, "blood_o2": 95, "temperature": 97.81020200542864, "entry_time": "2022-04-05 12:16:11.897"}
    ]
}
```
</details>

---

## [Workflow 7 - Deleting Data](#Workflow-7---Deleting-Data)

---

<details><summary> (click me to exapnd) </summary>

### Let's register a `test` user
Arguments:
```rexx
username = test
password = test
password2 = test
```

Request:
```jq
https://api.crimemap.hopto.org/register/username/test/password/test/password2/test
```

Response:
```json
{
  "message": "new user created",
  "user_id": "6",
  "username": "test",
}
```
### Verify by fetching all users in the `users` table
Request:
```jq
https://api.crimemap.hopto.org/get/users
```

Response:
```json
{
  "message": "found 6 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "756a404bd66b7f081a936fe6fbcf2374de5c6ce018d62f37e664be8df02de03807b51fc4273dc06d12c11f7075369b5e96e2b0fef57037f6711f7e0f07a224af", "create_time": "2022-10-28 09:34:39.683"},
    {"user_id": 2, "username": "alice", "password": "1d5f25f69d22e57f92408247a304ab513e32791505c3f4eb878b732fb87d78c5dab7f5f46766e2fd7f2167f395829fd37feb7e8a773352830f70b5eeeef6d809", "create_time": "2022-11-15 22:52:22.768"},
    {"user_id": 3, "username": "bob", "password": "541803a1dc5e1e822dc34cecfc43bb634c9604bb612e65e1b02ee1a239a2aac5d3605469e24418dc327eb9f66af74ce9fd127ae8b50246e43497e3efce73dfe2", "create_time": "2022-11-15 22:52:23.082"},
    {"user_id": 4, "username": "anna", "password": "d5501e6216fc43dd32fd50a86eb306f414d6fee4692217c6303481e86513f1277930e058fc12564a3daa5ef9ba95544c0c0f9dc811c0bb2ee7ea3dd90d79c503", "create_time": "2022-11-15 22:52:23.185"},
    {"user_id": 5, "username": "steve", "password": "be93fe20d457f6d23539baf51e8c2fb9e38ae9232d8a2ae04e45e60e2c0e019d5cd56a380611046f9c904dfaf47f725b87a6dc1b84c8b9cf4e15b03e8f30ddd6", "create_time": "2022-11-15 22:52:23.343"},
    {"user_id": 6, "username": "test", "password": "f959966570daf8d6361d6385ccf576141672717507d7dd58fe235566e8b071bdd4efd85e4980a48bae02f83e8ff1fbf8e508c636b8bd18c6b942280b48dd7d37", "create_time": "2022-11-22 23:23:00.929"},
  ],
}
```

### Now let's delete the `test` user
Arguments:
```rexx
filter = (username = "test")
```

Request:
```erlang
https://api.crimemap.hopto.org/delete/users?filter=(username = "test")
```

Response:
```json
{
  "message": "1 user entry deleted",
  "submitted": [{"filter": "(username = "test")"}],
}
```

### Verify by fetching all users in the `users` table
Request:
```jq
https://api.crimemap.hopto.org/get/users
```

Response:
```json
{
  "message": "found 5 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "756a404bd66b7f081a936fe6fbcf2374de5c6ce018d62f37e664be8df02de03807b51fc4273dc06d12c11f7075369b5e96e2b0fef57037f6711f7e0f07a224af", "create_time": "2022-10-28 09:34:39.683"},
    {"user_id": 2, "username": "alice", "password": "1d5f25f69d22e57f92408247a304ab513e32791505c3f4eb878b732fb87d78c5dab7f5f46766e2fd7f2167f395829fd37feb7e8a773352830f70b5eeeef6d809", "create_time": "2022-11-15 22:52:22.768"},
    {"user_id": 3, "username": "bob", "password": "541803a1dc5e1e822dc34cecfc43bb634c9604bb612e65e1b02ee1a239a2aac5d3605469e24418dc327eb9f66af74ce9fd127ae8b50246e43497e3efce73dfe2", "create_time": "2022-11-15 22:52:23.082"},
    {"user_id": 4, "username": "anna", "password": "d5501e6216fc43dd32fd50a86eb306f414d6fee4692217c6303481e86513f1277930e058fc12564a3daa5ef9ba95544c0c0f9dc811c0bb2ee7ea3dd90d79c503", "create_time": "2022-11-15 22:52:23.185"},
    {"user_id": 5, "username": "steve", "password": "be93fe20d457f6d23539baf51e8c2fb9e38ae9232d8a2ae04e45e60e2c0e019d5cd56a380611046f9c904dfaf47f725b87a6dc1b84c8b9cf4e15b03e8f30ddd6", "create_time": "2022-11-15 22:52:23.343"},
  ],
}
```

</details>

---


# [Extra Functions](#Extra-Functions)
The examples listed below will cover the **1 extra function**.<br />
All examples shown are executed via a **GET** request and can be tested with any browser. <br />
All endpoints support 4 *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

# 1. `/uploadImageUrl`
**Upload an image to the backend via image url** 

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr>
<tr><td>

```jq
/uploadImageUrl
```
</td><td>

```rexx
returns: {"message": "missing parameters", "required params": ["url"]}
```
</td></tr>
<tr></tr><tr><td>

```jq
/uploadImageUrl/usage
```
</td><td>

```rexx
returns: {"message": "usage_info"}
```
</td></tr>
<tr></tr><tr><td>

```jq
/uploadImageUrl/<param_name>/<param_value>
```
</td><td>

```rexx
upload with url_paths: 'param_name=param_value'
```
</td></tr>
<tr></tr>
<tr><td>

```jq
/uploadImageUrl?param_name=param_value
```
</td><td>

```rexx
upload with params: 'param_name=param_value'
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Description </td></tr>
<tr>
<td>

```rexx
url
```

</td>
<td>

```rexx
the full url path of the image you wish to upload and save into the backend
```

</td>
</tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/uploadImageUrl`
Request:
```jq
https://api.crimemap.hopto.org/uploadImageUrl
```

Response:
```json
{
  "message": "missing parameters",
  "required": [["url"]],
  "submitted": [{}],
}
```

Request:
```ruby
/uploadImageUrl/usage
```

Response:
```json
{
  "message": "usage info: /uploadImageUrl",
  "description": "upload an image to the backend via image url",
  "end_points": {
    "/uploadImageUrl": {
      "returns": "missing paramaters"
    },
    "/uploadImageUrl/usage": {
      "returns": "message: 'usage-info'"
    },
    "/uploadImageUrl/<param_name>/<param_value>": {
      "url_paths": "upload with: 'param_name=param_value'",
      "example": "/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
      "response": {
        "message": "image url uploaded",
        "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
        "filename": "/static/img/2.png"
      }
    },
    "/uploadImageUrl?param_name=param_value": {
      "url_paths": "upload with: 'param_name=param_value'",
      "example": "/uploadImageUrl?url=https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
      "response": {
        "message": "image url uploaded",
        "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
        "filename": "/static/img/2.png"
      }
    },
    "Required": {
      "Parameters": {
        "url": "TEXT"
      }
    },
    "Response": {
      "message": "image url uploaded",
      "url": "TEXT",
      "filename": "TEXT"
    }
  }
}
```

Arguments:
```Mpython
url = "https://api.crimemap.hopto.org/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png"
```

Request:
```ruby
https://api.crimemap.hopto.org/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
  "filename": "/static/img/1.png"
}
```

</details>

---
