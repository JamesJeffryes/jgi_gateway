# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from jgi_gateway_eap.jgi_gateway_eapImpl import jgi_gateway_eap
from jgi_gateway_eap.jgi_gateway_eapServer import MethodContext


class jgi_gatewayTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        if not isinstance(token, str):
            raise(ValueError('invalid or missing token'))

        header = {'Authorization': token}
        endpoint = 'https://ci.kbase.us/services/auth/api/V2/token'
        result = requests.get(endpoint, headers=header).json()
        user_id = result['user']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'jgi_gateway_eap',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('jgi_gateway_eap'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = jgi_gateway_eap(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = 'test_jgi_gateway_eap_' + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa

    # These tests cover the simple cases of the control parameters.
    def test_search_simple(self):
        # Test default result size of 10 for the given user and a wildcard 
        # that should give us everything.
        query = {'query': {'_all': '*'}}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret)
        self.assertIn('hits', ret)
        self.assertEquals(len(ret['hits']), 10)

        # Test an explicit limit of 20, still for wildcard
        query = {'query': {'_all': '*'}, 'limit': 20}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret)
        self.assertIn('hits', ret)
        self.assertEquals(len(ret['hits']), 20)

        # Test the same query, this time fetching the second page of hits
        query = {'query': {'_all': '*'}, 'limit': 20, 'page': 1}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret)
        self.assertIn('hits', ret)
        self.assertEquals(len(ret['hits']), 20)

    # Trigger input validation errors
    def test_search_input_validation(self):
        tests = [
            [{}, 'missing', 'query'],
            [{'query': 'i am wrong'}, 'wrong-type', 'query'],
            [{'query': {'_all': '*'}, 'filter': 1}, 'wrong-type', 'filter'],
            [{'query': {'_all': '*'}, 'limit': 'x'}, 'wrong-type', 'limit'],
            [{'query': {'_all': '*'}, 'limit': 0}, 'out-of-range', 'limit'],
            [{'query': {'_all': '*'}, 'limit': 10001}, 'out-of-range', 'limit'],
            [{'query': {'_all': '*'}, 'page': 'x'}, 'wrong-type', 'page'],
            [{'query': {'_all': '*'}, 'page': 0}, 'out-of-range', 'page'],
            [{'query': {'_all': '*'}, 'page': 10001}, 'out-of-range', 'page'],
            [{'query': {'_all': '*'}, 'include_private': 'x'}, 'wrong-type', 'include_private'],
            [{'query': {'_all': '*'}, 'include_private': -1}, 'out-of-range', 'include_private'],
            [{'query': {'_all': '*'}, 'include_private': 2}, 'out-of-range', 'include_private']
        ]
        for query, error_code, error_key in tests:
            ret, err, status = self.getImpl().search(self.getContext(), query)
            self.assertIsNone(ret)
            self.assertIsNone(status)
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], 'input')
            self.assertEquals(err['code'], error_code)
            self.assertEquals(err['info']['key'], error_key)


    # Test control parameters at, just under, just over the limits.

    # Test the return structure using the simplest query and all default
    # control parameters.
    def test_search_return_structure(self):
        query = {'query': {'_all': '*'}}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNotNone(ret)
        self.assertIn('hits', ret)
        hits = ret['hits']
        self.assertIsInstance(hits, list)
        self.assertEquals(len(hits), 10)
        a_hit = hits[0]
        self.assertIsInstance(a_hit, dict)
        self.assertIn('total', ret)
        total = ret['total']
        self.assertIsInstance(total, int)
        for key in ['source', 'index', 'score', 'id']:
            self.assertIn(key, a_hit)
        source = a_hit['source']
        self.assertIsInstance(source, dict)
        index = a_hit['index']
        self.assertIsInstance(index, basestring)
        score = a_hit['score']
        self.assertIsInstance(score, float)
        hitid = a_hit['id']
        self.assertIsInstance(hitid, basestring)

    # Test the error structure. 
    # Use a 
    # def test_search_error_structure(self):
    #     query = {}


    # Test staging

    def test_stage(self):
        req = {'ids': ['51d4fa27067c014cd6ed1a90', '51d4fa27067c014cd6ed1a96']}
        ret, error, status = self.getImpl().stage(self.getContext(), req)
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, dict)
        self.assertIn('job_id', ret)
        job_id = ret['job_id']
        self.assertIsInstance(job_id, basestring)

    # Test staging validation errors

    # Trigger input validation errors
    def test_stage_input_validation(self):
        tests = [
            [{}, 'missing', 'ids'],
            [{'ids': 'x'}, 'wrong-type', 'ids']
        ]
        for req, error_code, error_key in tests:
            ret, err, status = self.getImpl().stage(self.getContext(), req)
            #   ret, err, status = self.getImpl().stage(self.getContext(), param)
            self.assertIsNone(ret)
            self.assertIsNone(status)
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], 'input')
            self.assertEquals(err['code'], error_code)
            self.assertEquals(err['info']['key'], error_key)

    # def test_status(self):
    #     ret, err, status = self.getImpl().status(self.getContext())

    # These tests cover the simple cases of the control parameters.
    def test_search_timeout(self):
        # Test default result size of 10 for the given user and a wildcard 
        # that should give us everything.
        impl = self.getImpl()
        original_timeout = impl.connection_timeout
        test_timeout = 0.0001
        impl.connection_timeout = test_timeout

        query = {'query': {'_all': '*'}}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNone(ret)
        self.assertIsNotNone(err)
        self.assertEquals(err['info']['timeout'], test_timeout)
        self.assertEquals(err['type'], 'network')
        self.assertEquals(err['code'], 'connection-timeout')
        impl.connection_timeout = original_timeout

    def test_search_bad_host(self):
        # Test default result size of 10 for the given user and a wildcard 
        # that should give us everything.
        impl = self.getImpl()
        original_host = impl.jgi_host
        bad_host = original_host + 'x'
        impl.jgi_host = bad_host

        query = {'query': {'_all': '*'}}
        ret, err, stats = self.getImpl().search(self.getContext(), query)
        self.assertIsNone(ret)
        self.assertIsNotNone(err)
        # self.assertEquals(err['info']['timeout'], test_timeout)
        self.assertEquals(err['type'], 'network')
        self.assertEquals(err['code'], 'connection-error')
        impl.jgi_host = original_host
 