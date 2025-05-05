from typing import Annotated, Literal
from pydantic import Field

# We are using Literal because Claude desktop does not support enums

AutocompleteType = Annotated[
    Literal[
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
    ],
    Field(
        description="The field to autocomplete. Must be one of the supported filters such as 'job_title' or 'company_size'.")
]

NumberOfEmployeesRange = Annotated[
    Literal[
        "1-10",
        "11-50",
        "51-200",
        "201-500",
        "501-1000",
        "1001-5000",
        "5001-10000",
        "10001+",
    ],
    Field(description="Company size based on employee count.")
]

CompanyRevenue = Annotated[
    Literal[
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
    ],
    Field(description="Company revenue range in USD (e.g., '1M-5M').")
]

CompanyAge = Annotated[
    Literal[
        "0-3",
        "3-6",
        "6-10",
        "10-20",
        "20+",
    ],
    Field(description="Company age in years (e.g., '6-10' means 6 to 10 years old).")
]

NumberOfLocations = Annotated[
    Literal[
        "0-1",
        "2-5",
        "6-20",
        "21-50",
        "51-100",
        "101-1000",
        "1001+",
    ],
    Field(description="Number of physical company locations (e.g., offices, stores).")
]

JobDepartment = Annotated[
    Literal[
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
    ],
    Field(description="Department or function in the organization (e.g., 'Engineering', 'Marketing').")
]

JobLevel = Annotated[
    Literal[
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
    ],
    Field(
        description="Seniority level of the job (e.g., 'vp', 'manager', 'entry'). cxo is a catch-all for C-level positions such as CEO, CTO, etc.")]
