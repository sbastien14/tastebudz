# Tastebudz
A web application that leverages machine learning to recommend local restaurants to the user based on their swipes.

In addition to the information below on installation, setup, and testing, we have more information in the following locations:

| Item | Location |
| --- | --- |
| Bug Tracker | [docs/bugs.md](docs/bugs.md) |
| UI/UX Designs | [designs/](designs/) |

## Installation & Setup
1. Clone this git repository to your computer.
2. Install the frontend application by following the steps [here](#installation).
3. Install the backend application by following the steps [here](#installation-1).
4. Run the backend application by following the steps [here](#running-the-backend).
5. Run the frontend application by following the steps [here](#running-the-frontend).
6. Navigate to http://localhost:3000 and get started!

## How To Use Tastebudz
...

## Frontend
The frontend is built using React and provides a dynamic, user-friendly interface to interact with the Tastebudz service.

### Installation
  1. Ensure that Node.js and npm (Node Package Manager) are installed on your system.
  2. Navigate to the frontend directory of the project and run `npm install` to install all required dependencies.

### Running the Frontend
  1. In the parent directory of the frontend project, run the command `npm start`. This will compile the React application and open it in your default web browser.
  __Note:__ The frontend will run on `http://localhost:3000` by default. Ensure that no other service is using this port. 
  2. The frontend application should now be accessible and connect to the backend services as configured.
### Structure
The frontend codebase is organized to support a clear separation of concerns, with directories for assets, components, pages, and more:
- `assets`: Contains static files like images, global stylesheets, and any additional resources required for the user interface.
- `components`: This directory includes reusable React components that form the user interface, organized in subdirectories:
  - `home`: Components specifically designed for the main food swiping interface, which is the core feature of the application.
    - `FilterMenu.jsx`: The component for filtering the displayed food options.
    - `FriendsList.jsx`: A component to display and manage a user's friends list.
    - `SideMenu.jsx`: The side navigation menu component for the home page.
  - `shared`: Contains common components used across multiple pages of the application.
    - `Button.jsx`: A customizable button component used throughout the application.
    - `Navbar.jsx`: The navigation bar component that appears across the top of most pages.
    - `ReviewCard.jsx`: A card component used to display individual reviews.
    - `SwipeView.jsx`: The swipeable view component used in the main food swiping interface.

- `data`: Stores JSON files, configuration files, and other data formats that the frontend might use.

- `pages`: Each JSX file represents a different page in the application, providing unique structure and functionality.
  - `ErrorPage.jsx`: Renders an error view when the application encounters a routing issue.
  - `HomePage.jsx`: Acts as the main swiping interface where users interact with food options.
  - `LandingPage.jsx`: Serves as the initial view for users, offering an overview and entry to the application.
  - `LoginPage.jsx`: Provides the login interface for users to authenticate and gain access to the application.

- `App.js`: The root React component that encapsulates the entire application's structure.

- `App.test.js`: Includes tests for the `App.js` root component.

- `index.js`: The starting point for the React application that mounts the `App` component to the DOM.

- `setupTests.js`: Prepares the testing environment for the application.

## Backend
Backend is based on Flask and wrapped in an ASGI application through the Connexion library that delivers automatic routing and request verification based on OpenAPI 3.0 specifications.

### Installation
  1. Ensure that you have Python 3 installed and run `pip install -r requirements.txt`
  2. API keys and other variables may be modified in `config.py` but this is not necessary at this time.

### Running the Backend
  1. In the parent directory of this project, run the command `uvicorn tastebudz:create_app --factory --port 5000`
  __Note:__ if you would like the backend to automatically reload the server when its component files are modified (for development purposes), append the following to the above command: `--reload --reload-dir tastebudz`
  2. You may send requests according to the OpenAPI 3.0 specifications, which can be found in the `tastebudz/openapi/` folder. You may also access the specifications from a web page automatically generated for each. See the section below for more information.

### API Specifications
| API | Specification File | Interactive URL |
| :--: | :--: | :--: |
| Auth | [auth.yaml](./tastebudz/openapi/auth.yaml) | http://127.0.0.1:5000/auth/ui |
| Restaurant | [restaurants.yaml](./tastebudz/openapi/restaurants.yaml) | http://127.0.0.1:5000/restaurant/ui |

### Testing
I have implemented testing using the Pytest framework. To run through all tests, use the command `pytest --disable-warnings`. Additional information:
- Configuration of the framework can be found in [conftest.py](conftest.py)
- Some additional testing configuration is done in the corresponding section of [pyproject.toml](pyproject.toml)
- Test cases, setup, and additional code needed for testing are under the `tests/` directory.
