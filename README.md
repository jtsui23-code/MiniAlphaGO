# Mini AlphaGo (9x9) - Work In Progress

A full-stack, reinforcement learning-based Go AI engine for the 9x9 board—complete with Monte Carlo Tree Search (MCTS), a neural policy/value network, self-play training pipeline, and an interactive web app with user login and game replay features.

> Inspired by DeepMind's AlphaGo Zero, built with modern ML and web technologies.

---

## Features
### ✅ Implemented

- 🎯 **Go Engine** – Clean Python implementation of 9x9 Go rules.
- 🧩 **Policy & Value Network** – PyTorch neural network for move prediction and win estimation.
- 🌲 **MCTS Integration** – Search algorithm guided by neural policy and value.
- 🔁 **Self-Play Training** – Replay buffer + reinforcement learning loop.

### 🔜 Work In Progress
- 🌐 **Interactive Web App** – Play against the AI in real-time via React + WebSocket frontend.
- 🔒 **Login & Game Logs** – View previous games after logging in.
- 🐳 **Dockerized Deployment** – Reproducible containerized setup.

---

## 🛠 Tech Stack

| Layer     | Tools                                    |
|----------|-------------------------------------------|
| Frontend | React, TypeScript, TailwindCSS, Konva     |
| Backend  | FastAPI, WebSockets                       |
| ML/AI    | PyTorch, NumPy                            |
| DevOps   | Docker, GitHub Actions                    |
| Training | Jupyter, Python                           |

