import requests
import random
import os
import re


def lambda_handler(event, context):
    token = os.environ['TOKEN']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chat_id = event["message"]["chat"]["id"]

    def pick_lottery_numbers(text):
        nums = [re.sub('[^0-9]', "", x) for x in text]
        if any(not x.isnumeric() for x in nums):
            data = "Input should be numbers"
            return data
        nums = list(map(int, nums))
        if len(nums) > 6:
            data = "Pick less than 6 numbers"
        elif any(x > 45 or x < 1 for x in nums):
            data = "All numbers must be less than 45 and greater than 0"
        else:
            remaining = 6 - len(nums)
            sample = random.sample(range(1, 46), remaining) + nums
            sample.sort()
            data = " ".join(list(map(str, sample)))
        return data

    text = event["message"]["text"].split(',')
    data = pick_lottery_numbers(text)
    data = {"chat_id": chat_id, "text": data}
    requests.post(url=url, data=data)

    return {
        'statusCode': 200
    }
