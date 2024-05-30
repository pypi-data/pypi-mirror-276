from .constant import api
import time
from requests import Session
from .signalr import Connection
from . import FCTradingClient


class FCTradingStream(object):

	def __init__(self, fctrading_client: FCTradingClient, stream_url: str, on_message, on_error, last_notify_id: str = "-1"):
		self.client = fctrading_client
		self._stream_url = stream_url
		self._fc_handlers = []
		self._fc_handlers.append(on_message)
		self._fc_error_handlers = []
		self._fc_error_handlers.append(on_error)
		self.lastId = last_notify_id

	def fc_on_message(self, fc_message):
		for fc_handler in self._fc_handlers:
			fc_handler(fc_message)

	def fc_on_error(self, fc_error):

		for fc_error_handler in self._fc_error_handlers:
			fc_error_handler(fc_error)

	def start(self):
		
		headers = {}
		headers['Authorization'] = "Bearer " + self.client.get_access_token()
		headers["NotifyID"] = self.lastId
			
		self.connection = Connection(self._stream_url + api.SIGNALR, headers)
		
		self.hub_proxy = self.connection.register_hub(api.SIGNALR_HUB_FC)

		self.hub_proxy.client.on(api.SIGNALR_METHOD, self.fc_on_message)

		self.hub_proxy.client.on(api.SIGNALR_METHOD_ERROR, self.fc_on_error)
		
		self.connection.error += self.fc_on_error
		self.connection.start()


