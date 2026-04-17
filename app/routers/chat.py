from fastapi import APIRouter, HTTPException, Depends
from app.schema.toolCalling import HeaderDetail, RequestBody
from app.helpers.middleware import get_header_details

router = APIRouter(prefix="/toolcalling", tags=["toolcalling"])

@router.post("/call")
async def tool_calling(request :RequestBody, getHeaderDetail: HeaderDetail = Depends(get_header_details)):
    try:

        return {
            "status": "success",
            "message": f"Tool calling endpoint is working fine {getHeaderDetail['userId']}! You sent the message: {request.message}"
        }
    except Exception as e:
        raise HTTPException( status_code=500, detail="The AI service failed to process the request. Please try again later." )