# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class jgi_gateway_eap(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://kbase.us/services/authorization/Sessions/Login'):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = None
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc)

    def search_jgi(self, input, context=None):
        """
        The search_jgi function takes a search string and returns a list of
        documents.
        :param input: instance of type "SearchInput" (search_jgi searches the
           JGI service for matches against the search_string Other parameters
           @optional limit @optional page) -> structure: parameter
           "search_string" of String, parameter "limit" of Long, parameter
           "page" of Long
        :returns: instance of type "SearchResults" -> structure: parameter
           "doc_data" of list of type "docdata" -> mapping from String to
           String
        """
        return self._client.call_method(
            'jgi_gateway_eap.search_jgi',
            [input], self._service_ver, context)

    def stage_objects(self, input, context=None):
        """
        :param input: instance of type "StageInput" -> structure: parameter
           "ids" of list of String
        :returns: instance of type "StagingResults" -> mapping from String to
           String
        """
        return self._client.call_method(
            'jgi_gateway_eap.stage_objects',
            [input], self._service_ver, context)

    def debug(self, context=None):
        """
        :returns: instance of type "DebugResults" -> structure: parameter
           "config" of String
        """
        return self._client.call_method(
            'jgi_gateway_eap.debug',
            [], self._service_ver, context)

    def status(self, context=None):
        return self._client.call_method('jgi_gateway_eap.status',
                                        [], self._service_ver, context)
