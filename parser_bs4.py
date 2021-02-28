import logging
import collections
import csv
import requests
import bs4

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')

ParseResult = collections.namedtuple(
    'ParseResult',
    ('brand_name',
     'goods_name',
     'url'
    ),
)
HEADERS = (
    'Бренд',
    'Товар',
    'Ссылка'
)

class Client():

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Accept-Language': 'ru'
        }
        self.result = []

    def load_page(self, page : int = None):
        url = 'https://www.wildberries.ru/catalog/muzhchinam/dlya-vysokih'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text:str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        countainer = soup.select('div.dtList.i-dtList.j-card-item')
        for block in countainer:
            self.parse_block(block=block)

    def parse_block(self,block):


        url_block = block.select_one('a.ref_goods_n_p.j-open-full-product-card')
        if not url_block:
            logger.error('no url_block')
            return


        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return


        name_block = block.select_one('div.dtlist-inner-brand-name')
        if not name_block:
            logger.error(f'no name block on {url}')
            return
        brand_name = name_block.select_one('strong.brand-name.c-text-sm')
        if not brand_name:
            logger.error(f'no brand name on {url}')
            return
        goods_name = name_block.select_one('span.goods-name.c-text-sm')
        if not goods_name:
            logger.error(f'no goods name on {url}')

        #Wrangler
        brand_name = brand_name.text
        brand_name = brand_name.replace('/', '').strip()
        goods_name = goods_name.text
        goods_name = goods_name.replace('/', '').strip()

        logger.info('%s, %s, %s', url, brand_name, goods_name)

        self.result.append(ParseResult(
            url=url,
            brand_name=brand_name,
            goods_name=goods_name
        ))
        logger.debug('-' * 100)

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(f'Получили{len(self.result)} элементов')

        self.save_results()

    def save_results(self):
        path = '/Users/moddy/PycharmProjects/ParcerStudy/venv/test.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)

if __name__ == '__main__':
    parser = Client()
    parser.run()