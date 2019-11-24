# Project: Item Catalog (Animal Photos)

## Description
Animal Photos App is a Web App which uses `Flask` framework & works with a database using `SQLite` server.

The idea of the app is a website for sharing popular animal photos where the existing photos are available to any client who orders it, where the user must log in to commit his own contributions.

## Authentication and Authorization

* **The website supports OAuth**
* **The Website provides two sign-in options.**
  1. Login Using Google Account
  2. Login Using Server's Local database
* **User can only commit contributions when he is logged in.**
* **User can only Edit or delete his own contributions. Nobody is able to modify posts that don't belong to him through website.**

## CRUD

The website allows the user to:
* **READ** the content of database through website or API endpoints.
* **CREATE** new items as soon as he is logged in.
* **UPDATE** and **DELETE** his own items

## Requirements
In order to run this application your PC need to include these Programs:
* Terminal (Linux-Based)
* Python 3.7
* Flask, SQLAlchemy & OAuth2 libraries  
**for more information see next section**

## Prerequisites & Preparation

* To run this app you should download `Git` from [here](https://git-scm.com/) and install it on your device.
* You can use _Udacity_'s virtual machine instance to run server on your PC without making it affected.
  1. Download `VirtualBox` form [here](https://www.virtualbox.org/) and install it.
  2. Download `Vagrant` form [here](https://www.vagrantup.com/) and install it.
  3. Open `Git Bash` on `Windows` or your favourite terminal program on `Linux` or `MacOS`
  4. Change the directory to the main directory of the project using `cd` command.
  5. Now run the following two commands with the same order.
     ```shell
     $ vagrant up
     $ vagrant ssh
     ```
  6. Since the Virtual Machine is ready, you can run the following commands to start server.
     ```shell
     $ cd /catalog
     $ python views.py
     ```
* You can install used programs on your PC instead.
  1. Download & Install Python using [this tutorial](https://realpython.com/installing-python/).
  2. Copy & Run the following command in your terminal program.
     ```shell
     $ pip install flask sqlalchemy oauth2client requests json httplib2
     ```
     **If you get errors from `pip` command, check [this tutorial](https://www.liquidweb.com/kb/install-pip-windows/)**
  3. Open `Git Bash` on `Windows` or your favourite terminal program on `Linux` or `MacOS`
  4. Change the directory to the main directory of the project using `cd` command.
  5. Now you can simply run app using `python views.py` command.
* After running python script file `views.py`, you can visit website at http://localhost:5000

## API Implementation Guide

The web server returns API responds in `JSON` forms

### Get Species names
Client can get Species names by sending a GET request to the url (http://localhost:5000/API/species)  
**Respond Sample**
```json
{
  "species": [
    {
      "id": 1, 
      "name": "Cats"
    }, 
    {
      "id": 2, 
      "name": "Turtles"
    }
  ]
}
```

### Get All Photos
Client can get all photos data by sending a GET request to the url (http://localhost:5000/API/photos)  
**Respond Sample**
```json
{
  "photos": [ 
    {
      "description": "With how cute I am I could be charging a fortune. But I am a simple dog. All I need are kisses and a full food dish.", 
      "id": 12, 
      "title": "Cute Dog Kiss Of The Day", 
      "url": "https://i.pinimg.com/originals/3e/8a/d9/3e8ad9163e7633370687539efb9d8378.jpg"
    }, 
    {
      "description": null, 
      "id": 13, 
      "title": "your daily cute puppy", 
      "url": "https://static.standard.co.uk/s3fs-public/thumbnails/image/2019/03/15/17/pixel-dogsofinstagram-3-15-19.jpg"
    }
  ]
}
```

### Get Photos of a certain species
Client can get all photos data in a species by sending a GET request to the url (http://localhost:5000/API/species/{SPECIES_ID})  
**Respond Sample**
```json
{
  "photos": [ 
    {
      "description": "With how cute I am I could be charging a fortune. But I am a simple dog. All I need are kisses and a full food dish.", 
      "id": 12, 
      "title": "Cute Dog Kiss Of The Day", 
      "url": "https://i.pinimg.com/originals/3e/8a/d9/3e8ad9163e7633370687539efb9d8378.jpg"
    }, 
    {
      "description": null, 
      "id": 13, 
      "title": "your daily cute puppy", 
      "url": "https://static.standard.co.uk/s3fs-public/thumbnails/image/2019/03/15/17/pixel-dogsofinstagram-3-15-19.jpg"
    }
  ]
}
```

### Get a certain photo
Client can get a certain photo data by sending a GET request to the url (http://localhost:5000/API/species/{SPECIES_ID}/{PHOTO_ID})  
**Respond Sample**
```json
{
  "photo_data": {
    "description": "The green sea turtle is an endangered species with a population that is, unfortunately, on the decline. However, they can be seen on the Great Barrier Reef and Lady Elliot Island, at the southern end of the reef. This is a perfect place to see these oceanic reptiles. While snorkelling, with my camera in an underwater housing, this inquisitive turtle decided to have a closer look, investigating me and my camera. It was an incredible experience and wonderful to photograph this creature in the wild.", 
    "id": 8, 
    "title": "Green Sea Turtle!", 
    "url": "https://cdn11.bigcommerce.com/s-s5d5u8bn61/images/stencil/1280x1280/products/238/1076/0E3A7368-1_Lagoon_green_turtle__75795.1548630091.jpg"
  }
}
```

## For More Information

[Python 3 documentations](https://docs.python.org/3/)  
[Flask Documentations](http://flask.palletsprojects.com/en/1.1.x/)  
[SQLAlchemy Documentations](https://docs.sqlalchemy.org/en/13/)  
[OAuth2 Documentations](https://oauth.net/getting-started/)  
[Google Sign-In Implementation tutorial](https://realpython.com/flask-google-login/)