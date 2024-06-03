import json

class Message:
    def __init__(self, service, event, time, bucket, request_id, host_id):
        self.service = service
        self.event = event
        self.time = time
        self.bucket = bucket
        self.request_id = request_id
        self.host_id = host_id

    def to_dict(self):
        return {
            "Service": self.service,
            "Event": self.event,
            "Time": self.time,
            "Bucket": self.bucket,
            "RequestId": self.request_id,
            "HostId": self.host_id
        }

    def __str__(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)
