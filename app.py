import streamlit as st
import os
import tempfile
import google.generativeai as genai
import PyPDF2
import docx
import io
import json
import re
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="LegalAssist AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini API
def initialize_gemini():
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        st.sidebar.error("Please set your Google API key in the sidebar")
        api_key = st.sidebar.text_input("Enter your Google API Key", type="password")
        if not api_key:
            return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

# Text extraction functions for different file types
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

# Extract text from uploaded document
def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        return extract_text_from_txt(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload PDF, DOCX, or TXT files.")
        return None

# Function to generate response from Gemini
def generate_response(model, prompt, input_text=None):
    try:
        if input_text:
            response = model.generate_content([prompt, input_text])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

# Define custom CSS
def local_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f5f7f9;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
        }
        .stTextArea>div>div>textarea {
            border-radius: 5px;
        }
        .sidebar .sidebar-content {
            background-color: #2c3e50;
        }
    </style>
    """, unsafe_allow_html=True)

# Main application
def main():
    local_css()
    
    # Sidebar
    st.sidebar.image("https://via.placeholder.com/150x80?text=LegalAssist", width=150)
    st.sidebar.title("LegalAssist AI")
    
    # Initialize Gemini model
    model = initialize_gemini()
    if not model:
        st.warning("Please enter a valid API key to continue")
        return
    
    # Main navigation
    app_mode = st.sidebar.selectbox(
        "Choose a service",
        ["Legal Advice", "Document Analysis", "Case Law Summarization", 
         "Argument Generator", "Citation Generator", "Bias Detection", 
         "IPC Search", "Legal Research Assistant"]
    )
    
    # Add a session state for history if it doesn't exist
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Display chat history in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Recent Activity")
    for item in st.session_state.history[-5:]:
        st.sidebar.markdown(f"**{item['service']}** - {item['timestamp']}")
    
    st.sidebar.markdown("---")
    st.sidebar.info("This application uses Google's Gemini API to provide AI-powered legal assistance. It is intended as a tool to assist legal professionals and should not replace professional legal advice.")
    
    # Legal Advice Section
    if app_mode == "Legal Advice":
        st.title("Legal Advice Assistant")
        st.write("Get AI-powered legal advice based on your situation.")
        
        legal_area = st.selectbox(
            "Select area of law",
            ["General", "Corporate", "Criminal", "Civil", "Family", "Property", "Intellectual Property", "Labor", "Tax"]
        )
        
        user_query = st.text_area("Describe your legal situation or question:", height=150)
        
        if st.button("Get Legal Advice"):
            if user_query:
                with st.spinner("Generating legal advice..."):
                    prompt = f"""
                    As a legal expert specializing in {legal_area} law in India, provide professional legal advice for the following situation. 
                    Include relevant laws, precedents, and practical next steps. 
                    Structure your response with these sections:
                    1. Legal Analysis
                    2. Applicable Laws and Statutes
                    3. Potential Courses of Action
                    4. Recommended Next Steps
                    5. Disclaimer

                    Remember that this is for informational purposes only and not a substitute for personalized legal counsel.
                    """
                    
                    response = generate_response(model, prompt, user_query)
                    if response:
                        st.subheader("Legal Advice")
                        st.markdown(response)
                        
                        # Add to history
                        st.session_state.history.append({
                            "service": "Legal Advice",
                            "query": user_query[:50] + "...",
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
            else:
                st.warning("Please enter your legal situation or question")
    
    # Document Analysis Section
    elif app_mode == "Document Analysis":
        st.title("Legal Document Analysis")
        st.write("Upload a legal document for AI-powered analysis and insights.")
        
        uploaded_file = st.file_uploader("Upload a legal document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
        
        analysis_type = st.multiselect(
            "Select types of analysis",
            ["Contract Review", "Legal Risk Assessment", "Plain Language Summary", "Legal Compliance Check"]
        )
        
        if uploaded_file and analysis_type and st.button("Analyze Document"):
            with st.spinner("Extracting and analyzing document..."):
                text = extract_text_from_file(uploaded_file)
                
                if text:
                    st.subheader("Document Text (Preview)")
                    st.text_area("Extracted text:", text[:1000] + "...", height=150)
                    
                    analysis_results = {}
                    
                    for analysis in analysis_type:
                        if analysis == "Contract Review":
                            prompt = """
                            As a contract law expert, review this legal document and provide:
                            1. Key contract terms and obligations
                            2. Potential issues or ambiguities
                            3. Missing clauses or protections
                            4. Suggestions for improvement
                            """
                        elif analysis == "Legal Risk Assessment":
                            prompt = """
                            Identify and analyze all potential legal risks in this document, including:
                            1. Liability concerns
                            2. Regulatory compliance issues
                            3. Enforcement challenges
                            4. Risk mitigation recommendations
                            """
                        elif analysis == "Plain Language Summary":
                            prompt = """
                            Translate this legal document into clear, plain language that a non-lawyer can understand.
                            Explain key concepts, obligations, and rights in simple terms.
                            """
                        elif analysis == "Legal Compliance Check":
                            prompt = """
                            Evaluate this document for compliance with Indian laws and regulations. Consider:
                            1. Applicable regulatory frameworks
                            2. Mandatory disclosures or provisions
                            3. Prohibited terms or practices
                            4. Compliance recommendations
                            """
                        
                        analysis_response = generate_response(model, prompt, text)
                        if analysis_response:
                            analysis_results[analysis] = analysis_response
                    
                    for analysis, result in analysis_results.items():
                        st.subheader(analysis)
                        st.markdown(result)
                    
                    # Add to history
                    st.session_state.history.append({
                        "service": "Document Analysis",
                        "query": uploaded_file.name,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
    
    # Case Law Summarization
    elif app_mode == "Case Law Summarization":
        st.title("Case Law Summarization")
        st.write("Get AI-powered summaries and analyses of case laws.")
        
        case_input_method = st.radio("Input method", ["Enter Case Citation", "Upload Case Document", "Paste Case Text"])
        
        case_text = ""
        if case_input_method == "Enter Case Citation":
            citation = st.text_input("Enter case citation (e.g., AIR 2019 SC 1234)")
            if citation and st.button("Fetch and Summarize"):
                st.info("This would typically connect to a legal database API. For now, please provide the case text.")
                # In a full implementation, this would connect to a legal database API
        
        elif case_input_method == "Upload Case Document":
            case_file = st.file_uploader("Upload case document", type=["pdf", "docx", "txt"])
            if case_file and st.button("Extract and Summarize"):
                with st.spinner("Extracting text..."):
                    case_text = extract_text_from_file(case_file)
                    if case_text:
                        st.text_area("Extracted case text (preview):", case_text[:500] + "...", height=100)
        
        elif case_input_method == "Paste Case Text":
            case_text = st.text_area("Paste case text:", height=200)
            
        if case_text and st.button("Summarize Case"):
            with st.spinner("Analyzing case law..."):
                prompt = """
                Analyze the following case law and provide:
                1. Case Name and Citation
                2. Court and Date
                3. Brief Facts
                4. Legal Issues
                5. Court's Decision and Reasoning
                6. Key Legal Principles Established
                7. Significance and Impact
                
                Structure your response in a clear, organized format suitable for legal professionals.
                """
                
                response = generate_response(model, prompt, case_text)
                if response:
                    st.subheader("Case Summary")
                    st.markdown(response)
                    
                    # Add to history
                    st.session_state.history.append({
                        "service": "Case Law Summarization",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
    
    # Argument Generator
    elif app_mode == "Argument Generator":
        st.title("Legal Argument Generator")
        st.write("Generate structured legal arguments for your case.")
        
        case_type = st.selectbox(
            "Select case type",
            ["Civil Litigation", "Criminal Defense", "Criminal Prosecution", "Constitutional", "Administrative"]
        )
        
        facts = st.text_area("Case facts and context:", height=150)
        legal_question = st.text_input("Legal question or issue to address:")
        
        position = st.radio("Position to argue", ["Plaintiff/Prosecution", "Defendant/Defense", "Both Sides"])
        
        if st.button("Generate Arguments"):
            if facts and legal_question:
                with st.spinner("Generating legal arguments..."):
                    if position in ["Plaintiff/Prosecution", "Both Sides"]:
                        plaintiff_prompt = f"""
                        As an experienced trial lawyer representing the Plaintiff/Prosecution in a {case_type} case, 
                        develop compelling legal arguments based on these facts:
                        
                        FACTS: {facts}
                        
                        ADDRESS THIS LEGAL QUESTION: {legal_question}
                        
                        Structure your response with:
                        1. Summary of Position
                        2. Legal Framework and Applicable Laws
                        3. Legal Arguments with Case Law Support
                        4. Anticipated Counter-Arguments
                        5. Rebuttal to Counter-Arguments
                        6. Conclusion and Requested Relief
                        
                        Focus on Indian law and relevant precedents.
                        """
                        
                        plaintiff_response = generate_response(model, plaintiff_prompt)
                        if plaintiff_response and position == "Plaintiff/Prosecution":
                            st.subheader("Plaintiff/Prosecution Arguments")
                            st.markdown(plaintiff_response)
                    
                    if position in ["Defendant/Defense", "Both Sides"]:
                        defense_prompt = f"""
                        As an experienced defense lawyer in a {case_type} case, 
                        develop compelling legal arguments based on these facts:
                        
                        FACTS: {facts}
                        
                        ADDRESS THIS LEGAL QUESTION: {legal_question}
                        
                        Structure your response with:
                        1. Summary of Position
                        2. Legal Framework and Applicable Laws
                        3. Legal Arguments with Case Law Support
                        4. Anticipated Counter-Arguments
                        5. Rebuttal to Counter-Arguments
                        6. Conclusion and Requested Relief
                        
                        Focus on Indian law and relevant precedents.
                        """
                        
                        defense_response = generate_response(model, defense_prompt)
                        if defense_response and position == "Defendant/Defense":
                            st.subheader("Defendant/Defense Arguments")
                            st.markdown(defense_response)
                    
                    if position == "Both Sides":
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("Plaintiff/Prosecution Arguments")
                            st.markdown(plaintiff_response)
                        with col2:
                            st.subheader("Defendant/Defense Arguments")
                            st.markdown(defense_response)
                    
                    # Add to history
                    st.session_state.history.append({
                        "service": "Argument Generator",
                        "query": legal_question,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
            else:
                st.warning("Please provide both case facts and a legal question")
    
    # Citation Generator
    elif app_mode == "Citation Generator":
        st.title("Legal Citation Generator")
        st.write("Generate properly formatted legal citations for various sources.")
        
        citation_type = st.selectbox(
            "Source type",
            ["Case Law", "Statute/Act", "Rules/Regulations", "Legal Journal/Article", "Books", "Reports"]
        )
        
        if citation_type == "Case Law":
            case_name = st.text_input("Case name (e.g., State of Punjab v. Singh)")
            court = st.selectbox("Court", ["Supreme Court", "High Court", "District Court", "Tribunal", "Other"])
            year = st.text_input("Year")
            volume = st.text_input("Volume (if applicable)")
            reporter = st.selectbox("Reporter", ["AIR", "SCC", "SCR", "CrLJ", "Other"])
            if reporter == "Other":
                reporter = st.text_input("Enter reporter abbreviation")
            page = st.text_input("Starting page number")
            
            if st.button("Generate Citation"):
                if case_name and court and year:
                    with st.spinner("Generating citation..."):
                        prompt = f"""
                        Generate a properly formatted legal citation for this Indian case:
                        - Case name: {case_name}
                        - Court: {court}
                        - Year: {year}
                        - Volume (if given): {volume}
                        - Reporter: {reporter}
                        - Page: {page}
                        
                        Provide the citation in:
                        1. Bluebook format
                        2. Indian citation style
                        3. Short form for subsequent citations
                        
                        Ensure proper formatting, including italics where required (shown between * symbols).
                        """
                        
                        response = generate_response(model, prompt)
                        if response:
                            st.subheader("Generated Citation")
                            st.markdown(response)
                            
                            # Add to history
                            st.session_state.history.append({
                                "service": "Citation Generator",
                                "query": case_name,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                else:
                    st.warning("Please fill in at least case name, court, and year")
        
        elif citation_type == "Statute/Act":
            act_name = st.text_input("Act name (e.g., Indian Penal Code)")
            year = st.text_input("Year of enactment")
            section = st.text_input("Section(s) (if applicable)")
            
            if st.button("Generate Citation"):
                if act_name:
                    with st.spinner("Generating citation..."):
                        prompt = f"""
                        Generate a properly formatted legal citation for this Indian statute:
                        - Act name: {act_name}
                        - Year: {year}
                        - Section(s): {section}
                        
                        Provide the citation in:
                        1. Bluebook format
                        2. Indian citation style
                        3. Short form for subsequent citations
                        
                        Ensure proper formatting, including italics where required (shown between * symbols).
                        """
                        
                        response = generate_response(model, prompt)
                        if response:
                            st.subheader("Generated Citation")
                            st.markdown(response)
                            
                            # Add to history
                            st.session_state.history.append({
                                "service": "Citation Generator",
                                "query": act_name,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                else:
                    st.warning("Please enter at least the act name")
        
        # Other citation types would follow similar patterns
    
    # Bias Detection
    elif app_mode == "Bias Detection":
        st.title("Judicial Bias Detection")
        st.write("Analyze judgments for potential biases or prejudicial language.")
        
        judgment_input_method = st.radio("Input method", ["Upload Judgment", "Paste Judgment Text"])
        
        judgment_text = ""
        if judgment_input_method == "Upload Judgment":
            judgment_file = st.file_uploader("Upload judgment document", type=["pdf", "docx", "txt"])
            if judgment_file and st.button("Extract Text"):
                with st.spinner("Extracting text..."):
                    judgment_text = extract_text_from_file(judgment_file)
                    if judgment_text:
                        st.text_area("Extracted judgment text (preview):", judgment_text[:500] + "...", height=100)
        
        elif judgment_input_method == "Paste Judgment Text":
            judgment_text = st.text_area("Paste judgment text:", height=200)
        
        bias_types = st.multiselect(
            "Select types of bias to analyze",
            ["Gender Bias", "Religious Bias", "Socioeconomic Bias", "Caste Bias", "Age Bias", "Regional Bias", "Language Bias", "General Prejudicial Language"]
        )
        
        if judgment_text and bias_types and st.button("Analyze for Bias"):
            with st.spinner("Analyzing judgment for potential bias..."):
                prompt = f"""
                Analyze the following judicial text for potential biases related to: {', '.join(bias_types)}.
                
                For each type of bias, provide:
                1. Assessment of whether bias exists (yes, no, or inconclusive)
                2. Specific examples from the text that suggest bias, if any
                3. Analysis of the implicit assumptions or stereotypes present
                4. Recommendations for more neutral language or reasoning
                
                Approach this analysis academically and objectively. Consider both explicit and implicit bias markers.
                """
                
                response = generate_response(model, prompt, judgment_text)
                if response:
                    st.subheader("Bias Analysis Results")
                    st.markdown(response)
                    
                    # Add to history
                    st.session_state.history.append({
                        "service": "Bias Detection",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
    
    # IPC Search
    elif app_mode == "IPC Search":
        st.title("Indian Penal Code Search")
        st.write("Search and navigate the Indian Penal Code with AI assistance.")
        
        search_method = st.radio("Search method", ["Section Number", "Keyword Search", "Legal Concept"])
        
        if search_method == "Section Number":
            section_number = st.text_input("Enter IPC section number (e.g., 302)")
            
            if section_number and st.button("Search Section"):
                with st.spinner("Retrieving section information..."):
                    prompt = f"""
                    Provide comprehensive information about Indian Penal Code Section {section_number}, including:
                    
                    1. Full text of the section
                    2. Elements of the offense/provision
                    3. Punishment/consequences
                    4. Important case law interpreting this section (3-5 landmark cases)
                    5. Related sections or provisions
                    
                    If this is not a valid IPC section, please indicate that and suggest the closest relevant sections.
                    """
                    
                    response = generate_response(model, prompt)
                    if response:
                        st.subheader(f"IPC Section {section_number}")
                        st.markdown(response)
                        
                        # Add to history
                        st.session_state.history.append({
                            "service": "IPC Search",
                            "query": f"Section {section_number}",
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
        
        elif search_method == "Keyword Search":
            keywords = st.text_input("Enter keywords (e.g., murder, theft, defamation)")
            
            if keywords and st.button("Search Keywords"):
                with st.spinner("Searching IPC for keywords..."):
                    prompt = f"""
                    Identify and explain Indian Penal Code sections related to these keywords: {keywords}
                    
                    For each relevant section, provide:
                    1. Section number and title
                    2. Brief summary of the provision (2-3 sentences)
                    3. Typical punishment or consequences
                    
                    List the most directly relevant sections first, followed by related provisions.
                    """
                    
                    response = generate_response(model, prompt)
                    if response:
                        st.subheader(f"IPC Sections Related to: {keywords}")
                        st.markdown(response)
                        
                        # Add to history
                        st.session_state.history.append({
                            "service": "IPC Search",
                            "query": keywords,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
        
        elif search_method == "Legal Concept":
            concept = st.text_input("Enter legal concept (e.g., mens rea, abetment, criminal conspiracy)")
            
            if concept and st.button("Search Concept"):
                with st.spinner("Analyzing concept in IPC..."):
                    prompt = f"""
                    Explain how the legal concept of "{concept}" is treated within the Indian Penal Code.
                    
                    Include:
                    1. Definition and explanation of the concept
                    2. Relevant IPC sections that incorporate this concept
                    3. How courts have interpreted this concept (key cases)
                    4. Practical application in criminal proceedings
                    
                    Structure your response for legal professionals, with appropriate citations.
                    """
                    
                    response = generate_response(model, prompt)
                    if response:
                        st.subheader(f"Legal Concept: {concept} in IPC")
                        st.markdown(response)
                        
                        # Add to history
                        st.session_state.history.append({
                            "service": "IPC Search",
                            "query": concept,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
    
    # Legal Research Assistant
    elif app_mode == "Legal Research Assistant":
        st.title("Legal Research Assistant")
        st.write("Get help with legal research questions and find relevant resources.")
        
        research_question = st.text_area("Enter your legal research question:", height=100)
        
        jurisdiction = st.selectbox(
            "Jurisdiction",
            ["India (All)", "Supreme Court of India", "Specific High Court", "International/Comparative"]
        )
        
        if jurisdiction == "Specific High Court":
            high_court = st.selectbox(
                "Select High Court",
                ["Delhi", "Bombay", "Calcutta", "Madras", "Allahabad", "Gujarat", "Other"]
            )
        
        time_period = st.select_slider(
            "Relevant time period",
            options=["All Time", "Last 5 Years", "Last 10 Years", "Last 20 Years", "Since 2000", "Since 1950"]
        )
        
        if st.button("Conduct Research"):
            if research_question:
                with st.spinner("Researching your legal question..."):
                    prompt = f"""
                    Act as a legal research expert conducting research on the following question:
                    
                    RESEARCH QUESTION: {research_question}
                    
                    JURISDICTION: {jurisdiction if jurisdiction != "Specific High Court" else f"{high_court} High Court"}
                    TIME PERIOD: {time_period}
                    
                    Provide a comprehensive research memo including:
                    
                    1. Legal Analysis of the Question
                       - Break down the key legal issues
                       - Identify relevant legal principles and doctrines
                    
                    2. Relevant Statutory Framework
                       - Key statutes and specific sections
                       - Legislative history if relevant
                       
                    3. Case Law
                       - Leading cases with citations (focus on Supreme Court and High Courts)
                       - Circuit splits or conflicting interpretations if any
                       - Recent developments in the law
                       
                    4. Academic Commentary
                       - Prominent scholarly perspectives
                       - Law commission reports if applicable
                       
                    5. Research Gaps and Recommendations
                       - Areas where law is unsettled
                       - Suggested arguments or approaches
                    
                    Focus on Indian law but include comparative perspectives if relevant.
                    """
                    
                    response = generate_response(model, prompt)
                    if response:
                        st.subheader("Legal Research Findings")
                        st.markdown(response)
                        
                        # Add to history
                        st.session_state.history.append({
                            "service": "Legal Research",
                            "query": research_question[:50] + "...",
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
            else:
                st.warning("Please enter a research question")

if __name__ == "__main__":
    main()
