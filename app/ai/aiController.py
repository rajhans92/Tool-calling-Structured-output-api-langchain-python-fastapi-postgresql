from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from app.helper.config import (
    LLM_MODEL
)
from app.schema.toolCalling import ExecutionPlan 
load_dotenv()

class AIController:
    def __init__(self):
        self.model = init_chat_model(LLM_MODEL)
        self.tools = []
        self.model_with_tools = self.model.with_tools(self.tools)
        self.extractor = self.model.with_structured_output(ExecutionPlan)

    def parseUserData(self, message: str):
        try:
            planner_prompt = PromptTemplate(
                input_variables=["user_input"],
                template="""
                    You are an AI planning agent.

                    Available tools:
                    - search_flights(source, destination, date)
                    - search_hotels(city, budget)
                    - get_weather(city)

                    Return ONLY JSON in this format:
                    {
                    "execution_plan": [
                        {
                        "tool": "tool_name",
                        "args": {},
                        "depends_on": []
                        }
                    ]
                    }

                    User Query: {user_input}
                    """
            )
            prompt = planner_prompt.format(user_input=message)
            plan: ExecutionPlan = self.structured_llm.invoke(prompt)
            return plan
        except Exception as e:
            raise Exception("Error parsing user data: " + str(e))

    def executeTool(structuredData: dict):
        # Implement the logic to execute the tool based on the structured data
        # This is a placeholder implementation and should be replaced with actual tool execution logic
        toolDataReturn = {
            "toolResult": f"Executed tool with data: {structuredData['parsedMessage']}"
        }
        return toolDataReturn

    def callLLM(toolData: dict):
        # Implement the logic to call the LLM (Language Model) with the tool data
        # This is a placeholder implementation and should be replaced with actual LLM calling logic
        llmCallReturn = f"LLM response based on tool data: {toolData['toolResult']}"
        return llmCallReturn


