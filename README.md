# Mini AlphaGo (9x9) - Work In Progress
A full-stack web application with user authentication that allows players to compete against Go AI bots of varying difficulty levels. Each AI is built from the ground up using a custom Go engine, reinforcement learning, Monte Carlo Tree Search (MCTS), and a self-trained neural policy/value network.

---

![goDemo](https://github.com/user-attachments/assets/066aeed3-c383-45c5-a3e0-35d10633cbe8)
<img width="1882" height="862" alt="goHome" src="https://github.com/user-attachments/assets/60166e1f-4365-4210-a6ae-149a2d0c59a7" />
<img width="1882" height="862" alt="goLogin" src="https://github.com/user-attachments/assets/8bf07848-7296-4f3a-9648-c5aebe667640" />


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

