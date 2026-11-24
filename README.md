# GameLog

**GameLog** is a web application for discovering video games, building a personal game library, and tracking gaming progress.

The project is built with Django and integrates with the RAWG API to retrieve video game information.

## Features

### Implemented

- Search for video games by title using the RAWG API.
- View game details, including descriptions, release dates, and ratings.
- **Search filters** — by genre, platform, and release year.
- **User registration and authentication** (login, logout, register).
- **Personal game library** — add games from RAWG with a status:
  - Planned, Playing, Completed, Dropped.
- **Wishlist** — games the user wants to play.
- **Personal game ratings and reviews** — rate games 1–5 and write a review.
- **Game recommendation system** — suggests games based on the user's most played/completed genres.
- **Admin panel** — manage genres, developers, publishers, platforms, games, library entries, wishlist, and ratings.

### Planned

- Improve and finalize the user interface.
- Prepare the application for deployment.

## Tech Stack

- **Python** — primary programming language.
- **Django** — web framework.
- **RAWG API** — external video game database.
- **HTML / CSS** — frontend.
- **python-dotenv** — environment variable management.
- **Git** — version control.

## Project Structure

```text
GameLog/
├── gamelog/            # Django project settings
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── games/              # Django app
│   ├── migrations/
│   ├── templates/games/
│   │   ├── base.html
│   │   ├── game_detail.html
│   │   ├── game_list.html
│   │   ├── game_search.html
│   │   ├── login.html
│   │   ├── rate_game.html
│   │   ├── rawg_game_detail.html
│   │   ├── recommendations.html
│   │   ├── register.html
│   │   ├── user_library.html
│   │   └── wishlist.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/css/
│   └── style.css
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd GameLog/gamelog
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Linux / macOS**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (next to `manage.py`):

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
RAWG_API_KEY=your-rawg-api-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

You can obtain a RAWG API key at: https://rawg.io/apidocs

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## Running Tests

```bash
python manage.py test games
```

## Roadmap

- [x] Search for video games by title using the RAWG API.
- [x] View game details.
- [x] Search filters (genre, platform, year).
- [x] User registration and authentication.
- [x] Personal game library with status tracking.
- [x] Wishlist.
- [x] Personal game ratings and reviews.
- [x] Game recommendation system.
- [x] Automated tests.
- [ ] Improve and finalize the user interface.
- [ ] Prepare the application for deployment.

## Project Status

**In Development**

GameLog is a personal development project focused on improving backend development skills with Python and Django.