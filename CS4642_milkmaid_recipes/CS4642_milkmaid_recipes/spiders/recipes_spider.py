import scrapy


class RecipesSpider(scrapy.Spider):
    name = "recipes"
    start_urls = [
        'https://www.milkmaid.lk/en/recipes',
    ]
    def parse(self, response):
        for inner_col in response.css('div.inner_col'):
            yield response.follow(inner_col.css('a::attr(href)').extract_first(), callback=self.parse_page)
        next_page = response.css('ul.pagination li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def get_numerical_val(str_):
        value = ''.join(x for x in str_ if x.isdigit())
        if len(value) > 0:
            return value
        else:
            return None

    def parse_page(self, response):
        total_time_string = response.xpath('//*[@id="block-system-main"]/div/section[1]/div/div/div[2]/div/div[1]/span/text()').extract_first()
        total_time = self.get_numerical_val(total_time_string)
        cook_time_string = response.xpath('//*[@id="block-system-main"]/div/section[1]/div/div/div[2]/div/div[2]/div[2]/span[2]/text()').extract_first()
        cook_time = self.get_numerical_val(cook_time_string)
        preparation_time_string = response.xpath('//*[@id="block-system-main"]/div/section[1]/div/div/div[2]/div/div[2]/div[1]/span[2]/text()').extract_first()
        preparation_time = self.get_numerical_val(preparation_time_string)
        directions_list = response.css('div.direction div.row').extract()
        directions = []
        for direction in directions_list:
            dir_str = direction.split('<p class="step_para_heading">')[1].split('</p>\r\n\t\t\t\t\t\t\t<p class="step_para">')[
                0] + "-" + direction.split('<p class="step_para_heading">')[1].split('</p>\r\n\t\t\t\t\t\t\t<p class="step_para">')[
                1].split('</p>')[0]
            directions.append(dir_str)
        ingredients_list = response.css('div.row.ingredient_row div.row.ingredient').extract()
        ingredients = []
        for ingredient in ingredients_list:
            ingredient_str = ingredient.split('<div class="col-sm-5 col-xs-6 ingredient_col">')[1].split('</div>')[0] \
                      + " - " + \
                      ingredient.split('<div class="col-sm-5 col-xs-6 ingredient_col">')[1].split('<div class="col-sm-7 col-xs-6 ingredient_col">')[1].split('</div>')[0]
            ingredients.append(ingredient_str)

        nutritions_fact_list = response.css('div.row.nutritional_fact p').extract()
        nutritions_fact = ""
        if(len(nutritions_fact_list)!=0):
            for nutri_fact in nutritions_fact_list:
                nutritions_fact= nutritions_fact+(nutri_fact.split('<strong>')[1].split('</strong>')[0])
        nutritions_list = response.css('div.row.nutritional_row div.row.nutritional').extract()
        nutritions = []
        if(len(nutritions_list)!=0):
            for nutrition in nutritions_list:
                nutri_str = nutrition.split('<div class="col-sm-5 col-xs-6 nutritional_col">')[1].split('</div>')[0]\
                        +" "+nutrition.split('<div class="col-sm-7 col-xs-6 nutritional_col">')[1].split('</div>')[0]
                nutritions.append(nutri_str)

        yield {
            'name': response.css('h2.recipe_name::text').extract_first(),
            'total_time_mins' : total_time,
            'cook_time_mins' : cook_time,
            'preparation_time_mins' : preparation_time,
            'servings' : response.xpath('//*[@id="block-system-main"]/div/section[1]/div/div/div[2]/div/div[2]/div[3]/span[2]/text()').extract_first(),
            'vote' : response.css('div.heart_widget li::text').extract_first(),
            'ingredients' : ingredients,
            'directions' : directions,
            'nutritional_facts' : nutritions_fact,
            'nutritional_info' : nutritions,
        }


