# Mini AlphaGo (9x9) - Work In Progress
A full-stack web application with user authentication that allows players to compete against Go AI bots of varying difficulty levels. Each AI is built from the ground up using a custom Go engine, reinforcement learning, Monte Carlo Tree Search (MCTS), and a self-trained neural policy/value network. This project is developed by Jack Tsui and Daniel Prince.

---

### Home Page
<img width="1882" height="862" alt="Replay Viewer" src="https://github.com/user-attachments/assets/22122647-6f3d-447e-9d5d-c3354e0ff2a2" />
### Gameplay Demo
![goDemo](https://github.com/user-attachments/assets/def36e66-61d4-473a-83a6-b9738141cc37)


### Login & Registration
![Login](https://github.com/user-attachments/assets/a622e1c5-a67a-4738-802e-e81e71a2cc0e)

### Replay System
![Replay](https://github.com/user-attachments/assets/80263c12-5f53-4cdd-9d0f-d07fa7aa9290)





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

