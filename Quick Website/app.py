import streamlit as st
import time
import hashlib
import datetime
import json
from typing import Dict, List

# Configure Streamlit page
st.set_page_config(
    page_title="Quick - Global Daily Challenge",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        color: #FFFFFF;
        font-family: 'Courier New', monospace;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #06B6D4;
        margin-bottom: 2rem;
    }
    
    .target-time {
        font-size: 2rem;
        text-align: center;
        color: #FFFFFF;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .current-time {
        font-size: 4rem;
        text-align: center;
        color: #06B6D4;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        margin: 2rem 0;
    }
    
    .score-display {
        font-size: 2.5rem;
        text-align: center;
        color: #10B981;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .accuracy-display {
        font-size: 1.5rem;
        text-align: center;
        color: #F59E0B;
        margin: 0.5rem 0;
    }
    
    .stats-container {
        background-color: #1F2937;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #374151;
    }
    
    .challenge-complete {
        background-color: #065F46;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid #10B981;
        text-align: center;
    }
    
    .global-info {
        background-color: #1E3A8A;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #3B82F6;
    }
    
    .leaderboard-row {
        background-color: #374151;
        border-radius: 5px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #06B6D4;
    }
    
    .button-container {
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DailyChallengeManager:
    @staticmethod
    def get_daily_target() -> int:
        """Generate deterministic daily target based on UTC date"""
        today = datetime.date.today()
        
        # Create deterministic seed from date
        date_string = today.strftime("%Y-%m-%d")
        seed = int(hashlib.md5(date_string.encode()).hexdigest(), 16) % 1000000
        
        # Generate target between 1-15 seconds
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
        st.session_state.game_state = 'ready'  # ready, running, stopped
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

def render_game_interface():
    """Render the main game interface"""
    game_manager = st.session_state.game_manager
    
    # Title and subtitle
    st.markdown('<div class="main-title">QUICK</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">🌍 Global Daily Challenge - {DailyChallengeManager.get_date_string()}</div>', unsafe_allow_html=True)
    
    # Target time display
    st.markdown(f'<div class="target-time">🎯 Target: {game_manager.target_time} seconds</div>', unsafe_allow_html=True)
    
    # Current time display
    if st.session_state.game_state == 'running':
        if st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            st.session_state.current_time = elapsed
            st.markdown(f'<div class="current-time">{elapsed:.2f}</div>', unsafe_allow_html=True)
        
        # Auto-refresh for running timer
        time.sleep(0.01)
        st.rerun()
    else:
        display_time = st.session_state.final_time if st.session_state.game_state == 'stopped' else 0.0
        st.markdown(f'<div class="current-time">{display_time:.2f}</div>', unsafe_allow_html=True)
    
    # Game buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.game_state == 'ready':
            if st.session_state.has_played_today:
                st.markdown('<div class="challenge-complete">', unsafe_allow_html=True)
                st.markdown("### 🎯 Daily Challenge Complete!")
                st.markdown("Come back tomorrow for a new challenge")
                st.markdown(f"New target at midnight UTC")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button("🚀 START", key="start_btn", help="Start the timer"):
                    st.session_state.game_state = 'running'
                    st.session_state.start_time = time.time()
                    st.rerun()
        
        elif st.session_state.game_state == 'running':
            if st.button("⏹️ STOP", key="stop_btn", help="Stop the timer"):
                st.session_state.final_time = st.session_state.current_time
                st.session_state.game_state = 'stopped'
                score = game_manager.calculate_score(st.session_state.final_time)
                save_score(score)
                st.rerun()
        
        elif st.session_state.game_state == 'stopped':
            score = game_manager.calculate_score(st.session_state.final_time)
            
            # Display results
            st.markdown(f'<div class="score-display">Score: {score}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="accuracy-display">{game_manager.get_accuracy_text(st.session_state.final_time)}</div>', unsafe_allow_html=True)
            
            # Completion message
            st.markdown('<div class="challenge-complete">', unsafe_allow_html=True)
            st.markdown("### 🎉 Challenge Complete!")
            st.markdown("Come back tomorrow for a new precision challenge")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🔄 Reset for Tomorrow", key="reset_btn"):
                reset_game()
                st.rerun()

def render_global_info():
    """Render global challenge information"""
    st.markdown('<div class="global-info">', unsafe_allow_html=True)
    st.markdown("### 🌍 Global Daily Challenge")
    st.markdown(f"**Today's Target:** {st.session_state.game_manager.target_time} seconds")
    st.markdown("**Challenge:** Everyone worldwide attempts the same target today")
    st.markdown("**Scoring:** Get as close as possible to the target time")
    st.markdown("**Perfect Score:** 1000 points (exact match)")
    st.markdown('</div>', unsafe_allow_html=True)

def render_leaderboard():
    """Render today's scores leaderboard"""
    if st.session_state.todays_scores:
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        st.markdown("### 📊 Your Attempts Today")
        
        # Sort scores by best first
        sorted_scores = sorted(st.session_state.todays_scores, key=lambda x: x['score'], reverse=True)
        
        for i, attempt in enumerate(sorted_scores[:5]):  # Show top 5
            crown = "👑 " if i == 0 else f"#{i+1} "
            st.markdown(
                f'<div class="leaderboard-row">{crown}Score: {attempt["score"]} | Time: {attempt["time"]:.2f}s</div>',
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_how_to_play():
    """Render how to play instructions"""
    with st.expander("📖 How to Play", expanded=False):
        st.markdown("""
        **Welcome to Quick - The Global Daily Precision Challenge!**
        
        🎯 **Goal:** Stop the timer as close as possible to today's target time
        
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

def reset_game():
    """Reset game state for new attempt"""
    st.session_state.game_state = 'ready'
    st.session_state.start_time = None
    st.session_state.current_time = 0.0
    st.session_state.final_time = 0.0

def main():
    """Main application function"""
    initialize_session_state()
    
    # How to play section
    render_how_to_play()
    
    # Main game interface
    render_game_interface()
    
    # Global challenge info
    render_global_info()
    
    # Leaderboard
    render_leaderboard()
    
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