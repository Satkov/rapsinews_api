# RAPSI News API

## Project Description

RAPSI News API is a backend for a mobile news application that parses RSS pages to provide access to a list of news articles, bookmarks, and search functionality via a REST API. The project is built using Django, with Django Rest Framework for API development, Redis for caching, and PostgreSQL as the database.

## Installation and Launch

### Cloning the Repository

```
git clone <repository>
cd rapsinews_api
```

### Installing Dependencies

The project uses Poetry:

```
poetry install
```

### Environment Variables Configuration

Create a `.env` file in the root folder with the following content:

```
POSTGRES_DB=rapwsinews
POSTGRES_USER=rapwsinews_user
POSTGRES_PASSWORD=rapwsinews_pass
```

### Running the Application with Docker Compose

```
docker-compose up --build
```

The application will be available at:

```
http://localhost:8000/
```

## API Endpoints

### Get List of Posts

**GET /api/v1/posts/**

Response Example:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/posts/?limit=10&offset=10",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "News 1",
      "link": "http://example.com",
      "image": "http://example.com/image.jpg",
      "category": "Politics",
      "published": "2025-05-13T12:00:00Z",
      "full_text": "News text"
    }
  ]
}
```

### Add Posts to Bookmarks

**POST /api/v1/bookmarks/**

Request Body:

```json
{
  "ids": [1, 2, 3]
}
```

Response Example:

```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "title": "News 1",
      "link": "http://example.com"
    }
  ]
}
```

### Search for News by Title

**GET /api/v1/search/?query=news**

Response Example:

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "title": "News 1",
      "link": "http://example.com"
    }
  ]
}
```

## Dependencies

| Dependency                | Version   |
| ------------------------- | --------- |
| Python                    | 3.12      |
| Django                    | 5.1       |
| Django Rest Framework     | 3.15      |
| PostgreSQL                | 16-alpine |
| Redis                     | 7-alpine  |
| Docker and Docker Compose | Latest    |
| Gunicorn                  | 23.0.0    |
| Poetry                    | 2.0.0+    |

## License

The project is distributed under the Apache 2.0 license.
