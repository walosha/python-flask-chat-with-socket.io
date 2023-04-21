# CLIENT-SERVER-CONCURRENT-PROGRAM

This is a simple chat application which uses Python, Flask and Socket IO.

### Installation

1.  Clone the repository.

        `$ python3 -m venv venv

    $ source venv/bin/activate
    `

2.  Install all the required libraries by running the following command

    `pip install -r requirements.txt`

### Run

Execute the application by

`python app.py
`

## Design

| Login Screen![enter image description here](./designs/Screenshot%20from%202023-04-06%2015-52-35.png) | Chat Window![enter image description here](./designs/Screenshot%20from%202023-04-06%2015-52-42.png)

`export FLASK_APP=app
flask shell

from app import db, ChatMessage
db.create_all()
`
