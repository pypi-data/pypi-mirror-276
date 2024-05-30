import json
import logging
from dlqhandler.dataprovider.send_to_aws_sqs import SendToAwsSqs
from .cloudwatch import CloudWatch
from dlqhandler.dataprovider.sqs_queue import SQSQueue

ERROR_STATUS = "ERRO"
ERROR_MESSAGE = "Número de retentativas excedido"
REPROCESSING_STATUS = "REPROCESSANDO"
ATTEMPTS_KEY = "processamento_tentativas"
STATUS_KEY = "processamento_status"
MESSAGE_KEY = "processamento_mensagem"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ProcessMessage:
    def __init__(self, dlq_queue_url, original_queue_url, max_attempts=5, region_name='us-east-1', env=None, 
                 nome_lambda='lambda-reprocessamento-dlq', namespace='DLQ-Mensageria'):
        self.dlq_queue = SQSQueue(dlq_queue_url, region_name)
        self.original_queue_url = original_queue_url
        self.max_attempts = max_attempts
        self.cloudwatch = CloudWatch(env, nome_lambda, namespace)
        self.env = env

    def execute(self):
        messages = self.dlq_queue.receive_messages_dlq()
        
        if not messages:
            return {'message': 'No messages to process'}

        for body, receipt_handle in messages:
            message = json.loads(body)
            logger.info(f"Processing message: {message}")

            attempts = int(message.get('Attributes', {}).get(ATTEMPTS_KEY, 0))
            logger.info(f"processamento_tentativas: {attempts}")
            if attempts > self.max_attempts:
                self.set_status(message, ERROR_STATUS, ERROR_MESSAGE)
                self.cloudwatch.count('maximo_reprocessamento_alcancada', attempts)
                self.dlq_queue.delete_message_dlq(receipt_handle)
                logger.error(f"Máximo de retentativas alcançadas: {message}")
                
            else:
                logger.info(f"Mensagem para ser reprocessada: {message}")
                self.increment_attempts(message)
                self.set_status(message, REPROCESSING_STATUS)
                self.send_to_aws_sqs(self.env, message)
                self.count_retry_metric(message)

            self.dlq_queue.delete_message_dlq(receipt_handle)

        return {
            'message': 'Mensagem reenviada para fila',
            'sqs': message
        }

    def increment_attempts(self, message):
        message[ATTEMPTS_KEY] = message.get(ATTEMPTS_KEY, 0) + 1

    def set_status(self, message, status, msg=None):
        message[STATUS_KEY] = status
        if msg:
            message[MESSAGE_KEY] = msg

    def send_to_aws_sqs(self, env, messagebody):
        send_to_sqs = SendToAwsSqs(env)
        send_to_sqs.send_message_to_queue(json.dumps(messagebody))

    def count_retry_metric(self, message):
        self.cloudwatch.count("reprocessamento_quantidade", 1)