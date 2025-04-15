from enum import Enum


class AutocompleteType(str, Enum):
    COUNTRY = "country"
    COUNTRY_CODE = "country_code"
    REGION_COUNTRY_CODE = "region_country_code"
    GOOGLE_CATEGORY = "google_category"
    NAICS_CATEGORY = "naics_category"
    LINKEDIN_CATEGORY = "linkedin_category"
    COMPANY_TECH_STACK_TECH = "company_tech_stack_tech"
    COMPANY_TECH_STACK_CATEGORIES = "company_tech_stack_categories"
    JOB_TITLE = "job_title"
    COMPANY_SIZE = "company_size"
    COMPANY_REVENUE = "company_revenue"
    NUMBER_OF_LOCATIONS = "number_of_locations"
    COMPANY_AGE = "company_age"
    JOB_DEPARTMENT = "job_department"
    JOB_LEVEL = "job_level"
    CITY_REGION_COUNTRY = "city_region_country"
    COMPANY_NAME = "company_name"


class BaseFilterEnum(str, Enum):
    """
    Base class for all filter enums. This class is used to ensure that all filter enums
    are of type str and can be easily converted to a string representation.
    """

    @classmethod
    def _missing_(cls, value: str) -> Enum:
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        raise ValueError(f"{value!r} is not a valid {cls.__name__}")


class NumberOfEmployeesRange(BaseFilterEnum):
    RANGE_1_10 = "1-10"
    RANGE_11_50 = "11-50"
    RANGE_51_200 = "51-200"
    RANGE_201_500 = "201-500"
    RANGE_501_1000 = "501-1000"
    RANGE_1001_5000 = "1001-5000"
    RANGE_5001_10000 = "5001-10000"
    RANGE_10001_PLUS = "10001+"


class CompanyRevenue(BaseFilterEnum):
    ZERO_TO_500K = "0-500K"
    FIVE_HUNDRED_THOUSAND_TO_1_MILLION = "500K-1M"
    ONE_MILLION_TO_5_MILLION = "1M-5M"
    FIVE_MILLION_TO_TEN_MILLION = "5M-10M"
    TEN_MILLION_TO_25_MILLION = "10M-25M"
    TWENTY_FIVE_MILLION_TO_75_MILLION = "25M-75M"
    SEVENTY_FIVE_MILLION_TO_200_MILLION = "75M-200M"
    TWO_HUNDRED_MILLION_TO_500_MILLION = "200M-500M"
    FIVE_HUNDRED_MILLION_TO_ONE_BILLION = "500M-1B"
    ONE_BILLION_TO_TEN_BILLION = "1B-10B"
    TEN_BILLION_TO_100_BILLION = "10B-100B"
    ONE_HUNDRED_BILLION_TO_ONE_TRILLION = "100B-1T"
    ONE_TRILLION_TO_TEN_TRILLION = "1T-10T"
    TEN_TRILLION_PLUS = "10T+"


class CompanyAge(BaseFilterEnum):
    RANGE_0_3 = "0-3"
    RANGE_3_6 = "3-6"
    RANGE_6_10 = "6-10"
    RANGE_10_20 = "10-20"
    RANGE_20_PLUS = "20+"


class NumberOfLocations(BaseFilterEnum):
    RANGE_0_1 = "0-1"
    RANGE_2_5 = "2-5"
    RANGE_6_20 = "6-20"
    RANGE_21_50 = "21-50"
    RANGE_51_100 = "51-100"
    RANGE_101_1000 = "101-1000"
    RANGE_1001_PLUS = "1001+"


class JobDepartment(BaseFilterEnum):
    REAL_ESTATE = "Real estate"
    CUSTOMER_SERVICE = "Customer service"
    TRADES = "Trades"
    UNKNOWN = "Unknown"
    PUBLIC_RELATIONS = "Public relations"
    LEGAL = "Legal"
    OPERATIONS = "Operations"
    MEDIA = "Media"
    SALES = "Sales"
    MARKETING = "Marketing"
    FINANCE = "Finance"
    ENGINEERING = "Engineering"
    EDUCATION = "Education"
    GENERAL = "General"
    HEALTH = "Health"
    DESIGN = "Design"
    HUMAN_RESOURCES = "Human resources"


class JobLevel(BaseFilterEnum):
    OWNER = "owner"
    CXO = "cxo"
    VP = "vp"
    DIRECTOR = "director"
    SENIOR = "senior"
    MANAGER = "manager"
    PARTNER = "partner"
    NON_MANAGERIAL = "non-managerial"
    ENTRY = "entry"
    TRAINING = "training"
    UNPAID = "unpaid"
    UNKNOWN = "unknown"
