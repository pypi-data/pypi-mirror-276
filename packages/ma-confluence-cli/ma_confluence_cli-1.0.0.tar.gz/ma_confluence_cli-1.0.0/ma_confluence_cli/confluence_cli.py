from __future__ import annotations
import os
import re
import io
import socket
import random
import string
import uuid
import itertools
import sys
import time

from datetime import datetime
from typing import List

import markdown
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functional import seq
from atlassian import Confluence
from dateutil import parser
from deprecated import deprecated
from loguru import logger
from bs4 import BeautifulSoup


class TableCell:
    def __init__(self, html: str = "", type: str = 'str') -> None:
        self.html = html
        self.type = type
        self.file = []


class Table:
    '''
    cell content: str, or the path to the file
    cell type   : can be
        "str"
        "image" : upload a image, show as image
        "file"  : upload a file, show as thumbnail
        "link"  : upload a file, show as a link
    '''

    def __init__(self, height: int, width: int, default_content=None, default_type=None, header: bool = True) -> None:
        self.height = height
        self.width = width
        self.header: bool = header
        self.data = np.array([TableCell() for _ in range(
            height * width)]).reshape((height, width))
        self.acceptable_type = ['str', 'image', 'file', 'link']
        if default_content or default_type:
            for i in range(height):
                for j in range(width):
                    self.set(i, j, default_content, default_type)

    def _cell(self, x, y) -> TableCell:
        assert x < self.height and y < self.width, f"{x},{y} is out of range of the table {self.height}x{self.width}"
        return self.data[x][y]

    def __repr__(self) -> str:
        return self.to_html()

    def __str__(self) -> str:
        return self.__repr__()

    def set_row(self, row, content_list, type_list, args_list=None):
        args_list = args_list or [{} for _ in range(self.width)]
        for _col, _content, _type, _args in zip(range(self.width), content_list, type_list, args_list):
            self.set(row, _col, _content, _type, **_args)

    def set_col(self, col, content_list, type_list, args_list=None):
        args_list = args_list or [{} for _ in range(self.height)]
        for _row, _content, _type, _args in zip(range(self.height), content_list, type_list, args_list):
            self.set(_row, col, _content, _type, **_args)

    def set(self, x, y, content, type='str', **kwargs) -> None:
        assert type in self.acceptable_type, f"type {type} not acceptable! Acceptale types: {self.acceptable_type}"
        cell = self._cell(x, y)
        cell.type = type
        if type == 'str':
            cell.html = str(content)
            cell.file.clear()
        elif type == 'image':
            cell.html = ConfluenceCli._generate_image_html(
                image_name=os.path.basename(content), height=kwargs.get('height'), width=kwargs.get('width')
            )
            cell.file.append(content)
        elif type == 'file':
            cell.html = ConfluenceCli._generate_file_html(
                file_name=os.path.basename(content), as_link=False)
            cell.file.append(content)
        elif type == 'link':
            cell.html = ConfluenceCli._generate_file_html(
                file_name=os.path.basename(content), as_link=True)
            cell.file.append(content)
        else:
            cell.html = str(content)
            cell.file.clear()

    def set_str(self, x, y, content: str):
        cell = self._cell(x, y)
        cell.html = str(content)
        cell.file.clear()

    def set_image(self, x, y, file_name: str, height=None, width=None):
        cell = self._cell(x, y)
        cell.html = ConfluenceCli._generate_image_html(
            image_name=os.path.basename(file_name), height=height, width=width
        )
        cell.file.append(file_name)

    def set_file(self, x, y, file_name: str, as_link=True):
        cell = self._cell(x, y)
        cell.html = ConfluenceCli._generate_file_html(
            file_name=os.path.basename(file_name), as_link=as_link)
        cell.file.append(file_name)

    def get(self, x, y):
        return self._get_html(x, y)

    def _get_html(self, x, y) -> str:
        return self._cell(x, y).html

    def _get_file(self, x, y) -> List[str]:
        return self._cell(x, y).file

    def _get_all_files(self) -> List[str]:
        return seq(self.data.tolist()).flatten().map(lambda cell: cell.file).flatten().to_list()

    def to_html(self) -> str:
        '''
        <table>
        <tbody>
            <tr>
                <th>
                    <ac:link><ri:attachment ri:filename="report_no_price_test_WEEK.pdf" /></ac:link>
                </th>
                <th>
                    Table Heading Cell 2
                </th>
            </tr>
            <tr>
                <td><ac:link><ri:attachment ri:filename="report_no_price_test_WEEK.pdf" /></ac:link></td>
                <td><ac:image ac:height="250"><ri:attachment ri:filename="test.png" /></ac:image></td>
            </tr>
        </tbody>
        </table>
        '''
        ret_html = '<p><table border="1" class="dataframe">\n<tbody>\n'
        for row_num, row in enumerate(self.data):
            if row_num == 0 and self.header:
                row_html = seq(row).map(
                    lambda cell: f'<th>{cell.html}</th>').reduce(lambda x, y: f'{x}\n{y}')
            else:
                row_html = seq(row).map(
                    lambda cell: f'<td>{cell.html}</td>').reduce(lambda x, y: f'{x}\n{y}')
            ret_html += f'<tr>\n{row_html}\n</tr>\n'
        ret_html += '</tbody>\n</table></p>'
        return ret_html

    def to_mail_html(self):
        '''
        Issue here: Image html cannot shown in table.
        '''
        return self.to_html()

    @classmethod
    def encode(cls, html) -> Table:

        def _clean_wrapper(html) -> str:
            html = str(html).strip()
            if html.startswith('<td>') and html.endswith('</td>'):
                html = html[len('<td>'):-len('</td>')]
            if html.startswith('<th>') and html.endswith('</th>'):
                html = html[len('<th>'):-len('</th>')]
            return html

        soup = BeautifulSoup(str(html), features='lxml')
        header = len(soup.find_all('th')) > 0
        rows: List[str] = soup.find_all('tr')
        height = len(rows)
        if not height:
            return None
        width = max(len(rows[0].find_all('th')), len(rows[0].find_all('td')))
        table = Table(height=height, width=width,
                      default_type='str', header=header)
        for row_num, row in enumerate(rows):
            if row_num == 0 and header:
                table.set_row(
                    row_num,
                    content_list=[_clean_wrapper(html)
                                  for html in row.find_all('th')],
                    type_list=itertools.repeat('str')
                )
            else:
                table.set_row(
                    row_num,
                    content_list=[_clean_wrapper(html)
                                  for html in row.find_all('td')],
                    type_list=itertools.repeat('str')
                )
        return table

    @classmethod
    def encode_all(cls, html) -> List[Table]:
        soup = BeautifulSoup(html, features='lxml')
        return [cls.encode(table) for table in soup.find_all('table')]


