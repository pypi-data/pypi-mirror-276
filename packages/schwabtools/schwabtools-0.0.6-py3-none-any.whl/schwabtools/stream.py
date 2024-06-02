"""
This file contains functions to stream data
Coded by Tyler Bowers
Github: https://github.com/tylerebowers/Schwab-API-Python
"""

import json
import asyncio
import threading
import websockets
import websockets.exceptions
from time import sleep
from datetime import datetime, time
from schwabtools import terminal, api


class Stream:

    def __init__(self, client):
        self._web_socket = None
        self._streamer_info = None
        self._start_timestamp = None
        self._terminal = None
        self._request_id = 0  # a counter for the request id
        self._subscriptions = {}
        self.active = False
        self.client = client  # so we can get streamer info

    async def _start(self, receiver="default"):
        # get streamer info
        response = self.client.preferences()
        if response.ok:
            self._streamer_info = response.json().get('streamerInfo', None)[0]
        else:
            terminal.color_print.error("Could not get streamerInfo")
            return None

        # specify receiver (what do we do with received data)
        if receiver == "default":
            if self._terminal is None:
                self._terminal = terminal.multiTerminal(title="Stream output")

            def defaultReceiver(data):
                self._terminal.print(data)
            receiver = defaultReceiver


        while True:
            try:
                self._start_timestamp = datetime.now()
                async with websockets.connect(self._streamer_info.get('streamerSocketUrl'), ping_interval=None) as self._web_socket:
                    receiver("[INFO]: Connecting to server...")
                    await self._web_socket.send(json.dumps(self.admin.login()))
                    receiver(f"[INFO]: {await self._web_socket.recv()}")
                    self.active = True
                    # TODO: resend requests if the stream crashes
                    while True:
                        received = await self._web_socket.recv()
                        receiver(received)
            except Exception as e:
                self.active = False
                terminal.color_print.error(f"{e}")
                if e is websockets.exceptions.ConnectionClosedOK:
                    terminal.color_print.info("Stream has closed.")
                    break
                elif e is RuntimeError:
                    terminal.color_print.warning("Streaming window has closed.")
                    break
                elif (datetime.now() - self._start_timestamp).seconds < 70:
                    terminal.color_print.error("Stream not alive for more than 1 minute, exiting...")
                    break
                else:
                    receiver("[INFO]: Connection lost to server, reconnecting...")

    def start(self, receiver="default"):
        def start_async():
            asyncio.run(self._start(receiver))

        threading.Thread(target=start_async).start()
        sleep(2)  # wait for thread/stream to start


    def start_automatic(self, after_hours=False, pre_hours=False):
        start = time(9, 30, 0)  # market opens at 9:30
        end = time(16, 0, 0)  # market closes at 4:00
        if pre_hours:
            start = time(8, 0, 0)
        if after_hours:
            end = time(20, 0, 0)

        def checker():

            while True:
                in_hours = (start <= datetime.now().time() <= end) and (0 <= datetime.now().weekday() <= 4)
                if in_hours and not self.active:
                    self.start()
                elif not in_hours and self.active:
                    terminal.color_print.info("Stopping Stream.")
                    self.stop()
                sleep(60)

        threading.Thread(target=checker).start()

        if not start <= datetime.now().time() <= end:
            terminal.color_print.info("Stream was started outside of active hours and will launch when in hours.")


    def send(self, listOfRequests):
        async def _send(toSend):
            await self._web_socket.send(toSend)

        if type(listOfRequests) is not list:
            listOfRequests = [listOfRequests]
        if self.active:
            toSend = json.dumps({"requests": listOfRequests})
            asyncio.run(_send(toSend))
        else:
            terminal.color_print.warning("Stream is not active, nothing sent.")


    #TODO: Fix this (wont properly close)
    def stop():
        self._request_id += 1
        send(admin.logout())
        self.active = False


    def basicRequest(self,service, command, parameters=None):
        request = {"service": service.upper(),
                   "command": command.upper(),
                   "requestid": self._request_id,
                   "SchwabClientCustomerId": self._streamer_info.get("schwabClientCustomerId"),
                   "SchwabClientCorrelId": self._streamer_info.get("schwabClientCorrelId")}
        if parameters is not None: request["parameters"] = parameters
        self._request_id += 1
        return request

    def listToString(ls):
        if type(ls) is str: return ls
        elif type(ls) is list: return ",".join(map(str, ls))


    class admin:
        @staticmethod
        def login():
            return Stream.basicRequest(service="ADMIN", command="LOGIN", parameters={"Authorization": api.tokens.accessToken, "SchwabClientChannel": self._streamer_info.get("schwabClientChannel"), "SchwabClientFunctionId": self._streamer_info.get("schwabClientFunctionId")})

        @staticmethod
        def logout():
            return Stream.basicRequest(service="ADMIN", command="LOGOUT")

        #@staticmethod
        #def qos(qosLevel):
        #    return Stream.basicRequest(service="ADMIN", command="QOS", parameters={"qoslevel": qosLevel})


    class chart:
        @staticmethod
        def equity(keys, fields, command="SUBS"):
            return Stream.basicRequest("CHART_EQUITY", command, parameters={"keys": Stream.listToString(keys), "fields": Stream.listToString(fields)})

        @staticmethod
        def futures(keys, fields, command="SUBS"):
            return Stream.basicRequest("CHART_FUTURES", command, parameters={"keys": Stream.listToString(keys), "fields": Stream.listToString(fields)})


    class levelOne:
        @staticmethod
        def quote(keys, fields, command="SUBS"):  # Service not available or temporary down.
            return Stream.basicRequest("QUOTE", command, parameters={"keys": Stream.listToString(keys), "fields": Stream.listToString(fields)})

        @staticmethod
        def option(keys, fields, command="SUBS"):
            return Stream.basicRequest("OPTION", command, parameters={"keys": Stream.listToString(keys), "fields": Stream.listToString(fields)})

        @staticmethod
        def futures(keys, fields, command="SUBS"):
            return Stream.basicRequest("LEVELONE_FUTURES", command, parameters={"keys": Stream.listToString(keys), "fields": Stream.listToString(fields)})

        @staticmethod
        def forex(keys, fields, command="SUBS"):
            return Stream.basicRequest("LEVELONE_FOREX", command, parameters={"keys": Stream.listToString(keys), "fields": Stream.listToString(fields)})

        @staticmethod
        def futures_options(keys, fields, command="SUBS"):
            return Stream.basicRequest("LEVELONE_FUTURES_OPTIONS", command, parameters={"keys": Stream.listToString(keys), "fields": Stream.listToString(fields)})


    """
    
    class account:
        @staticmethod
        def activity(keys, fields, command="SUBS"):
            return Stream.request(command, "ACCT_ACTIVITY", keys, fields)
    
    
    class actives:
        @staticmethod
        def nasdaq(keys, fields, command="SUBS"):
            return Stream.request(command, "ACTIVES_NASDAQ", keys, fields)
    
        @staticmethod
        def nyse(keys, fields, command="SUBS"):
            return Stream.request(command, "ACTIVES_NYSE", keys, fields)
    
        @staticmethod
        def otcbb(keys, fields, command="SUBS"):
            return Stream.request(command, "ACTIVES_OTCBB", keys, fields)
    
        @staticmethod
        def options(keys, fields, command="SUBS"):
            return Stream.request(command, "ACTIVES_OPTIONS", keys, fields)
    
    
    
    class book:
        @staticmethod
        def forex(keys, fields, command="SUBS"):
            return Stream.request(command, "FOREX_BOOK", keys, fields)
    
        @staticmethod
        def futures(keys, fields, command="SUBS"):
            return Stream.request(command, "FUTURES_BOOK", keys, fields)
    
        @staticmethod
        def listed(keys, fields, command="SUBS"):
            return Stream.request(command, "LISTED_BOOK", keys, fields)
    
        @staticmethod
        def nasdaq(keys, fields, command="SUBS"):
            return Stream.request(command, "NASDAQ_BOOK", keys, fields)
    
        @staticmethod
        def options(keys, fields, command="SUBS"):
            return Stream.request(command, "OPTIONS_BOOK", keys, fields)
    
        @staticmethod
        def futures_options(keys, fields, command="SUBS"):
            return Stream.request(command, "FUTURES_OPTIONS_BOOK", keys, fields)
    
    
    class levelTwo:
        @staticmethod
        def _NA():
            print("Not Available")
    
    
    class news:
        @staticmethod
        def headline(keys, fields, command="SUBS"):
            return Stream.request(command, "NEWS_HEADLINE", keys, fields)
    
        @staticmethod
        def headlineList(keys, fields, command="SUBS"):
            return Stream.request(command, "NEWS_HEADLINELIST", keys, fields)
    
        @staticmethod
        def headlineStory(keys, fields, command="SUBS"):
            return Stream.request(command, "NEWS_STORY", keys, fields)
    
    
    class timeSale:
        @staticmethod
        def equity(keys, fields, command="SUBS"):
            return Stream.request(command, "TIMESALE_EQUITY", keys, fields)
    
        @staticmethod
        def forex(keys, fields, command="SUBS"):
            return Stream.request(command, "TIMESALE_FOREX", keys, fields)
    
        @staticmethod
        def futures(keys, fields, command="SUBS"):
            return Stream.request(command, "TIMESALE_FUTURES", keys, fields)
    
        @staticmethod
        def options(keys, fields, command="SUBS"):
            return Stream.request(command, "TIMESALE_OPTIONS", keys, fields)
            
    """

