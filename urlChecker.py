import requests
import sys
import ssl
import re
import getopt

requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive'
}


def get_status(url):
    try:
        r = requests.get(url, allow_redirects=True, verify=False, timeout=5, headers=headers)
        if 200 <= r.status_code <= 206:
            # 获取title
            r.encoding = 'UTF-8'
            content = r.text
            title = re.findall('<title>(.+)</title>', content)
            print("\033[1;32;40m[*] %s Exist! >> %s\033[0m" % (url, title))
            return True, title[0]
        else:
            print("[!] %s Not Exist!" % url)
            return False, None
    except Exception as e:
        # print(e)
        print("[!] %s Timeout!" % url)
        return False, None


def main(argv):
    file, out = '', ''
    res = []

    try:
        opts, args = getopt.getopt(argv, "hf:o:", ["help", "file=", "out="])
    except getopt.GetoptError:
        print('checkUrl.py -f <file> -o <out>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('checkUrl.py -f <file> -o <out>')
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-o", "--out"):
            out = arg

    if file == '' or out == '':
        print('checkUrl.py -f <file> -o <out>')
        sys.exit(2)

    with open(file, 'r') as fp:
        url = fp.readline().strip()
        while url:
            status = get_status(url)
            if status[0]:
                # 当前站点信息：url, title
                info = [url, status[1]]
                res.append(info)
            url = fp.readline().strip()
    if len(res) > 0:
        with open(out, 'w') as fp:
            for u in res:
                fp.write(u[0] + '\t>>\t' + u[1] + '\n')
        print("\033[1;32;40m[*] Save result in %s !\033[0m" % out)


if __name__ == "__main__":
    main(sys.argv[1:])
