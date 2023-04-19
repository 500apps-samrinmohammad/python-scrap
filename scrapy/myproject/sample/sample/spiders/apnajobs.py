import scrapy
from scrapy import Selector

class ApnajobsSpider(scrapy.Spider):
    name = "apnajobs"
    allowed_domains = ["apna.co"]
    start_urls = ["https://apna.co/jobs"]

    def parse(self, response):
        job_data = response.xpath("//div[@class='styles__JobDetails-sc-1eqgvmq-1 koxkvV']/h3/a").xpath('@href').getall()
        print(job_data,">>>>>>>>>>>>")
        for job in job_data:
            job_url = "https://apna.co"+job
            print(job)
            yield scrapy.Request(url=job_url, callback=self.parse_job)
    
    def start_requests(self):
        categories = ['full_time-jobs', 'part_time-jobs']
        i=0
        while True:
           for category in categories:
                url = f"https://apna.co/jobs/{category}?page={i}"
                yield scrapy.Request(url=url, callback=self.parse)
                i += 1
                if i==500:
                  break  

    def parse_job(self, response):
        print("=== Job Details ===",response)
        title = response.xpath("//h1/text()").getall()
        company = response.xpath("//div[@class='styles__TextJobCompany-sc-15yd6lj-5 kIILUO']/text()").get()
        salary = response.xpath("//div[contains(@class,'styles__TextJobSalary-sc-15yd6lj-8 dGHiHv')]/text()").get()
        description = response.xpath("//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]/text()").get()
        openings = response.xpath("//div[contains(@class,'styles__JobOpeningCount-sc-15yd6lj-14 hRzbXS')]/text()").get()
        
        experience = ""
        education = ""
        englishlevel = ""
        gender = ""
        address = ""
        job_dict = {
            'title': title,
            'company': company,
            'salary': salary,
            'description': description,
            'openings':openings,
            'experience':experience,
            'education':education,
            'englishlevel':englishlevel,
            'gender':gender,
            'address':address
        }
        job_details = response.xpath("//div[@class='styles__JobDetailBlockContainer-sc-1532ppx-4 fqUGaU']").getall()
        print(len(job_details),"***********************")
        for detail in job_details: 
            k = Selector(text=detail)
            print(detail)
            label = k.xpath("//div[@class='styles__JobDetailBlockHeading-sc-1532ppx-2 iGzafA']/text()").get().strip()
            value =  k.xpath("//div[@class='styles__JobDetailBlockValue-sc-1532ppx-3 jtaqAv']/text()").get().strip()
            print(label,">>>>>>>>><<<<<<<<<<<<",value)
            job_dict[label]=value   
      
        print(job_dict , "::::::::::::::::::::::::")
        yield job_dict