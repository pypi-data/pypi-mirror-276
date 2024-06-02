from dataclasses import asdict
import json
import os
from typing import List
from dalpha.logging import logger
import sentry_sdk
from dalpha.backend_cli import BackendCli
from dalpha.context import Context, get_context, set_context
from dalpha.data_update_consumer import DataUpdateItem, KafkaDataUpdateConsumer
from dalpha.logging.events import Event
from dalpha.backend_cli import slack_alert

class UpdateAgent:
    def __init__(
        self,
        kafka_topic: str,
        api_id: int = int(os.environ.get('API_ID', 0)),
        dev_server: bool = bool(os.environ.get('DEV_SERVER', 'True') == 'True')
    ):
        if not isinstance(kafka_topic, str): raise TypeError('kafka_topic is not a str')
        if not isinstance(api_id, int): raise TypeError('api_id is not a int')
        if not isinstance(dev_server, bool): raise TypeError('dev_server is not a bool')

        self.kafka_topic = kafka_topic
        self.token = os.environ['TOKEN']
        self.sentry_dsn = os.environ['SENTRY_DSN']
        if dev_server:
            self.sentry_env = "exp"
        else:
            self.sentry_env = "production"
        
        self.backend_cli = BackendCli(
            api_id = api_id,
            dev_server = dev_server,
            token = self.token
        )
        self.data_update_consumer = KafkaDataUpdateConsumer(
            api_id = api_id,
            backend_cli = self.backend_cli,
            kafka_topic = kafka_topic
        )

        set_context(Context(
            inference_id = api_id,
            service_code = kafka_topic,
            env = "exp" if dev_server else "prod"
        ))

        sentry_sdk.set_context("context",asdict(get_context()))
        sentry_sdk.init(
            dsn=self.sentry_dsn,

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
            environment = self.sentry_env
        )
        sentry_sdk.set_tag("api_id", api_id)
        sentry_sdk.set_tag("service_code", kafka_topic)
        sentry_sdk.set_tag("engineer", self.backend_cli.get_internal_slack())

    def poll(self):
        '''
        data update의 경우 kafka로부터 data update event가 담긴 메세지를 받아온다.
        '''
        ret: List[DataUpdateItem] = self.data_update_consumer.poll()
        if len(ret) == 0:
            # 가져온 메세지가 없으면 None 반환
            return None
        elif len(ret) == 1:
            # 가져온 메세지가 1개면 list 형태가 아닌 낱개로 반환
            logger.info(
                message = f"return evaluate item: {ret[0]}",
                event = Event.POLL,
                data = ret[0]
            )
            sentry_sdk.set_context("context",asdict(get_context()))
            return ret[0]
        else:
            # 가져온 메세지가 여러개면 list 형태로 반환
            logger.info(
                message = f"return evaluate item: {ret}",
                event = Event.POLL,
                data = ret
            )
            return ret
        
    def validate(self, output={}, alert = False):
        '''
        data update 파이프라인에서의 validate이라고 보면 된다.
        update가 끝난뒤 이 함수를 통해서 kafka의 offset을 commit한다.
        원한다면 slack alert를 보낼 수 있다.
        '''
        self.data_update_consumer.commit()
        logger.info(
            message = f"update completed - {output}",
            event = Event.VALIDATE,
            data = output
        )
        if alert:
            slack_alert(
                '#data-update-alarm',
                f"update_complete payload for topic: {self.kafka_topic} - result: {output}"
            )
        

    def validate_error(self, output={}, alert = False):
        '''
        data update 파이프라인에서의 validate_error이라고 보면 된다.
        update 도중 에러가 발생했을 때 이 함수를 통해서 kafka의 offset을 commit한다.
        원한다면 slack alert를 보낼 수 있다.
        '''
        self.data_update_consumer.commit()
        logger.info(
            message = f"update error - {output}",
            event = Event.VALIDATE_ERROR,
            data = output
        )
        if alert:
            slack_alert(
                '#data-update-alarm',
                f"update_error payload for topic: {self.kafka_topic} - result: {output}"
            )

    def close(self):
        self.data_update_consumer.close()