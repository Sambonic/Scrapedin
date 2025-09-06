# API URLs 
JOB_DETAILS_API = (
    "https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_number}?"
    "decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65&topN=1"
    "&topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)"
)

SKILLS_API = (
    "https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true"
    "&variables=(jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{job_number})"
    "&queryId=voyagerJobsDashJobPostingHowYouFitDetails.bb4a0f9a189c19cfb8b2fe0acbddd62a"
)

JOB_LISTINGS_API = (
    "https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards"
    "?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-216&count=25"
    "&q=jobSearch&query=(origin:HISTORY,keywords:{role},locationUnion:(geoId:103644278),"
    "selectedFilters:(distance:List(2000.0)),spellCorrectionEnabled:true)&start={job_number}"
)


# Variables
LINKEDIN_LIMIT = 1000
REQUEST_DELAY = 0.3
WAIT = 1

# Linkedin URLs
HOMEPAGE_URL = 'https://www.linkedin.com'
LINKEDIN_LOGIN = 'https://www.linkedin.com/login'
JOBS_URL = "https://www.linkedin.com/jobs/search/?keywords={role}&start={job_number}"


# Session headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'X-Restli-Protocol-Version': '2.0.0',
}


