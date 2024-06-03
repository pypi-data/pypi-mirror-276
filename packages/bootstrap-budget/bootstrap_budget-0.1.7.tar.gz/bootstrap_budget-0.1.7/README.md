# Bootstrap-Budget: Pull your budget up by its bootstraps!
Bootstrap Budget is a user-friendly financial application designed to help you manage your money and achieve your financial goals. Built with simplicity and self-reliance in mind, Bootstrap Budget allows you to track income, expenses, and budgets for a streamlined personal finance experience – all hosted on your own server.

## Getting Started
### Prerequisites:
* Python 3.x (https://www.python.org/downloads/)

### Installation:
1. Create a Python Virtual Environment:

    It's recommended to install Bootstrap Budget within a virtual environment to isolate its dependencies from other Python projects on your system. You can use tools like `venv` or `virtualenv` to create one. Refer to the official Python documentation for instructions on creating virtual environments: https://docs.python.org/3/tutorial/venv.html


2. Install Bootstrap Budget:

    Activate your virtual environment and install Bootstrap Budget using pip:

   ```Bash
   pip install bootstrap-budget
   ```


3. Initial Setup:

   The Bootstrap Budget package comes with a command-line tool for initial setup. Run the following command to configure the application:

   ```Bash
   bootstrap --setup
   ```

   This will guide you through creating an admin password and setting up the data model for your application.


4. Start the Server:

   Once the setup is complete, start the Bootstrap Budget server using Flask:

   ```Bash
   flask --app bootstrap_budget run
   ```

   This will launch the development server. By default, the application will be accessible on http://127.0.0.1:5000/ in your web browser.

> :raised_hand: Please note: This is a basic installation guide for development purposes.  For production use on your server, additional configuration may be required (e.g., web server setup).