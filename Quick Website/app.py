import streamlit as st
import time
import hashlib
import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Quick - Global Daily Challenge",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with good contrast and readability
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Clean light theme with good contrast */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #1a202c;
    }
    
    /* Override Streamlit's default text colors */
    .stMarkdown {
        color: #1a202c;
    }
    
    /* Main title */
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        color: #2d3748;
        font-family: 'Georgia', serif;
        letter-spacing: 0.1em;
        margin: 2rem 0 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #4a5568;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    /* Target display */
    .target-display {
        font-size: 2rem;
        text-align: center;
        color: #2d3748;
        font-weight: 700;
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Timer display */
    .timer-display {
        font-size: 6rem;
        text-align: center;
        color: #2b6cb0;
        font-family: 'Georgia', serif;
        font-weight: bold;
        margin: 3rem 0;
        letter-spacing: 0.05em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Score display */
    .score-display {
        font-size: 3.5rem;
        text-align: center;
        color: #38a169;
        font-weight: bold;
        margin: 2rem 0;
        font-family: 'Georgia', serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .accuracy-display {
        font-size: 1.4rem;
        text-align: center;
        color: #d69e2e;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    /* Completion card */
    .completion-card {
        background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid #38a169;
        text-align: center;
        box-shadow: 0 8px 20px rgba(56, 161, 105, 0.2);
        color: #1a202c;
    }
    
    .completion-card h3 {
        color: #1a202c !important;
        margin-bottom: 1rem;
    }
    
    /* Info card */
    .info-card {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: #1a202c;
    }
    
    .info-card h3 {
        color: #2d3748 !important;
        margin-bottom: 1rem;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1.2rem 3rem;
        font-size: 1.4rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.5);
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
    }
    
    /* Stop button styling */
    .stop-button .stButton > button {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%) !important;
        animation: pulse 2s infinite;
        box-shadow: 0 6px 20px rgba(245, 101, 101, 0.4) !important;
    }
    
    .stop-button .stButton > button:hover {
        background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%) !important;
        box-shadow: 0 8px 25px rgba(229, 62, 62, 0.5) !important;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f7fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        color: #1a202c !important;
    }
    
    /* Footer styling */
    .footer-text {
        color: #718096 !important;
        text-align: center;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

class DailyChallengeManager:
    @staticmethod
    def get_daily_target() -> int:
        """Generate deterministic daily target based on UTC date"""
        today = datetime.date.today()
        date_string = today.strftime("%Y-%m-%d")
        seed = int(hashlib.md5(date_string.encode()).hexdigest(), 16) % 1000000
        target = 1 + (seed % 15)
        return target
    
    @staticmethod
    def get_date_string() -> str:
        return datetime.date.today().strftime("%B %d, %Y")

class GameManager:
    def __init__(self):
        self.target_time = DailyChallengeManager.get_daily_target()
        
    def calculate_score(self, actual_time: float) -> int:
        """Calculate score based on accuracy (max 1000 points)"""
        difference = abs(actual_time - self.target_time)
        accuracy = max(0, 1 - (difference / self.target_time))
        return int(accuracy * 1000)
    
    def get_accuracy_text(self, actual_time: float) -> str:
        difference = abs(actual_time - self.target_time)
        return f"Off by: {difference:.2f}s"

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'ready'
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'current_time' not in st.session_state:
        st.session_state.current_time = 0.0
    if 'final_time' not in st.session_state:
        st.session_state.final_time = 0.0
    if 'has_played_today' not in st.session_state:
        st.session_state.has_played_today = False
    if 'todays_scores' not in st.session_state:
        st.session_state.todays_scores = []
    if 'game_manager' not in st.session_state:
        st.session_state.game_manager = GameManager()

def save_score(score: int):
    """Save score to session state"""
    st.session_state.todays_scores.append({
        'score': score,
        'time': st.session_state.final_time,
        'timestamp': datetime.datetime.now().isoformat()
    })
    st.session_state.has_played_today = True

def reset_game():
    """Reset game state for new attempt"""
    st.session_state.game_state = 'ready'
    st.session_state.start_time = None
    st.session_state.current_time = 0.0
    st.session_state.final_time = 0.0

def main():
    """Main application function"""
    initialize_session_state()
    game_manager = st.session_state.game_manager
    
    # Title and subtitle
    st.markdown('<div class="main-title">QUICK</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">🌍 Global Daily Challenge - {DailyChallengeManager.get_date_string()}</div>', unsafe_allow_html=True)
    
    # Target time display
    st.markdown(f'<div class="target-display">🎯 Target: {game_manager.target_time} seconds</div>', unsafe_allow_html=True)
    
    # Timer display
    timer_placeholder = st.empty()
    
    # Update timer display based on state
    if st.session_state.game_state == 'running' and st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        st.session_state.current_time = elapsed
        timer_placeholder.markdown(f'<div class="timer-display">{elapsed:.2f}</div>', unsafe_allow_html=True)
    else:
        display_time = st.session_state.final_time if st.session_state.game_state == 'stopped' else 0.0
        timer_placeholder.markdown(f'<div class="timer-display">{display_time:.2f}</div>', unsafe_allow_html=True)
    
    # Game controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.game_state == 'ready':
            if st.session_state.has_played_today:
                st.markdown('<div class="completion-card">', unsafe_allow_html=True)
                st.markdown("### 🎯 Daily Challenge Complete!")
                st.markdown("Come back tomorrow for a new challenge")
                st.markdown("New target at midnight UTC")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button("🚀 START", key="start_btn", help="Start the timer"):
                    st.session_state.game_state = 'running'
                    st.session_state.start_time = time.time()
                    st.rerun()
        
        elif st.session_state.game_state == 'running':
            # Use a container with custom CSS class for stop button
            stop_container = st.container()
            with stop_container:
                st.markdown('<div class="stop-button">', unsafe_allow_html=True)
                if st.button("⏹️ STOP", key="stop_btn", help="Stop the timer"):
                    st.session_state.final_time = st.session_state.current_time
                    st.session_state.game_state = 'stopped'
                    score = game_manager.calculate_score(st.session_state.final_time)
                    save_score(score)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif st.session_state.game_state == 'stopped':
            score = game_manager.calculate_score(st.session_state.final_time)
            
            # Display results
            st.markdown(f'<div class="score-display">Score: {score}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="accuracy-display">{game_manager.get_accuracy_text(st.session_state.final_time)}</div>', unsafe_allow_html=True)
            
            # Completion message
            st.markdown('<div class="completion-card">', unsafe_allow_html=True)
            st.markdown("### 🎉 Challenge Complete!")
            st.markdown("Come back tomorrow for a new precision challenge")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🔄 Reset for Tomorrow", key="reset_btn"):
                reset_game()
                st.rerun()
    
    # Global challenge info
    with st.expander("📖 How to Play", expanded=False):
        st.markdown(f"""
        **Welcome to Quick - The Global Daily Precision Challenge!**
        
        🎯 **Goal:** Stop the timer as close as possible to **{game_manager.target_time} seconds**
        
        📅 **Daily Challenge:** Everyone worldwide gets the same target each day
        
        ⏱️ **How to Play:**
        1. Click START to begin the timer
        2. Watch the timer count up
        3. Click STOP when you think you've hit the target
        4. See how close you got!
        
        🏆 **Scoring:**
        - Perfect timing = 1000 points
        - The closer you are, the higher your score
        - One attempt per day
        
        🌍 **Global Challenge:**
        - Same target time for everyone worldwide
        - New challenge every day at midnight UTC
        """)
    
    # Leaderboard
    if st.session_state.todays_scores:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Your Attempts Today")
        
        sorted_scores = sorted(st.session_state.todays_scores, key=lambda x: x['score'], reverse=True)
        
        for i, attempt in enumerate(sorted_scores[:5]):
            crown = "👑 " if i == 0 else f"#{i+1} "
            st.markdown(f"**{crown}Score: {attempt['score']} | Time: {attempt['time']:.2f}s**")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-refresh when timer is running
    if st.session_state.game_state == 'running':
        time.sleep(0.1)
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #6B7280; margin-top: 2rem;">'
        '🎯 Quick - Global Daily Precision Challenge<br>'
        'Built with Streamlit • New challenge daily at midnight UTC'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()