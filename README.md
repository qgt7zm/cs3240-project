# CS 3420 Whistleblower App

## Description

Report an Athlete is a web application that helps student athletes privately report physical or mental health problems
about themselves or their peers.

This project was created for CS 3240 (Advanced Software Development) at UVA during Spring 2024.
Throughout the course, we learned about the main steps of the software development process (Requirements, Design,
Construction, Testing, and Release) while we worked on our project.
The app was built with the Django framework and integrates Google OAuth login and Amazon S3 storage.
The completed version was previously deployed to Heroku.

## My Contributions

I worked with 4 other students using the Scrum process to complete the project in several sprints.
Each member contributed equally to the development and held a different team role.
I chose to serve as the Software Architect because I enjoy methodically planning out projects and seeing how
components interact with each other.

As the Software Architect, I guided my team through a requirements change in the middle of the semester and drew
class diagrams and flowcharts for new features.
As an experienced programmer, I also provided technical support, such as creating initial GitHub pull requests and
CI actions and debugging Heroku and Python errors.
Lastly, as a group member, I assisted in implementing features, namely creating models for site users and file uploads
and creating the filterable table for viewing reports.

## Running Locally

Below are steps to run the application. For the best experience, use PyCharm and Python 3.12.

1. Create a virtual environment through an IDE or using `python3 -m venv .venv`.
    - You may need to activate the virtual environment using `source .venv/bin/activate` (Unix) or
      `.venv\Scripts\activate` (Windows).
2. Install the packages using `pip3 install -r requirements.txt`.
3. Fill in your secret keys in [.env.blank](.env.blank) and rename the file to .env.
    - Generate a Django secret key using `python3 gen_key.py`.
    - You will need a Google OAuth key, an Amazon AWS account, and a local or remote PostgreSQL database.
4. Migrate your database using `python3 manage.py migrate`.
5. Run the app using `python3 manage.py runserver 8000`.
6. Visit the development server at http://127.0.0.1:8000/.

## Deploying to Production

Below are steps to deploy the application. Make sure not to include any secret keys in your repository!

1. Create GitHub repository secrets for each field in .env and move [django.yml](django.yml) to .github/workflows to
   enable continuous integration.
2. Fill out the environment variables on the hosting server and set `DEBUG` to `False`.
3. Run `python3 manage.py collectstatic` to collect static files into a single folder.
4. Upload the static files folder to the hosting server.

## Data Disclaimer

This project was created for a university course to learn how to develop software in a group.
As such, no real names, photos, cases, or other data will be uploaded to this repository.
Any examples bearing resemblance to real-life data are purely coincidental and unintentional.

## Licensing

This code is released under the permissive BSD-3 license (the same as Django's).
If you wish to consult this repository for your own academic project, you should also contact your instructors
regarding their plagiarism policy.