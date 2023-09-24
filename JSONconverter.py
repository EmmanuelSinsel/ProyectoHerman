import json


class JSONtoLIST:

    def insert(self, JSON):
        keys = list(JSON.__dict__.keys())
        ans = ""
        for i in keys:
            if(not i == "where"):
                ans += i + ", "
        ans = ans[:-2]
        values = []
        for key, value in JSON:
            if value is not None:
                values.append(value)
        return ans, values

    def update(self,JSON):
        values = []
        for key, value in JSON:
            if value is not None:
                values.append(key +"='"+value+"'")
        return values
