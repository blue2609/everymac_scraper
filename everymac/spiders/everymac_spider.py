import scrapy
import re 
import itertools


class Macbook2Spider(scrapy.Spider):
    name = 'everymac_spider'
    allowed_domains = ['everymac.com']
    # start_urls = (
    #     'https://everymac.com/systems/apple/macbook/index-macbook.html',)
    start_urls = (
        'https://everymac.com/systems/apple/macbook_pro/index-macbookpro.html',)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    def start_requests(self):
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            
            yield scrapy.Request(url, headers=self.headers,callback=self.parse)
            # yield scrapy.Request(url=laptop_url, callback=self.parse_laptop_details, meta={'laptop_specs': laptop_specs}, headers=headers)

    def parse(self, response):

        # get the header of each macbook model
        mac_models = response.xpath(
            "//span[@id='contentcenter_specs_externalnav_wrapper' and position() >= 2]")

        # get the specs of each macbook model
        mac_specs = response.xpath(
            "//div[@id = 'contentcenter_specs_internalnav_wrapper']")

        for (model, spec) in zip(mac_models, mac_specs):

            # table_rows = spec.xpath(".//table/tbody/tr")
            table_rows = spec.xpath(".//table/tr")

            # Extract URL for each laptop model
            laptop_url = response.urljoin(model.xpath(
                ".//span[@id = 'contentcenter_specs_externalnav_2']/a/@href").get())

            # get the laptop name
            laptop_name_xpath = model.xpath(
                ".//span[@id = 'contentcenter_specs_externalnav_2']/a/text()").get()

            # get laptop specs and construct a dictionary
            laptop_specs = {'Laptop Name': model.xpath(".//span[@id = 'contentcenter_specs_externalnav_2']/a/text()").get(),
                            # 'Laptop CPU': model.xpath(".//span[@id = 'contentcenter_specs_externalnav_3']/text()").get(),
                            'Release Date': table_rows[0].xpath(".//td[2]/text()").get(),
                            'Order No.': table_rows[1].xpath(".//td[2]/text()").get(),
                            'Model No.': table_rows[1].xpath(".//td[4]/a[1]/text()").get(),
                            'ID': table_rows[2].xpath(".//td[4]/a/text()").get(),
                            # 'Default Memory' : table_rows[3].xpath(".//td[2]/text()").get(),
                            'Video Memory': table_rows[3].xpath(".//td[4]/text()").get(),
                            'Storage': table_rows[4].xpath(".//td[2]/text()").get(),
                            'Optical Drive': table_rows[4].xpath(".//td[4]/text()").get(),
                            'URL': laptop_url}

            # yield response.follow(url=)
            yield scrapy.Request(url=laptop_url, callback=self.parse_laptop_details, meta={'laptop_specs': laptop_specs},headers=self.headers)

    def parse_laptop_details(self, response):

        # get the passed laptop_specs data
        laptop_specs = response.request.meta['laptop_specs']

        # try to get additional information from this detail page
        # and add the additional info to the dictionary

        # ================================================
        #               Get details for the CPU
        # ================================================

        # <--------- # of CPU Cores ---------->
        cpu_cores_string = response.xpath(
            "//td[contains(text(),'Processors:')]/following-sibling::td[1]/text()").get()
        no_of_cores = re.findall("[0-9]+(?= Cores)", cpu_cores_string)[0]
        laptop_specs['CPU Cores'] = no_of_cores

        # <--------- CPU Name ---------->
        cpu_name = response.xpath(
            "//td[contains(text(),'Processor Type:')]/following-sibling::td[1]/text()").get()
        laptop_specs['CPU Name'] = cpu_name

        # <--------- CPU Frequency ---------->
        cpu_freq = response.xpath(
            "//td[contains(text(),'Processor Speed:')]/following-sibling::td[1]/text()").get()
        laptop_specs['CPU Frequency'] = cpu_freq

        # ================================================
        #               Get details for the RAM
        # ================================================

        # <--------- Standard RAM Capacity ---------->
        standard_ram = response.xpath(
            "//td[contains(text(),'Standard RAM:')]/following-sibling::td[1]/text()").get()

        # <--------- Max RAM Capacity ---------->
        max_ram = response.xpath(
            "//td[contains(text(),'Maximum RAM:')]/following-sibling::td[1]/text()").get()

        ram_capacity = f'{standard_ram},{max_ram}'
        laptop_specs['Memory Capacity'] = ram_capacity  # to be revised later

        # <--------- RAM Type & Speed ---------->
        ram_type = response.xpath(
            "//td[contains(text(),'RAM Type:')]/following-sibling::td[1]/text()").get()
        ram_speed = response.xpath(
            "//td[contains(text(),'Min. RAM Speed:')]/following-sibling::td[1]/text()").get()

        laptop_specs['RAM Type'] = ram_type
        laptop_specs['RAM Speed'] = ram_speed

        # ================================================
        #               Video Card Details
        # ================================================

        gpu = response.xpath(
            "//td[contains(text(),'Video Card:')]/following-sibling::td[1]/text()").get()
        gpu_type = response.xpath(
            "//td[contains(text(),'VRAM Type:')]/following-sibling::td[1]/text()").get()
        standard_vram = response.xpath(
            "//td[contains(text(),'Standard VRAM:')]/following-sibling::td[1]/text()").get()
        maximum_vram = response.xpath(
            "//td[contains(text(),'Maximum VRAM:')]/following-sibling::td[1]/text()").get()

        laptop_specs['GPU'] = gpu
        laptop_specs['GPU Type'] = gpu_type
        laptop_specs['GPU Standard VRAM'] = standard_vram
        laptop_specs['GPU Max VRAM'] = maximum_vram

        # ================================================
        #               Screen Detail
        # ================================================

        # Get the laptop display max resolution
        display_resolution = response.xpath(
            "//td[contains(text(),'Native Resolution:')]/following-sibling::td[1]/text()").get()
        laptop_specs['Display Resolution'] = display_resolution

        # ================================================
        #              Storage
        # ================================================

        # get pattern matching with spacy

        # = response.xpath("//td[contains(text(),'Native Resolution:')]/following-sibling::td[1]/text()").get()

        # laptop_specs['cpu_cores'] = response.xpath("//td[contains(text(),'Processors:')]/following-sibling::td/text())

        # ================================================
        #              Return the Dictionary
        # ================================================

        yield laptop_specs
