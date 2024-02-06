# Django

Deployment Steps:-

1. Add **STATIC_ROOT = BASE_DIR / "staticfiles"** in the settings.py file
2. Run a command **py manage.py collectstatic**  -To collect all the static files into that folder
3. then add **+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)** this command in the project url file to server the static file
4. then run this command in the terminal-  **py -m pip freeze > requirements.tx**t -to create a file with all installed dependencies
5. then create environment variables by importing from os import getenv -in the settings.py for allowed host, secret key. like **getenv("VARIABLE_NAME")**
6. Then create .ebextensions folder inside the project folder and inside that create django.config file and enter the following:option_settings:
      aws:elasticbeanstalk:container:python:
      WSGIPath: my_site.wsgi:application
7. Then Zip the django project folder except static and virtual env folder.
8. upload the zip file into aws elasticbean and then click on configure more options and set the environment variable values
9. And click on create application. To create an application and Our application will be deployed.
10. To connect databse with postgresql we need to follow these below steps:
      **Run {pip install psycopg2-binary} command to install postgresql into django**
      **update using requirement.txt file using the same above command**
      **go to settings.py to configure db: *first create RDS in aws* **settings.py -->  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': '<your-rds-db-username>',
        'PASSWORD': '<your-rds-db-user-password>',
        'HOST': '<your-rds-db-host>',
        'PORT': '5432'
    }

}**
    **Then run manage.py makemigrations and migrate to configure databse setup**
    **then create super user**

12. In RDS edit security group. edit inbound rules and set anywhere to allow every device to access.
13. Then create **static-files.config** inside the .ebextensions file to make the server serve static files:
        option_settings:
          aws:elasticbeanstalk:environment:proxy:staticfiles:
          /static: staticfiles #this is used to server static files like css
          /files: uploads  #this is used to serve files, images, etc.
              ******OR******
13. Using AWS S3 is used to store files and serve files:
14. 

     


