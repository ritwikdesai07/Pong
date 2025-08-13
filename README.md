Pong Game with AI & Data Collection
===================================

This project is a Python-based **Pong game** with two modes:

*   **Data Collection Mode** – Play manually and record game data for AI training.
    
*   **AI Mode** – Play against an AI-controlled paddle trained from collected data.
    

The AI uses a **Random Forest Classifier** trained on real gameplay.

🎮 Features
-----------

*   **Two Game Modes**:
    
    *   **Data Collection Mode** – Save paddle movement and ball position data to pong\_data.csv.
        
    *   **AI Mode** – The right paddle is controlled by an AI model (pong\_model.pkl).
        
*   **Smooth Ball and Paddle Movement** with turtle graphics.
    
*   **CSV Data Logging** for machine learning.
    
*   **Customizable AI Training** using scikit-learn.
    

📂 Project Structure
--------------------

├── PongGame.py         # Main game logic (data collection & AI mode)  
├── train_model.py      # Script to train AI from collected data  
├── pong_data.csv       # Generated during data collection  
├── pong_model.pkl      # Trained AI model  
└── README.md           # This documentation file   

⚙️ Requirements
---------------

Install dependencies with this command:

pip install pandas scikit-learn joblib   `

**Note:** turtle is included with Python, so no installation is needed for it.

🚀 Usage
--------

### 1️⃣ Data Collection Mode

To collect data, open PongGame.py and set this variable to True:

DATA_COLLECTION_MODE = True   `

Then, run the game from your terminal:

python PongGame.py   `

**Controls:**

*   **Left Paddle:** W (Up), S (Down)
    
*   **Right Paddle:** ↑ (Up), ↓ (Down)
    

Gameplay data will be saved to pong\_data.csv.

### 2️⃣ Train the AI

After you've collected enough data, run the training script:

python train_model.py   `

This script will:

1.  Train a **Random Forest Classifier**.
    
2.  Save the trained model as pong\_model.pkl.
    

### 3️⃣ AI Mode

To play against the AI, set the variable in PongGame.py to False:

DATA_COLLECTION_MODE = False   `

Then, run the game:

python PongGame.py   `

**Controls:**

*   **Left Paddle:** W (Up), S (Down)
    
*   **Right Paddle:** Controlled by the AI.
    

📊 Data Format
--------------

Gameplay data is stored in CSV format with the following columns:

Column

Description

ball\_x

Ball’s X coordinate

ball\_y

Ball’s Y coordinate

ball\_dx

Ball’s X velocity

ball\_dy

Ball’s Y velocity

paddle\_y

Right paddle’s Y coordinate

action

Paddle action (0 = stay, 1 = up, 2 = down)

🛠️ Customization
-----------------

You can tweak game settings directly inside PongGame.py:

*   **Paddle speed**: PADDLE\_SPEED
    
*   **Ball speed**: BALL\_SPEED\_FACTOR
    
*   **Max data points for collection**: max\_data\_points
    

Model parameters can be tuned in train\_model.py by modifying param\_grid:

param_grid = {      'n_estimators': [50, 100],      'max_depth': [5, 10, 15]  }   `

📌 Notes
--------

*   For best results, collect diverse gameplay data to improve the AI's performance.
    
*   The AI mode requires pong\_model.pkl, which is created by running train\_model.py.
    
*   This project works with Python 3.x and relies on turtle for its graphics.
