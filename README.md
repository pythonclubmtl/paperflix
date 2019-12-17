# paperflix

Welcome to Paperflix !

# Running Paperflix

### Cloning the repo

In your terminal:
```
git clone https://github.com/pythonclubmtl/paperflix.git
```

You can also download the repository using the green "Clone or download" button in the top right corner of this webpage.

### Install dependencies

It is recommended that you try this code in a virtual environment. If you already have python3 installed on your machine, you should be able to create a virtual environment from your terminal:

```
python3 -m venv .env
source .env/bin/activate
```

You can the install the necessary dependencies using:
```
pip install -r requirements.txt
```
### Configuring the bot

You will need a token API for your Telegram bot. To get one of those, you will need to bargain with the @botfather user in Telegram.
Once you have it, you will need to insert it in the 8th line of the `main.py` file.

### Run it

```
python main.py
```

Interact with your bot from a Telegram account.