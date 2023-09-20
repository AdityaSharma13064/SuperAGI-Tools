from typing import Type, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from assets.base_file import BaseToolClient

# from superagi.helper.s3_helper import upload_to_s3

class WriteFileInput(BaseModel):
    """Input for CopyFileTool."""
    file_name: str = Field(..., description="Name of the file to write. Only include the file name. Don't include path.")
    content: str = Field(..., description="File content to write")


class WriteFileTool(BaseTool):
    """
    Write File tool

    Attributes:
        name : The name.
        description : The description.
        agent_id: The agent id.
        args_schema : The args schema.
        resource_manager: File resource manager.
    """
    name: str = "Write File"
    args_schema: Type[BaseModel] = WriteFileInput
    description: str = "Writes text to a file"
    agent_id: int = None
    resource_manager: Optional[BaseToolClient] = None
    session=Session()
    class Config:
        arbitrary_types_allowed = True

    def _execute(self, file_name: str, content: str):
        """
        Execute the write file tool.

        Args:
            file_name : The name of the file to write.
            content : The text to write to the file.

        Returns:
            success message if message is file written successfully or failure message if writing file fails.
        """
        
        self.resource_manager = BaseToolClient(self.session)
        
        return self.resource_manager.use_file_manager_write_file(file_name,content)
        # return self.resource_manager.write_file(file_name, content)
