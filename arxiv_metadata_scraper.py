# This script gets data on papers posted to the arXiv

""" NOTE TO USERS:
    
    Specify the directory for storing data - lines 129, 137, 145, 153, 162 """

# Importing required modules

import urllib
from bs4 import BeautifulSoup as bs

# Initializing lists for storing the data

submission_dates = []
updated_dates = []
category_data = []
authorship_data = []
affiliation_data = []

# Creating the components of the query url

base = 'http://export.arxiv.org/api/query?search_query=all:'
mid = '&start='
end = '&max_results=1000'

# List of year month combinations for id query

years = ['91', '92', '93', '94', '95', '96', '97', '98', '99', '00', '01', '02',
         '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
         '15', '16', '17', '18', '19', '20']

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

yymm = [y+m for y in years for m in months]

# Running the outer loop

for ym in yymm[0:352]:
    
    # Resetting start to 0 for each ym in yymm
    
    start = 0
    flags = 0
    
    # Outer loop progress checker
    
    print('Harvesting data for ' + ym + '...')
    
    # Running the inner loop
    
    while start < 17000 and flags < 5:
        
        # Specifying the url
        
        url = base + ym + mid + str(start) + end
        
        # Inner loop progress checker
        
        print('Harvesting data for entries ' + str(start) + ' through ' + str(start+999) + '...')
        
        # Getting the raw data from the url with bs4
        
        page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(page)
        soup = bs(response, 'html.parser')
        
        # Separates the metadata for each paper into its own entry in a list
        
        raw_data = soup.find_all('entry')
        
        # Makes sure that the query was successful
        
        if len(raw_data) < 2:
            
            # If the query does not return data, increase the value of flags
            
            flags += 1
        
        # If the query returned data, parse it
        
        else:
        
            # Extracting the desired metadata from each paper and appending it to the appropriate lists
            
            for raw in raw_data:
                
                # Get the submission date and priary arxiv category for the paper
                
                date = raw.find_all('published')
                update = raw.find_all('updated')
                cat = raw.find_all('arxiv:primary_category')
                
                # Isolate each author to extract author level metadata
                
                # Create a list of authors on the paper (includes their affiliation data)
                
                authors = raw.find_all('author')
                
                # Get each author name and affilation for the paper
                
                auths = []
                affils = []
                
                for a in authors:
                    
                    auths.append(a.find_all('name'))
                    affils.append(a.find_all('arxiv:affiliation'))
                
                # Removing tags from the metadata
                
                date2 = str(date)[12:22]
                update2 = str(update)[10:20]
                cat2 = str(cat)[str(cat).find('term="')+6:str(cat).find('" xmlns:arxiv')]
                auths2 = [str(a)[7:len(str(a))-8] for a in auths]
                affils2 = [str(a)[64:len(str(a))-21] for a in affils]
                
                # Appending the metadata from each paper to the appropriate lists
                
                submission_dates.append(date2) # In YYYY-MM-DD format
                updated_dates.append(update2) # In YYYY-MM-DD format
                category_data.append(cat2)
                authorship_data.append(auths2)
                affiliation_data.append(affils2)
            
            # Increase start value for next query
            
            start = start + 1000

# Writing results to txt files

with open('C:/Users/User/Documents/Data/arxiv_covid/category_data.txt', 'w') as file:
    
    for entry in category_data:
    
        file.write('%s\n' % entry)

file.close()

with open('C:/Users/User/Documents/Data/arxiv_covid/submission_dates.txt', 'w') as file:
    
    for entry in submission_dates:
    
        file.write('%s\n' % entry)

file.close()

with open('C:/Users/User/Documents/Data/arxiv_covid/updated_dates.txt', 'w') as file:
    
    for entry in updated_dates:
    
        file.write('%s\n' % entry)

file.close()

with open('C:/Users/User/Documents/Data/arxiv_covid/affiliation_data.txt', 'w', encoding = 'utf-8') as file:
    
    for row in range(len(affiliation_data)):
        
        entry = str(affiliation_data[row])
        file.write('%s\n' % entry)

file.close()

with open('C:/Users/User/Documents/Data/arxiv_covid/authorship_data.txt', 'w', encoding = 'utf-8') as file:
    
    for row in range(len(authorship_data)):
        
        entry = str(authorship_data[row])
        file.write('%s\n' % entry)

file.close()

