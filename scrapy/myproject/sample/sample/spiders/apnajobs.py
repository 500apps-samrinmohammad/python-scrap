import scrapy


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

    def parse_job(self, response):
        print("=== Job Details ===",response)
        title = response.xpath("//h1/text()").getall()
        company = response.xpath("//div[@class='styles__TextJobCompany-sc-15yd6lj-5 kIILUO']/text()").get()
        location = response.xpath("//div[contains(@class,'styles__TextJobArea-sc-15yd6lj-7 cHFGaJ')]/text()").get()
        salary = response.xpath("//div[contains(@class,'styles__TextJobSalary-sc-15yd6lj-8 dGHiHv')]/text()").get()
        description = response.xpath("//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]/text()").get()
        job_dict = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'description': description
        }
        print(job_dict , "::::::::::::::::::::::::")
        yield job_dict