import streamlit as st
import pandas as pd
import plotly.express as px

# ====================================
# Page Configuration
# ====================================

st.set_page_config(
    page_title="SmartHire AI",
    page_icon="🤖",
    layout="wide"
)

# ====================================
# Header
# ====================================

st.title("🤖 SmartHire AI")

st.subheader(
    "AI-Powered Candidate Ranking System"
)

st.markdown("""
### Intelligent Candidate Discovery & Ranking

This system ranks candidates using:

✅ Semantic Similarity

✅ Behavioral Signals

✅ Retrieval & Ranking Experience

✅ AI/ML Career Relevance

✅ Experience Analysis

✅ Candidate Fit Scoring
""")

# ====================================
# Load CSV
# ====================================

try:

    df = pd.read_csv(
        "submission.csv"
    )

    st.success(
        "submission.csv loaded successfully!"
    )

    st.divider()

    # ====================================
    # Dashboard Metrics
    # ====================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Candidates Ranked",
            len(df)
        )

    with col2:

        st.metric(
            "Top Score",
            round(
                df.iloc[0]["score"],
                4
            )
        )

    with col3:

        st.metric(
            "Top Candidate",
            df.iloc[0]["candidate_id"]
        )

    with col4:

        st.metric(
            "Average Score",
            round(
                df["score"].mean(),
                4
            )
        )

    st.divider()

    # ====================================
    # Candidate Search
    # ====================================

    st.subheader(
        "🔍 Search Candidate"
    )

    search_candidate = st.text_input(
        "Enter Candidate ID"
    )

    if search_candidate:

        filtered_df = df[
            df["candidate_id"]
            .astype(str)
            .str.contains(
                search_candidate,
                case=False
            )
        ]

        if len(filtered_df):

            st.success(
                f"{len(filtered_df)} candidate(s) found"
            )

            st.dataframe(
                filtered_df,
                use_container_width=True
            )

        else:

            st.warning(
                "No candidate found"
            )

    st.divider()

    # ====================================
    # Best Candidate
    # ====================================

    st.subheader(
        "🏆 Top Ranked Candidate"
    )

    best = df.iloc[0]

    st.write(
        f"**Candidate ID:** {best['candidate_id']}"
    )

    st.write(
        f"**Rank:** {best['rank']}"
    )

    st.write(
        f"**Score:** {best['score']}"
    )

    st.write(
        f"**Reasoning:** {best['reasoning']}"
    )

    st.divider()

        # ====================================
    # Score Distribution
    # ====================================

    st.subheader(
        "📊 Candidate Score Distribution"
    )

    fig = px.histogram(
        df,
        x="score",
        nbins=20,
        title="Distribution of Candidate Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ====================================
    # Top 10 Candidates Chart
    # ====================================

    st.subheader(
        "🏅 Top 10 Ranked Candidates"
    )

    top10 = df.head(10)

    fig2 = px.bar(
        top10,
        x="candidate_id",
        y="score",
        text="score",
        title="Top 10 Candidate Scores"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # ====================================
    # Top 10 Table
    # ====================================

    st.subheader(
        "⭐ Top 10 Candidates"
    )

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.divider()

    # ====================================
    # Leaderboard
    # ====================================

    st.subheader(
        "🥇 Candidate Leaderboard"
    )

    leaderboard = df[
        [
            "rank",
            "candidate_id",
            "score"
        ]
    ]

    st.dataframe(
        leaderboard,
        use_container_width=True
    )

    st.divider()

    # ====================================
    # Full Ranking
    # ====================================

    st.subheader(
        "📋 Top 100 Ranked Candidates"
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )

    st.divider()

    # ====================================
    # Download Button
    # ====================================

    st.subheader(
        "📥 Download Submission"
    )

    with open(
        "submission.csv",
        "rb"
    ) as file:

        st.download_button(
            label="Download submission.csv",
            data=file,
            file_name="submission.csv",
            mime="text/csv"
        )

    st.divider()

    # ====================================
    # Footer
    # ====================================

    st.markdown(
        """
        ---
        ### SmartHire AI

        AI-Powered Candidate Ranking System

        Built for the Redrob Intelligent Candidate Discovery & Ranking Challenge.
        """
    )

except Exception as e:

    st.warning(
        "Please run generate_submission_fast.py first."
    )

    st.error(
        str(e)
    )