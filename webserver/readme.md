# Deploying a real word database through PostgreSQL using Python

PostgreSQL Account :im2594

URL: http://35.231/138.166:8111//

**Description:**
1. Search by facility name
2. Search by specialty
3. Search by specialty and county (aka custom search)
4. One form of view for patients to input their information in order to find a provider near their county aka (A view to display a list of providers based on the user’s input.)
5. Once a user selects the provider they are interested in, a pop-up view will display all the locations this specific provider is available on.

**Webpages:**
We query the database and force the output to be present as a drop-down menu. The user can be able to choose any attribute(facility name, speciality etc.) to search. We also incorporate
a search input text box as well as a drop-down menu together. This is "interesting" because we use two queries and importing them differently in our python file. Another "interesting" feature we have is that we made a query to find the most occurring provider in our database. We went through a real-world database and found out that there is such a facility with 4406103 occurrences in New York State.
