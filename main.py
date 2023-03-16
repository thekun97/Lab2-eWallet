import uvicorn
from fastapi import FastAPI

import frontend

app = FastAPI()

frontend.init(app)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
