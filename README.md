
# Role Manager

## Overview

Role Manager is a web application designed to manage and assign roles within an organization or group. This application leverages Flask, SQLAlchemy, and jQuery to provide a responsive and interactive experience for managing role assignments and requests.

## Features

- Request roles with specific player information.
- Assign roles dynamically.
- Release roles when no longer needed.
- Display current roles and waiting queue.
- Asynchronous data fetching and rendering using jQuery.

## Project Structure

```plaintext
role_manager/
├── __init__.py
├── app.py
├── config.py
├── create_app.py
├── models.py
├── role_manager.py
├── routes/
│   ├── __init__.py
│   ├── main_routes.py
│   ├── role_routes.py
├── static/
├── templates/
│   ├── base.html
│   ├── index.html
```

### Files

- **`__init__.py`**: Marks the directory as a Python package.
- **`app.py`**: Entry point for running the Flask application.
- **`config.py`**: Contains configuration settings for the Flask application.
- **`create_app.py`**: Factory function to create and configure the Flask application.
- **`models.py`**: Defines database models using SQLAlchemy.
- **`role_manager.py`**: Contains the `RoleManager` class for managing roles.
- **`routes/__init__.py`**: Initializes and registers routes with the Flask application.
- **`routes/main_routes.py`**: Contains the main application routes.
- **`routes/role_routes.py`**: Contains routes for role-related operations.
- **`static/`**: Directory for static files like CSS and JavaScript.
- **`templates/`**: Directory for HTML templates.

## Setting Up the Project

### Prerequisites

- Python 3.8 or later
- Virtualenv (optional but recommended)
- SQLite (default database)

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/blackms/role_manager.git
   cd role_manager
   ```

2. **Create and Activate Virtual Environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the project root and set the necessary environment variables.

   ```plaintext
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///app.db
   ```

5. **Initialize the Database**

   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the Application**

   ```sh
   flask run
   ```

   The application should now be running at `http://127.0.0.1:5000`.

## Detailed Code Explanation

### `create_app.py`

The `create_app` function sets up the Flask application, configures the database, and registers blueprints.

### `models.py`

Defines the `RoleRequest` model with fields for `alliance`, `player`, `role`, `coordinates`, `request_time`, and `status`.

### `role_manager.py`

Contains the `RoleManager` class that handles role requests, assignments, and releases.

### `routes/__init__.py`

Registers the route blueprints with the Flask application.

### `routes/role_routes.py`

Contains routes for handling role requests, assignments, and releases, and serves JSON data for asynchronous operations.

### `templates/index.html`

Uses jQuery to asynchronously fetch and display data. Handles form submissions for role requests and updates the DOM dynamically.

## Running the Application

1. **Start the Flask Development Server**

   ```sh
   flask run
   ```

2. **Access the Application**

   Open a web browser and navigate to `http://127.0.0.1:5000`.

## Making Requests and Managing Roles

1. **Requesting a Role**

   Fill out the form on the home page to request a role. The request is handled by the `/request_role` endpoint and updates the waiting queue.

2. **Assigning a Role**

   Click the "Assign" button next to a role to assign it to the next request in the queue. The assignment is handled by the `/assign_role/<role>` endpoint.

3. **Releasing a Role**

   Click the "Release" button next to an assigned role to release it. The release is handled by the `/release_role/<role>` endpoint.

## Contributing

1. **Fork the Repository**

2. **Create a Branch**

   ```sh
   git checkout -b feature/your-feature
   ```

3. **Commit Your Changes**

   ```sh
   git commit -m "Add your feature"
   ```

4. **Push to the Branch**

   ```sh
   git push origin feature/your-feature
   ```

5. **Open a Pull Request**

## License

This project is licensed under the MIT License.

---

By following this guide, you should be able to set up, run, and understand the Role Manager application. If you encounter any issues or have further questions, please consult the project's documentation or open an issue on the GitHub repository.
