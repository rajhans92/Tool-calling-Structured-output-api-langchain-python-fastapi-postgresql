from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.tools import tool
from dotenv import load_dotenv
from app_without_structure_output.helpers.config import (
    LLM_MODEL
)
import asyncio
from app_without_structure_output.schema.toolCalling import ExecutionPlan 
load_dotenv()

class AIController:
    def __init__(self):
        self.model = init_chat_model(LLM_MODEL)
        self.tools = [self.search_hotels, self.get_weather]
        self.toolSet = {"search_hotels":self.search_hotels, "get_weather":self.get_weather}
        self.model_with_tools = self.model.bind_tools(self.tools)
    
    @tool
    async def search_hotels(city: str, budget: int) -> dict:
        """Search hotels in a given city within a budget."""
        return {"hotels": [f"{city} Hotel A", f"{city} Hotel B"], "budget": budget}


    @tool
    async def get_weather(city: str) -> dict:
        """Get current weather for a city."""
        return {"city": city, "weather": "sunny"}
    
    def parseUserData(self, message: str):
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an AI planning agent. Decide which tools to call based on user query."),
                ("user", "{user_input}")
            ])

            chain = prompt | self.model_with_tools

            response = chain.invoke({"user_input": message})
            # print("LLM Response: ", response.tool_calls)  # Debugging line to see the raw response
            return response.tool_calls  # contains tool_calls if any

        except Exception as e:
            raise Exception("Error parsing user data: " + str(e))

    async def executeTool(self, plan):
        tasks = []
        if not plan:
            return {}
        else:
            for step in plan:
                tool_name = step["name"]
                args = step["args"]

                func = self.toolSet.get(tool_name)
                if not func:
                    continue

                tasks.append(func.ainvoke(args))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            return results

    def callLLM(self, userQuery, toolData: dict):
        propmpt = PromptTemplate(
            input_variables=["toolData", "userQuery"],
            template="""You are an AI travel assistant.

                    Your job is to generate a clear, helpful, and accurate response using the provided tool data.

                    ---

                    ### USER QUERY:
                    {userQuery}

                    ---

                    ### TOOL OUTPUTS:
                    {toolData}

                    ---

                    ### INSTRUCTIONS:

                    - Use ONLY the provided tool data
                    - Do NOT make up information
                    - If data is missing, clearly say so
                    - Provide a well-structured response
                    - Be concise but informative
                    - Format response in a user-friendly way
                    - Include:
                    - Key recommendations
                    - Cost summary (if available)
                    - Important notes (weather, timing, etc.)

                    ---

                    ### RESPONSE FORMAT:

                    - Summary of the plan
                    - Key details (flights, hotels, weather, etc.)
                    - Suggestions or improvements
                    - Final recommendation

                    ---

                    ### IMPORTANT RULES:

                    - Do NOT mention tools or APIs
                    - Do NOT explain internal logic
                    - Do NOT hallucinate missing data
                    - Only use facts from tool outputs

                    ---

                    Now generate the final response."""
        )
        llmCallReturn = self.model.invoke(propmpt.format(toolData=toolData, userQuery=userQuery))
        return llmCallReturn.content


