<img src="images/box-dev-logo.png" 
alt= “box-dev-logo” 
style="margin-left:-10px;"
width=40%;>


# Sample application using the Box Python SDK and oAuth 2.0
This application is a template to get you started quickly with the Box Python SDK and oAuth 2.0.


## Box configuration steps

1. Create a Box free account if you don't already have one.
2. Complete the registration process for a Box developer account.
3. Making sure you're logged in navigate to the [Box Developer Console](https://app.box.com/developers/console). This will activate your developer account.
4. Create a new Box application. Select Custom App, fill in the form and then click Next.
5. Select User Authentication (OAuth 2.0) and then click Create App.
6. Scroll down to Redirect URIs and add the following redirect URI:
    - http://127.0.0.1:5000/callback
    - (or whatever you have configured in the .env file)
7. Check all boxes in application scopes.
    - (or only what you think will be necessary)
8. Click Save Changes.
9. Note the Client ID and Client Secret. You will need these later.

## Installation and configuration

You will need to have [python](https://www.python.org/downloads/) installed on your machine. 

> Get the code
```bash
git clone git@github.com:barduinor/box-python-oauth-template.git
cd box-python-oauth-template
```

> Set up your virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Create your local application environment file
```bash
cp .env.sample .env
```

> Open the code in the code editor of your choice.
```
code .
```

> Update the CLIENT_ID and CLIENT_SECRET field values in the env file with the Box application client id and client secret you created on the developer console.

## Run the application 


```bash
python main.py
```

The first time you run the application, it should open a web browser window and prompt you to log in to Box. 
After you log in, it will ask you to authorize the application.
Once this process is complete you can close the browser window.
By default the sample app prints the current user's name to the console, and lists the items on the root folder.

The authorization token last for 60 minutes, and the refresh toke for 60 days.
If you get stuck, you can delete the .outh.json file and reauthorize the application.

### Questions
If you get stuck or have questions, make sure to ask on our [Box Developer Forum](https://support.box.com/hc/en-us/community/topics/360001932973-Platform-and-Developer-Forum)