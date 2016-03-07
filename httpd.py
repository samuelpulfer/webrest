#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	import simplejson as json
except ImportError:
	import json
import sys, os

#mimerender = mimerender.WebPyMimeRender()
sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'lib', 'web.py-0.37'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'lib', 'mimerender-master', 'src'))
import mimerender
import web

mimerender = mimerender.WebPyMimeRender()

urls = (
	'/(.*)', 'greet'
)

class MyApplication(web.application):
	def run(self, port=8080, ip='127.0.0.1', *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, (ip, port))


class greet:
	render_xml  = lambda message: '<message>%s</message>'%message
	render_json = lambda **args: json.dumps(args)
	render_html = lambda message: '<html><body>%s</body></html>'%message
	render_txt  = lambda message: message

	@mimerender(
		default = 'html',
		html = render_html,
		xml  = render_xml,
		json = render_json,
		txt  = render_txt
	)
	
	def GET(self, name):
		if not name: 
			name = 'world'
		return {'message': 'Hello, ' + name + '!'}

if __name__ == "__main__":
	app = MyApplication(urls, globals())
	app.run(port=8082)
