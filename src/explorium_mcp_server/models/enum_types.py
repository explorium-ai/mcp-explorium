from typing import Literal

# Currently claude desktop does not support python enum, so we are using Literal instead

AutocompleteType = Literal[
    "country",
    "country_code",
    "region_country_code",
    "google_category",
    "naics_category",
    "linkedin_category",
    "company_tech_stack_tech",
    "company_tech_stack_categories",
    "job_title",
    "company_size",
    "company_revenue",
    "number_of_locations",
    "company_age",
    "job_department",
    "job_level",
    "city_region_country",
    "company_name",
]

NumberOfEmployeesRange = Literal[
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1001-5000",
    "5001-10000",
    "10001+",
]

CompanyRevenue = Literal[
    "0-500K",
    "500K-1M",
    "1M-5M",
    "5M-10M",
    "10M-25M",
    "25M-75M",
    "75M-200M",
    "200M-500M",
    "500M-1B",
    "1B-10B",
    "10B-100B",
    "100B-1T",
    "1T-10T",
    "10T+",
]

CompanyAge = Literal[
    "0-3",
    "3-6",
    "6-10",
    "10-20",
    "20+",
]

NumberOfLocations = Literal[
    "0-1",
    "2-5",
    "6-20",
    "21-50",
    "51-100",
    "101-1000",
    "1001+",
]

JobDepartment = Literal[
    "Real estate",
    "Customer service",
    "Trades",
    "Unknown",
    "Public relations",
    "Legal",
    "Operations",
    "Media",
    "Sales",
    "Marketing",
    "Finance",
    "Engineering",
    "Education",
    "General",
    "Health",
    "Design",
    "Human resources",
]

JobLevel = Literal[
    "owner",
    "cxo",
    "vp",
    "director",
    "senior",
    "manager",
    "partner",
    "non-managerial",
    "entry",
    "training",
    "unpaid",
    "unknown",
]
