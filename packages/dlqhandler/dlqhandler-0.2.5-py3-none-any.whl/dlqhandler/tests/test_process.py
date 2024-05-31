import unittest
import json
from unittest.mock import patch, MagicMock
from dlqhandler.services.process import ProcessMessage

class TestProcessMessage(unittest.TestCase):

    @patch('dlqhandler.services.cloudwatch.CloudWatch')
    @patch('dlqhandler.dataprovider.sqs_queue.SQSQueue')
    @patch('dlqhandler.dataprovider.send_to_aws_sqs.SendToAwsSqs')
    @patch('boto3.client')
    def setUp(self, MockBotoClient, MockSendToAwsSqs, MockSQSQueue, MockCloudWatch):
        # Mock boto3 client
        self.mock_boto_client = MockBotoClient.return_value

        self.mock_sqs_queue = MockSQSQueue.return_value
        self.mock_cloudwatch = MockCloudWatch.return_value
        self.mock_send_to_aws_sqs = MockSendToAwsSqs.return_value
        self.env = MagicMock()
        self.env.region_name = 'us-east-1'
        self.handler = ProcessMessage(
            dlq_queue_url='test-dlq-queue-url',
            original_queue_url='original-queue-url',
            max_attempts=5,
            region_name='us-east-1',
            env=self.env,
            nome_lambda='test-lambda',
            namespace='test-namespace'
        )

    def test_process_messages_no_messages(self):
        self.mock_sqs_queue.receive_messages_dlq.return_value = []
        result = self.handler.execute()
        self.assertEqual(result['message'], 'No messages to process')
        #self.mock_sqs_queue.receive_messages_dlq.assert_called_once()
        self.mock_cloudwatch.count.assert_not_called()
        self.mock_send_to_aws_sqs.send_message_to_queue.assert_not_called()  

    def test_process_messages_below_max_attempts(self):
        message_body = json.dumps({
            "Attributes": {
                "processamento_tentativas": 2
            }
        })
        
        self.mock_sqs_queue.receive_messages_dlq.return_value = [(message_body)]
        self.mock_send_to_aws_sqs.send_message_to_queue.return_value = {}

        result = self.handler.execute()
        print(f"test result 01", result)    
        self.assertEqual(result['message'], 'Mensagem reenviada para fila')
        self.assertEqual(result['sqs']['Attributes']['processamento_tentativas'], 3)
        #self.mock_sqs_queue.receive_messages_dlq.assert_called_once()
        #self.mock_send_to_aws_sqs.send_message_to_queue.assert_called_once()
        self.mock_cloudwatch.count.assert_any_call("reprocessamento_quantidade", 1)
        self.mock_sqs_queue.delete_message_dlq.assert_called_once_with('handle1')

    def test_process_messages_exceed_max_attempts(self):
        message_body = json.dumps({
            "Attributes": {
                "processamento_tentativas": 6
            }
        })
        self.mock_sqs_queue.receive_messages_dlq.return_value = [(message_body, 'handle1')]

        result = self.handler.execute()
        print(f"test result 01", result)
        self.assertEqual(result['message'], 'Mensagem reenviada para fila')
        self.assertEqual(result['sqs']['Attributes']['processamento_tentativas'], 6)
        self.mock_sqs_queue.receive_messages_dlq.assert_called_once()
        self.mock_send_to_aws_sqs.send_message_to_queue.assert_not_called()
        self.mock_cloudwatch.count.assert_any_call('maximo_reprocessamento_alcancada', 6)
        self.mock_sqs_queue.delete_message_dlq.assert_called_once_with('handle1')    

if __name__ == '__main__':
    unittest.main()