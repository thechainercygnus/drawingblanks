# Drawing Blanks

Sometimes I just need to create a new project folder to dink around with an idea. That's where this project came from.

**Drawing Blanks is a REST API for naming things.**

The names aren't going to be good, but they'll get the job done for now. Currently Drawing Blanks only generates some basic 3 word names. More will come!

## Self Hosting

I recommend that you set up and run your own Drawing Blanks API locally for a number of reasons. Mostly because this thing is just a hobby project of mine, so infrastructure is limited.

### Prepare the Environment

```bash
git clone https://github.com/thechainercygnus/drawingblanks.git
cd drawingblanks
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
touch .env
```

To connect to WordsAPI to get the words, you will need to get an API Key from Rapid API. *Quick Walkthrough Pending*

To generate a `SECRET_KEY` use `openssl rand -hex 32`.

```
# .env
RAPID_API_KEY=
SECRET_KEY=
```

Alternatively, if you're not a fan of `.env` files, you can set these environment variables for your development environment as appropriate for your particular setup.

#### bash/zsh

```bash
export SECRET_KEY="85856417bfb2e9aebc495e769f478020425cfc2bb7dab102a94f2de2423d82a5"
```

#### fish

```fish
set -x SECRET_KEY 85856417bfb2e9aebc495e769f478020425cfc2bb7dab102a94f2de2423d82a5
```

### Run the Server Locally

```bash
uvicorn main:app --reload
```

This will stand up a simple local server you can reach.

Check `localhost:8000/docs` or `localhost:8000/redoc` to learn more about what is actually available.

## Authentication

Authentication is currently implemented with no backend, however. So until I implement that this doesn't work.