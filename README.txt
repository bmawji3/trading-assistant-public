DESCRIPTION

INSTALLATION
This project is based in python3. You will need this at a minimum to install dependencies and run the project on your local environment.
There are 2 different files provided for installing dependencies:
    1. requirements.txt
    2. environment.yml

With python3, have a dependency manager like Anaconda or pip to install packages for you.
For example, you can get pip via shell command `curl -O https://bootstrap.pypa.io/get-pip.py`,
and run `python3 get-pip.py --user`. Optionally, download Anaconda from https://www.anaconda.com/products/individual

Download dependencies via command `pip install -r requirements.txt`
or by importing conda environment via command `conda env create -f environment.yml`. Also activate the environment
with command `conda activate TradingAssistantApp`.

EXECUTION
The data gathering, preparation, and model training is done in advance to provide the user a seamless experience and
avoid having to take extra time away from the application experience.
Consequently, path variables in WebAPI/trading_assistant_app/app.py are configured to be run with the WebAPI/API.py.

Open up your first terminal shell, and use an environment with the correct python version and dependencies specified above.
This first step will run the backend for the application.
`cd trading-assistant/WebAPI`
`python API.py`

In your second terminal shell, run the following command:
`cd trading-assistant/WebApp`
`python -m http.server`

In your browser, navigate to http://localhost:8000/ to see the WebApp running.
Additionally, this WebApp is running on an EC2 instance http://ec2-18-208-47-240.compute-1.amazonaws.com:6242/

For setting up on EC2, changes needed to be made to the index to read from correct hosts/ports.
Additionally, there needs to be processes set up and running.
On the EC2 instance, Apache HTTP is serving the WebApp and Gunicorn is serving the WebAPI.
