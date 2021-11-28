# -*- coding: utf-8 -*-
import asyncio
import requests
import json
import os

class Api:

    def valid_method( self, name ):

        if not name.upper() in [ 'GET', 'POST', 'DELETE', 'PUT' ]:
            return False
        
        return True

    async def send_request(self, method:str, url:str, header:str=None, data:any=None):

        try:

            if not self.valid_method( method ):
                return json.dumps({ 'status' : False, 'message' : 'Invalid method' })
            
            if not url:
                return json.dumps({ 'status' : False, 'message' : 'Invalid url' })
            
            method = method.upper()

            if( method == 'POST' ):
                response = requests.post( url, headers=header, data=data )

            elif( method == 'PUT' ):
                response = requests.put( url, headers=header, data=data )
            elif( method == 'DELETE' ):
                response = requests.delete( url, headers=header, data=data )
            else:
                response = requests.get( url, headers=header, data=data, timeout=None )

            if not response.status_code in [ 200, 201 ]:
                return json.dumps({ 'status' : False, 'message' : str( response ) })

            return json.dumps({ "status": True, "message": "success", "data" : response.json() })

        except requests.ConnectionError as error:
            return json.dumps({ "status": False, "message": str( error ) })

