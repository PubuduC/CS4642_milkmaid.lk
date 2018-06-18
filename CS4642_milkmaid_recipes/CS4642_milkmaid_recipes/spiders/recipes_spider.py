import scrapy


class RecipesSpider(scrapy.Spider):
    name = "recipes"
    start_urls = [
        'https://www.milkmaid.lk/en/recipes',
    ]
    def parse(self, response):
        for inner_col in response.css('div.inner_col'):
            yield response.follow(inner_col.css('a::attr(href)').extract_first(), callback=self.parse_page)
    def parse_page(self, response):
        yield {
            'name': response.css('h2.recipe_name::text').extract_first(),
            'total_time' : response.xpath('//*[@id="block-system-main"]/div/section[1]/div/div/div[2]/div/div[1]/span/text()').extract_first(),
            'cook_time' : response.xpath('//*[@id="block-system-main"]/div/section[1]/div/div/div[2]/div/div[2]/div[2]/span[2]/text()').extract_first(),
            'preparation_time' : response.xpath('//*[@id="block-system-main"]/div/section[1]/div/div/div[2]/div/div[2]/div[1]/span[2]/text()').extract_first(),
            'servings' : response.xpath('//*[@id="block-system-main"]/div/section[1]/div/div/div[2]/div/div[2]/div[3]/span[2]/text()').extract_first(),
            'vote' : response.css('div.heart_widget li::text').extract_first(),
            'ingredients' : response.css('div.row.ingredient_row div.row.ingredient').extract(),
            'directions' : response.css('div.direction div.row').extract(),
        }
