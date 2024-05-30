"""BSD 2-Clause License

Copyright (c) 2024, harumaki4649

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
import os.path
import random
import re
import time
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}


def download(url, path="./archive_download", mode=0):
    print(path[-1])
    if not path[-1] == "/":
        path += "/"
    html_path = path
    html_path += "index.html"
    tmp_path = ""
    print(html_path)
    for tmp in html_path.split("/"):
        tmp_path += tmp + "/"
        if not os.path.exists(tmp_path) and not "." in tmp:
            os.mkdir(tmp_path)
    session = requests.session()
    while True:
        try:
            r = session.get(url, headers=headers)
            break
        except Exception:
            print("レート制限のため数秒後再試行します")
            time.sleep(random.uniform(5, 15))

    if r.ok:
        # HTMLをファイルに保存
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(r.text)
    else:
        print(r.status_code)
        raise

    from bs4 import BeautifulSoup

    # HTMLファイルを読み込む
    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(html_content, 'html.parser')

    f_pth = path + "index_files/"
    datas = {}

    def download_file(url):
        print(url)
        while True:
            try:
                if url.startswith("//"):
                    r = session.get(f"https:{url}", headers=headers)
                else:
                    r = session.get(url, headers=headers)
                print("OK")
                break
            except Exception as e:
                print(e)
                print("レート制限のため数秒後再試行します")
                time.sleep(random.uniform(1, 15))
        if r.ok:
            try:
                if not os.path.exists(f_pth):
                    os.mkdir(f_pth)
                ch_tmp = url.split('/')[-1].split('?')[0]
                if "." in ch_tmp:
                    ch_tmp = ch_tmp.split('.')[1]
                url_tmp = url.split('/')[-1]
                if "?" in url_tmp:
                    url_tmp = url_tmp.split('?')[0]
                if ch_tmp in ["css", "js"]:
                    # レスポンスのエンコーディングを設定（例えば'utf-8'など）
                    r.encoding = 'utf-8'
                    with open(f"{f_pth}{url_tmp}", "w", encoding="utf-8") as f:
                        f.write(r.text)
                else:
                    with open(f"{f_pth}{url_tmp}", "wb") as f:
                        f.write(r.content)
                datas[url] = f"index_files/{url_tmp}"
                print("File Save")
            except Exception as e:
                print(e)

    if not mode == 0:
        # 全ての<script>タグと<link>タグを取得
        script_tags = soup.find_all('script')
        link_tags = soup.find_all('link')

        # URLを抽出するための正規表現パターン
        url_pattern = re.compile(r'(?:https?:\/\/|\/\/)[^\s/$.?#].[^\s]*')

        # 各<script>タグのsrc属性の値を抽出
        for script in script_tags:
            src = script.get('src')
            if src:
                urls = re.findall(url_pattern, src)
                for url in urls:
                    download_file(url)

        # 各<link>タグのhref属性の値を抽出
        for link in link_tags:
            href = link.get('href')
            if href:
                urls = re.findall(url_pattern, href)
                for url in urls:
                    download_file(url)
        # すべてのdivタグを取得
        div_tags = soup.find_all('div', class_=True)

        # URLを格納するリスト
        urls = []

        # divタグごとにループ
        for div_tag in div_tags:
            # data-bg属性を取得
            data_bg = div_tag.get('data-bg')

            # data-bg属性が存在し、その値がURLを含むか確認
            if data_bg and re.match(r"url\('.*?'\)", data_bg):
                # URLを正規表現で抽出
                match = re.search(r"url\('(.*?)'\)", data_bg)
                if match and not url in urls:
                    url = match.group(1)
                    urls.append(url)
                    download_file(url)

    # 特定の<div>要素を削除
    div_to_remove = soup.find("div", id="wm-ipp-inside")
    if div_to_remove:
        div_to_remove.decompose()

    # 特定の<div>要素を削除
    div_to_remove = soup.find("div", id="wm-ipp-print")
    if div_to_remove:
        div_to_remove.decompose()

    # 特定の<div>要素を削除
    div_to_remove = soup.find("div", id="wm-ipp-base")
    if div_to_remove:
        div_to_remove.decompose()

    # 残りのコンテンツを取得
    new_html_content = soup.prettify()
    soup = BeautifulSoup(new_html_content, 'html.parser')

    if not mode == 2:
        # 動的なスクリプトを探して置き換え
        script_tag = soup.find("script", text=re.compile(r'__wm\.wombat'))
        if script_tag:
            original_script = script_tag.string
            replace_data = original_script.split('__wm.wombat("')[1].split('"')[0]
            new_html_content = new_html_content.replace("https://web-static.archive.org/_static/", replace_data)
            soup = BeautifulSoup(new_html_content, 'html.parser')
            script_tag = soup.find("script", text=re.compile(r'__wm\.wombat'))
            script_tag.decompose()
        # 残りのコンテンツを取得
        new_html_content = soup.prettify()
        replace_list = []
        for tmp in new_html_content.split("//web.archive.org/web/"):
            dt = tmp.split("/")[0]
            if not dt in replace_list:
                replace_list.append(dt)
        for tmp in replace_list:
            dt = "//web.archive.org/web/" + tmp + "/"
            new_html_content = new_html_content.replace("https:" + dt, "")
            new_html_content = new_html_content.replace(dt, "")
    else:
        print(datas)
        for tmp in datas.keys():
            print(tmp)
            print(datas[tmp])
            new_html_content = new_html_content.replace(tmp, datas[tmp])
    new_html_content = new_html_content.split("<!--\n     FILE ARCHIVED ON")[0]

    # 新しいHTMLをファイルに保存
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(new_html_content)
