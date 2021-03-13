class PipelineBuilder:
    def __init__(self):
        self._pipeline = []

    def match(self, data: dict):
        self._pipeline.append({"$match": data})
        return self

    def group(self, data: dict):
        self._pipeline.append({"$group": data})
        return self

    def unwind(self, data: dict):
        self._pipeline.append({"$unwind": data})
        return self

    def lookup(self, data: dict):
        self._pipeline.append({"$lookup": data})
        return self

    def addFields(self, data: dict):
        self._pipeline.append({"$addFields": data})
        return self

    def project(self, data: dict):
        self._pipeline.append({"$project": data})
        return self

    def build(self):
        return self._pipeline
