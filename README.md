# 📝 Notes API

A simple REST API for managing personal notes, built with **FastAPI**.

---

## Endpoints

### 👤 Users — `/users`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register a new user |
| POST | `/users/login` | Login and get token |
| GET | `/users/me` | Get current user profile |

### 📝 Notes — `/notes`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | Get all your notes |
| POST | `/notes` | Create a new note |
| GET | `/notes/{id}` | Get a single note |
| PUT | `/notes/{id}` | Update a note |
| DELETE | `/notes/{id}` | Delete a note |

---

## Quick Start

```bash
git clone https://github.com/your-username/notes-api.git
cd notes-api
pip install -r requirements.txt
uvicorn main:app --reload
```

API runs at **`http://localhost:8000`**  
Swagger docs at **`http://localhost:8000/docs`**

---

## License

[MIT](LICENSE)
