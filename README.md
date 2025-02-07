# Chat Application

This is a real-time chat application built with a React frontend and a Django backend. It allows users to create accounts, start conversations, and exchange messages in real-time.

live verssion is at https://irateassessment.netlify.app/

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- Node.js (v14.0.0 or later)
- npm (v6.0.0 or later)
- Python (v3.8 or later)
- pip (v20.0 or later)
- PostgreSQL (v12.0 or later)

## Frontend Setup

1. Clone the repository:
   \`\`\`
   git clone https://github.com/Digidev-hash/iratefrontend.git
  
   \`\`\`

2. run npm install
   \`\`\`
   
   \`\`\`

3. Install the dependencies:
   \`\`\`
   npm install
   \`\`\`


4. Start the development server:
   \`\`\`
   npm run dev
   \`\`\`

The frontend should now be running on \`localhost`.

## Backend Setup

1. Navigate to the backend directory:
   \`\`\`
   clone this repository
   \`\`\`

2. Create a virtual environment and activate it:
   \`\`\`
   python -m venv venv
   source venv/bin/activate  # On Windows, use \`venv\\Scripts\\activate\`
   \`\`\`

3. Install the required Python packages:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

4. Create a PostgreSQL database for the project.

5. Create a \`.env\` file in the backend root directory and add the following:
   \`\`\`
   DEBUG=True
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=postgres://username:password@localhost:5432/database_name
   \`\`\`
   Replace \`your_secret_key_here\` with a secure random string, and update the database URL with your PostgreSQL credentials.

6. Run migrations:
   \`\`\`
   python manage.py migrate
   \`\`\`

7. Create a superuser:
   \`\`\`
   python manage.py createsuperuser
   \`\`\`

8. Start the Django development server:
   \`\`\`
   python manage.py runserver
   \`\`\`

The backend should now be running on \`http://localhost:8000\`.

## Running the Application

With both the frontend and backend servers running, you can now use the application:

1. Open your browser and 
2. Register a new account or log in with existing credentials
3. Start chatting!

## Additional Notes

- The backend uses Django Channels for WebSocket support. Make sure you have Redis installed and running for the WebSocket functionality to work correctly.
- For production deployment, you'll need to set up proper web servers (e.g., Nginx) and process managers (e.g., Gunicorn for Django, PM2 for Next.js).
- Remember to never commit sensitive information like secret keys or database credentials to your repository.

## Troubleshooting

If you encounter any issues while setting up or running the application, please check the following:

1. Ensure all prerequisites are correctly installed and up to date.
2. Verify that all environment variables are correctly set.
3. Check the console output for both frontend and backend for any error messages.

If problems persist, please open an issue in the GitHub repository with a detailed description of the problem and the steps to reproduce it.
\`\`\`

This README provides a comprehensive guide for setting up and running your chat application locally. It includes instructions for both the frontend and backend, as well as some additional notes and troubleshooting tips. You may need to adjust some details (like the GitHub repository URL) to match your specific project setup.

