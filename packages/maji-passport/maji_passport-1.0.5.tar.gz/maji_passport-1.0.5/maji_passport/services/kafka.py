from enum import Enum
import json
from django.conf import settings
from loguru import logger

from confluent_kafka import Consumer, Producer

from maji_passport.models import PassportUser
from maji_passport.services.passport import PassportService
from maji_passport.utils import invalidate_cache, format_cache_prefix

from maji_passport.serializers.kafka import KafkaUpdateUserSerializer


class KafkaService:
    def __init__(self):
        self.config = {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVER,
            "security.protocol": settings.KAFKA_SECURITY_PROTOCOL,
            "sasl.username": settings.KAFKA_SASL_USERNAME,
            "sasl.mechanisms": settings.KAFKA_SASL_MECHANISM,
            "session.timeout.ms": settings.KAFKA_SESSION_TIMEOUT_MS,
            "sasl.password": settings.KAFKA_SASL_PASSWORD,
        }

        self.topic = settings.PASSPORT_KAFKA_INTERNAL_SERVER_TOPIC

    def _decode_message(self, msg):
        return msg.value().decode("utf-8")

    def process_message(self, msg):
        """
        Business logic for consuming messages
        """
        try:
            data = self._decode_message(msg)
        except UnicodeDecodeError as e:
            logger.error(e)
            return

        logger.info(f"Received message: {data}")
        try:
            data = json.loads(data)
        except ValueError as e:
            logger.error(e)
            return
        action_service = MessageActionService(**data)
        action = data.get("action", None)
        if action == MessageActionService.Action.LOGOUT.value:
            action_service.logout()
        elif action == MessageActionService.Action.UPDATE_USER_INFO.value:
            action_service.update_user()
        elif action == MessageActionService.Action.UPDATE_REFRESH_TOKEN.value:
            action_service.refresh_token()
        else:
            logger.warning("Unhandled action")

    def consume_messages(self):
        """
        Default part of flow for python consumer
        """
        config = self.config

        config["group.id"] = settings.KAFKA_GROUP_ID
        config["auto.offset.reset"] = "earliest"

        # creates a new consumer and subscribes to your topic
        consumer = Consumer(config)
        consumer.subscribe([self.topic])
        try:
            while True:
                # consumer polls the topic and prints any incoming messages
                msg = consumer.poll(1.0)
                if msg is not None and msg.error() is None:
                    self.process_message(msg)
        except KeyboardInterrupt as e:
            logger.error(e)
            raise e
        finally:
            consumer.close()

    def produce_message(self, kafka_message):
        """
        Produce message to message queue. Need to implement it on a client side
        """
        producer = Producer(self.config)

        producer.produce(self.topic, value=kafka_message)
        logger.info(f"Produced message to topic {self.topic}: value = {kafka_message}")

        # send any outstanding or buffered messages to the Kafka broker
        producer.flush()


class MessageActionService:
    class Action(Enum):
        LOGOUT = "logout"
        UPDATE_USER_INFO = "update_user_info"
        UPDATE_REFRESH_TOKEN = "update_refresh_token"

    def __init__(
        self,
        action: Action,
        uuid: str,
        description: str = "",
        extra=None,
    ):
        if extra is None:
            extra = {}
        self.action = action
        self.uuid = uuid
        self.description = description
        self.extra = extra
        self.passport = PassportUser.objects.filter(passport_uuid=uuid).first()

    def logout(self):
        """
        Action need to process after getting request for logout from a client side
        """
        if self.passport:
            logger.info(f"Consumer's message to logout: uuid - {self.uuid}")
            passport_service = PassportService(self.passport)
            passport_service.invalidate_access_tokens()
            logger.info(f"Tokens was invalidated: uuid - {self.uuid}")

    def update_user(self):
        if self.passport:
            if not self.passport.argo_user:
                logger.warning(
                    f"Argo user doesn't exist for passport - {self.passport}"
                )
                return None
            if self.extra.get("username") and not self.passport.argo_user.display_name:
                self.extra["display_name"] = self.extra["username"]

            logger.info(f"Consumer's message to update_user: " f"uuid - {self.uuid}")
            serializer = KafkaUpdateUserSerializer(
                self.passport.argo_user, data=self.extra, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                logger.info(f"Model user: {self.passport.argo_user}")
                # todo check about duplication
                try:
                    user = serializer.update(self.passport.argo_user, self.extra)
                    cache_key = format_cache_prefix(
                        settings.AUTH_USER_API_CACHE, user.id
                    )
                    invalidate_cache(cache_key)

                except BaseException as e:
                    raise e
                logger.info(
                    f"Model user was updated: {user}, "
                    f"user was updated: uuid - {self.uuid}"
                )
            else:
                logger.warning(f"Passport doesn't exist for user - {self.uuid}")
        else:
            logger.warning(f"Passport doesn't exist - {self.uuid}")

    def refresh_token(self):
        # deprecated. We don't use refresh token with Passport v2
        if self.passport and self.extra.get("refresh_token"):
            self.passport.refresh_token = self.extra.refresh_token
            self.passport.save()
            logger.info(f"Passport refresh token was updated: {self.passport}, ")
        else:
            logger.warning(f"Passport doesn't exist - {self.uuid}")
