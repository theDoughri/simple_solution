# SampleCompany: Computer Tracking Solution

This is a simple computer tracking solution implemented in **Python** using the **FastAPI** framework. The application runs on the **Uvicorn** web server and utilizes **SQLite** as the database with the help of SQLAlchemy.

## Assumptions:

- Each computer's MAC address is unique.

- Only IPv4 addresses are used; IPv6 addresses are not considered.

## Setup the App Environment:

1. Clone the project locally.

2. Open a terminal or command line in the **simple_solution** directory.

3. Create a new environment named **env** with the command `python -m venv env`.

4. After successfully creating the environment, activate it using the command `source env/bin/activate` (for Unix-like systems) or `env\Scripts\activate` (for Windows).

5. Run the command `pip install -r requirements.txt` to install all required dependencies.

## Running the App:

1. Ensure the Greenbone notification server is running properly and the local **port 8080** is mapped to its running Docker image.

2. Open a terminal or command prompt in the **app/** subdirectory.

3. Execute the command `uvicorn main:app --reload`.

4. Verify that the application starts up correctly and Uvicorn is running on its default configuration at **http://127.0.0.1:8000**.

## Testing the App:
1. Using a web browser, open the link **http://127.0.0.1:8000**, which will redirect you to the Swagger documentation at **http://127.0.0.1:8000/docs**. This will allow you to perform the endpoints functional tests, as shown in the screenshot:

![Swagger Doc](Screenshot.png)

2. On the other hand, you can also verify the functionality of `main.py` using `pytest` testing freamwork using the command `pytest test_main.py`, as shown in the next screenshot:

![Swagger Doc](Next%20screenshot.png)

## Potential Application Enhancements:

1. **Enhance Unit Testing**: To enhance the overall code quality and reliability, it is recommended to implement additional unit testing.

2. **Validate User Entries**: The present implementation lacks validation checks for IP addresses and MAC addresses submitted by users. It is advisable to introduce these checks at the front-end level to ensure the precision and integrity of data.

3. **Optimize Admin Notifications**: Refactor the `notify_admin` function to operate asynchronously, optimizing the admin notification process. Additionally, enrich the function to provide a status indicator denoting the success of the notification procedure. The current basic implementation only log the admin notification server to the console.

4. **Implement Secure Login Management**: A vital enhancement required for a production-ready application is the implementation of robust login management. This integral feature is currently absent and should be integrated for improved security and functionality.

5. **Refine Project Architecture** Although this is a compact application, It is a good idea to refin its architecture by embracing principles of `Clean Architecture` or `Modular Architecture`. This step can provide clarity, maintainability...