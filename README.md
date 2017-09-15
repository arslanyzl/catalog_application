# Udacity Catalog Item Project

This project part of [Udacity Front-End Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

### Project Description

An application that provides a list of Soccer leagues within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own Soccer leagues and related teams.



### How to RUN

#### Required programs:
  * Python3
  * Vagrant
  * VirtualBox

#### Setup a Facebook OAuth for add, edit and delete items
1. Go to https://developers.facebook.com/apps/ and login with Facebook account information.
2. Create new project.
3. Get App ID and App Secret.
4. Go to the Client OAuth setting then activate "Client OAuth Login" and "Web OAuth Login".
  To the "Valid OAuth redirect URIs" paste "http://localhost:5000/"
5. Clone or download this "catalog_application" directory.
6. Open "fb_client_secrets.json" file then paste your App Id and Secret ID to the related place.
7. Open "login.html" file in templates folder then paste your App Id related place.
  
#### Star the Server
1. Change the dricety to the downloaded catalog_application
2. Use commond "vagrant up"
3. Use commonf "vagrant ssh"
4. Enter the "cd /vagrant"
5. Run "python database_setup.py"
6. Run "python adding_teams.py"
7. Finally run "python project.py" then open in your browser "http://localhost:5000/"

Enjoy
