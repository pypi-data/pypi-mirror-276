class PythonExecutor:
    def __init__(self):
        pass

    def run(self, code):
        local_vars = {}
        try:
            exec(code, {}, local_vars)
            return local_vars
        except Exception as e:
            return str(e)
            