from abc import ABCMeta, abstractmethod
import json
from time import sleep
from typing import List, Optional
from pydantic import BaseModel

from dalpha.backend_cli import BackendCli
from dalpha.logging import logger

class DataUpdateEvent(BaseModel):
    type: str
    timestamp: str
    payload: dict
    metadata: dict
    version: str

class S3File(BaseModel):
    url: str
    bucket: Optional[str]
    key: Optional[str]
    size: int

class DataUpdateItem(BaseModel):
    file: S3File

    def __str__(self):
        return self.model_dump_json()
    
def message_to_item(message) -> DataUpdateItem:
    payload = message.get("payload")
    return DataUpdateItem(
        file = S3File(
            url = payload.get("file").get("url"),
            bucket = payload.get("file").get("bucket"),
            key = payload.get("file").get("key"),
            size = payload.get("file").get("size"),
        )
    )

class DataUpdateConsumer(metaclass=ABCMeta):
    @abstractmethod
    def poll(self, records: int = 1, timeout_ms: int = 5000) -> List[DataUpdateItem]:
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass

class KafkaDataUpdateConsumer(DataUpdateConsumer):
    def __init__(self, api_id: int, backend_cli: BackendCli, kafka_topic: str):
        self.kafka_topic = kafka_topic
        from dalpha.kafka_cli import get_consumer
        self.kafka_consumer = get_consumer(self.kafka_topic, api_id)
        self.backend_cli = backend_cli


    def poll(self, records: int = 1, timeout_ms: int = 5000) -> List[DataUpdateItem]:
        try:
            #print(self.kafka_consumer.beginning_offsets(partitions))
            record = self.kafka_consumer.poll(
                timeout_ms=timeout_ms,
                max_records=records,
                update_offsets=False,
            )
            logger.info(f"polled record: {record}")
            sleep(10)
            
            ret = []
            # 1개만 받아온 경우
            v = record.values()
            for messages in v:
                if not isinstance(messages, list):
                    logger.error(f"unexpected kafka message format: {type(message)}")
                    break
                for message in messages:
                    try:
                        event = json.loads(message.value.decode('utf-8'))
                        ret.append(message_to_item(event))
                    except json.JSONDecodeError:
                        # TODO: 현재 로직이면 이 경우 offset skip 됨, 잘못된 동작은 아닌 듯 하나 체크 필요
                        logger.error("유효한 JSON 형식이 아닙니다.")

            return ret
        except Exception as e:
            logger.error(f"error from kafka poll\n{e}")
            return []

    def commit(self):
        try:
            self.kafka_consumer.commit()
        except Exception as e:
            print(e)
            logger.error(f"error from kafka commit\n{e}")
        
    def close(self):
        self.kafka_consumer.close()