"""

def _streamResponseHandler(streamOut):
    try:
        parentDict = json.loads(streamOut)
        for key in parentDict.keys():
            match key:
                case "notify":
                    self._terminal.print(
                        f"[Heartbeat]: {Stream.epochMSToDate(parentDict['notify'][0]['heartbeat'])}")
                case "response":
                    for resp in parentDict.get('response'):
                        self._terminal.print(f"[Response]: {resp}")
                case "snapshot":
                    for snap in parentDict.get('snapshot'):
                        self._terminal.print(f"[Snapshot]: {snap}")
                case "data":
                    for data in parentDict.get("data"):
                        if data.get('service').upper() in universe.streamFieldAliases:
                            service = data.get("service")
                            timestamp = data.get("timestamp")
                            for symbolData in data.get("content"):
                                tempSnapshot = database.Snapshot(service, symbolData.get("key"), timestamp, symbolData)
                                if universe.preferences.usingDatabase:
                                    database.DBAddSnapshot(tempSnapshot)  # add to database
                                if universe.preferences.usingDataframes:
                                    database.DFAddSnapshot(tempSnapshot)  # add to dataframes
                                self._terminal.print(
                                    f"[Data]: {tempSnapshot.toPrettyString()}")  # to stream output
                case _:
                    self._terminal.print(f"[Unknown Response]: {streamOut}")
    except Exception as e:
        self._terminal.print(f"[ERROR]: There was an error in decoding the stream response: {streamOut}")
        self._terminal.print(f"[ERROR]: The error was: {e}")
"""