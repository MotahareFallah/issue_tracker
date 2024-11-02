# Issue Tracker

A simple issue-tracking application built with Python and Django. This project allows users to create, manage, and track issues efficiently.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Features

- **User Authentication**: Register and log in to manage your issues securely.
- **Issue Management**: Create, view, update, and delete issues.
- **Status Tracking**: Keep track of the status of each issue (e.g., open, in progress, closed).
- **Responsive Design**: Access the application from any device.

## Technologies Used

- **Python**: The programming language used for backend development.
- **Django**: A lightweight web framework for building web applications.
- **Postgres**: A lightweight database for storing user and issue data.
- **HTML/CSS/JavaScript**: For frontend development.
- **Docker**: for running the project easily in the cloud.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MotahareFallah/issue_tracker.git
   cd issue_tracker
   ```
   
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

4. **Set up the database**:
  - Initialize the database by running the application for the first time or using a provided script (if available).

5. **Run the application**:
   ```bash
   python manage.py runserver
   ```

   The application will be available at http://127.0.0.1:8000.

## Usage

1. Open your web browser and navigate to http://127.0.0.1:5000.
2. Register a new account or log in with an existing account.
3. Start creating and managing your issues!

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeature).
3. Make your changes and commit them (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.

## License

This project is licensed under the MIT License. Feel free to customize this README further based on specific features or instructions relevant to your project!


   
