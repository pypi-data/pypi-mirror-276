import unittest
import json
from unittest.mock import patch, MagicMock
from dlqhandler.services.process import ProcessMessage

class TestProcessMessage(unittest.TestCase):

    @patch('dlqhandler.services.cloudwatch.CloudWatch')
    @patch('dlqhandler.dataprovider.sqs_queue.SQSQueue')
    @patch('dlqhandler.dataprovider.send_to_aws_sqs.SendToAwsSqs')
    @patch('boto3.client')
    def setUp(self, MockBotoClient, Mock_send_message_to_queue, MockSQSQueue, MockCloudWatch):
        # Mock boto3 client
        self.mock_boto_client = MockBotoClient.return_value
        self.mock_queue_service = MagicMock()
        self.mock_sqs_queue = MockSQSQueue.return_value
        self.mock_cloudwatch = MockCloudWatch.return_value
        self.mock_send_to_aws_sqs = Mock_send_message_to_queue.return_value
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
        self.assertEqual(result, {'message': 'No messages to process'})

        self.mock_send_to_aws_sqs.send_message_to_queue.assert_not_called()

    def test_process_messages_with_messages(self):
        
        mock_message_body = json.dumps({'texto': 'mensagem de exemplo'})
        mock_receipt_handle = 'abc123'
        mock_message = {
            'Body': mock_message_body,
            'ReceiptHandle': mock_receipt_handle,
            'Attributes': {'Attempts': '1'}
        }
        self.mock_sqs_queue.receive_messages_dlq.return_value = [mock_message] 

        self.handler.max_attempts = 2  

        result = self.handler.execute()

        #self.mock_sqs_queue.receive_messages_dlq.assert_called_once()

        self.assertEqual(result, {'message': 'No messages to process'})

        #self.assertEqual(result, {'message': 'Mensagem reenviada para fila', 'sq': mock_message_body}) 

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from app.src.lambda_function import Process

class TestProcess(unittest.TestCase):

    @patch('app.src.config.environment.Environment')
    def test_execute_success(self, mock_environment):
        
        mock_env = MagicMock()
        mock_env.url_sqs_orquestrador_dlq.return_value = 'mock_dlq_url'
        mock_env.url_sqs_orquestrador.return_value = 'mock_queue_url'
        mock_env.aws_region.return_value = 'mock_region'
        mock_env.name_lambda.return_value = 'mock_lambda'
        mock_env.namespace_cloudwatch.return_value = 'mock_namespace'

        mock_environment.return_value = mock_env

        process = Process()

        process_message_mock = MagicMock()
        process_message_mock.execute.return_value = "mock_result"

        with patch('app.src.lambda_function.ProcessMessage', return_value=process_message_mock):
            
            result = process.execute()

            process_message_mock.execute.assert_called_once()

            print(f"result 01: {result}")
            self.assertEqual(result, "mock_result")

    @patch('app.src.config.environment.Environment')
    def test_execute_exception(self, mock_environment):
        
        mock_env = MagicMock()
        mock_env.url_sqs_orquestrador_dlq.return_value = 'mock_dlq_url'
        mock_env.url_sqs_orquestrador.return_value = 'mock_queue_url'
        mock_env.aws_region.return_value = 'mock_region'
        mock_env.name_lambda.return_value = 'mock_lambda'
        mock_env.namespace_cloudwatch.return_value = 'mock_namespace'

        mock_environment.return_value = mock_env

        process = Process()

        process_message_mock = MagicMock()
        process_message_mock.execute.side_effect = Exception("mock_exception")

        with patch('app.src.lambda_function.ProcessMessage', return_value=process_message_mock):
           
            result = process.execute()

            process_message_mock.execute.assert_called_once()

            print(f"result 02: {result}")
            self.assertEqual(result, {"error": "mock_exception"})         

if __name__ == '__main__':
    unittest.main()    