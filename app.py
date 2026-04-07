import streamlit as st
import os
from dotenv import load_dotenv
from transcriber import Transcriber
from supervisor_agent import SupervisorAgent
from collaborator_agent import CollaboratorAgent
from prompts import ERROR_PROMPT

# Load environment variables
load_dotenv()

# Initialize agents
transcriber = Transcriber()
supervisor=SupervisorAgent()
collaborator=CollaboratorAgent()

def main():
    st.title("AI Medical Report Generator Assistant")
    st.write("Upload an audio file or Enter a transcrript to generate a structured medical report.")
 
    # File Upload
    audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])   
    
    # Text Input
    transcript_text = st.text_area("Or Enter Transcript Text:",height=200)
    
    if st.button("Generate Medical Report"):
        try:
            # Get Transcript
            if audio_file:
                # Validate audio file
                transcriber.validate_audio(audio_file)
                #Show processing message
                with st.spinner("Transcribing audio..."):
                    transcript = transcriber.transcribe(audio_file)
            elif transcript_text:
                transcript = transcript_text
            else:
                st.error("Please Upload an audio file or enter transcript text.")
                return
            #Display transcript
            st.subheader("Transcript")
            st.write(transcript)
            # Analyze Transcript
            with st.spinner("Analyzing transcript..."):
                structured_analysis = supervisor.analyze_transcript(transcript)
                supervisor.validate_analysis(structured_analysis)
            # Generate Sections
            with st.spinner("Generating medical report sections..."):
                final_report = []
                for section,context in structured_analysis.items():
                    section_content = collaborator.generate_section(section, context)
                    collaborator.validate_section(section_content)
                    
                    #formatted section
                    formatted_section = collaborator.format_section(section, section_content)
                    final_report.append(formatted_section)
                    
                #Display Final Report
                st.subheader("Generated Medical Report")
                st.write("".join(final_report))
                
                #Add download button
                report_text = "".join(final_report)
                st.download_button(
                    label="Download Report",
                    data=report_text,
                    file_name="medical_report.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(ERROR_PROMPT.format(error=str(e)))
            
if __name__ == "__main__":
    main()