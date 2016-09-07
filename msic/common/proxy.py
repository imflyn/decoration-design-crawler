'''
This proxy is goagent/wallproxy
If you want to disable it, plz configure settings.py
'''
PROXIES = [
	# {"ip_port": "127.0.0.1:8087"}, #goagent
	# {"ip_port": "127.0.0.1:8118"}, #tor via privoxy
	{"ip_port": "127.0.0.1:1080"},  # tor via privoxy
]

FREE_PROXIES = [
]
