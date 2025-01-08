import requests
from bs4 import BeautifulSoup
from weapon import Weapon
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_weapon(url):
    try:
        response = requests.get(url,headers=headers)
        response.encoding = 'utf-8'  # 设置编码为 UTF-8
        soup = BeautifulSoup(response.text, 'html.parser')

        name = ''
        count = 0
        dps = []
        sr = ''

        h1_element = soup.find('h1', class_='title')
        if h1_element:
            name = h1_element.text

        tables = soup.find_all("table")  # 找到所有表格
        for table in tables:
            rows = table.find_all("tr")  # 找到所有行
            for row in rows:
                ths = row.find_all("th")  # 找到所有单元格
                tds = row.find_all("td")
                # 找到 "DPS" 所在的列索引
                dps_index = None
                for i, th in enumerate(ths):
                    if "DPS" in th.text:
                        dps_index = i
                        break
                # 提取 "DPS" 列的数据
                if dps_index is not None:
                        if dps_index < len(tds):  # 确保列索引有效
                            dps.append(tds[dps_index].text.strip())
                            count+=1

                if sr!='':
                    continue
                # 找到 "SR補正" 所在的列索引
                sr_index = None
                for i, th in enumerate(ths):
                    if "SR補正" in th.text:
                        sr_index = i
                        break
                # 提取 "DPS" 列的数据
                if sr_index is not None:
                        if sr_index < len(tds):  # 确保列索引有效
                            sr = tds[sr_index].text.strip()
        dps0 = dps[0] if count>0 else ''
        dps1 = dps[1] if count>1 else ''
        return Weapon(name,dps0,dps1,sr)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None
    
def write_weapon_to_csv(weapon, filename="weapons.csv"):
    # 打开 CSV 文件，追加模式
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入表头（如果文件是新创建的）
        if file.tell() == 0:  # 检查文件是否为空
            writer.writerow(["Name", "DPS", "DPS(Other)", "DPS(SR)"])
        
        # 写入武器数据
        writer.writerow([weapon.name, weapon.dps,weapon.dpsOther])

def get_hrefs_from_table():
    url = "https://wikiwiki.jp/splatoon3mix/%E3%83%96%E3%82%AD"
    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'  # 设置编码为 UTF-8
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all("table")
    for table in tables:
        # 查找表格中是否有 <th> 含有 "対象ブキ"
        ths = table.find_all("th")
        for th in ths:
            if "対象ブキ" in th.text:  # 匹配目标表格
                # 从该表格中提取所有链接的 href
                hrefs = []
                links = table.find_all("a", href=True)  # 找到所有 <a> 标签且有 href 属性
                for link in links:
                    hrefs.append(link["href"])
                return hrefs  # 返回 href 列表
    return []  # 如果没有找到目标表格，返回空列表


if __name__ == "__main__":
    dns = "https://wikiwiki.jp"
    hrefs = get_hrefs_from_table()
    for href in hrefs:
        url = dns+href
        weapon = fetch_weapon(url)
        if weapon:
            write_weapon_to_csv(weapon)