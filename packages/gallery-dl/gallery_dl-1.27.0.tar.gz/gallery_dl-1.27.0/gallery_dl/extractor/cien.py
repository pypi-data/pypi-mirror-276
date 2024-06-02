# -*- coding: utf-8 -*-

# Copyright 2024 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://ci-en.net/"""

from .common import Extractor, Message
from .. import text, util

BASE_PATTERN = r"(?:https?://)?ci-en\.(?:net|dlsite\.com)"


class CienExtractor(Extractor):
    category = "cien"
    root = "https://ci-en.net"

    def __init__(self, match):
        self.root = text.root_from_url(match.group(0))
        Extractor.__init__(self, match)

    def _pagination_articles(self, url, params):
        data = {"extractor": CienArticleExtractor}
        params["page"] = text.parse_int(params.get("page"), 1)

        while True:
            page = self.request(url, params=params).text

            for card in text.extract_iter(
                    page, ' class="c-cardCase-item', '</div>'):
                article_url = text.extr(card, ' href="', '"')
                yield Message.Queue, article_url, data

            if ' rel="next"' not in page:
                return
            params["page"] += 1


class CienArticleExtractor(CienExtractor):
    subcategory = "article"
    pattern = BASE_PATTERN + r"/creator/(\d+)/article/(\d+)"
    example = "https://ci-en.net/creator/123/article/12345"

    def items(self):
        url = "{}/creator/{}/article/{}".format(
            self.root, self.groups[0], self.groups[1])
        page = self.request(url, notfound="article").text
        return
        yield 1


class CienCreatorExtractor(CienExtractor):
    subcategory = "creator"
    pattern = BASE_PATTERN + r"/creator/(\d+)(?:/article(?:\?([^#]+))?)?/?$"
    example = "https://ci-en.net/creator/123"

    def items(self):
        url = "{}/creator/{}/article".format(self.root, self.groups[0])
        params = text.parse_query(self.groups[1])
        params["mode"] = "list"
        return self._pagination_articles(url, params)


class CienRecentExtractor(CienExtractor):
    subcategory = "recent"
    pattern = BASE_PATTERN + r"/mypage/recent(?:\?([^#]+))?"
    example = "https://ci-en.net/mypage/recent"

    def items(self):
        url = self.root + "/mypage/recent"
        params = text.parse_query(self.groups[0])
        return self._pagination_articles(url, params)


class CienFollowingExtractor(CienExtractor):
    subcategory = "following"
    pattern = BASE_PATTERN + r"/mypage/subscription(/following)?"
    example = "https://ci-en.net/mypage/subscription"

    def items(self):
        url = self.root + "/mypage/recent"
        params = text.parse_query(self.groups[0])
        return self._pagination_articles(url, params)
