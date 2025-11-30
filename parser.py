from collections import Counter
import requests

Errors_Status = {
    400 : "Плохой запрос",
    401 : "Unauthorized",
    403 : "Forbidden",
    404 : "Не найдено"
}


def status_decorator(func):
    def wrapper(self):
        try:
            res = func(self)
            if self.status_code in Errors_Status:
                raise Errors_Status[self.status_code]
            return res
        except Exception as e:
            print(e)
    return wrapper


class Parser:
    urls = []

    def __init__(self, url):
        self.urls.append(url)
        self.status_code = None

    @status_decorator
    def parse(self):
        if not self.urls:
            return "Done!"
        
        response = requests.get(self.urls.pop())
        self.status_code = response.status_code

        #if response.status_code == 200: 
        dict = response.json()
        list_users = [post.get("userId") for post in dict]
        return list_users

class DataManager:
    def Count_posts(self, list_users):
        count = Counter(list_users)
        result = ""
        for userid, posts in count.items():
            result += f"userid({userid})   count: {posts}\n"
        return result


parser = Parser("https://jsonplaceholder.typicode.com/posts")
data = parser.parse()
manager = DataManager() 
print(manager.Count_posts(data))