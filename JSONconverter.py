import json


class JSONtoLIST:

    def insert(self, JSON):
        print(list(JSON.keys()))
        ans = ""
        values = []
        for key, value in JSON.items():
            if value is not None:
                ans += key + ", "
                values.append(value)
        ans = ans[:-2]
        return ans, values

    def update(self,JSON):
        values = []
        for key, value in JSON.items():
            if value is not None:
                values.append(key +"='"+value+"'")
        return values
