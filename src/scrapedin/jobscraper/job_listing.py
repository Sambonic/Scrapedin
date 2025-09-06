from scrapedin.config.common_imports import *
from scrapedin.managers.logger_manager import logger
from typing import List, Dict, Any

class JobListing:
    """
    A class to manage and extract details from a job listing.
    """

    def __init__(self):
        self.job_details = {}
    

    def _extract_details(self, details: Dict[str, Any], skills: Dict[str, Any]) -> None:
        """
        Extracts and updates job details from the provided `details` and `skills` dictionaries.
        """
        # NB. Fix salary
        self.job_details.update({
            "id": details.get("jobPostingId"),
            "company": details.get("companyDetails", {}).get("com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany", {}).get("companyResolutionResult", {}).get("name"),
            "salary": details.get("salaryInsights"), 
            "employment_status": details.get("formattedEmploymentStatus"),
            "title": details.get("title"),
            "headcount": details.get("companyDetails", {}).get("com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany", {}).get("companyResolutionResult", {}).get("staffCountRange", {}).get("start"),
            "industry": details.get("formattedIndustries"),
            "experience": details.get("formattedExperienceLevel"),
            "applicants": details.get("applies"),
            "hiring_team": details.get("allJobHiringTeamMembersInjectionResult", {}).get("hiringTeamMembers"),
            "location": details.get("formattedLocation"),
            "workplace": details.get("workplaceTypesResolutionResults", {}).get("urn:li:fs_workplaceType:3", {}).get("localizedName"),
            "skills": self._extract_skills(skills),
            "description": details.get("description", {}).get("text"),
            "views": details.get("views"),
            "job_function": details.get("formattedJobFunctions"),
            "role": details.get("standardizedTitleResolutionResult", {}).get("localizedName"),
            "benefits": details.get("benefits"),
            "referrals_elgible": details.get("eligibleForReferrals"),
        })

    def _extract_skills(self, skills: Dict[str, Any]) -> List[str]:
        """
        Extracts a list of skills from the provided `skills` dictionary.
        """
        try:
            insights = (
                skills.get("data", {}).get("jobsDashJobPostingHowYouFitDetailsByJobPosting", {})
                    .get("elements", [{}])[0]
                    .get("howYouFitDetailSections", [{}])[1]
                    .get("howYouFitInsights", [])
            )
            
            return [
                insight.get("displayText")
                for insight in insights
                if "displayText" in insight
            ]
        except Exception:
            return []

    def _display_details(self) -> None:
        """
        Displays the extracted job details in the terminal using the logger.
        """
        logger.info("⬛ Job Listing Details:")
        for key, value in self.job_details.items():
            logger.info(f"{key.capitalize().replace('_', ' ')}: {value}")