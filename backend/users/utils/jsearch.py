import os
import requests
import json
import random
from datetime import datetime

class JSearchClient:
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY')
        self.host = "jsearch.p.rapidapi.com"
        self.base_url = "https://jsearch.p.rapidapi.com"
        
    def _get_headers(self):
        if not self.api_key:
            return None
        return {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }

    def search_jobs(self, query, location="India", num_pages=1):
        """
        Fetches job listings from JSearch API.
        Returns a list of job dictionaries or None if API fails/key missing.
        """
        if not self.api_key:
            print("JSearchClient: No API Key found.")
            return None

        url = f"{self.base_url}/search"
        headers = self._get_headers()
        
        # JSearch params
        querystring = {
            "query": f"{query} in {location}",
            "page": "1",
            "num_pages": str(num_pages),
            "date_posted": "month" # Get recent data for trends
        }

        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                print(f"JSearch API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"JSearch Client Exception: {e}")
            return None

    def estimate_market_stats(self, query, location="India"):
        """
        Derives market stats from a fresh search.
        Returns:
            - job_count: Total jobs found (or estimated from result size)
            - avg_salary: Estimated max salary from results
            - roles: List of unique job titles found
        """
        jobs = self.search_jobs(query, location)
        
        if not jobs:
            return None
            
        # 1. Estimate Count (Soft estimate based on density of return)
        # JSearch doesn't always give a "total_count" metadata field reliable in free tier, 
        # but we can infer density. Let's return the length for now, or scaled.
        # Actually, let's just return the count of fetched jobs as a sample size.
        job_count = len(jobs)
        
        # 2. Extract Salaries
        salaries = []
        roles = []
        skills_mentioned = []
        
        for job in jobs:
            # Roles
            title = job.get('job_title')
            if title: roles.append(title)
            
            # Salary (Check min/max fields)
            # JSearch structure: 'job_min_salary', 'job_max_salary', 'job_salary_currency'
            min_sal = job.get('job_min_salary')
            max_sal = job.get('job_max_salary')
            
            if min_sal and max_sal:
                avg = (min_sal + max_sal) / 2
                salaries.append(avg)
            elif max_sal:
                salaries.append(max_sal)
                
            # Description for skill approximation (optional, heavy compute)
            # Let's skip description text mining for now to keep it fast.

        avg_salary = sum(salaries) / len(salaries) if salaries else 0
        
        # 3. Top Roles
        from collections import Counter
        top_roles = [role for role, _ in Counter(roles).most_common(5)]
        
        return {
            "sample_size": job_count,
            "avg_salary": avg_salary,
            "top_roles": top_roles,
            "raw_jobs": jobs[:5] # Return top 5 for detail view if needed
        }
