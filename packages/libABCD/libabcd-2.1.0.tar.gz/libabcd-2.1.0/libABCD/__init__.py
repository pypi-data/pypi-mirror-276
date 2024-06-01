import paho.mqtt.client as mqtt
import logging
from logging.handlers import TimedRotatingFileHandler
import configparser, json, os, sys, time


### logging in UTC
logging.Formatter.converter = time.gmtime


### global variables
pid = os.getpid()
name = 'libABCD'
mqttp = None    # publisher mqtt client
mqttl = None    # listener mqtt client
bInitialized = False # whether `init` has been run
bReportStatus = False # whether to publish the status when on and off
bPingPong = False # whether to subscribe and answer to ping calls
host = 'localhost'  # mqtt defaults
port = 1883
subscriptions = []
mqttreconnections = 0
logger = logging.getLogger(name)


def _init_logger(loglevel, fileloglevel, mqttp):

    # configure the root logger
    rlogger = logging.getLogger()    

    # global logging level
    rlogger.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)-10s - %(levelname)-8s - %(message)s')

    # create console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)
    rlogger.addHandler(ch)

    # create file handler if requested
    if fileloglevel:
        # file log directory
        logdir = ("log")
        if not os.path.isdir(logdir):
            os.makedirs(logdir)

        # create file handler
        fh = TimedRotatingFileHandler(
            os.path.join(logdir, name+'.log'), when='midnight', utc=True, delay=True)
        fh.setLevel(fileloglevel)
        fh.setFormatter(formatter)
        rlogger.addHandler(fh)
    
    # add an ABCDHandler if publishing is on
    if mqttp:
        ph = ABCDHandler(level=logging.INFO)
        ph.setFormatter(formatter)
        rlogger.addHandler(ph)

    global logger
    logger = logging.getLogger(name)


def _init_mqtt(publisher, listener, username, password):

    ### start mqtt client(s)
    global mqttp, mqttl

    # publisher
    if publisher:
        mqttp = mqtt.Client(name)
        mqttp.on_connect = _on_connect
        mqttp.on_disconnect = _on_disconnect
        mqttp.on_publish = _on_publish
        mqttp.username_pw_set(username, password)

    # listener
    if listener:
        mqttl = mqtt.Client(name+'_listener')
        mqttl.on_connect = _on_connect_l
        mqttl.on_disconnect = _on_disconnect
        mqttl.on_message = _on_message 
        mqttl.on_subscribe = _on_subscribe
        mqttl.on_unsubscribe = _on_unsubscribe
        mqttl.username_pw_set(username, password)


### mqtt generic callbacks
def _on_connect(mqttc: mqtt.Client, userdata, flags, rc):

    id = mqttc._client_id.decode()

    if rc == 0:
        logger.debug(f"mqtt client {id} connected to server")
        logger.debug(f'FLAGS: {flags}')

        if bReportStatus:
            # report on
            msg = _format_msg('on')
            mqttc.publish(f'status/{id}', msg, retain=True)

    else:
        logger.error(f"mqtt client {id} connection error, rc={rc}")
        

def _on_connect_l(mqttc: mqtt.Client, userdata, flags, rc):

    _on_connect(mqttc, userdata, flags, rc)

    global mqttreconnections
    mqttreconnections += 1

    if mqttreconnections > 1:
        for sub in subscriptions:
            logger.debug(f'Subscribing to {sub} (on_connect)')
            mqttc.subscribe(sub, qos=2)


def _on_publish(mqttc, userdata, mid):
    # logger.debug(f"published mid {mid}")
    pass


def _on_disconnect(mqttc: mqtt.Client, userdata, rc):
    
    id = mqttc._client_id.decode()

    if rc == 0:
        logger.debug(f"mqtt client {id} disconnected from server")
    else:
        logger.warning(f"mqtt client {id} unexpected disconnection, rc={rc}")


def _on_message(mqttc: mqtt.Client, userdata, msg: mqtt.MQTTMessage):

    logger.debug(f'Unhandled message on topic {msg.topic}: {msg.payload}')


