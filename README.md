Setup Instructions (for linux)

1. Open terminal

2. Create a Virtual Environment:
   
    python -m venv venv

3. Activate the Virtual Environment:
   
     source venv/bin/activate

4. Install Required Dependencies:
   
     pip install -r requirements.txt

5. Prepare the database by running migrations:

    python3 manage.py makemigrations
  
    python3 manage.py migrate

6. Populate the database with test data for running the system:

    python3 manage.py seed

7. Finally, execute the system by running the following script:

    python3 manage.py runscript algorithm

