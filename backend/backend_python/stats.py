from fastapi import FastAPI
import requests 

app = FastAPI


javaBackendUrl = "http://localhost:8080/getallbyuser"


@app.get("/stats")
def getStats(User):
    try:
        response = requests.get(javaBackendUrl)

        # 200 means connected
        if response.status_code != 200: 
            return{"error": "Java backend error", "status": response.status_code}
        
        data = response.json()

        return data
    
    except requests.RequestException as e:
        return {"error": "Failed to connect to java backend server", "detail": str(e)}

