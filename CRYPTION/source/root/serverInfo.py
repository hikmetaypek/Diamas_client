
STATE_NONE = '...'
		
STATE_DICT = {
	0 : '....',
	1 : 'NORM',
	2 : 'BUSY',
	3 : 'FULL'
}

SERVER1_CHANNEL_DICT = {
	1:{'key':11,'name':'CH1   ','ip':'localhost','tcp_port':18001,'state':STATE_NONE,},
}

SERVE2_CHANNEL_DICT = {
	1:{'key':11,'name':'CH1   ','ip':'185.184.26.250','tcp_port':18001,'state':STATE_NONE,},
}

SERVE3_CHANNEL_DICT = {
	1:{'key':11,'name':'CH1   ','ip':'185.184.26.251','tcp_port':18001,'state':STATE_NONE,},
}

REGION_NAME_DICT = {
	0 : '',
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { 'ip':'localhost', 'port':11055, }, 
		2 : { 'ip':'185.184.26.250', 'port':11055, }, 
		3 : { 'ip':'185.184.26.251', 'port':11055, }, 
	}	
}

REGION_DICT = {
	0 : {
		1 : { 'name' : 'Local', 'channel' : SERVER1_CHANNEL_DICT, },
		2 : { 'name' : 'Win Server', 'channel' : SERVE2_CHANNEL_DICT, },
		3 : { 'name' : 'BSD Server', 'channel' : SERVE3_CHANNEL_DICT, },
	},
}

MARKADDR_DICT = {
	10 : { 'ip' : 'localhost', 'tcp_port' : 18001, 'mark' : '10.tga', 'symbol_path' : '10', },
	20 : { 'ip' : '185.184.26.250', 'tcp_port' : 18001, 'mark' : '10.tga', 'symbol_path' : '10', },
	30 : { 'ip' : '185.184.26.251', 'tcp_port' : 18001, 'mark' : '10.tga', 'symbol_path' : '10', },
}
