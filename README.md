##Use it yourself
https://emirhanc.pythonanywhere.com/

## Overview

Stocker is a single page web application to get live information for stocks in the American stock market as well as currencies and futures. The app gives us Nasdaq compenents to access the most common stocks and a list of most popular currencies and futures by default. In this list we can see the symbol, description of the symbol and the price for each item for some quick information. We can also get information about any stock, currency or future by entering its symbol in the search bar. 

Any symbol that was clicked on or searched for gives us a much more detailed view that shows the current price graph of the item as well as information like previous close, target price or avarage 50 day price and more depending on the item. We also have five buttons that makes the graph display 1 day, 1 month, 3 months, 1 year or 5 years of price data with intervals set accordingly without reloading the page.

Under the graph we have an "arbitrage" field that we can enter another stock symbol to compare the two stocks and get the ratio of them as a graph to better understand how these stocks are gaining or losing in relation to one another so that for example we can make a desicion to transition to the other stock. This arbitrage field shows us the ratio of the two symbols entered but if a currency is entered it shows us a price graph of that stock or future in the entered currency rather than a ratio. So instead of getting the US Dollar price of the item we get it in our selected currency.

We also have a button to add or remove an item to our portfolio without reloading the page if we are a signed in user. If we click on portfolio button in our navigation bar we get a list that gives us all of the items that we have added to our portfolio to track them easily. This list behaves just like other list views, we can see some quick information for the items and can click on them to get more information.

Login and register views are the only other separate pages in this app. They were also custom made to have a simple UI, a link go register page login page and a closing button if we decided not to login or register and get back to the index page. Also the whole site is mobile responsive.


## Distinctiveness and Complexity:


**Distinctive Features:**

- It utilizes a library called yfinance to get us live information from Yahoo. In other projects the apps provided their information in themselves but this one uses an external source. 

- It uses a JavaScript module called Plotly to create a price graph or ratio graph for the given symbols and it provides the information by fetch calls made to view functions that uses yfinance to get price hsitory. We did not manipulate data in this way in other projects. 

- It's a single page app and none of the functions require a reload of the page (apart from login/register). This was in some of the projects but not for the entire app.

- It has custom made animations for when a view is loading or when a row on the table is hovered on. Its completely mobile responsive. (Also the the the level of visual detailing of the site with CSS although not perfect, made with the best of my abilities)


**Complexity:**

For the complexity I wanted to challange myself with 2 libraries, yfinance and Plotly. Learning them and using them in conjuction with each other was definetely a challange for me. 

The information for an item from yfinance was different from each other. So there had to be a detections for the type of the item (e.g., stock or currency) in order to send it accordingly whether It's for an arbitrage graph or for just displaying information of the item.

Figuring out how to set up a Plotly graph and how to feed it the correct information took a lot of trial and error, and definetely made me understand how to understand whats causing the issue and thought me problem solving all over again.

I also did error handling and giving error messages to the user accordingly. For example if the searched stock does not exist, or whether the add/remove button worked.

The application uses 3 models. One for adding and removing of an item to user portfolio. Other two is for storing a list of currecies and futures so that the list of these items are not hard coded and can be added or removed via Django admin.


## File Structure:

The file structure and whats contained in them are just like how it was in the other projects.
There is a single app called "stocker", inside we have our 'views.py' file which has our Python functions that we make our calls to, we have our 3 models in  the 'models.py' file, url paths in 'urls.py', user authentication form in 'forms.py' and model registirations to make them editable by a superuser is in 'admin.py'. We also have static file that has 'script.js' file for our JavaScript and 'style.css' for the CSS styling of the app. Finally we have the templates folder with the 'index.html' which is our main html file where most of the functionality of the app happens, as well as 'login.html' and 'register.html' for logging in and registering respectively.






