import requests
import json
import time

from aura_tools.llm.base.llm_base_client import LLMBaseClient


class DeepSeekClient(LLMBaseClient):
    def __init__(self, api_key, model="deepseek-chat", max_retries=3, retry_interval=60):
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.base_url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def send_request(self, messages, stream=False):
        """
        发送请求到DeepSeek大模型
        :param messages: 消息列表
        :param stream: 是否使用流式传输
        :return: 请求结果
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Request failed with status code {response.status_code}")
            except Exception as e:
                retries += 1
                if retries < self.max_retries:
                    print(
                        f"Request failed: {str(e)}. Retrying in {self.retry_interval} seconds... (Attempt {retries}/{self.max_retries})")
                    time.sleep(self.retry_interval)
                else:
                    raise Exception(f"Request failed after {self.max_retries} retries: {str(e)}")

    def parse_result(self, response):
        """
        解析请求返回的结果，提取assistant的回答内容
        :param response: 请求返回的JSON响应
        :return: 解析出的结果
        """
        try:
            result = response['choices'][0]['message']['content']
            return result
        except (KeyError, IndexError) as e:
            print(f"Error parsing result: {str(e)}")
            return None


if __name__ == '__main__':
    api_key = "YOUR_API_KEY"

    client = DeepSeekClient(api_key, model="deepseek-chat", max_retries=3, retry_interval=60)

    messages = [
        {"role": "user", "content": "你是谁"}
    ]
    try:
        response = client.send_request(messages)
        result = client.parse_result(response)
        print(result)
    except Exception as e:
        print(f"请求失败：{str(e)}")