from bs4 import BeautifulSoup
import requests
import csv

def write(dict_data):
    #write to csv file

def scrape():
    job_list = []
    url = 'https://www.indeed.com/jobs?q=software+developer+intern&start=0'
    job_list_page = requests.get(url)
    soup = BeautifulSoup(job_list_page.content, 'html.parser')
    pages = soup.find(id="searchCountPages").text
    total_pages = int(pages.split()[3].replace(',', ''))/15
    for i in range(1, int(total_pages)+1):
        new_url = 'https://www.indeed.com/jobs?q=software+developer+intern&start=0' + str(i * 10)
        job_list_page = requests.get(new_url)
        job_list_soup = BeautifulSoup(job_list_page.content, 'html.parser')
        job_data = dict()
        job_data["Company Name"] = job_list_soup.find(class_='companyName').text
        job_data["Location"] = job_list_soup.find(class_='companyLocation').text
        job_list.append(job_data.update(parseJobHtml(job_list_soup.find(id='mosaic-provider-jobcards'))))


def parseJobHtml(htmlString):
    job_hyperlink_list = htmlString.find_all('a')
    job_info = dict()
    for hyperlink in job_hyperlink_list:
        link = "https://www.indeed.com" + hyperlink['href']
        job_page = requests.get(link)
        job_page_soup = BeautifulSoup(job_page.content, 'html.parser')
        title = job_page_soup.find(class_='jobsearch-JobInfoHeader-title-container').text
        job_info["Title"] = title
        application = job_page_soup.find(id='applyButtonLinkContainer').find('a')['href']
        job_info["Application"] = application
        description = job_page_soup.find(id="jobDescriptionText").text
        job_info["Description"] = description

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape()
    write()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
