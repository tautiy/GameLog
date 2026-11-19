# GameLog

**GameLog** is a web application for discovering video games, building a personal game library, and tracking gaming progress.

The project is built with Django and integrates with the RAWG API to retrieve video game information.

## Features

### Implemented
- Search for video games by title using the RAWG API.
- View game details, including descriptions, release dates, and ratings.

### Planned
- User registration and authentication.
- Personal game library.
- Wishlist for games users want to play.
- Game status tracking (Planned, Played).
- Personal game ratings and reviews.
- Game recommendation system.

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
├── gamelog/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── games/
│   ├── migrations/
│   ├── templates/
│   │   └── games/
│   ├── models.py
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd GameLog
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

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
RAWG_API_KEY=your-rawg-api-key
```

You can obtain a RAWG API key at:

https://rawg.io/apidocs

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

The application will be available at:

http://127.0.0.1:8000/

## Roadmap

- [ ] Improve and finalize the user interface.
- [ ] Implement personal game libraries.
- [ ] Add user authentication.
- [ ] Implement a game recommendation system.
- [ ] Add game ratings and reviews.
- [ ] Improve search and filtering functionality.
- [ ] Add automated tests.
- [ ] Prepare the application for deployment.

## Project Status

**In Development**

GameLog is a personal development project focused on improving backend development skills with Python and Django.