import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SUPERVISOR_PROMPT

load_dotenv()

class SupervisorAgent:
    def __init__(self):
        self.client = OpenAI()
        self.sections = [
            "Patient History", 
            "Diagnosis Summary", 
            "Treatment Plan", 
            "Follow-up instructions"
            ]
    def analyze_transcript(self, transcript):
        """
        Analyze transcript and break it down into sections.
        
        Args:
            transcript (str): Raw transcript text
        Returns:
            dict: Structured braek down of sections
        
        """
        try:
            #Get Initial analysis from the GPT
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system","content": SUPERVISOR_PROMPT},
                    {"role": "user","content": transcript}
                ],
                temperature=0.3
            )
            #Extract the analysis
            analysis = response.choices[0].message.content
            #Structure the analysis into sections
            structured_analysis = self.structure_analysis(analysis)
            return structured_analysis
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
        
    def _structure_analysis(self, analysis):
        """Structure the analysis into defined sections.
        Args:
            analysis (str): Raw analysis text
        Returns:
            dict: Structured sections
        """
        structured={}
        current_section = None
        current_content = []
        
        #Split Analysis into lines
        lines = analysis.split("\n")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            #Check if line is a section header
            if any(section in line for section in self.sections):
                #Save previous section if exists
                if current_section:
                    structured[current_section]='\n'.join(current_content)
                    
                    #start new section
                    current_section = next(section for section in self.sections if section in line)
                    current_content=[]
                else:
                    #Add content to current_section
                    if current_section:
                        current_content.append(line)
        #Save last section
        if current_section:
            structured[current_section]='\n'.join(current_content)
        return structured
    def validate_analysis(self, structured_analysis):
        """   
        validate that all required section are present.
        Args:
            structured_analysis (dict): Structured analysis
        Returns:
            bool: True if valid
        """
        missing_sections = [section for section in self.sections if section not in structured_analysis]
        if missing_sections:
            raise ValueError(f"Missing required sections: {', '.join(missing_sections)}")   
        return True 