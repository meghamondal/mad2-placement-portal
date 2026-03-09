# mad2-placement-portal

# Overview
It is a multi-user placement portal app.

 # Frameworks used
- Vue JS for the frontend
- Flask for application back-end
- SQLite for database
- Celery & Redis for backend jobs
- Redis for caching

# Setup the project

To run the backend, go to the backend directory, then,
- create a virtual environment by giving the command:
  
      ```python -m venv .venv```

- Then activate the virtual environment as per your OS:

    - For Windows using bash terminal:
    
          ```source .venv/Scripts/activate```
    
    - For Linux/MacOS:
    
          ```souce .venv/bin/activate```
  
- Install the dependencies by the command:
  
       ```pip install -r requirements.txt```

- Then finallly run the project by the command:

      ```python app.py```

- Then start the redis server:
      ```redis-server```

- Start the celery worker:
      ```celery -A app:celery worker --loglevel INFO```

-  Start the mailhog service:
      ```MailHog```

- Start the celery beat:
      ```celery -A app:celery beat --loglevel INFO```


To run the frontend, go to the frontend directory, then,
- install the dependencies:
  
      ```pnpm install```
      
- start the frontend:
  
      ```pnpm run dev```


Then explore the project using the frontend in the provisioned port.


  
 
