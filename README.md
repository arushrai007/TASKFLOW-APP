<<<<<<< HEAD
# 🚀 TaskFlow: Full-Stack TO-DO Application

<p align="center"> <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"> <img alt="React" src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black"> <img alt="MongoDB" src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"> <img alt="Tailwind CSS" src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white"> </p>

A modern, full-stack TO-DO task management application built with a powerful Python (FastAPI) backend and a sleek React frontend. This project is designed for users to securely manage their tasks with features like authentication, task prioritization, filtering, and analytics.

## ✨ Features

  * **Secure User Authentication:** JWT-based user signup and login system with password hashing.
  * **Full CRUD for Tasks:** Create, read, update, and delete tasks.
  * **Task Details:** Add priorities (High, Medium, Low), descriptions, due dates, categories, and tags.
  * **Powerful Dashboard:**
      * **Search:** Instantly find tasks by title, description, or tags.
      * **Filter:** View all, completed, or incomplete tasks.
      * **Sort:** Organize tasks by creation date, priority, or due date.
  * **Analytics Page:** Get a quick overview of your productivity with stats on total, completed, pending, and overdue tasks.
  * **Dark Mode:** A beautiful, responsive UI with a dark mode toggle.
  * **Responsive Design:** Clean and modern interface built with Tailwind CSS and `shadcn/ui`.

-----

## 💻 Tech Stack

| Area | Technology |
| :--- | :--- |
| **Backend** | Python, FastAPI, Motor (Async MongoDB), Uvicorn, JWT |
| **Frontend** | React, React Router, Context API, Tailwind CSS, shadcn/ui |
| **Database** | MongoDB Atlas |

-----

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

  * **Python 3.7+** & `pip`
  * **Node.js** & `yarn` (or `npm`)
  * **MongoDB Atlas Account:** A (free) MongoDB cloud database.

### 1\. Configure Backend

1.  **Navigate to the backend:**
    ```bash
    cd TO-DO-APP-main/backend
    ```
2.  **Create a virtual environment:**
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create `.env` file:** Create a file named `.env` inside the `backend` folder and add the following, replacing the placeholders with your own credentials:
    ```env
    # Your MongoDB connection string
    MONGO_URL="mongodb+srv://<USERNAME>:<PASSWORD>@cluster0.xhqncic.mongodb.net/"

    # The name for your database (can be anything)
    DB_NAME="todo_database"

    # URL for your frontend
    CORS_ORIGINS="http://localhost:3000"

    # A strong secret key for JWT
    JWT_SECRET_KEY="your-super-strong-secret-key-here"
    ```
5.  **Whitelist your IP in MongoDB Atlas:**
      * Go to your MongoDB Atlas dashboard.
      * Go to **Security** \> **Network Access**.
      * Click **"Add IP Address"** and select **"Allow Access From My Current IP Address"**.

### 2\. Configure Frontend

1.  **Navigate to the frontend:**
    ```bash
    cd TO-DO-APP-main/frontend
    ```
2.  **Install dependencies:**
    ```bash
    yarn install
    ```
3.  **Create `.env` file:** Create a file named `.env` inside the `frontend` folder and add the following:
    ```env
    REACT_APP_BACKEND_URL="http://localhost:8000"
    ```

-----

## ▶️ How to Run

You must run both the backend and frontend in two separate terminals.

1.  **Terminal 1: Run the Backend**

    ```bash
    # Go to the backend directory
    cd TO-DO-APP-main/backend

    # Activate the virtual environment
    source venv/bin/activate  # (or .\venv\Scripts\activate on Windows)

    # Start the server
    uvicorn server:app --reload
    ```

    ✅ Your backend is now running at `http://localhost:8000`

2.  **Terminal 2: Run the Frontend**

    ```bash
    # Go to the frontend directory
    cd TO-DO-APP-main/frontend

    # Start the React app
    yarn start
    ```

    ✅ Your frontend is now running at `http://localhost:3000`

You can now access the application in your browser at `http://localhost:3000`.
=======
# Here are your Instructions
>>>>>>> bd739ec (Initial commit: Added full project code)
