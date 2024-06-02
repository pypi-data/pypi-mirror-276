import typing
import types

import json
import subprocess
import io
import os

class AppError(Exception):
    pass

class LoadError(Exception):
    pass

class App:
    def __init__(self, launchArgs:typing.List[str]) -> None:
        self.launchArgs = launchArgs
        
    def __call__(self, *args:typing.List[any]) -> any:
        proc = subprocess.Popen(args=self.launchArgs, 
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        
        argJSON = json.dumps(args)
        
        stdout:io.BytesIO = None
        stderr:io.BytesIO = None
        out, error = proc.communicate(argJSON.encode())
        
        out = out.decode()
        error = error.decode().strip()
        
        if error:
            raise AppError("app error when running:" + "\n" + error)
        
        
        try:
            return json.loads(out)
        except json.JSONDecodeError as e:
            raise AppError("bad return from app: {}".format(out)) from e

def loadPackage(path:str) -> App:
    try:
        with open(path) as f:
            data = json.load(f)
        format = {
            "app_dir": os.path.join(os.path.dirname(path), data["app_dir"])
        }
        
        arguments = data["launch"]
        for index, argument in enumerate(arguments):
            arguments[index] = argument.format(**format)
            
        return App(arguments)
        
    except Exception as e:
        raise LoadError("fail to load the package:") from e

def entry(f:types.FunctionType) -> types.FunctionType:
    def wrapped() -> None:
        import sys
    
        logger = open("nul", "w+")
        stdout = sys.stdout
        sys.stdout = logger
    
        args = json.load(sys.stdin)
        result = f(*args)
        stdout.write(json.dumps(result))
    
        sys.stdout = stdout
    
    wrapped()
    
    return wrapped