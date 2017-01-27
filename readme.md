ITEM CATALOG


This is an application that provides a list of items within a variety of categories as well as provides a user registration and authentication system.
Registered users will have the ability to post, edit and delete their own items.
This RESTful web application uses the Python framework Flask along with third-party OAuth authentication.


Steps to run this application :

-> Have Vagrant and Virtual Box installed on your machine.
-> Unzip the file and put the contents in the vagrant directory.
-> Launch the Vagrant VM.
-> Run the project.py file from the Vagrant VM.
-> The web app will be running on your localhost at port 5000 ( http://localhost:5000/ )
-> Open the above mentioned link to use the web app.
-> You can only view the catalog without signing in.
-> To create, update and delete the items in the catlog, sign in using Google+ or Facebook.



Go to ,

-> http://localhost:5000/login to login to the app using Google+ or Facebook

-> http://localhost:5000/ or http://localhost:5000/restaurant to view the list of restaurants. You have to be signed in to make new restaurants and to edit & delete restaurants.

-> You can then click on each restaurant's title to view it's menu. You have to be signed in to make new menu items and to edit & delete menu items.   

-> http://localhost:5000/restaurant/JSON to get the list of restaurants in a serialized JSON format

-> http://localhost:5000/restaurant/<int:restaurant_id>/menu/JSON to get the menu of a specific restaurant in a serialized JSON format. Replace <int:restaurant_id> in the url with the id of the restaurant that you need.

-> http://localhost:5000/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/ to get the menu item of a specific menu in a specific restaurant in a serialized JSON format. Replace <int:restaurant_id> and <int:menu_id> in the url with the id of the restaurant and the id of the menu that you need.

