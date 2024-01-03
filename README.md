# Project Overview

## Description
This project involves creating a website with functionality similar to Wikipedia for the CS50 Web Programming Course by Harvard. Users can search for, create, and edit encyclopedia entries using Markdown language.

### Entry Page
Visiting `/wiki/TITLE` displays the content of the encyclopedia entry with the specified title. If the entry does not exist, an error page is shown. If the entry exists, the page displays the content, and the title includes the entry name.

### Index Page
Update `index.html` to allow users to click on entry names, taking them directly to the corresponding entry page.

### Search
Users can type a query in the sidebar's search box to find encyclopedia entries. If the query matches an entry name, the user is redirected to that entry's page. If not, a search results page displays entries with the query as a substring. Clicking on a result takes the user to the corresponding entry page.

### New Page
Clicking "Create New Page" in the sidebar takes users to a page where they can create a new entry. They can enter a title and Markdown content in a textarea, save the page, and, if the title exists, see an error message. Otherwise, the entry is saved, and the user is directed to the new entry's page.

### Edit Page
On each entry page, a link allows users to edit the entry's Markdown content in a pre-populated textarea. After saving changes, users are redirected back to the entry page.

### Random Page
Clicking "Random Page" in the sidebar takes users to a randomly selected encyclopedia entry.

### Markdown to HTML Conversion
Markdown content in entry files is converted to HTML before being displayed on the entry page.
