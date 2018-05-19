# -*- coding: utf-8 -*-
import scrapy
import requests

class KrishaSpider(scrapy.Spider):
	name = 'krisha'
	allowed_domains = ['krisha.kz']
	start_urls = ['http://krisha.kz/pro/specialist/']
	initial_next_urls = []
	page = 0

	def parse(self, response):
		self.page += 1
		with open('krisha.csv', 'a') as f:
			realtors = response.xpath("//div[@class='pitem']")
			for i in realtors:
				#photo = i.css('div.image_cover').css('img.photo/@href').extract_first()
				name = i.css('div.pr_block').css('a.name::text').extract_first()
				speciality = i.css('div.pr_block').css('div.speciality::text').extract_first()
				total = i.css('div.total_block').css('div.total::text').extract_first()
				numbers = i.css('div.pr_block').css('div.phones::text').extract_first().replace(' ', '').replace('(', '').replace(')', '').split(',')

				f.write('{}'.format(name.encode('utf8')) + ',')
				f.write('{}'.format(speciality.encode('utf8')).replace(',', '') + ',')
				f.write('{}'.format(total.encode('utf8')) + ',')
				f.write('{}\n'.format(','.join(numbers).encode('utf8')))
				
		next_page_url = response.xpath("//link[@id='NextLink']/@href").extract_first()
		if next_page_url and next_page_url not in self.initial_next_urls:
			if len(self.initial_next_urls) < 2:
				self.initial_next_urls.append(next_page_url)
			yield scrapy.Request(response.urljoin(next_page_url))