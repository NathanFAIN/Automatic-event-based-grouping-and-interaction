# Automatic event-based grouping and interaction with personal multimedia information
This repository contains an application to group media by event.


In the `.env` file you will find all the API keys used for this project. 
You can generate your own API keys through the following links:
- https://beta.openai.com/account/api-keys
- https://keywordsready.com/api
- https://api.imgur.com
- https://developer.rosette.com/

This application requires a recent version of python (python3): https://www.python.org/downloads/

To install all the required dependencies, you will need to enter this line: 
```
pip install -r requirements.txt
```

To start the application:
```
python3 App.py
```

The different actions that can be done:
- Use the file `data-set/test.yml` to load a profile with multiple media by clicking on `File -> Open`.
- Save the profile by clicking on `File -> Save` or `File -> Save As`.
- Add new files (media) by clicking on `Edit -> Add File`.
- Group the media into events by clicking on `Edit -> Groupping data`.

All test data are located in the `data-set` folder.
