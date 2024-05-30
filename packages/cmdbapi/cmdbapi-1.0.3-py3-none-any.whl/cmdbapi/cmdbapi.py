#!/usr/bin/env python3

import json
import requests

class CMDBAPI(object):
    """Класс взаимодействия с API CMDB.
    
    Примеры вызова:
    #   print(cmdb.api_request(api_type='get',api_method='exampleauth'))
    #   print(cmdb.api_request('get','exampleauth'))
    #   print(cmdb.get.exampleauth())

    """    
    def __init__(self, api_host=None, api_user=None,api_password=None,debug_mode=False,api_timeout=10):
#        self.api_prefix='/api/v1/cmdb/'
        if api_host is None:
            raise ValueError("api_host can not have value 'None'")
        
        self.api_prefix='/v1/'
        self.token=False
        self.api_timeout=int(api_timeout)
        self.api_host=api_host
        self.api_user=api_user
        self.api_password=api_password
        self.debug_mode=debug_mode
        result={'token': False}
        if api_user and api_password is not None:
            login_data={"login": api_user,"password": api_password}
            rapi=requests.post(self.api_host+'/auth/default', data=json.dumps(login_data),headers={'Content-Type': 'application/json'},timeout=self.api_timeout)
            try:
                rapi.raise_for_status()
                try:
                    result = json.loads(rapi.text)
                except json.JSONDecodeError:
                    raise json.JSONDecodeError('Failed to parse JSON response: {}'.format(rapi.text))
            except requests.HTTPError as expt:
                raise requests.HTTPError('Can not connect to API. ErrorCode: {}. Response: {}'.format(expt.response.status_code,rapi.text))
        
        self.token=result['token']

    def __getattr__(self, attr):
        return CMDBAPIObject(attr,self)

    def api_request(self, api_type='get', api_method='', **params):
        """Метод для выполнения запроса к API.
        :param api_type: название запроса (put, get, post, etc.)
        :param api_method: название метода из списка функций API
        :param params: параметры соответствующего метода API
        :return: данные в формате JSON
        """
        if self.debug_mode is True:
            print(("Send {} request to {}. Parameters: {}").format(api_type, self.api_host +self.api_prefix +api_method, str(json.dumps(params))))
        if self.token is not False:
            dod_headers={'Authorization': 'Bearer '+self.token,'Content-Type': 'application/json'}
        else:
            dod_headers={'Content-Type': 'application/json'}
        if api_type=='post':
            rapi = requests.post(self.api_host +self.api_prefix +api_method, verify=False, data=json.dumps(params),headers=dod_headers, timeout=self.api_timeout)
        elif api_type=='put':
            rapi = requests.put(self.api_host +self.api_prefix +api_method, verify=False, data=json.dumps(params),headers=dod_headers, timeout=self.api_timeout)
        elif api_type=='delete':
            rapi = requests.detete(self.api_host +self.api_prefix +api_method, verify=False, data=json.dumps(params),headers=dod_headers, timeout=self.api_timeout)
        else:
            rapi = requests.get(self.api_host +self.api_prefix +api_method, verify=False, params=params,headers=dod_headers, timeout=self.api_timeout)
        
        result = None
        try:
            rapi.raise_for_status()
            try:
                result = json.loads(rapi.text)
            except json.JSONDecodeError:
                raise json.JSONDecodeError('Failed to parse JSON response: {}'.format(rapi.text))
        except requests.HTTPError as expt:
            raise requests.HTTPError('API request failed with error. ErrorCode: {}. Response: {}'.format(expt.response.status_code,rapi.text))
        
        return result

class CMDBAPIObject:
    """Динамически вычисляемые объекты CMDB API.

    """
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __getattr__(self, attr):
        """Динамически создаем методы объекта CMDB API.

        """
        def wrapper(*args, **kw):
            return self.parent.api_request(api_type=self.name, api_method='{}'.format(str(attr)),**kw)
        return wrapper


