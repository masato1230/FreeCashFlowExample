import requests

from constants import securities_code_list

# ご自身のAPIキーを入力してください。
API_KEY = '8888888888888888888888888888'


def retrieve_json_by_securities_code(securities_code: int):
    """
    JP Funda APIにアクセスして、引数の証券コードに対応するJson形式のデータを取得する関数
    """
    url = 'https://www.jp-funda.com/api/jp/securities_code/' + \
        str(securities_code)
    headers = headers = {'Authorization': f'Token {API_KEY}'}

    res = requests.get(url, headers=headers)
    return res.json()


def calcurate_fcf_from_api_res(res_dict: dict):
    """
    上の関数の返り値からフリーキャッシュフローを取得する関数
    """
    # 必要なデータを取得できない時は、0をいれる
    if res_dict.get('会社名') is None:
        return {'no_data': 0}
    if res_dict.get('連結経営指標') is None:
        return {'no_data': 0}
    if res_dict.get('連結経営指標').get('営業活動によるキャッシュフロー') is None:
        return {'no_data': 0}
    if res_dict.get('連結経営指標').get('投資活動によるキャッシュフロー') is None:
        return {'no_data': 0}
    
    company_name = res_dict.get('会社名')
    cash_ope = res_dict.get('連結経営指標').get('営業活動によるキャッシュフロー')
    cash_inv = res_dict.get('連結経営指標').get('投資活動によるキャッシュフロー')

    # 簡易版のFCFの計算式
    fcf = cash_ope + cash_inv
    return {company_name: fcf}



if __name__ == '__main__':
    # まず、全社分のデータを辞書(all_dict)に格納=> 会社名: FCF
    all_dict = {}
    i = 1
    for securities_code in securities_code_list:
        print(i, '社目のデータ取得')
        i += 1
        res_dict = retrieve_json_by_securities_code(securities_code)
        all_dict.update(calcurate_fcf_from_api_res(res_dict))
    # ソート
    fcf_sorted = sorted(all_dict.items(), key=lambda x:x[1], reverse=True)
    
    i = 0
    for result in fcf_sorted:
        i += 1
        print(f'{i}位: ', result)
