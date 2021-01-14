import requests
import sys
import ssl
import re
import getopt
import threading
import time
import pyfiglet

requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive'
}
# result
res = []


def initBanner():
    banners = pyfiglet.figlet_format('urlChecker')
    print(banners)
    print('\t\t\t\t\t\tPower by metaStor  v1.1\n\n')


def get_status(url, threadm):
    try:
        r = requests.get(url, allow_redirects=True, verify=False, timeout=3, headers=headers)
        if 200 <= r.status_code <= 206:
            # 获取title
            r.encoding = 'UTF-8'
            content = r.text
            title = re.findall('<title>(.+)</title>', content)
            print("\033[1;32;40m[*] %s Exist!\t>>\t[%d]\t>>\t%s\033[0m" % (url, r.status_code, title))
            # 当前站点信息：url, status_code, title
            info = [url, r.status_code, title]
            res.append(info)
        else:
            print("[!] %s Not Exist!\t>>\t[%d]" % (url, r.status_code))
    except TimeoutError as e:
        # print(e)
        print("[!] %s Timeout!" % url)
    except Exception as e:
        # print(e)
        print("[!] %s Fail!" % url)
    finally:
        threadm.release()


def main(argv):
    file, out = '', ''
    threadCount = 64
    start_time = time.time()

    try:
        opts, args = getopt.getopt(argv, "hf:o:t:", ["help", "file=", "out=", "thread"])
    except getopt.GetoptError:
        print('urlChecker.py -f <file> -o <out> -t <thread default:64>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('urlChecker.py -f <file> -o <out> -t <thread default:64>')
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-o", "--out"):
            out = arg
        elif opt in ("-t", "--thread"):
            if arg.isnumeric():
                threadCount = int(arg)
            else:
                print("-t thread should be numeric")
                sys.exit(-1)

    if file == '' or out == '':
        print('urlChecker.py -f <file> -o <out>')
        sys.exit(-1)

    # Init thread
    threads = []
    threadm = threading.BoundedSemaphore(threadCount)

    with open(file, 'r', encoding='utf-8') as fp:
        url = fp.readline().strip()
        while url:
            threadm.acquire()
            t = threading.Thread(target=get_status, args=(url, threadm))
            threads.append(t)
            t.start()
            url = fp.readline().strip()
    for t in threads:
        t.join()
    # save result
    if len(res) > 0:
        with open(out, 'w', encoding='utf-8') as fp:
            for u in res:
                fp.write(str(u[0]) + '\t>>\t[' + str(u[1]) + "]\t>>\t" + str(u[2]) + '\n')
        print("\033[1;32;40m[*] Save result in %s !\033[0m" % out)
        print("\033[1;32;40m[*] Cost time: %f !\033[0m" % (time.time() - start_time))


if __name__ == "__main__":
    initBanner()
    main(sys.argv[1:])