def _on_subscribe(client, userdata, mid, granted_qos):

    logger.debug(f'Broker answered to a subscribe request: {granted_qos} ')


def _on_unsubscribe(client, userdata, mid):

    logger.debug(f'Broker answered to unsubscribe request {mid}.')


### module init
def init(client_name: str, expconfig=None, loglevel=logging.INFO, fileloglevel=None,
         publisher=True, listener=False, connect=True, report_status=False, pingpong=False,
         unique=False):
    """
    Create a libABCD client. This includes a logger in all cases and mqtt publisher and/or 
    listener according to the parameters. It also initializes the generic mqtt callbacks.

    Parameters
    ----------
    client_name: str
        a name that will be assigned to the client. If logging is active, the name of the log 
        will match this name.
    expconfig: str or None, optional
        name of the configuration file for the connections. If None (default), uses mqtt
        defaults.
    loglevel: logging.<LEVEL>, optional
        the stdout logging level to use. Default: logging.INFO.
    fileloglevel: logging.<LEVEL> or None, optional
        the file logging level to use. If None (default), does not log to file. If set, it creates a 
        TimeRotatedFileHandler with a hard-coded formatting. The name of this log will be 
        'log/<client_name>.log<date>'
    publisher: bool, optional
        whether to include a publisher client or not. Default: True. If this client is not 
        supposed to publish to any topics, then `publisher` should be True.
    listener: bool, optional
        whether to include a listener client or not. Default: False. If this client is supposed 
        to subscribe to any topics, then `listener` should be True.
    connect: bool, optional
        whether to connect the mqtt clients. Default: True.
    report_status: bool, optional
        whether to publish an on/off message in the 'status' topic when connected/disconnected. Default: False
    pingpong: bool, optional
        whether to subscribe and answer to ping calls. Default: False.
    unique: bool, optional
        whether the client should be unique or not. If 'False' (default), appends
        the process ID to the end of the client name.
    """
    
    global bInitialized
    if bInitialized:
        print('ERROR: libABCD already initialized. Nothing will happen.')
        return

    # set this client's name
    global name
    name = client_name
    if not unique:
        name = name+'_'+str(pid)

    # report status flag
    global bReportStatus
    bReportStatus = report_status

    # start logging
    _init_logger(loglevel, fileloglevel, publisher)

    # ping-pong flag
    global bPingPong
    if pingpong and (not listener or not publisher):
        logger.warning('Both `publisher` and `listener` should be True for pingpong to work.')
    bPingPong = pingpong

    # parse network configuration
    global host, port
    username = None
    password = None

    if expconfig:
        config = configparser.ConfigParser()
        try:
            config.read_file(open(expconfig))
        except Exception as e:
            logger.error(f'Could not parse expconfig file. Exception: {e}. Skipping.')
        else:
            if config.has_section('NETWORK'):

                if config.has_option('NETWORK', 'host'):
                    host = config.get('NETWORK', 'host')

                if config.has_option('NETWORK', 'port'):
                    port = int(config.get('NETWORK', 'port'))

                if config.has_option('NETWORK', 'username'):
                    username = config.get('NETWORK', 'username')

                if config.has_option('NETWORK', 'password'):
                    password = config.get('NETWORK', 'password')

    _init_mqtt(publisher, listener, username, password)

    ### toggle flag
    bInitialized = True

    if connect:
        mqconnect()


def _mqconnect(mqttc: mqtt.Client):
    if bReportStatus:
        # set will if client dies unexpectedly
        mqttc.will_set(f'status/{mqttc._client_id.decode()}', None, retain=True)
    mqttc.connect(host, port)
    mqttc.loop_start()


def _mqdisconnect(mqttc: mqtt.Client):
    
    if bReportStatus:
        # report off
        msg = _format_msg('off')
        mqttc.publish(f'status/{mqttc._client_id.decode()}', msg, retain=True)

    mqttc.loop_stop()
    mqttc.disconnect()


