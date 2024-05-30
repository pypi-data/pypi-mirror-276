import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from .util import gen_random_params, clean_html_tags, logger

class BaiduMobile:
    
    def __init__(self):
        self.random_params = gen_random_params()
        self.keyword = None
        self.recomment_list = []

    def extract_baidum_data(self, html_content):
        search_data = []
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.find_all(class_='c-result result')
        for result in search_results:
            title_element = result.find('p', class_='cu-title')

            url = result.get('data-log')
            if url:
                url = json.loads(url)['mu']

            description = ""
            date_time = ""

            summary_element = result.find('div', class_=lambda x: x and 'summary-' in x)
            if summary_element:
                description = clean_html_tags(summary_element.get_text().strip())

                date_time_element = summary_element.find('span', class_='c-gap-right-small c-color-gray')
                if date_time_element:
                    description = description.replace(date_time_element.get_text().strip(), '')
                    date_time = date_time_element.get_text().strip()

            if title_element and url:
                title_text = clean_html_tags(title_element.get_text().strip())
                search_data.append({'title': title_text, 'url': url, 'description': description, 'date_time': date_time})

        return search_data

    def get_recommend(self, keyword, qid, proxies=None):
        url = 'https://m.baidu.com/rec'
        params = {
            'word': keyword,
            'platform': 'wise',
            'ms': '1',
            'lsAble': '1',
            'rset': 'rcmd',
            'qid': qid,
            'rq': 'python',
            'from': '0',
            'baiduid': f'BAIDUID={self.random_params["baiduid"]}:FG=1',
            'tn': '',
            'clientWidth': '412',
            't': self.random_params['timestamp'],
            'r': self.random_params['r'],
        }
        headers = {
            'Cookie': f'BAIDUID={self.random_params["baiduid"]}:FG=1; BAIDUID_BFESS={self.random_params["baiduid"]}:FG=1;BDUSS={self.random_params["bduss"]};',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 baiduboxapp/13.10.0.10',
        }
        try:
            response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            json_data = response.json()
            # 获取所有键名为'up'和'down'的值
            up_values = []
            down_values = []
            for item in json_data['rs']['rcmd']['list']:
                up_values.extend(item['up'])
                down_values.extend(item['down'])

            # 排重并合并为新的列表
            recomment_list = list(set(up_values + down_values))
            logger.debug(len(recomment_list))
            return recomment_list
        except requests.exceptions.RequestException as e:
            return {'code': 500, 'msg': '网络请求错误'}

    def get_baidum_serp(self, keyword, date_range=None, pn=None, proxies=None):
        url = 'https://m.baidu.com/s'
        params = {
            'word': keyword
        }
        if date_range:
            start_date, end_date = date_range.split(',')
            start_timestamp = int(datetime.strptime(start_date, '%Y%m%d').timestamp())
            end_timestamp = int(datetime.strptime(end_date, '%Y%m%d').timestamp())
            params['gpc'] = f'stf={start_timestamp},{end_timestamp}|stftype=2'
        if pn:
            params['pn'] = str((int(pn) - 1) * 10)
        headers = {
            'Cookie': f'BAIDUID={self.random_params["baiduid"]}:FG=1; BAIDUID_BFESS={self.random_params["baiduid"]}:FG=1;BDUSS={self.random_params["bduss"]};',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 baiduboxapp/13.10.0.10'
        }
        try:
            response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=10)
            # 如果没有传页码或者是第1页则获取相关搜索词
            if pn is None or pn==1:
                res_headers = response.headers
                if 'qid' in res_headers:
                    qid = res_headers['qid']
                self.recomment_list = self.get_recommend(keyword, qid=qid, proxies=proxies)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f'{keyword}相关搜索词获取失败')
            return []

    def handle_response(self, response):
        if isinstance(response, str):
            if '百度安全验证' in response:
                return {'code': 501, 'msg': '百度安全验证'}
            elif '未找到相关结果' in response:
                return {'code': 404, 'msg': '未找到相关结果'}
            else:
                soup = BeautifulSoup(response, 'html.parser')
                if not soup.find('p', class_='cu-title'):
                    return {'code': 403, 'msg': '疑似违禁词'}
                search_results = self.extract_baidum_data(response)
                last_page = 'new-nextpage' not in response
                return {'code': 200, 'msg': 'ok', 'data': {'results': search_results, 'recomment': self.recomment_list, 'last_page': last_page}}
        else:
            return response

    def search(self, keyword, date_range=None, pn=None, proxies=None):
        html_content = self.get_baidum_serp(keyword, date_range, pn, proxies)
        return self.handle_response(html_content)
