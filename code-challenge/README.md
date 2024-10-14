
# Flask API Challenge - Models, Relationships, Validations, and Routes

## Overview

This project is a Flask API that manages Episodes, Guests, and Appearances. It showcases the implementation of models, relationships, validations, and routes using SQLAlchemy. You will create and manage data for these entities through the API.

## Setup

To download the dependencies for the backend, run:

```sh
pipenv install
```

There is some starter code in the `app/seed.py` file that can help populate your database after you've set up the models and migrations.

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by running:

```sh
python app.py
```

You can interact with the API via tools like Postman, cURL, or your preferred API client.

There are also tests included, which you can run using `pytest -x` to check your work.

## Models

The API keeps track of guests that have appeared in various episodes of a show. There are three main models:

- `Guest`
- `Episode`
- `Appearance`

### Relationships

- An `Episode` has many `Guests` through `Appearance`
- A `Guest` has many `Episodes` through `Appearance`
- An `Appearance` belongs to both a `Guest` and an `Episode`

### Validations

The `Appearance` model must validate:

- `rating` between 1 and 5 (inclusive).

### Database Migrations

After setting up your models and relationships, run the migrations and seed the database using the following commands:

```sh
flask db revision --autogenerate -m 'message'
flask db upgrade
python app/seed.py
```

If the provided seed file does not work, you can generate your own seed data for testing purposes.

## Routes

### GET /episodes

Return JSON data of all episodes in the following format:

```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

### GET /episodes/:id

Return detailed information for a specific episode, including its guests:

```json
{
  "id": 100,
  "date": "9/30/99",
  "number": 100,
  "guests": [
    {
      "id": 122,
      "name": "Bruce McCulloch",
      "occupation": "actor"
    },
    {
      "id": 123,
      "name": "Mark McKinney",
      "occupation": "actor"
    }
  ]
}
```

If the episode does not exist, return:

```json
{
  "error": "Episode not found"
}
```

### DELETE /episodes/:id

Delete an episode and any associated appearances. If successful, return an empty response. If the episode does not exist, return:

```json
{
  "error": "Episode not found"
}
```

### GET /guests

Return JSON data of all guests:

```json
[
  {
    "id": 122,
    "name": "Bruce McCulloch",
    "occupation": "actor"
  },
  {
    "id": 123,
    "name": "Mark McKinney",
    "occupation": "actor"
  }
]
```

### POST /appearances

Create a new `Appearance` by associating an existing episode and guest, with a rating between 1 and 5. Request body:

```json
{
  "rating": 5,
  "episode_id": 100,
  "guest_id": 123
}
```

Successful response:

```json
{
  "id": 1,
  "rating": 5,
  "episode": {
    "id": 100,
    "date": "9/30/99",
    "number": 100
  },
  "guest": {
    "id": 123,
    "name": "Mark McKinney",
    "occupation": "actor"
  }
}
```

If validation fails, return:

```json
{
  "errors": ["validation errors"]
}
```


## Conclusion

This API allows you to manage episodes, guests, and their appearances on a show, focusing on key features such as database relationships, data validation, and efficient route handling.