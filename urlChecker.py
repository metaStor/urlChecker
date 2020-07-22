import requests
import sys
import getopt


file = r'url.txt'

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com/'
}


def get_status(url):
    try:
        r = requests.get(url, allow_redirects = True, timeout=5, headers=headers)
        if r.status_code == 200:
            print("[*] \033[1;31;44m%s\033[0m Exist!" % url)
            return True
        else:
            print("[!] %s Not Exist!" % url)
            return False
    except:
        print("[!] %s Not Exist!" % url)
        return False
    
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
            if status:
                res.append(url)
            url = fp.readline().strip()
    if len(res) > 0:
        with open(out, 'w') as fp:
            for u in res:
                fp.write(u + '\n')
        print("[*] \033[1;33;44mSave result in %s !\033[0m" % out)

if __name__=="__main__":
    main(sys.argv[1:])
