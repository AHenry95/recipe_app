# Recipe App

A Django web application for discovering, creating, and sharing recipes. Users can browse recipes, save favorites, and upload their favorite recipes. 

**Live Demo:** [Recipe App on Heroku](https://sheltered-basin-42687-d57135d9635e.herokuapp.com/)

## Features

### Recipe Management
- **Create and Manage Recipes** - Add recipes with ingredients, cooking time, instructions, and photos
- **Automatic Difficulty Rating** - Recipes are automatically categorized as Easy, Medium, Intermediate, or Hard based on their cooking time and ingredient count
- **Author Permissions** - Only recipe authors can edit or delete their own recipes

### User System
- **User Registration & Authentication** - Secure signup, login, and logout functionality
- **User Profiles** - Personal dashboard displaying authored recipes and favorites
- **Favorites** - Save favorite recipes via favorite button on recipe detail page

### Search & Discovery
- **Advanced Search** - filter recipes by name, ingredient, difficulty level, or maximum cooking time
- **Data Visualization** - Generate charts to analyze recipe data:
  - Bar chart: Cooking time by recipe
  - Pie chart: Recipe distribution by diffiulty
  - Line chart: Recipe distribution by difficulty

### User Experience
- **Responseive Design** - Clean interface that works on desktop and mobile
- **Protected Content** - Recipe details require authentication, encouraging user registation
- **Visual Feedback** - Elements such as color-coded difficulty badges and interctive UI elements 

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Python 3.11, Django 4.2 |
| Database | PostgreSQL (production), SQLite (devlopment) |
| Data Visualization | Pandas, Matplotlib |
| Static Files | Whitenoise |
| Production Server | Gunicorn |
| Image Processing | Pillow |
| Deployment | Heroku |

## Installation

### Prerequisites
- Python 3.11+
- pip
- virtual environment (

### Local Development Setup

1. **Clone the repoitory**
  ```bash 
  git clone https://github.com/AHenry95/recipe-app.git
  cd recipe-app
  ```

2. **Create and activate a virtual environment** 
  ```bash
  # Mac: python -m venv venv source venv/bin/activate
  # Windows: python -m venv venv/Scripts/activate
  ```

3. **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```
4. **Navigate to the source directory**
  ```bash
  cd src
  ```

5. **Run database migrations**
  ```bash
  python manage,py migrate
  ```

6. **Create a superuser for admin access**
  ```bash
  python manage.py createsuperuser
  ```

7. **Run development server**
  ```bash
  python manage.oy runserver
  ```

8. **Access the application**  
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Visitors
- Browse the home page to see available recipes
- View recipe cards with cooking times and difficulty ratings

### For Registered Users
- **View Recipes** - Access full recipe details, including ingredients and instructions
- **Add Recipes** - Create new recipes with the "Add Recipe" button in the nav bar
- **Manage Your Recipes** - Edit or delete recipes you've added from each recipe's detail page
- **Save Favorites** - Click "Add Favorite" button on any recipe's detail page to save to your favorites
- **Search** - Use the search page to find recipes, using various critera, and to generate data visulizations about the search results
- **Profile** - View all your authored and favorited recipes in one place

### Difficulty Calcuation

Recipe difficulty is automatically assigned based on the following criteria:

| Difficulty | Criteria |
|------------|----------|
| Easy | < 10 minutes AND < 4 ingredients |
| Medium | < 10 minutes AND >= 4 ingredients |
| Intermediate | >= 10 minutes AND  < 4 ingredients |
| Hard | >= 10 minutes AND >= 4 ingredients |

## Testing

To run the test suite:

```bash
cd src
python manage,py test recipes
```

The test suites includes:
- Model tests (difficulty calculation, field validation)
- URL resolution tests
- View tests (authentication, CRUD operations)
- Form validation tests
- Chart generation tests
- Integration tests (user flows)

## Enivronmet Variables

For production deployment, set the following environment variables:

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Django secret key for sessions, tokens, and security features |
| `DEBUG` | Sate to `False` in production |
| `DaATABASE_URL` | PostgreSQL connection string |

## Deployment

This application is configured for Heroku deployment:

1. Ensure `Procfile` and `requirements.txt` are in the root directory
2. Configure the environment variables with Heroku
3. Deploy via Heroku CLI or Heroku-Github integration

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch(`git push origin feature/new-feature`)
5. Open a Pull request

## Acknoledgements
- The project was created as part of CareerFoundry's FullStack Web Development/Python for Web Developers curriculum 
