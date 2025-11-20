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

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Dark theme */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Main title */
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        color: #FFFFFF;
        font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
        letter-spacing: 0.2em;
        margin: 2rem 0 1rem 0;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.1rem;
        text-align: center;
        color: #06B6D4;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    /* Target display */
    .target-display {
        font-size: 1.8rem;
        text-align: center;
        color: #FFFFFF;
        font-weight: 600;
        margin: 2rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
        border-radius: 15px;
        border: 1px solid #4B5563;
    }
    
    /* Timer display */
    .timer-display {
        font-size: 5rem;
        text-align: center;
        color: #06B6D4;
        font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
        font-weight: bold;
        margin: 3rem 0;
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
        letter-spacing: 0.1em;
    }
    
    /* Score display */
    .score-display {
        font-size: 3rem;
        text-align: center;
        color: #10B981;
        font-weight: bold;
        margin: 2rem 0;
        font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
    }
    
    .accuracy-display {
        font-size: 1.3rem;
        text-align: center;
        color: #F59E0B;
        margin: 1rem 0;
    }
    
    /* Completion card */
    .completion-card {
        background: linear-gradient(135deg, #065F46 0%, #047857 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid #10B981;
        text-align: center;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.2);
    }
    
    /* Info card */
    .info-card {
        background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #4B5563;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 3rem;
        font-size: 1.3rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(16, 185, 129, 0.4);
    }
    
    /* Stop button styling */
    .stop-button > button {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
        animation: pulse 2s infinite;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3) !important;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
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