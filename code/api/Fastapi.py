import nest_asyncio
import uvicorn

nest_asyncio.apply() 

uvicorn.run(app, host="127.0.0.1", port=8000)
