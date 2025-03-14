import configparser
import redis
import json

global redis1
config = configparser.ConfigParser()
config.read('config.ini')

redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']), decode_responses=(config['REDIS']['DECODE_RESPONSE']), username=(config['REDIS']['USER_NAME']))


if(redis1.exists('gis_conv')):
    conv=redis1.get('gis_conv')
    print(conv)
    #conv_list=json.loads(conv)
    #print(len(conv_list))
    #print(type(json.dumps(conv_list)))