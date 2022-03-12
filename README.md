# Introduction

Instagram-clone type of application with main focus on authentication and authorization.

### Technology used
Django&Python

### Db
SQLite3

### Libraries
Pillow, Oauthlib, Urllib3

## Running the project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repo, cd into the folder and create your virtual environment

```
python -m venv venv
```

That will create a new folder `env` in your project directory. Next activate the environment

Mac OS / Linux:
```
source venv/bin/activate
```

Windows:
```
venv\Scripts\activate
```

Install the project dependencies with

```
pip install -r requirements.txt
```

Run migrations

```
python manage.py migrate
```

Run local server

```
python manage.py runserver
```

## Demo
Profile 
![Screenshot (546)](https://user-images.githubusercontent.com/85017668/149665043-8bd8a633-2d51-4215-9e54-daf477da8a24.png)
Login
![Screenshot (547)](https://user-images.githubusercontent.com/85017668/149665048-4ebd5d71-d55c-4ae9-86c2-61881e403873.png)
Sign-up
![Screenshot (548)](https://user-images.githubusercontent.com/85017668/149665059-b9e7d53d-8384-4fa6-b8d8-9fe1d8dfd32a.png)
Forgot password
![Screenshot (549)](https://user-images.githubusercontent.com/85017668/149665063-a26a5ef2-eacf-4b75-b6fe-6f78e0dab95f.png)
