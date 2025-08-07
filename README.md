# Mini AlphaGo (9x9) - Work In Progress
A full-stack web application that lets users play 9x9 Go against AI opponents of varying difficulty. Each AI is built from scratch using a custom Go engine, reinforcement learning, Monte Carlo Tree Search (MCTS), and a self-trained neural policy/value network.

The project includes a React + WebSocket frontend, FastAPI + Spring Boot backend, and a PyTorch-based training pipeline. Users can log in, play matches, and view past games through a replay system.

Developed by Jack Tsui and Daniel Prince.

---

### Home Page
<img width="1882" height="862" alt="Replay Viewer" src="https://github.com/user-attachments/assets/22122647-6f3d-447e-9d5d-c3354e0ff2a2" />

### Gameplay Demo

![goDemo](https://github.com/user-attachments/assets/def36e66-61d4-473a-83a6-b9738141cc37)


### Login & Registration
![login](https://github.com/user-attachments/assets/9915bfd3-c662-4759-85ed-cae670e99e73)


### Replay System
![Replay](https://github.com/user-attachments/assets/80263c12-5f53-4cdd-9d0f-d07fa7aa9290)





## Features
### ✅ Implemented

-  **Go Engine** – Clean Python implementation of 9x9 Go rules.
-  **Policy & Value Network** – PyTorch neural network for move prediction and win estimation.
-  **MCTS Integration** – Search algorithm guided by neural policy and value.
-  **Self-Play Training** – Replay buffer + reinforcement learning loop.
-  **Interactive Web App** – Play against the AI in real-time via React + WebSocket frontend.
-  **Login & Game Logs** – View previous games after logging in.

###  Work In Progress

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

