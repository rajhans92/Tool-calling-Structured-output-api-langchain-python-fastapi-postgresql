from fastapi import APIRouter, HTTPException, Depends
from app_without_structure_output.schema.toolCalling import HeaderDetail, RequestBody
from app_without_structure_output.helpers.middleware import get_header_details
from app_without_structure_output.ai.aiController import AIController

llmModel = AIController()

router = APIRouter(prefix="/toolcalling", tags=["toolcalling"])

@router.post("/call")
async def tool_calling(request :RequestBody, getHeaderDetail: HeaderDetail = Depends(get_header_details)):
    try:
        structuredReturn = llmModel.parseUserData(request.message)
        toolDataReturn = await llmModel.executeTool(structuredReturn)
        print("Tool Data Return: ", toolDataReturn)  # Debugging line to see the tool data return
        llmCallReturn = llmModel.callLLM(request.message,toolDataReturn)
        return {
            "status": "success",
            "message": f"T{llmCallReturn}"
        }
    except Exception as e:
        print("Error in tool calling: ", str(e))
        raise HTTPException( status_code=500, detail="The AI service failed to process the request. Please try again later." )