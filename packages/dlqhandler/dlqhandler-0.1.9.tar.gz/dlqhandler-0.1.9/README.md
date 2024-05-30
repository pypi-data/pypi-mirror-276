# DLQ Handler Library

A library for handling DLQ (Dead Letter Queue) messages in AWS SQS. This library allows you to reprocess messages from a DLQ with specified parameters such as the queue URL, original queue URL, and maximum number of attempts.

## Installation

To install the library, use `pip`:

```sh
pip install dlq_handler_lib

from dlq_handler_lib import DLQHandler

# Initialize the DLQHandler with the required parameters
handler = DLQHandler(
    dlq_queue_url='https://sqs.us-east-1.amazonaws.com/123456789012/my-dlq',
    original_queue_url='https://sqs.us-east-1.amazonaws.com/123456789012/my-queue',
    max_attempts=5,
    region_name='us-east-1',
    env=my_env_config,  # replace with your actual environment config
    nome_lambda='lambda-reprocessamento-dlq',
    namespace='DLQ-Mensageria'
)

# Process the messages from the DLQ
handler.process_messages()
