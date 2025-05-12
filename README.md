# rapsinews API

A lightweight RESTful service powering the **RAPSI** mobile application. It exposes endpoints for listing, searching and bookmarking news posts.

Built with **Django 5.1** and **Django REST Framework 3.15+**.

---

## Features

* Search posts by title (`/api/v1/search/?query=...`)
* List all posts ordered by publication date (newest first)
* Bookmark any set of posts by sending their IDs
* Limit–offset pagination with `limit` and `offset` parameters (default 10, max 50)

## Requirements

Python ≥ 3.12

```
django==5.1
djangorestframework>=3.15,<4.0
feedparser>=6.0.11,<7.0.0
python-dateutil>=2.9.0.post0,<3.0.0
beautifulsoup4>=4.13.4,<5.0.0
django-apscheduler>=0.7.0,<0.8.0
requests>=2.32.3,<3.0.0
```

Install everything with **Poetry**:

```bash
poetry install
```

## Running the development server

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/v1/`.

## API Documentation

### 1. List posts

```
GET /api/v1/posts/?limit=10&offset=0
```

### 2. Search posts

```
GET /api/v1/search/?query=bankruptcy
```

### 3. Bookmark posts

```
POST /api/v1/bookmarks/
Content-Type: application/json

{
  "ids": [1, 42, 99]
}
```

### Example JSON response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 42,
      "title": "Supreme Court clarifies insolvency rules",
      "link": "https://rapsi.org/news/42",
      "image": "https://rapsi.org/images/42.jpg",
      "category": "Judicial News",
      "published": "2025-05-11T08:15:00Z",
      "full_text": "Full article text..."
    },
    {
      "id": 41,
      "title": "Constitutional Court decision on tax benefits",
      "link": "https://rapsi.org/news/41",
      "image": null,
      "category": "Constitutional Law",
      "published": "2025-05-10T14:30:00Z",
      "full_text": "Full article text..."
    }
  ]
}
```

## Data model

| Field      | Type           | Description                      |
| ---------- | -------------- | -------------------------------- |
| id         | Integer (PK)   | Auto-generated primary key       |
| title      | CharField(255) | Post title                       |
| link       | URLField       | Unique link to the original post |
| image      | URLField       | Optional preview image           |
| category   | CharField(255) | Human‑readable category          |
| published  | DateTimeField  | Publication timestamp            |
| full\_text | TextField      | Complete article text            |

## License

Distributed under the **Apache License 2.0**. See the `LICENSE` file for full text.
