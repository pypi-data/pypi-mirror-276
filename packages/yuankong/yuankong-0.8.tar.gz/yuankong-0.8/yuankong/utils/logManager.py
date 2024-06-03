import os
import json
import requests

import yuankong


class LogManager:
    def __init__(self, usr_id, agent_id, task_id, bucket):
        # self.path = os.path.join(usr_id, agent_id, 'milestone.log')
        self.usr_id = usr_id
        self.agent_id = agent_id
        self.task_id = task_id
        self.path = f"{usr_id}/{agent_id}/{task_id}/milestone.log"
        self.bucket = bucket

        self.milestones = []
        self.cnt = 0

    def append(self, attr, content):
        if hasattr(self, attr):
            raise f"{attr} has already existed!"
        setattr(self, attr, {'content': content, 'state': 'waiting', 'attr': attr, 'path': '', 'url': ''})

    def init_milestones(self, milestones):
        self.cnt = 0
        self.milestones = []
        for m in milestones:
            self.milestones.append(
                {'attr': "", "content": m, "state": 'waiting', 'path': "", 'url': ""}
            )

    def start(self):
        self.milestones[0]['state'] = 'running'
        self.send()

    def next(self, path="", url="", case={}, request_data={}, rsp={}, model='GPT-3.5', **kwargs):
        self.milestones[self.cnt]['state'] = 'done'
        self.milestones[self.cnt]['path'] = path
        self.milestones[self.cnt]['url'] = url
        self.milestones[self.cnt]['case'] = case
        self.milestones[self.cnt]['request_data'] = request_data
        self.milestones[self.cnt]['rsp'] = rsp
        self.milestones[self.cnt]['model'] = model
        self.milestones[self.cnt].update(kwargs)
        self.cnt += 1

        if self.cnt < len(self.milestones):
            self.milestones[self.cnt]['state'] = 'running'
        self.send()

    def err(self, path="", **kwargs):
        for _ in range(self.cnt, len(self.milestones)):
            self.milestones[self.cnt]['state'] = 'error'
            self.milestones[self.cnt]['path'] = path
            self.milestones[self.cnt].update(kwargs)
            self.cnt += 1
        self.send()

    def send(self):
        json_str = json.dumps(self.milestones)
        rsp = self.bucket.write(self.path, json_str)

        task_json = {
            'taskid': self.task_id,
            'agentid': self.agent_id,
            'usrid': self.usr_id,
            'from_wuying': True
        }
        rsp = requests.post(url=f"{yuankong.agent_url}/GetTaskLog", json=task_json)

        return rsp


if __name__ == "__main__":
    json_str = [
        {
            "attr": str,
            "content": str,
            "state": str ["waiting", "running", "error", "done"],
            "path": str,
            "url": str,
            "case": {
                "content": [
                    {
                        'type': str ["text", "image", "video"],
                        "text": str,
                        "image": "base64 encode",
                        "video": ""
                    }
                ]
            },
            "request_data": {"question": "Hey, how are you?"},
            "rsp": {
                "text": "Hello! I'm just a text-based AI here to assist you. How can I help you today? If you have a specific blog content and associated comments for me to analyze, please provide them, and I'll be happy to help with your request.",
                "question": "Hey, how are you?",
                "chatId": "529f6baa-a41b-4cac-95da-b60bec401cce",
                "chatMessageId": "ffad0464-0ff7-4be5-bb2e-07a89b4336b0"
            },
            "model": ""
        }
    ]
