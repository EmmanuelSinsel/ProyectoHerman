import json


class JSONtoLIST:

    def insert(self, JSON):
        print(list(JSON.keys()))
        keys = list(JSON.keys())
        ans = ""
        for i in keys:
            if(not i == "where"):
                ans += i + ", "
        ans = ans[:-2]
        values = []
        for key, value in JSON.items():
            if value is not None:
                values.append(value)
        return ans, values

    def update(self,JSON):
        values = []
        for key, value in JSON.items():
            if value is not None:
                values.append(key +"='"+value+"'")
        return values
