# cs-316-project

Emma Chun: Converted the individual race selection menu to a dropdown for accessibility. Implemented a feature where hovering over a state in the map brings up a box with the names and parties of its current senators. Highlighted the receipts received by the winning candidate in each individual state race. Added a color key for the map and fine tuned CSS styling of the states pages. 
Shravan Kalahasthy: Generated around 80000 tuples of fake data for candidate donations and then added these donations to the candidate page. Also add a table grouped by contributor so that a user can see how much each contributor donated to a candidate in total. These tables can be sorted and searched within. 
Michelle Qiu: Gathered and organized over 17000 tuples of real data from FEC on committees and implemented into committee pages. Added additional functionalities (different ways to sort/display data, option to select categories of committees/recipients, ability to paginate through data, etc). Added feature to allow users to go to state election data based on the state that a committee is based in (if state data is available). Added CSS styling framework (see below for reference).
Ameya Rao: Compiled and merged real data from OpenSecrets about donations received by senators during the last election cycle and which industries they received from. Displayed donations in a table below the bill sponsorships as well as visualizations for easily understandable comparisons. Allowed user to directly click on the legislation URL for easy access to information on the bill. Auto-generated options for the selection drop downs based on real data on legislation subject and senator. Connected Issues and Candidate pages to allow the user to easily navigate to the candidate page for further voting information. 
Kieran Lele: Pulled and cleaned data for 20,000 tuples from the available online FEC data. Then filtered this data to provide meaningful insights by dropping low donation amounts. Displayed this data in a table that users could then filter based upon a series of preset parameters. Then allowed users to make a graph using selected data. The graph is customizable based on several different parameters to make for more effective visualization. Finally, allowed users to download this graph for later use.

Repository: https://github.com/ameyasr24/cs-316-project 

Data Sources: 
https://www.fec.gov/data/browse-data/?tab=bulk-data
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PEJ5QU 
https://www.congress.gov/search?
https://www.mockaroo.com/
q=%7B%22congress%22%3A%5B%22117%22%5D%2C%22source%22%3A%22legislation%22%2C%22chamber%22%3A%22Senate%22%2C%22type%22%3A%22bills%22%2C%22bill-status%22%3A%5B%22failed-one%22%2C%22passed-one%22%2C%22passed-both%22%5D%7D
Lewis, Jeffrey B., Keith Poole, Howard Rosenthal, Adam Boche, Aaron Rudkin, and Luke Sonnet (2021). Voteview: Congressional Roll-Call Votes Database. https://voteview.com/
Congress Legislation: https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22congress%22%3A%5B%22117%22%2C%22116%22%2C%2294%22%2C%2295%22%2C%2296%22%2C%2297%22%2C%2298%22%2C%2299%22%2C%22100%22%2C%22101%22%2C%22102%22%2C%22103%22%2C%22104%22%2C%22105%22%2C%22106%22%2C%22107%22%2C%22108%22%2C%22109%22%2C%22110%22%2C%22111%22%2C%22112%22%2C%22113%22%2C%22114%22%2C115%5D%7D
Open Secrets Donation Industries: https://www.opensecrets.org/members-of-congress
CSS Styling template: https://templatemo.com/tm-562-space-dynamic
Datables: https://datatables.net/
