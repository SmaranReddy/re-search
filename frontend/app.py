import streamlit as st
import sys
import os

# --- Add backend to Python path ---
# This is crucial for Streamlit to find your 'backend' module

# Get the directory of this file (app.py), which is '.../Projectsss/frontend'
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the main project directory '.../Projectsss'
root_project_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add this root directory to the Python path
# Now Python can find the 'backend' folder inside '.../Projectsss'
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)
# ----------------------------------


# Now we can import from the backend
try:
    # This imports the run_graph function from backend/main.py
    from backend.main import run_graph
except ImportError as e:
    st.error(f"Could not import backend modules. Error: {e}")
    st.error(f"Current Path: {sys.path}")
    st.stop()
# ----------------------------------

st.title("Re-Search: Dynamic AI Literature Assistant 📚")
st.markdown("Enter a research topic, and the AI agents will find, read, and summarize relevant papers for you.")

topic = st.text_input("Enter your research topic:", placeholder="e.g., 'Attention is all you need'")

if st.button("Analyze", type="primary"):
    if topic:
        # 1. Show a loading spinner while the graph runs
        with st.spinner("🤖 Agents are working... Planning, retrieving, and summarizing..."):
            try:
                # 2. Call the new graph function
                final_state = run_graph(topic)

                # 3. Process and display the results from the final state
                st.success("Analysis complete!")

                keywords = final_state.get('keywords')
                papers = final_state.get('papers', [])
                summaries = final_state.get('summaries', [])

                if keywords:
                    st.subheader("Extracted Keywords")
                    st.info(f"**Keywords:** {keywords}")

                if not papers:
                    st.warning("No papers were found for this topic.")

                # Loop through papers and summaries to display them
                for i, (paper, summary) in enumerate(zip(papers, summaries)):
                    st.divider()
                    st.subheader(f"Paper {i+1}: {paper.get('title', 'No Title')}")

                    with st.expander("Show AI-Generated Summary"):
                        st.markdown(summary)

                    with st.expander("Show Original Abstract"):
                        st.text_area("Abstract", paper.get('abstract', 'No Abstract'), height=150)

            except Exception as e:
                st.error(f"An error occurred while running the analysis: {e}")
                st.exception(e)  # Provides a full traceback
    else:
        st.warning("Please enter a research topic.")