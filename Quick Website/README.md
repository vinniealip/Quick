# Quick - Global Daily Precision Challenge

🎯 A web version of the precision timing game where players worldwide attempt the same daily challenge.

## Features

- **Global Daily Challenge**: Everyone gets the same target time each day
- **Precision Timing**: Stop the timer as close as possible to the target
- **Score System**: Up to 1000 points for perfect timing
- **Responsive Design**: Works on desktop and mobile
- **Real-time Timer**: Smooth timing with 0.01s precision

## How to Play

1. **Start**: Click the START button to begin timing
2. **Stop**: Click STOP when you think you've hit the target time
3. **Score**: See how close you got with your precision score
4. **Daily**: One attempt per day, new challenge at midnight UTC

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Set main file path to `app.py`
6. Deploy!

## Game Mechanics

- **Target Generation**: Deterministic algorithm ensures same target globally
- **Scoring**: `score = (1 - |actual - target| / target) * 1000`
- **Daily Reset**: New challenges at midnight UTC
- **One Attempt**: Maintains challenge integrity like Wordle

## Tech Stack

- **Frontend**: Streamlit
- **Styling**: Custom CSS
- **Deployment**: Streamlit Cloud
- **Version Control**: Git/GitHub

---

Built with ❤️ for precision timing enthusiasts worldwide!