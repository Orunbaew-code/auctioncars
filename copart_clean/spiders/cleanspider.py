import scrapy
from ..items import CopartItem
global page
page = 1

class CleanspiderSpider(scrapy.Spider):
    name = "cleanspider"
    allowed_domains = ["auctionexport.com"]
    start_urls = ["https://auctionexport.com/ru/cars/clean"]

    custom_settings = {
        'FEEDS' : {
            'carsdata.json': {'format': 'json', 'overwrite': True},
        }
    }

    def parse(self, response):
        global page
        cars = response.css('div.sv-container')
        for car in cars:
            car_page = car.css('div.sv-title-container a::attr(href)').get()
            car_page_url = 'https://www.auctionexport.com' + car_page
            yield response.follow(car_page_url, callback = self.parse_car_page)
        check = response.css('.sr-container .s-noresults::text').get()
        if check != 'No Results Found':
            page += 1
            next_page_url = f"https://auctionexport.com/ru/cars/clean/page/{str(page)}"
            yield response.follow(next_page_url, callback = self.parse)

    def parse_car_page(self, response):
        table_rows = response.css('.vi-vehicle-details-title-spacer table tr')
        sale_info = response.css('.vi-saleinfo-container table tr')
        copartItem = CopartItem()
        copartItem['Title'] = response.css('.vi-title-container span::text').get(),
        copartItem['Make'] = table_rows[1].css('td.value::text').get(),
        copartItem['Model'] = table_rows[2].css('td.value::text').get(),
        copartItem['Year'] = table_rows[3].css('td.value::text').get(),
        copartItem['Mileage'] = table_rows[4].css('td.value::text').get(),
        copartItem['Exterior'] = table_rows[5].css('td.value::text').get(),
        copartItem['Interior'] = table_rows[6].css('td.value::text').get(),
        copartItem['Drive_train'] = table_rows[7].css('td.value::text').get(),
        copartItem['Engine'] = table_rows[8].css('td.value::text').get(),
        copartItem['Transmission'] = table_rows[9].css('td.value::text').get(),
        copartItem['Sale_doc'] = table_rows[10].css('td.value::text').get(),
        copartItem['Keys'] = table_rows[11].css('td.value::text').get(),
        copartItem['Buy_now'] = response.css('.vi-optionbuy-container input::text').get(),
        copartItem['Fees'] = response.css('.c_fee_value_container .id_lblFeeAmountBuy::text').get(),
        copartItem['Cur_bid'] = response.css('.curr-bid .vi-price-value::text').get(),
        copartItem['Auction'] = sale_info[1].css('.value::text').get(),
        copartItem['End_date'] = sale_info[4].css('.value span::text').get()
        
        yield copartItem