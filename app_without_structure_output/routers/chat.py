from fastapi import APIRouter, HTTPException, Depends
from app.schema.toolCalling import HeaderDetail, RequestBody
from app.helpers.middleware import get_header_details
from app.ai.aiController import AIController

llmModel = AIController()

router = APIRouter(prefix="/toolcalling", tags=["toolcalling"])

@router.post("/call")
async def tool_calling(request :RequestBody, getHeaderDetail: HeaderDetail = Depends(get_header_details)):
    try:
        structuredReturn = llmModel.parseUserData(request.message)
        toolDataReturn = await llmModel.executeTool(structuredReturn)
        llmCallReturn = llmModel.callLLM(request.message,toolDataReturn)
        return {
            "status": "success",
            "message": f"T{llmCallReturn}"
        }
    except Exception as e:
        print("Error in tool calling: ", str(e))
        raise HTTPException( status_code=500, detail="The AI service failed to process the request. Please try again later." )