# Auction Site Project

## Description
This project, developed for Harvard's CS50 Web Programming Course, is a dynamic auction website allowing users to create, bid on, favorite, and close listings. Listings are categorized, and images can be displayed for each item.

## Specifications

### Models
The application includes three models: one for auction listings, one for bids, and one for comments. Additional models can be added as needed.

### Create Listing
Users can create a new listing by specifying a title, a text-based description, and the starting bid. Optionally, users can provide a URL for an image and/or select a category (e.g., Fashion, Toys, Electronics, Home, etc.).

### Active Listings Page
The default route displays all currently active auction listings. Each listing includes essential details such as the title, description, current price, and a photo if available.

### Listing Page
Clicking on a listing redirects users to a dedicated page with comprehensive details, including the current price. If signed in, users can add the item to their watchlist or place bids. The auction creator, when signed in, can close the auction, making the highest bidder the winner.

If a user is signed in on a closed listing page and has won the auction, the page indicates the user's victory. Additionally, signed-in users can add comments to the listing page, with all comments being visible.

### Watchlist
Signed-in users can visit a Watchlist page, displaying all listings they have added. Clicking on any of these listings redirects users to the specific listing page.

### Categories
A dedicated page allows users to explore all available listing categories. Clicking on a category name redirects the user to a page displaying all active listings within that category.

### Django Admin Interface
Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids on the site.
