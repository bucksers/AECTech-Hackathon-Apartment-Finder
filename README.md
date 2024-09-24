# AECTech-VIBESCOUT
VibeScout is an application that lets users find areas in LA that are similar to their input. All you have to do is input an address and the application will return the top five most similar areas based on properties such as green spaces, restauarants, cultural attractions, and much more.

Runner-up for "Best Overall Project" at AEC Tech+ Hackathon: Los Angeles.

## To Start the Front-End
This application was built in React on the front-end. To run the front-end portion, follow these steps:
1. cd into the `"aechackathon2024"` folder
2. run `npm install` to install node modules
3. run `npm run dev` to run the application

## To Set Up the Back-End
The back-end portion of VibeScout uses Flask, a lightweight Python framework, along with Flask-CORS to handle cross-origin resource sharing. First open up a new terminal in the parent directory of the `aechackathon2024` folder. To set up and run the Flask server:

### 1. Install Python and Virtual Environment

Make sure you have Python 3.x installed on your system. You can check by running:

```bash
python --version
```

Then, set up a virtual environment to keep your dependencies isolated:

```bash
python -m venv venv
```

Activate the virtual environent:

* On macOS/Linux:
```bash
source venv/bin/activate
```
* On Windows:
```bash
venv\\Scripts\\activate
```

### 2. Install Dependencies

After activating the virtual environment, intall the required Python packages by running: 
```bash
pip install -r requirements.txt
```
This will install Flask, Flask-CORS, and any other dependencies listed in the `requirements.txt` file.

### 3. Starting the Flask Server

Once the dependencies are installed, you can run the Flask app by executing:

```bash
flask run
```

By default, Flask will run on `http://127.0.0.1:5000/`. You should see output indicating that the server is running.


### 4. Using the Application

Once you have flask up and running, go back to the React webpage that opened with the `npm run dev` command from earlier. Now you can input an address and the application will display the 5 most similar areas to the area that the input address is in!
