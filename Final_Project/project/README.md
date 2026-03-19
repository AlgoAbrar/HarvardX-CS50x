# Habit Tracker & Goal Monitor

A web-based habit tracking application built with Flask (Python), SQLite, and JavaScript that helps users build and maintain daily habits through visual tracking and streak monitoring.

## Features

- **User Authentication**: Secure registration and login system
- **Habit Management**: Create, edit, and delete habits with custom colors and frequencies
- **Daily Tracking**: Toggle habit completion for each day
- **Streak Counter**: Automatically calculates and displays current habit streaks
- **Calendar View**: Visual monthly calendar showing habit completion history
- **Statistics Dashboard**: Detailed analytics on habit performance and completion rates
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Python with Flask web framework
- **Database**: SQLite with SQLAlchemy-style queries
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Visualization**: Chart.js for statistics and progress charts
- **Authentication**: Werkzeug password hashing and session management

## Project Structure

```
habit-tracker/
├── app.py                 # Main Flask application
├── helpers.py            # Utility functions and database helpers
├── habits.db             # SQLite database (created on first run)
├── requirements.txt      # Python dependencies
├── init_db.py           # Database initialization script
├── static/
│   ├── styles.css       # Application styles
│   └── script.js        # Frontend JavaScript functionality
└── templates/
    ├── layout.html      # Base template with navigation
    ├── index.html       # Dashboard/homepage
    ├── login.html       # User login page
    ├── register.html    # User registration page
    ├── habits.html      # Habit management page
    ├── calendar.html    # Calendar view page
    └── statistics.html  # Statistics and analytics page
```

## Database Schema

The application uses three main tables:

1. **users**: Stores user account information
   - id (INTEGER PRIMARY KEY)
   - username (TEXT UNIQUE)
   - hash (TEXT - password hash)

2. **habits**: Stores user habits
   - id (INTEGER PRIMARY KEY)
   - user_id (INTEGER FOREIGN KEY)
   - name (TEXT)
   - color (TEXT)
   - frequency (TEXT - daily, weekly, weekdays, weekends)
   - created_at (TIMESTAMP)

3. **completions**: Tracks daily habit completions
   - id (INTEGER PRIMARY KEY)
   - habit_id (INTEGER FOREIGN KEY)
   - date (DATE)
   - completed (BOOLEAN)
   - notes (TEXT)
   - created_at (TIMESTAMP)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project files**

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   python init_db.py
   ```
   This will create the `habits.db` file with all necessary tables.

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage Guide

### Creating an Account

1. Navigate to the registration page
2. Choose a username and password (minimum 6 characters)
3. You will be automatically logged in after registration

### Adding Habits

1. Click "Habits" in the navigation bar
2. Enter a habit name (e.g., "Morning Exercise")
3. Choose a color for visual identification
4. Select a frequency (daily, weekly, etc.)
5. Click "Add Habit"

### Tracking Daily Habits

1. On the dashboard, you'll see all your habits for today
2. Toggle the switch next to each habit to mark it as completed
3. Your streak counter will update automatically
4. Completed habits are saved immediately

### Viewing Calendar

1. Click "Calendar" in the navigation bar
2. Navigate between months using the Previous/Next buttons
3. Each day shows colored dots for completed habits
4. Hover over dots to see which habits were completed

### Viewing Statistics

1. Click "Statistics" in the navigation bar
2. View completion rates for each habit
3. See your best and worst performing habits
4. View daily completion trends over the last 30 days

## API Endpoints

- `GET /` - Dashboard (requires login)
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /register` - Registration page
- `POST /register` - Process registration
- `GET /logout` - Logout user
- `GET /habits` - Habit management page
- `POST /habits` - Add/edit/delete habits
- `POST /toggle` - Toggle habit completion (AJAX)
- `GET /calendar` - Calendar view
- `GET /statistics` - Statistics page

## Configuration

The application uses the following Flask configuration:

- `SESSION_PERMANENT = False` - Sessions expire when browser closes
- `SESSION_TYPE = "filesystem"` - Store sessions on the filesystem
- Debug mode is enabled by default (for development)

## Security Features

- Password hashing using Werkzeug security utilities
- SQL injection protection through parameterized queries
- Session-based authentication
- Login-required decorator for protected routes
- Input validation and sanitization

## Customization

### Changing Colors
Edit the color values in:
- `static/styles.css` - Main application colors
- Habit creation form - Individual habit colors

### Adding New Habit Frequencies
1. Update the frequency options in `templates/habits.html`
2. Add frequency validation in `app.py` if needed

### Modifying Streak Calculation
The streak calculation logic is in the `calculate_streak()` function in `app.py`. Modify this function to change how streaks are calculated.

## Troubleshooting

### Common Issues

1. **"Database is locked" error**
   - Ensure only one instance of the application is running
   - Check if the database file has proper read/write permissions

2. **CSS/JS files not loading**
   - Check if the Flask server is running
   - Clear browser cache
   - Verify file paths in templates

3. **"Module not found" errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Login/Registration issues**
   - Ensure database is properly initialized with `python init_db.py`
   - Check for duplicate usernames during registration

### Debug Mode
The application runs in debug mode by default. For production deployment, set `debug=False` in `app.py`:

```python
if __name__ == "__main__":
    app.run(debug=False)
```

## Deployment Notes

For production deployment:

1. **Change the secret key**: Generate a secure secret key for Flask sessions
2. **Disable debug mode**: Set `debug=False` in `app.py`
3. **Use a production server**: Consider using Gunicorn or uWSGI
4. **Use a production database**: Consider migrating to PostgreSQL for better performance
5. **Set up HTTPS**: Use a reverse proxy like Nginx with SSL certificates
6. **Environment variables**: Store sensitive data in environment variables

## License

This project is provided for educational purposes. Feel free to modify and distribute as needed.

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments for specific functionality
3. Ensure all dependencies are correctly installed

## Future Enhancements

Potential features for future development:

1. Email reminders for habit completion
2. Social features (friend connections, sharing)
3. Mobile application version
4. Data export (CSV, JSON)
5. Advanced analytics and reporting
6. Goal setting with progress tracking
7. Habit categories and tags
8. Custom frequency patterns
9. Offline functionality
10. API for third-party integrations

---

*This application is designed for personal use and educational purposes.*
