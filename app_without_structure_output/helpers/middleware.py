from fastapi import Header, HTTPException
from app.schema.toolCalling import HeaderDetail

def get_header_details(header: HeaderDetail= Header(...)):
    try:
        userId = header.userId
        return {"userId": userId}
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid User Session")