import requests
import json
import time

from aura_tools.llm.base.llm_base_client import LLMBaseClient


class BaiduAIClient(LLMBaseClient):
    def __init__(self, api_key, model="", max_retries=3, retry_interval=60):
        keys = api_key.split("|");
        self.api_key = keys[0]
        self.secret_key = keys[1]
        super().__init__(self.api_key, model, max_retries, retry_interval)
        self.model = model
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        response = requests.post(url, params=params)
        return str(response.json().get("access_token"))

    def send_request(self, messages):
        """
        发送请求到百度AI平台
        :param payload: 请求参数
        :return: 请求结果
        """
        payload = {
            "model": self.model,
            "messages": messages
        }
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={self.access_token}"
        headers = {'Content-Type': 'application/json'}
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                if response.status_code == 200:
                    response_json = response.json()
                    if 'error_code' in response_json and response_json['error_code'] != 0:
                        raise Exception(
                            f"Request failed with error code {response_json['error_code']}: {response_json['error_msg']}")
                    return response_json
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

    def parse_result(self, response_json):
        """
        解析返回结果中的result字段
        :param response_json: 请求返回的JSON对象
        :return: result字段的内容，或是None(如果没有result字段或response_json为None)
        """
        if response_json is None:
            return None
        return response_json.get('result')


if __name__ == '__main__':
    api_key = ""
    secret_key = ""
    client = BaiduAIClient(api_key=f"{api_key}|{secret_key}", max_retries=3, retry_interval=60)
    messages = [
        {
            "role": "user",
            "content": "你是谁"
        }
    ];
    try:
        result = client.send_request(messages)
        parsed_result = client.parse_result(result)
        print(parsed_result)
    except Exception as e:
        print(f"请求失败：{str(e)}")
