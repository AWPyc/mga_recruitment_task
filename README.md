# Task Manager API

A simple task tracking API built with **Django DRF**, using **PostgreSQL** and containerized with **Docker**.

---

## ⚙️ Features

* User registration & authentication (JWT + Session)
* Tasks with assignment and status updates
* Filtering for tasks
* Pagination
* PostgreSQL database
* Dockerized environment with **docker-compose**

---

## 🐳 Run with Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/AWPyc/mga_recruitment_task.git
   cd mga_recruitment_task
   ```

2. Copy example environment and adjust values:

   ```bash
   cp .env_example .env
   ```

   Adjust values in `.env`:

   ```
   DEBUG=true
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

   POSTGRES_USER=example_user
   POSTGRES_PASSWORD=example_passwd
   POSTGRES_DB=example_db
   ```

3. Build and run:

   ```bash
   docker-compose up --build
   ```

4. Migrations should be done automatically, if not run them manually (only needed first time if container didn’t do it):

   ```bash
   docker-compose run migrate
   ```

5. Access API at:

   * `http://localhost:8000/`
   * `http://localhost:8000/auth/registration/` - user register
   * `http://localhost:8000/auth/login/` - user login
   * `http://localhost:8000/tasks/` - task list
   * `http://localhost:8000/tasks/<task_id>` - task details
   * `http://localhost:8000/task_history` - task list history
   * Admin panel: `http://localhost:8000/admin/`

---


## 🔑 Authentication
Use e.g. Postman to send API requests:
* **JWT** (use application/x-form-www-urlencoded):
    
    * Obtain: `POST /api/token/ { "username": "...", "password": "..." }`
    * Refresh: `POST /api/token/refresh/`
    * To access any endpoint after authentication:
        - add `Authorization: Bearer <your_token>` to header    request

* **Session auth** works for browsing API in Django templates.


## 🔍 Filtering
* **/tasks/**
    * `/?id=<task_id>`
    * `/?title=<title_icontains>`
    * `/?description=<desc_icontains>`
    * `/?status=<status_value>` status_values: [new, in_progress, resolved]
    * `/?assigned_to=<user_id>`
* **/task_history/**
    * `/?title=<task_id>`

## 📂 Project Structure

```
core/               # Main Django project
tasks/              # Tasks app
users/              # Users app
templates/          # Templates for user registration/login
entrypoints/        # Entrypoint scripts for Docker
Dockerfile
docker-compose.yml
.env_example
requirements.txt
README.md
```

---
