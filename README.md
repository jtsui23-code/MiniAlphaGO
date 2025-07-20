# Mini AlphaGo (9x9) - Work In Progress
A full-stack web application with user authentication that allows players to compete against Go AI bots of varying difficulty levels. Each AI is built from the ground up using a custom Go engine, reinforcement learning, Monte Carlo Tree Search (MCTS), and a self-trained neural policy/value network.

---
<img width="1873" height="867" alt="goHomePage" src="https://github.com/user-attachments/assets/184c8dd3-bb28-4a5e-91d1-63f0fb194238" />


## Features
### ✅ Implemented

-  **Go Engine** – Clean Python implementation of 9x9 Go rules.
-  **Policy & Value Network** – PyTorch neural network for move prediction and win estimation.
-  **MCTS Integration** – Search algorithm guided by neural policy and value.
-  **Self-Play Training** – Replay buffer + reinforcement learning loop.

###  Work In Progress
-  **Interactive Web App** – Play against the AI in real-time via React + WebSocket frontend.
-  **Login & Game Logs** – View previous games after logging in.
-  **Dockerized Deployment** – Reproducible containerized setup.

---



## 🛠 Tech Stack

| Layer     | Tools                                    |
|----------|-------------------------------------------|
| Frontend | React, TypeScript, TailwindCSS            |
| Backend  | FastAPI, WebSockets, Spring Boot          |
| ML/AI    | PyTorch, NumPy                            |
| DevOps   | GitHub Actions                    |
| Training |  Python                           |

