# Pearings

This project was created during the first 4 weeks at Insight Data Science. The app returns recipe and ingredient combinations based off of a user's existing ingredient list. Recipe and ingredient data are requested using an API from bigoven.com (the API keys are expired, please request your own if you wish to use my request program). All data is stored in MongoDB and then processed using pandas,numpy,matplotlib,scikit,networkx,wordcloud and lda. The backend analysis and processing can be found in the DataHandlingAnalysis folder. App is kicked off on port 5000 using Flask. Frontend code can be found in app folder.  To run the app simply type "./run.py" into the command terminal. 