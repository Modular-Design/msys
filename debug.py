import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.msys.test:app", port=9000, reload=True)
