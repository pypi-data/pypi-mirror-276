import inspect
import json
import os
import random
import time

import paho.mqtt.client as mqtt

from fz_logger.fz_logger import Logger


class MqttClient(Logger):
    def __init__(
        self,
        config: dict,
    ):
        super().__init__(
            level=config["logger"]["level"],
            save_path=config["logger"]["save_path"],
        )
        self.pub_topic, self.sub_topic, self.qos = (
            config["mqtt"]["pub-topic"],
            config["mqtt"]["sub-topic"],
            config["mqtt"]["qos"],
        )
        self.logger.info(f"{self.pub_topic}, {self.sub_topic}, {self.qos}")
        self.client = mqtt.Client()
        self.client.username_pw_set(config["mqtt"]["id"], config["mqtt"]["pw"])

        self.qos = int(self.qos)
        self.broker_ip = config["mqtt"]["host"]
        self.broker_port = int(config["mqtt"]["port"])

        self.listener = {}
        self.max_delay = 30
        self.initial_delay = 1.0
        self.factor = 2.7182818284590451
        self.jitter = 0.119626565582
        self.delay = self.initial_delay

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.connect(self.broker_ip, self.broker_port)

    def connect(self, ip, port):
        try:
            self.client.connect(ip, port, keepalive=60)
        except Exception as e:
            self.logger.error(f"{inspect.currentframe().f_code.co_name} - {e}")
            self.reconnect()

    def reconnect(self):
        while True:
            try:
                self.delay = self.delay * self.factor
                if self.delay > self.max_delay:
                    self.delay = self.initial_delay
                self.delay = random.normalvariate(
                    self.delay,
                    self.delay * self.jitter,
                )
                time.sleep(self.delay)
                self.client.reconnect()
                self.logger.warning("mqtt reconnect")
                break
            except Exception as e:
                self.logger.info(f"{inspect.currentframe().f_code.co_name} - {e}")

    def add_listener(self, func):
        self.listener.update({self.sub_topic: func})

    def remove_listener(self, topic):
        if topic in self.listener:
            del self.listener[topic]

    def on_connect(self, client, userdata, flags, return_code):
        self.logger.info("Connected with result code: %s", str(return_code))

    def on_disconnect(self, client, userdata, reture_code):
        self.logger.info("Disconnected with result code: %s", reture_code)
        self.reconnect()

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.logger.info("subscribed: %s - %s", str(mid), str(granted_qos))

    def on_message(self, client, userdata, msg):
        if msg.topic in self.listener:
            self.listener[msg.topic](json.loads(msg.payload.decode("utf-8")))

    def pub_message(self, topic, msg):
        try:
            self.client.loop_start()
            msg = json.dumps(msg, indent=4)
            if self.client.is_connected():
                if msg is not None:
                    self.client.publish(topic, msg)
                    self.logger.info(f"{msg}")
                else:
                    pass
                    self.logger.warning("pub data is None")
            else:
                self.reconnect()

        except Exception as e:
            self.logger.error(f"{inspect.currentframe().f_code.co_name} - {e}")

    def sub_message(self):
        self.add_listener(self.mqtt_callback)
        self.client.loop_forever()