def mqconnect():
    """
    Connect initialized mqtt clients.
    """
    if not bInitialized:
        print('ERROR: libABCD not initialized. Nothing will happen.')
        return

    if mqttp:
        _mqconnect(mqttp)

    if mqttl:
        _mqconnect(mqttl)
        # mqttl.subscribe(f'to/{name}')
        if bPingPong:
            add_callback('pings', _pingpong)


def disconnect():
    """Disconnect initialized mqtt clients."""

    if mqttp:
        _mqdisconnect(mqttp)

    if mqttl:
        _mqdisconnect(mqttl)


def _format_msg(payload):
    try:
        return json.dumps({'from': name, 'timestamp': time.time(), 'payload': payload})
    except Exception as e:
        logger.error(f'payload {payload} could not be formatted. Exception: {e}')


def publish(topic, payload=None, **kwargs):
    """
    Publish a `payload` to `topic` with libABCD specific format.

    Parameters
    ----------
    topic: str
        where to publish the message
    payload: any
        what to publish. 
    **kwargs:
        keyword arguments passed to mqttp.publish
    """

    if mqttp:
        msg = _format_msg(payload)
        logger.debug(f'Publishing "{msg}" to topic "{topic}"')
        try:
            mqttp.publish(topic, msg, **kwargs)
            time.sleep(.001)
        except Exception as e:
            logger.error(f'Following exception raised trying to publish: {e}')
    else:
        logger.error('mqtt publisher was not initialized. Cannot publish.')


def subscribe(topic):
    """
    Subscribe the listener to `topic`. See `mqtt.client.subscribe`.
    """

    if mqttl:

        if topic in subscriptions: return

        subscriptions.append(topic)

        # subscribe to topic
        logger.debug(f'Subscribing to {topic}')
        mqttl.subscribe(topic, qos=2)

    else:
        logger.warning('Listener was not initialized. Cannot subscribe.')


def unsubscribe(topic):
    """
    Unsubscribe the listener from `topic`. See `mqtt.client.unsubscribe`.
    """

    if mqttl:

        if topic in subscriptions: subscriptions.remove(topic)

        # unsubscribe from topic
        logger.debug(f'Unsubscribing from {topic}')
        mqttl.unsubscribe(topic)
        
    else:
        logger.warning('Listener was not initialized. Cannot unsubscribe.')


def add_callback(sub, func, allow_empty_payload=False):
    """
    Add a callback `func` to message received in topic(s) `sub`. `func`
    must have the following signature: `func(msg, topic)` with `msg` 
    the payload of the received message and `topic` its topic.
    """

    def _msg_callback(mqttc: mqtt.Client, userdata, msg: mqtt.MQTTMessage):

        # decode and json-load msg
        dmsg = msg.payload.decode()

        if dmsg == '':
            if not allow_empty_payload:
                return      # ignore empty payloads
            jmsg = None

        else:
            try:
                jmsg = json.loads(dmsg)
            except Exception as e:
                logger.warning(f'Could not json-load following payload: {dmsg}. Exception: {e}.')
                return

            if 'from' not in jmsg or 'timestamp' not in jmsg \
                                                    or 'payload' not in jmsg:
                logger.warning(f'Wrong format in following message: {jmsg}. Nothing will happen.')
                return
        
        try:
            func(jmsg, msg.topic)
        except Exception as e:
            logger.error(f'Exception raised when processing message {jmsg}: {e}.')


    if mqttl:

        # subscribe and add callback
        subscribe(sub)
        logger.debug(f'Adding callback to topic {sub}')
        mqttl.message_callback_add(sub, _msg_callback)

    else:
        logger.warning('mqtt listener not initialized. Nothing will happen.')


def _pingpong(msg, topic):

    publish('pongs')


class ABCDHandler(logging.Handler):

    def __init__(self, level: int or str = 0) -> None: # type: ignore
        super().__init__(level)
        self.name = name

    def emit(self, record: logging.LogRecord):
        
        try:
            publish(f'logs/{record.name}', 
                    {'level': record.levelname, 'msg': record.msg})
        except Exception:
            self.handleError(record)