import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import COLLABORATOR_PROMPT

load_dotenv()

class CollaboratorAgent:
    def __init__(self):
        self.client = OpenAI()
        
    def generate_section(self,section,context):  
        """
        Generate a medical report section based on the provided context.
        
        Args:
            section (str):Section name(e.g., "Patient History")
            context (str): context from the transcript
        Returns:
            str: Generated section content
        """
        try:
            #Format the prompt with section and context
            prompt = COLLABORATOR_PROMPT.format(section=section, context=context)
            #Get response from GPT
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system","content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Section generation failed: {str(e)}")
    def validate_section(self,section_content):
        """
        Validate the generated section content.
        
        Args:
            section_content (str): Generated section content
        Returns:
            bool: True if valid
        """
        if not section_content:
            raise ValueError("Section content is empty.")
        if len(section_content) < 10:
                raise ValueError("Section content is too short.")
        return True
    def format_section(self,section_name,content):
        """
        Format the section with proper headers and structure.
            
        Args:
            section_name (str): Name of the section
            content (str): Content of the section
        Returns:
            str: Formatted section
        """
        return f"""
{section_name}     
{'=' * len(section_name)}
{content}
""" 