def IndeedScraper(Query, Location):
    #Query and Location are strings with - as spaces
    import requests
    import lxml.html
    import pandas as pd
    import datetime

    urlTemplate = 'https://ca.indeed.com/jobs?q={}&l={}&sort=date&start={}'
    urlTemplate_job = 'https://www.indeed.ca{}'
    titles = []
    companies = []
    descriptions = []
    locations = []
    dates = []
    time_of_scrapes=[]
    
    URL_first = urlTemplate.format(Query,Location,0)
    html_first = requests.get(URL_first)
    job_first = lxml.html.fromstring(html_first.content)
    count = job_first.xpath('.//div[@id="searchCount"]/text()')[0]
    count_split = count.split()
    count_total_str = list(filter(str.isdigit, count_split[3]))
    count_length = len(count_total_str)

    count_total = ''
    for count_number in range(count_length):
        count_total = count_total + count_total_str[count_number]
        
    count_number = int(count_total)

    #Loop over seach pages according to max_number_of_jobs
    for start in range(0,count_number,20):
        URL = urlTemplate.format(Query,Location,start)
        html = requests.get(URL)
        doc = lxml.html.fromstring(html.content)
        results = doc.xpath('.//div[@class="title"]')

        #For each individual job in results, grab the HTML content according to the HREF
        for result in results:

            HREF = result.xpath('.//a')[0].get('href')
            URL_job = urlTemplate_job.format(HREF)
            html_job = requests.get(URL_job)
            job = lxml.html.fromstring(html_job.content)

            ### Except instance where an Indeed help wanted ad appears instead of a job (Formatting is different) ###     
            try:
                head = job.xpath('.//div[@class="jobsearch-DesktopStickyContainer"]')[0]

            except IndexError:
                continue

            #Job Title
            title = head.xpath('.//h3[@class="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"]/text()')[0]

            #Company Name
            company_div = job.xpath('.//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]')[0]
            company = company_div.text_content()

            #Job Description
            body = job.xpath('.//div[@class="jobsearch-JobComponent-description icl-u-xs-mt--md"]')[0]
            body_div = body.xpath('.//div[@class="jobsearch-jobDescriptionText"]')[0]
            description = body_div.text_content()

            #Location
            location = job.xpath('.//span[@class="jobsearch-JobMetadataHeader-iconLabel"]/text()')[0]
            
            #Days Since Posting
            date = job.xpath('.//div[@class="jobsearch-JobMetadataFooter"]/text()')[0]

            #Current Date
            now = datetime.datetime.now()
            time_of_scrape = str(now.month)+' '+str(now.day)+' '+str(now.year)
    
            titles.append(title)
            companies.append(company)
            descriptions.append(description)
            locations.append(location)
            dates.append(date)
            time_of_scrapes.append(time_of_scrape)

            
            

    #Create a dataframe and export to csv
    d = {'Titles': titles, 'Companies': companies, 'Description' : descriptions, 'Location':locations,'Date':dates, 'Time of Scrape' :time_of_scrapes}
    df = pd.DataFrame(data=d)
    df.to_csv("./jobs_{}_{}.csv".format(Query,Location), sep=',',index=False)
  
