from urllib import request, parse
from urllib.error import HTTPError
import re
import copy
import os
import json
import subprocess
import traceback

ROOT_URL = 'https://adventofcode.com'

TEMPLATE_HEADER = {
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Encoding': 'none',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0.1; MotoG4 Build/MPI24.107-55) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.81 Mobile Safari/537.36'
}

ENCODING_TYPE = 'utf-8'


class AOCMiscUtil:
    @staticmethod
    def get_input_file_url(year, day):
        global ROOT_URL
        return ROOT_URL + '/' + "%d/day/%d/input" % (year, day)

    @staticmethod
    def get_question_url(year, day):
        global ROOT_URL
        return ROOT_URL + '/' + "%d/day/%d" % (year, day)

    @staticmethod
    def get_answer_url(year, day):
        global ROOT_URL
        return ROOT_URL + '/' + "%d/day/%d/answer" % (year, day)

    @staticmethod
    def get_cookie(cookie_file_path):
        data = None
        if not os.path.exists(cookie_file_path):
            raise Exception("Invalid cookie-file path - %s" % cookie_file_path)
        with open(cookie_file_path, 'r') as cf:
            try:
                data = json.load(cf)
            except:
                raise Exception("Invalid json file - %s" % cookie_file_path)

        cookie = data.get('aoc-session-cookie', None) if data else None
        if cookie is None:
            raise Exception("Invalid cookie file")

        return cookie

    @staticmethod
    def get_clean_response(page):
        page = re.findall("article\>(.*)\</article", page, re.DOTALL)[0]
        page = re.sub('\<a href.*?\</a\>', "", page)
        page = page.replace('<p>', '').replace('</p>', '')
        return page


class AOCCommunicator:
    def __init__(self, usession, uname=None):
        global TEMPLATE_HEADER
        self.headers = copy.deepcopy(TEMPLATE_HEADER)
        self.headers['Cookie'] = 'session=%s' % usession
        self.network_call_count = 0
        if uname is not None:
            self.validate_session(uname.strip())

    def get_user_name(self):
        global ROOT_URL
        page = self.get_response(ROOT_URL)
        # print(page)
        match = re.search('div class="user"\>(.*?) \<', page)
        if match:
            uname = match.group(1).strip()
            return uname
        return None

    def validate_session(self, uname):
        if uname == self.get_user_name():
            return True
        else:
            raise Exception("Invalid Session")

    def get_response(self, url, post_data=None):
        global ENCODING_TYPE
        req = request.Request(url, headers=self.headers)
        try:
            if post_data:
                post_data_raw = parse.urlencode(post_data).encode()
                res = request.urlopen(req, data=post_data_raw)
            else:
                res = request.urlopen(req)
        except HTTPError as ee:
            ss = "Link: %s\n" % (url)
            ss = ss + "is post request? %r\n" % (bool(post_data))
            ss = ss + "session-cookie: %s\n" % (self.headers['Cookie'])

            print(ss)
            print(ee.read().decode())
            raise

        self.network_call_count += 1
        #print("<DBG> Network call #%d" % (self.network_call_count))
        page = res.read().decode(ENCODING_TYPE)
        return page

    def get_input_file(self, year, day, force=False):
        file_name = "input_%d_%d.txt" % (year, day)
        if (not force) and os.path.exists(file_name):
            #print("<DBG> Input file for challenge - %d/day_%d already exists. Using the data from file" % (year, day))
            page = ''
            with open(file_name, 'r') as inp_file:
                page = inp_file.read()
        else:
            page = self.get_response(AOCMiscUtil.get_input_file_url(year, day))
            with open(file_name, 'w') as inp_file:
                inp_file.write(page)
        return page

    def submit_answer(self, year, day, level, answer):
        url = AOCMiscUtil.get_answer_url(year, day)
        post_data = {
            'level': level,
            'answer': str(answer)
        }
        page = self.get_response(url, post_data=post_data)
        return AOCMiscUtil.get_clean_response(page)


class bcolors:
    BMAGENTA = '\033[95m'
    BBLUE = '\033[94m'
    BCYAN = '\033[96m'
    BGREEN = '\033[92m'
    BYELLOW = '\033[93m'
    BRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clipboard_or_input(page):
    cp = subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

    if len(cp) > 5:
        print(f'{bcolors.BYELLOW}*** USING CLIPBOARD {len(cp)} LEN ***{bcolors.ENDC}')
        return cp
    else:
        print(f'{bcolors.BGREEN}*** USING PUZZLE INPUT {len(page)} LEN ***{bcolors.ENDC}')
        return page


def aoc_submit(settings):
    if 'cookie-path' not in settings:
        settings['cookie-path'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), './aoc_cookie.json')

    # print(settings)  # can't submit? try looking at cookie-path

    session_cookie = AOCMiscUtil.get_cookie(settings['cookie-path'])
    comm = AOCCommunicator(session_cookie)
    page = comm.get_input_file(settings['year'], settings['day'])
    page = clipboard_or_input(page)

    def f(ans, l):
        session_cookie = AOCMiscUtil.get_cookie(settings['cookie-path'])
        comm = AOCCommunicator(session_cookie)

        if (ans is None) or ("y" != input(f"{bcolors.BGREEN}Submit answer - {str(ans)}  for level {l}? {bcolors.ENDC}")):
            print(f"{bcolors.BRED}Ans for level - {l} not submitted {bcolors.ENDC}")
            return

        response = comm.submit_answer(settings['year'], settings['day'], l, ans)
        print(f"{bcolors.BCYAN}Response from AOC: {response} {bcolors.ENDC}")

    return page, f
