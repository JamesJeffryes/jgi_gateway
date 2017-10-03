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
           "search_string" of String, parameter "filter" of type
           "SearchFilter" (SearchFilter The jgi back end takes a map of
           either string, integer, or array of integer. I don't think the
           type compiler supports union typs, so unspecified it is.) ->
           mapping from String to unspecified object, parameter "limit" of
           Long, parameter "page" of Long, parameter "include_private" of
           type "bool" (a bool defined as int)
        :returns: multiple set - (1) parameter "result" of type
           "SearchResult" -> structure: parameter "search_result" of type
           "SearchQueryResult" (typedef mapping<string, string> docdata;) ->
           list of unspecified object, (2) parameter "stats" of type
           "CallStats" (Call performance measurement) -> structure: parameter
           "request_elapsed_time" of Long
        """
        return self._client.call_method(
            'jgi_gateway_eap.search_jgi',
            [input], self._service_ver, context)

    def stage_objects(self, input, context=None):
        """
        :param input: instance of type "StageInput" -> structure: parameter
           "ids" of list of String
        :returns: multiple set - (1) parameter "result" of type
           "StagingResult" (StagingResult returns a map entry for each id
           submitted in the stage_objects request. The map key is the _id
           property returned in a SearchResult item (not described here but
           probably should be), the value is a string describing the result
           of the staging request. At time of writing, the value is always
           "staging" since the request to the jgi gateway jgi service and the
           call to stage_objects in the jgi gateway kbase service are in
           different processes.) -> structure: parameter "job_id" of String,
           (2) parameter "stats" of type "CallStats" (Call performance
           measurement) -> structure: parameter "request_elapsed_time" of Long
        """
        return self._client.call_method(
            'jgi_gateway_eap.stage_objects',
            [input], self._service_ver, context)

    def stage_status(self, input, context=None):
        """
        Fetch the current status of the given staging fetch request as 
        identified by its job id
        :param input: instance of type "StagingStatusInput" -> structure:
           parameter "job_id" of String
        :returns: multiple set - (1) parameter "result" of type
           "StagingStatusResult" -> structure: parameter "message" of String,
           (2) parameter "stats" of type "CallStats" (Call performance
           measurement) -> structure: parameter "request_elapsed_time" of Long
        """
        return self._client.call_method(
            'jgi_gateway_eap.stage_status',
            [input], self._service_ver, context)

    def status(self, context=None):
        return self._client.call_method('jgi_gateway_eap.status',
                                        [], self._service_ver, context)
