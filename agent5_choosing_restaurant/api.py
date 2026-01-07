from fastapi import FastAPI, Query
from knn import RestaurantSearchAgent
import uvicorn

app = FastAPI(title="Restaurant Discovery API")
agent = RestaurantSearchAgent("menus.jsonl")

@app.on_event("startup")
async def startup_event():
    agent.load_and_prepare_data()

@app.get("/api/recommend")
async def recommend(query: str = Query(..., description="Ví dụ: trà sữa 30000 hoặc pizza")):
    """Endpoint trả về 10 quán ăn phù hợp nhất"""
    results = agent.search(query)
    return {
        "status": "success",
        "query": query,
        "total_found": len(results),
        "data": results
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)