class ConfluenceCli:
    _mother_type_map = {
        'image': ['bmp', 'dcm', 'gif', 'heif', 'heic', 'jpg', 'jpeg', 'png', 'psd', 'tif', 'tiff'],
        'audio': ['aac', 'ac3', 'aif', 'aiff', 'ape', 'au', 'flac', 'm4a', 'mid', 'miki', 'mod', 'mka', 'mp3', 'ogg', 'spx', 'rm', 'wav', 'wma'],
        'application': ['zip', 'rar', 'ai', 'csv', 'diff', 'docx', 'doc', 'dot', 'docm', 'dotx', 'dotm', 'odg', 'otg', 'odp', 'otp', 'ods', 'ots', 'odt', 'ott', 'odm', 'sxw', 'stw', 'sxc', 'stc', 'sxi', 'sti', 'sxd', 'std', 'pdf', 'perl', 'ppt', 'pptx', 'pot', 'pps', 'pptm', 'potx', 'potm', 'ppsx', 'ppsm', 'eps', 'ps', 'rb', 'rtf', 'txt', 'wpd', 'xls', 'xlt', 'xla', 'xlsx']
    }
    _type_map = {
        'msword': ['doc', 'dot', 'docm', 'dotx', 'dotm'],
        'vnd.openxmlformats-officedocument.presentationml.presentation': ['ppt', 'pptx', 'pot', 'pps', 'pptm', 'potx', 'potm', 'ppsx', 'ppsm'],
        'vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['xls', 'xlt', 'xla', 'xlsx', 'csv'],
        'octet-stream': ['rar'],
    }
    _default_commend = f'Page is updated via Cli by {os.getenv("USER")}@{socket.gethostname()}\nCommand: ' + ' '.join(
        sys.argv
    )

    def __init__(self, oauth_token: str = None) -> None:
        self.page_id = None
        self._oauth_token = oauth_token or os.getenv('CONFLUENCE_OAUTH')
        if not self._oauth_token:
            logger.error(
                "[Error] Confluence oauth token(CONFLUENCE_OAUTH) is not yet set! "
                "For detail, see http://portal.dfc.sh/x/zpdtAQ"
            )
        else:
            print(
                f'(confluence_cli) your confluence oauth token is {self._oauth_token[:4]}....{self._oauth_token[-4:]}'
            )
        self.confluence = Confluence(
            url='http://portal.dfc.sh/', token=self._oauth_token)
        self.body = []
        self._spaces = None
        self.check_access()
        pass

    # def _init_with_username_password(self, username, password) -> None:
    #     '''
    #     Don't use it if you've already passed oauth token during init.
    #     '''
    #     self.confluence = self.confluence(
    #         url='http://portal.dfc.sh/',
    #         username=username,
    #         password=password
    #     )
    #     pass

    @property
    def spaces(self):
        if self._spaces is None:
            self._spaces = self.confluence.get_all_spaces().get('results', [])
            assert self._spaces, '(Confluence_cli) No spaces found, there should be an issue.'
        return self._spaces

    def set_page_id(self, page_id):
        self.page_id = str(page_id)

    def _check_page_id(self, page_id):
        page_id = page_id or self.page_id
        assert page_id, "you have to provide a page_id!"
        return page_id

    def _get_page_metadata_by_id(self, page_id=None):
        page_id = self._check_page_id(page_id)
        return self.confluence.get_page_by_id(str(page_id))

    def _get_title_by_id(self, page_id=None):
        page_id = self._check_page_id(page_id)
        return self.confluence.get_page_by_id(page_id)['title']

    def _get_page_space(self, page_id=None):
        page_id = self._check_page_id(page_id)
        return self.confluence.get_page_space(page_id)

    def _get_child_title_list(self, page_id=None):
        page_id = self._check_page_id(page_id)
        return self.confluence.get_child_title_list(page_id)

    def _get_child_id_list(self, page_id=None):
        page_id = self._check_page_id(page_id)
        return self.confluence.get_child_id_list(page_id)

    def _get_child_pages(self, page_id=None):
        page_id = self._check_page_id(page_id)
        return [(page['id'], page['title']) for page in self.confluence.get_page_child_by_type(page_id, limit=2000)]

    def get_parent_page_id(self, page_id=None):
        page_id = self._check_page_id(page_id)
        return self.confluence.get_parent_content_id(page_id)

    def check_access(self, _id_or_name='') -> bool:
        if not self._oauth_token:
            print('(confluence_cli) oauth key has not been set!')
            return False
        if _id_or_name:
            if str(_id_or_name).isdigit():
                try:
                    self.get_page_content(_id_or_name)
                except Exception:
                    print(
                        f'(confluence_cli) page not exist or you have no permission to it: {_id_or_name}')
                    return False
                print(f'(confluence_cli) You have permission to {_id_or_name}')
                return True
            else:
                for space in self.spaces:
                    if space.get('key',
                                 '').lower() == _id_or_name.lower() or space.get('name',
                                                                                 '').lower() == _id_or_name.lower():
                        try:
                            self.confluence.get_space(space.get('key'))
                        except Exception:
                            print(
                                '✘ (Confluence_cli) you dont have access to the space'
                                f'{space.get("name")}({space.get("key")})'
                            )
                            return False
                        print(
                            f'✓ (Confluence_cli) you have access to space {space.get("name")}({space.get("key")})')
                        return True
                print(
                    f'✘ (Confluence_cli) cannot find a space key or name like {_id_or_name}')
                return False
        else:
            spaces_to_check_name_key_map = {
                'BASECAMP': 'BAS',
                'Base1': 'BAS1',
                'CAMP2': 'CAMP2',
                'CAMP2_REPORT': 'C2R',
                'HFSTAT_INTERN': 'WOR'
            }
            for name, key in spaces_to_check_name_key_map.items():
                self.check_access(key)
        ...

    def _insert_to_existing_page(self, page_id, insert_body, top_of_page=False, comment=None):
        self.confluence._insert_to_existing_page(
            page_id=page_id, title=self._get_title_by_id(page_id), insert_body=insert_body, top_of_page=top_of_page,
            version_comment=comment or self._default_commend
        )

    def _append_random_suffix(self, name):
        filename, file_extension = os.path.splitext(name)
        new_name = filename + '_' + self._timestamp_generator() + file_extension
        return new_name

    def _attach_content(self, page_id, content, name, content_type=None):
        self.confluence.attach_content(
            content=content, name=name, content_type=content_type or self._determine_file_type(name), page_id=page_id)

    def _update_page(self, page_id, body, comment=None):
        self.confluence.update_page(page_id=page_id, title=self.get_title(
            page_id), body=body, version_comment=comment or self._default_commend)

    def create_page_under_page(self, parent_page_id, title, body=''):
        space_key = self._get_page_space(parent_page_id)
        response = self.confluence.create_page(
            space=space_key, title=title, body=body, parent_id=str(parent_page_id))
        return response.get('id', None)

    def _get_page_by_title_under_page(self, parent_page_id, title: str):
        for page_id, page_title in self._get_child_pages(parent_page_id):
            if title.strip() == page_title:
                return page_id
        return None

    def create_or_get_page_by_title_under_page(self, parent_page_id, title: str, body=''):
        for _try in range(5):
            if (_page_id := self._get_page_by_title_under_page(parent_page_id, title)):
                return _page_id
            try:
                created_page_id = self.create_page_under_page(
                    parent_page_id, title, body=body)
                return created_page_id
            except Exception as e:
                print(
                    f"(create_or_get_page_by_title_under_page)"
                    f"Create page \"{title}\" under id {parent_page_id} failed, retry ({_try}).\n"
                    f"msg: {e}"
                )
                time.sleep(1)
        raise Exception(
            f"(create_or_get_page_by_title_under_page)"
            f"Tried 5 times, still cannot get or create page \"{title}\" under id {parent_page_id}"
        )

    def create_pages_under_page_using_title_timestamp_prefix(self, parent_page_id, title, body='', structure="%Y #{suffix}/%Y-%m #{suffix}/%Y-%m-%d {title_without_timestamp} #{suffix}", suffix=None, appendant_args={}) -> List:
        '''
        Title should be start with a timestamp format, e.g.: 20220117 MP_backtest;
        A tree structure will be created (or find out if exist) under the parent_page_id, by structure which is split by '/';

        You can use the following mapping in the structure:
            %Y %m %d ...
            {title} {title_without_timestamp} {timestamp} {suffix} {parent_page_title}

        By default, structure is:
            %Y #{suffix}/%Y-%m #{suffix}/%Y-%m-%d {title_without_timestamp} #{suffix}
        which means a tree structure like the following will be created:
            parent_page_name
                |--- 2022 #parent_page_name
                       |------- 2022-01 #parent_page_name
                                   └──────── 2022-01-17 MP_backtest #parent_page_name

        If suffix is not provided, the title of the parent_page_id will be used as the suffix;
        Return a list of page ids.
        '''
        if not re.findall('^\d+', title):
            print(f'Cannot find any time prefix in title {title}, do nothing.')
            return
        timestamp_str = re.findall('^\d+', title)[0]
        try:
            timestamp = parser.parse(timestamp_str)
        except Exception as e:
            print(
                f'Cannot parse timestamp {timestamp_str} (type:{type(timestamp_str)}), do nothing.\n{e}')
            return
        suffix = suffix or self.get_title(parent_page_id)
        _args_dict = {
            'title': title,
            'title_without_timestamp': title[len(timestamp_str):].strip(),
            'suffix': suffix,
            'parent_page_title': self.get_title(parent_page_id),
            'timestamp': timestamp_str,
            'year': timestamp.strftime('%Y'),
            'month': timestamp.strftime('%m'),
            'day': timestamp.strftime('%d'),
        }
        _args_dict.update(appendant_args)
        page_tree = seq(structure.split('/'))\
            .map(lambda s: s.strip())\
            .map(lambda folder_name:  timestamp.strftime(folder_name))\
            .map(lambda folder_name:  folder_name.format_map(_args_dict))\
            .to_list()
        previous_page_id = parent_page_id
        tree_ids = []
        for page_name in page_tree:
            previous_page_id = self.create_or_get_page_by_title_under_page(
                previous_page_id, page_name)
            tree_ids.append(previous_page_id)
        return tree_ids

    # parent_page_id: root page id of auto reports, by default is 26693126
    def create_auto_report_page(self, topic_name: str, date: str, parent_page_id=26693126):
        page_id = self.create_or_get_page_by_title_under_page(
            parent_page_id, topic_name)
        page_id_list = self.create_pages_under_page_using_title_timestamp_prefix(
            parent_page_id=page_id, title=date)
        return page_id_list[-1]

    def get_page_content(self, page_id=None):
        page_id = self._check_page_id(page_id)
        previous_body = (
            (self.confluence.get_page_by_id(page_id, expand="body.storage").get(
                "body") or {}).get("storage").get("value")
        )
        previous_body = previous_body.replace("&oacute;", u"ó")
        return previous_body

    def get_shareable_link(self, page_id=None, shortlink=True):
        page_id = self._check_page_id(page_id)
        long_link_template = 'http://portal.dfc.sh/pages/viewpage.action?pageId=${page_id}'
        short_link_template = 'http://portal.dfc.sh/${tinyui}'
        if shortlink:
            tinyui = self.confluence.get_page_by_id(
                page_id).get('_links', {}).get('tinyui', '')
            if tinyui:
                return string.Template(short_link_template).safe_substitute(tinyui=tinyui.strip('/'))
            else:
                print('[Warning] (confluence_cli) Cannot get page short link.')
        return string.Template(long_link_template).safe_substitute(page_id=page_id)

    @deprecated
    def insert_table_of_content(self, page_id=None, top_of_page=True):
        page_id = self._check_page_id(page_id)
        body = f'<p><ac:structured-macro ac:name="toc" ac:schema-version="1" ac:macro-id="{self._macro_id_generator()}" /></p>'
        self._insert_to_existing_page(
            page_id=page_id, insert_body=body, top_of_page=top_of_page)

    def insert_catalogue(self, page_id=None, floating=False, top_of_page=True):
        page_id = self._check_page_id(page_id)
        name = 'float_toc' if floating else 'toc'
        body = f'<p><ac:structured-macro ac:name="{name}" ac:schema-version="1" ac:macro-id="{self._macro_id_generator()}" /></p>'
        self._insert_to_existing_page(
            page_id=page_id, insert_body=body, top_of_page=top_of_page)

    def insert_markdown(self, markdown_text, page_id=None, top_of_page=False):
        page_id = self._check_page_id(page_id)
        body = self._markdown_preprocess(markdown_text)
        self._insert_to_existing_page(
            page_id=page_id, insert_body=body, top_of_page=top_of_page)

    def insert_raw_text(self, text, page_id=None, top_of_page=False):
        page_id = self._check_page_id(page_id)
        body = text
        self._insert_to_existing_page(
            page_id=page_id, insert_body=body, top_of_page=top_of_page)

    def insert_heading(self, text, level, page_id=None, top_of_page=False):
        page_id = self._check_page_id(page_id)
        body = f'<h{level}>{text}</h{level}>'
        if level not in range(1, 7):
            print('[Warning] heading level should be 1-6')
            body = text
        self.insert_raw_text(text=body, page_id=page_id,
                             top_of_page=top_of_page)

    def _create_include_page_html(self, include_page_id=None, include_page_title=None):
        assert include_page_id or include_page_title, "You have to specific page_id or title of the page you want to included!"
        include_page_title = include_page_title or self.get_title(
            include_page_id)
        body = '<p>'\
            f'<ac:structured-macro ac:name="include" ac:schema-version="1" ac:macro-id="{self._macro_id_generator()}">'\
            '<ac:parameter ac:name="">'\
            f'<ac:link><ri:page ri:content-title="{include_page_title}" /></ac:link>'\
            '</ac:parameter>'\
            '</ac:structured-macro></p>'
        return body

    def insert_include_page(self, include_page_id=None, include_page_title=None, page_id=None, top_of_page=False):
        assert include_page_id or include_page_title, \
            "You have to specific page_id or title of the page you want to included!"
        include_page_title = include_page_title or self.get_title(
            include_page_id)
        body = self._create_include_page_html(
            include_page_id=include_page_id, include_page_title=include_page_title)
        self.insert_raw_text(text=body, page_id=page_id,
                             top_of_page=top_of_page)

    def replace_include_page(self, from_title, to_title, page_id=None):

        def _title_to_replace_key(title):
            return f'content-title="{title}"'
        page_id = self._check_page_id(page_id)
        prev = self.get_page_content(page_id)
        aft = prev.replace(_title_to_replace_key(from_title),
                           _title_to_replace_key(to_title))
        self._update_page(page_id, body=aft)

    @classmethod
    def create_code_block_html(cls, code, language=None) -> str:
        '''
        Supported language are in the following supported_language_map
        '''
        supported_language_map = {
            "actionscript3": "ActionScript",
            "applescript": "AppleScript",
            "bash": "Bash",
            "c#": "C#",
            "cpp": "C++",
            "css": "CSS",
            "coldfusion": "ColdFusion",
            "delphi": "Delphi",
            "diff": "Diff",
            "erl": "Erlang",
            "groovy": "Groovy",
            "xml": "HTML and XML",
            "java": "Java",
            "jfx": "Java FX",
            "js": "JavaScript",
            "php": "PHP",
            "perl": "Perl",
            "text": "Plain Text",
            "powershell": "PowerShell",
            "py": "Python",
            "ruby": "Ruby",
            "sql": "SQL",
            "sass": "Sass",
            "scala": "Scala",
            "vb": "Visual Basic",
            "yml": "YAML"
        }
        reversed_language_map = seq(supported_language_map.items()).smap(
            lambda key, v: (v, key)).to_dict()
        language_marker = ''
        if language in reversed_language_map:
            language = reversed_language_map[language]
        if language in supported_language_map:
            language_marker = f'<ac:parameter ac:name="language">{language}</ac:parameter>'
        elif language:
            print(f'[Warning] Not supported language type: {language}.')
        body = f'<ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="{cls._macro_id_generator()}">'\
            f'{language_marker}<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body></ac:structured-macro>'
        return body

    def insert_code_block(self, text, language=None, page_id=None, top_of_page=False):
        '''
        Supported language are in the following supported_language_map
        '''
        page_id = self._check_page_id(page_id)
        body = self.create_code_block_html(code=text, language=language)
        self.insert_raw_text(text=body, page_id=page_id,
                             top_of_page=top_of_page)

    def insert_expand_macro(self, text, page_id=None, top_of_page=False, parse_newline=True):
        if parse_newline:
            text = ''.join([f'<p>{i}</p>' for i in text.strip().split('\n')])
        body = \
            f'<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="{self._macro_id_generator()}">'\
            f'<ac:rich-text-body>{text}</ac:rich-text-body>'\
            '</ac:structured-macro>'
        self.insert_raw_text(text=body, page_id=page_id,
                             top_of_page=top_of_page)

    def insert_paragraph(self, text, page_id=None, top_of_page=False):
        page_id = self._check_page_id(page_id)
        body = ''.join([f'<p>{i}</p>' for i in text.strip().split('\n')])
        self._insert_to_existing_page(
            page_id=page_id, insert_body=body, top_of_page=top_of_page)

    def insert_image(self, image, height=None, width=None, page_id=None, top_of_page=False):
        '''
        Support .jpg and .png file
        '''
        page_id = self._check_page_id(page_id)
        if isinstance(image, str):
            base_name = os.path.basename(image)
            with open(image, 'rb') as fin:
                self._attach_content(
                    page_id=page_id, content=fin.read(), name=base_name)
        elif isinstance(image, io.BytesIO):
            base_name = self._id_generator()+'.jpg'
            image.seek(0)
            self._attach_content(
                page_id=page_id, content=image.read(), name=base_name)
        elif isinstance(image, matplotlib.figure.Figure):
            image_byte = self.save_plot_to_buff(image)
            self.insert_image(image_byte, height=height, width=width,
                              page_id=page_id, top_of_page=top_of_page)
            # base_name = self._id_generator()+'.jpg'
            # image_byte.seek(0)
            # self._attach_content(page_id=page_id, content=image_byte.read(), name=base_name)
        else:
            raise Exception("Not supported type.")
        body = self._generate_image_html(base_name, height, width)
        self._insert_to_existing_page(
            page_id=page_id, insert_body=body, top_of_page=top_of_page)

    def insert_check_box_list(self, page_id, task_list, status=False, top_of_page=False):
        page_id = self._check_page_id(page_id)
        next_checkbox_id = seq(self.extract_all_inline_tasks_checkbox_inside_page(
            page_id)).smap(lambda task_id, status, name: task_id).map(int).max() + 1
        if isinstance(status, list):
            assert len(task_list) == len(
                status), f"status should have the same length as task_list! current task_list({len(task_list)}): {task_list}, status({len(status)}): {status}"
            status = ['complete' if sta else 'incomplete' for sta in status]
        else:
            status = ['complete' if status else 'incomplete']*len(task_list)
        html = '<ac:task-list>'
        for task_name, task_id, status in zip(task_list, range(next_checkbox_id, next_checkbox_id+len(task_list)), status):
            html += f'''
            <ac:task>
            <ac:task-id>{task_id}</ac:task-id>
            <ac:task-status>{status}</ac:task-status>
            <ac:task-body><span class="placeholder-inline-tasks">{task_name}</span></ac:task-body>
            </ac:task>
            '''
        html += '\n</ac:task-list>'
        self.insert_raw_text(html, page_id=page_id, top_of_page=top_of_page)

    def set_inline_tasks_checkbox(self, page_id, task_id, status: bool):
        page_id = self._check_page_id(page_id)
        self.confluence.set_inline_tasks_checkbox(
            page_id=page_id, task_id=task_id, status='CHECKED' if status else 'UNCHECKED')

    def set_inline_tasks_checkbox_by_task_name(self, page_id, task_name, status: bool):
        page_id = self._check_page_id(page_id)
        inline_tasks = self.extract_all_inline_tasks_checkbox_inside_page(
            page_id)
        for task_id, task_status, task_html_name in inline_tasks:
            if task_name in task_html_name:
                self.set_inline_tasks_checkbox(page_id, task_id, status)
        ...

    def extract_all_inline_tasks_checkbox_inside_page(self, page_id=None):
        '''
        <ac:task-list>
        <ac:task>
        <ac:task-id>1</ac:task-id>
        <ac:task-status>incomplete</ac:task-status>
        <ac:task-body><span class="placeholder-inline-tasks">hi</span></ac:task-body>
        </ac:task>
        <ac:task>
        <ac:task-id>2</ac:task-id>
        <ac:task-status>incomplete</ac:task-status>
        <ac:task-body><span class="placeholder-inline-tasks">abc</span></ac:task-body>
        </ac:task>
        '''
        page_id = self._check_page_id(page_id)
        content = self.get_page_content(page_id)
        return re.findall(r'task-id>(\d+?)<.+?task-status>(\w+?)<.+?task-body>(.+?)</ac:task-body>', content.replace('\n', ''))

    @classmethod
    def _generate_html(cls, file_path):
        mother_type = cls._get_according_mother_type(file_path)
        if mother_type == 'image':
            return cls._generate_image_html(file_path)
        else:
            return cls._generate_file_html(file_path)

    @staticmethod
    def _generate_image_html(image_name, height=None, width=None):
        height_tag = f' ac:height=\"{height}\"' if height else ''
        width_tag = f' ac:width=\"{width}\"' if width else ''
        return f'<p><ac:image{height_tag}{width_tag}><ri:attachment ri:filename=\"{image_name}\" /></ac:image></p>'

    @staticmethod
    def _generate_file_html(file_name, as_link=True):
        if as_link:
            return f'<p><ac:link><ri:attachment ri:filename="{file_name}" /></ac:link></p>'
        else:
            # MACRO_UUID = ret['container']['_links']['edit'].rpartition('=')[-1]
            MACRO_UUID = ConfluenceCli._macro_id_generator()
            return f'<p><ac:structured-macro ac:name="view-file" ac:schema-version="1" ac:macro-id="{MACRO_UUID}"><ac:parameter ac:name="name"><ri:attachment ri:filename="{file_name}" /></ac:parameter><ac:parameter ac:name="height">250</ac:parameter></ac:structured-macro></p>'

    def insert_file(self, file, page_id=None, top_of_page=False, as_link=True):
        page_id = self._check_page_id(page_id)
        if not os.path.isfile(file):
            print(f"File {file} not exist!")
            return
        base_name = os.path.basename(file)
        with open(file, 'rb') as fin:
            self._attach_content(
                page_id=page_id, content=fin.read(), name=base_name)
        body = self._generate_file_html(base_name, as_link=as_link)
        self._insert_to_existing_page(
            page_id=page_id, insert_body=body, top_of_page=top_of_page)

    @staticmethod
    def generate_template_table(height, width, default_content=None, default_type=None, header=True) -> Table:
        return Table(height, width, default_content, default_type, header)

    def insert_table(self, table: Table, page_id=None, top_of_page=False):
        page_id = self._check_page_id(page_id)
        # insert table files
        for file_path in table._get_all_files():
            with open(file_path, 'rb') as fin:
                base_name = os.path.basename(file_path)
                self._attach_content(
                    page_id=page_id, content=fin.read(), name=base_name)

        # insert table html
        body = table.to_html()
        self._insert_to_existing_page(
            page_id=page_id, insert_body=body, top_of_page=top_of_page)

    def insert_comment(self, text, page_id=None):
        page_id = self._check_page_id(page_id)
        text = ''.join([f'<p>{i}</p>' for i in text.strip().split('\n')])
        self.confluence.add_comment(page_id=page_id, text=text)

    def clear_page(self, page_id=None, delete_attachments=True):
        page_id = self._check_page_id(page_id)
        self._update_page(page_id=page_id, body="")
        if not delete_attachments:
            return
        seq(self.confluence.get_attachments_from_content(page_id).get('results', []))\
            .filter(lambda file_info_dct: file_info_dct and 'title' in file_info_dct)\
            .map(lambda file_info_dct: file_info_dct.get('title', None))\
            .filter(lambda file_title: file_title)\
            .for_each(lambda file_title: self.confluence.delete_attachment(page_id, file_title))

    def get_title(self, page_id=None):
        page_id = self._check_page_id(page_id)
        return self._get_title_by_id(page_id)

    @classmethod
    def _get_according_mother_type(cls, type: str, default=None):
        type = type.rpartition('.')[-1] if '.' in type else type
        for mother_type, type_list in cls._mother_type_map.items():
            if type in type_list:
                return mother_type
        return default

    @classmethod
    def _get_according_type(cls, type):
        type = type.rpartition('.')[-1] if '.' in type else type
        for _type, type_list in cls._type_map.items():
            if type in type_list:
                return _type
        return type

    @classmethod
    def _determine_file_type(cls, filename):
        extension = os.path.splitext(filename)[-1].lower().strip('.')
        return f'{cls._get_according_mother_type(extension)}/{cls._get_according_type(extension)}'

    @staticmethod
    def _id_generator(size=10, suffix='', chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size)) + suffix

    @staticmethod
    def _macro_id_generator():
        return str(uuid.uuid4())

    @staticmethod
    def _timestamp_generator():
        return datetime.now().strftime('%Y%m%d%H%M%S%f')

    @staticmethod
    def _read_content(path):
        with open(path, 'rb') as fin:
            content = fin.read()
        return content

    @staticmethod
    def save_plot_to_buff(plt, **kw):
        buff = io.BytesIO()
        plt.savefig(buff, format='png', **kw)
        buff.seek(0)
        return buff

    @staticmethod
    def _markdown_preprocess(markdown_text):
        md = markdown.Markdown()
        return md.convert(markdown_text)

    def _pack_content(self, type, **kwargs):
        kwargs = kwargs or {}
        kwargs['type'] = type
        self.body.append(kwargs)

    def add_raw_text(self, text):
        self._pack_content('text', text=text)

    def add_html(self, text):
        self._pack_content('text', text=text)

    def add_href(self, url, text=None):
        text = text or url
        self._pack_content(
            'text', text=f'<p><span class="placeholder-inline-tasks"><a href="{url}">{text}</a></span></p>')

    def add_heading(self, text, level):
        body = f'<h{level}>{text}</h{level}>'
        if level not in range(1, 7):
            print('[Warning] heading level should be 1-6')
            body = text
        self.add_html(body)

    def add_include_page(self, include_page_id=None, include_page_title=None):
        assert include_page_id or include_page_title, "You have to specific page_id or title of the page you want to included!"
        include_page_title = include_page_title or self.get_title(
            include_page_id)
        body = self._create_include_page_html(
            include_page_id=include_page_id, include_page_title=include_page_title)
        self.add_html(body)

    def add_code_block(self, text, language=None):
        body = self.create_code_block_html(code=text, language=language)
        self.add_html(body)

    def add_expand_macro(self, text, parse_newline=True):
        if parse_newline:
            text = ''.join([f'<p>{i}</p>' for i in text.strip().split('\n')])
        body = \
            f'<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="{self._macro_id_generator()}">'\
            f'<ac:rich-text-body>{text}</ac:rich-text-body>'\
            '</ac:structured-macro>'
        self.add_html(body)

    def add_markdown(self, markdown_text):
        self._pack_content(
            'text', text=self._markdown_preprocess(markdown_text))

    def add_general_image(self, image, height=None, width=None, name='', **kwargs):
        if isinstance(image, str):
            self.add_picture_file(path=image, height=height,
                                  width=width, rename=name)
        elif isinstance(image, io.BytesIO):
            self.add_byte_graph(byte=image, height=height,
                                width=width, name=name)
        elif isinstance(image, matplotlib.figure.Figure):
            self.add_plot(plt=image, height=height,
                          width=width, name=name, **kwargs)
        else:
            raise Exception("Not supported type.")
        ...

    def add_byte_graph(self, byte, height=None, width=None, name=''):
        name = name or self._id_generator(10, suffix='.png')
        if not name.lower().endswith('.png'):
            name += '.png'
        self._pack_content('byte_graph', content=byte,
                           name=name, height=height, width=width)

    def add_plot(self, plt, height=None, width=None, name='', **kw):
        byte = self.save_plot_to_buff(plt, **kw).read()
        self.add_byte_graph(byte=byte, height=height, width=width, name=name)

    def add_picture_file(self, path, height=None, width=None, rename=None):
        rename = rename or os.path.basename(path)
        if not rename.lower().endswith(os.path.splitext(os.path.basename(path))[-1].lower()):
            rename += os.path.splitext(os.path.basename(path))[-1].lower()
        byte = self._read_content(path)
        self._pack_content(
            'byte_graph',
            content=byte,
            name=rename,
            height=height,
            width=width,
        )

    def add_attachment(self, path, aslink=False, rename=None):
        rename = rename or os.path.basename(path)
        byte = self._read_content(path)
        self._pack_content('attachment', content=byte,
                           name=rename, aslink=aslink)

    def add_table(self, table: Table):
        file_content_list, file_name_list = [], []
        for file_path in table._get_all_files():
            file_content_list.append(self._read_content(file_path))
            file_name_list.append(file_path)
        self._pack_content('table', table=table,
                           files=file_content_list, file_names=file_name_list)

    def add_check_box_list(self, page_id, task_list, status=False, top_of_page=False):
        page_id = self._check_page_id(page_id)
        next_checkbox_id = seq(self.extract_all_inline_tasks_checkbox_inside_page(
            page_id)).smap(lambda task_id, status, name: task_id).map(int).max() + 1
        if isinstance(status, list):
            assert len(task_list) == len(
                status), f"status should have the same length as task_list! current task_list({len(task_list)}): {task_list}, status({len(status)}): {status}"
            status = ['complete' if sta else 'incomplete' for sta in status]
        else:
            status = ['complete' if status else 'incomplete']*len(task_list)
        html = '<p><ac:task-list>'
        for task_name, task_id, status in zip(task_list, range(next_checkbox_id, next_checkbox_id+len(task_list)), status):
            html += f'''
            <ac:task>
            <ac:task-id>{task_id}</ac:task-id>
            <ac:task-status>{status}</ac:task-status>
            <ac:task-body><span class="placeholder-inline-tasks">{task_name}</span></ac:task-body>
            </ac:task>
            '''
        html += '\n</ac:task-list></p>'
        self._pack_content('text', text=html, top_of_page=top_of_page)

    def add_catalogue(self, floating=False, top_of_page=True):
        self._pack_content('catalogue', floating=floating,
                           top_of_page=top_of_page)

    def update_page(self, page_id, append=False, top_of_page=False, drop_contents_after_update=False, comment=None):
        page_id = self._check_page_id(page_id)
        origin_content = self.get_page_content(page_id) if append else ''
        append_content = ''
        top_most_content = ''
        for item in self.body:
            type = item.get('type', None)
            if type == 'text':
                append_content += f"<p>{item.get('text','')}</p>"
            elif type == 'byte_graph':
                content = item.get('content')
                name = item.get('name')
                height = item.get('height')
                width = item.get('width')
                name = self._append_random_suffix(name)
                self._attach_content(
                    page_id=page_id, content=content, name=name)
                body = self._generate_image_html(
                    name, height=height, width=width)
                append_content += body
            elif type == 'attachment':
                content = item.get('content')
                name = item.get('name')
                aslink = item.get('aslink')
                self._attach_content(
                    page_id=page_id, content=content, name=name)
                body = self._generate_file_html(name, as_link=aslink)
                append_content += body
            elif type == 'table':
                table = item.get('table')
                files = item.get('files')
                file_names = item.get('file_names')
                for content, name in zip(files, file_names):
                    self._attach_content(
                        page_id=page_id, content=content, name=name)
                body = table.to_html()
                append_content += body
            elif type == 'catalogue':
                floating = item.get('floating', False)
                name = 'float_toc' if floating else 'toc'
                body = f'<p><ac:structured-macro ac:name="{name}" ac:schema-version="1" ac:macro-id="{self._macro_id_generator()}" /></p>'
                if item.get('top_of_page', True):
                    top_most_content = body + top_most_content
                else:
                    append_content += body
            else:
                raise Exception(f'unsupported type: {type}!')
        if append:
            self._insert_to_existing_page(
                page_id=page_id, insert_body=append_content, top_of_page=top_of_page, comment=comment
            )
        else:
            self._update_page(
                page_id=page_id, body=append_content, comment=comment)

        if top_most_content:
            self._insert_to_existing_page(
                page_id=page_id, insert_body=top_most_content, top_of_page=True, comment=comment
            )
        if drop_contents_after_update:
            self.body.clear()
