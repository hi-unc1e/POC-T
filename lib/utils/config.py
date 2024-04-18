#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

try:  # Python 2
    import ConfigParser
except:  # Python 3
    import configparser as ConfigParser
from lib.core.data import paths, logger
from lib.core.common import getSafeExString


class ConfigFileParser:
    @staticmethod
    def _get_option(section, option):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read(paths.CONFIG_PATH)
            return cf.get(section=section, option=option)
        except ConfigParser.NoOptionError as e:
            logger.warning('Missing essential options, please check your config-file.')
            logger.error(getSafeExString(e))
            return ''

    def ZoomEyeEmail(self):
        return self._get_option('zoomeye', 'email')

    def ZoomEyePassword(self):
        return self._get_option('zoomeye', 'password')

    def ShodanApikey(self):
        return self._get_option('shodan', 'api_key')

    def BingApikey(self):
        return self._get_option('bing', 'api_key')

    def CloudEyeApikey(self):
        return self._get_option('cloudeye', 'api_key')

    def ColudEyePersonaldomain(self):
        return self._get_option('cloudeye', 'personal_domain')

    def GoogleProxy(self):
        return self._get_option('google', 'proxy')

    def GoogleDeveloperKey(self):
        return self._get_option('google', 'developer_key')

    def GoogleEngine(self):
        return self._get_option('google', 'search_engine')

    def FofaEmail(self):
        return self._get_option('fofa', 'email')

    def FofaKey(self):
        return self._get_option('fofa', 'api_key')

    def QuakeKey(self):
        return self._get_option('quake', 'X-QuakeToken')

    def HunterKey(self):# todo:
        return self._get_option('hunter', 'api-key')
