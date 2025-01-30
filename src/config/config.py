# Constants used in linkedin_job_scraper.py
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
# Linkedin Login variables
LINKEDIN_LOGIN = "https://www.linkedin.com/login"
WAIT = 1

