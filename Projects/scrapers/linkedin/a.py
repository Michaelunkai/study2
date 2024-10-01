import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

# Keep track of processed job links
processed_job_links = set()

# Fired once for each successfully processed job
def on_data(data: EventData):
    if data.link not in processed_job_links:
        print('\033[1m' + '[ON_DATA]' + '\033[0m')
        print('\033[1m' + 'Title:' + '\033[0m', data.title)
        print('\033[1m' + 'Company:' + '\033[0m', data.company)
        print('\033[1m' + 'Company Link:' + '\033[0m', data.company_link)
        print('\033[1m' + 'Date:' + '\033[0m', data.date)
        print('\033[1m' + 'Job Link:' + '\033[0m', data.link)
        print('\033[1m' + 'Insights:' + '\033[0m', data.insights)
        print('\033[1m' + 'Description Length:' + '\033[0m', len(data.description))
        print('\033[1m' + 'Description:' + '\033[0m', data.description)
        print('\033[1m' + '-' * 100 + '\033[0m')  # Dashed line
        processed_job_links.add(data.link)


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('\033[1m' + '[ON_METRICS]' + '\033[0m', str(metrics))


def on_error(error):
    print('\033[1m' + '[ON_ERROR]' + '\033[0m', error)


def on_end():
    print('\033[1m' + '[ON_END]' + '\033[0m')


def sort_by_date(jobs):
    return sorted(jobs, key=lambda x: x.date, reverse=True)


scraper = LinkedinScraper(
    chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_binary_location=None,  # Custom path to Chrome/Chromium binary (e.g. /foo/bar/chrome-mac/Chromium.app/Contents/MacOS/Chromium)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = []

# Create a separate query for each term
for term in ['linux', 'administrator', 'junior']:
    query = Query(
        query=term,  # Individual term
        options=QueryOptions(
            locations=['Rehovot', 'Tel Aviv-Yafo', 'Ramat Gan', 'Petah Tikva', 'Herzliya', 'Raanana'],
            limit=27,  # Limit the number of jobs to scrape.
        )
    )
    queries.append(query)

scraper.run(queries)

# Sort the jobs by date after scraping
sorted_jobs = sort_by_date(scraper.get_jobs())
for job in sorted_jobs:
    print('\033[1m' + job.title, job.company, job.date + '\033[0m')
