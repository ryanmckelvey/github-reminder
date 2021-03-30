# github-reminder
*Flask app set up to remind me to do some work and make some commits*

## ⏮Prerequisites⏮
- An email account
- A GitHub Personal Access Token (PAT)
  - *if you don't have a PAT yet follow [this guide](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)
- An install of Python 3 and Pip

## 🛠Set Up🛠
To get the required packages run `pip install -r requirements.txt`
In `app.py`, replace the placeholder PAT with your own
In `email_service.py` replace sender_email, receiver_email, and password with your own
To run the flask app locally, navigate to the `github-reminder` folder in terminal and type `flask run`

## 🕹Interaction🕹
Go to localhost:5000 and that's all for now. An email will be sent to your reciever email from your sender email if you've not pushed any commits today!
