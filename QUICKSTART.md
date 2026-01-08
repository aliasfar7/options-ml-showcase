# Quick Start Guide

## 🚀 Get Up and Running in 10 Minutes

This guide will get you from clone to running your first RL trading agent.

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB+ RAM recommended
- (Optional) CUDA-capable GPU for faster training

---

## Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/aliasfar7/options-ml-showcase.git
cd options-ml-showcase

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: If `ta-lib` fails to install:
```bash
# On Mac:
brew install ta-lib

# On Ubuntu/Debian:
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install

# Then: pip install ta-lib
```

---

## Step 2: Run the Demo Notebook

The fastest way to see the system in action:

```bash
cd demo
jupyter notebook end_to_end_demo.ipynb
```

This notebook will:
1. Generate synthetic market data
2. Engineer features
3. Train an RL agent
4. Evaluate performance
5. Visualize results

**Expected runtime**: 5-10 minutes on a modern laptop

---

## Step 3: Train Your First Agent

### Option A: Use Synthetic Data (No API Keys Required)

```bash
cd code/gld_drl_alpha/src

# Train on synthetic data
python train_exec.py
```

**Output**:
- Trained model saved to `policy_exec.pt`
- Training logs showing episodic rewards
- Final evaluation metrics

### Option B: Use Real Market Data

**Get free API keys**:
- [Polygon.io](https://polygon.io/) - 5 API calls/min free tier
- [Alpha Vantage](https://www.alphavantage.co/) - 5 calls/min free
- [Yahoo Finance](https://finance.yahoo.com/) - No key needed (via yfinance)

**Configure**:
```bash
# Create .env file
echo "POLYGON_API_KEY=your_key_here" > .env
```

**Download data**:
```bash
cd bayn_drl_options/bayn_drl_options/scripts
python download_data.py --symbol AMD --start 2023-01-01 --end 2023-12-31
```

**Train**:
```bash
python train_ppo.py
```

---

## Step 4: Run a Backtest

### QuantConnect (Recommended for serious backtesting)

1. **Sign up**: [quantconnect.com](https://www.quantconnect.com/) (free tier)
2. **Install Lean CLI**:
```bash
pip install lean
lean init
```

3. **Copy strategy**:
```bash
cp bayn_qc2/BaynAmdNvdaAlphaV11/main.py ~/QuantConnect/MyStrategy/main.py
```

4. **Run backtest**:
```bash
cd ~/QuantConnect/MyStrategy
lean backtest MyStrategy
```

### Custom Backtest (Simpler, local)

```bash
cd code/lob_exec_sim
python main.py
```

---

## Step 5: Explore the Codebase

### Key Files to Read First

1. **`README.md`** (main) - Overview and motivation
2. **`demo/end_to_end_demo.ipynb`** - Complete working example
3. **`docs/ARCHITECTURE.md`** - System design philosophy
4. **`code/gld_drl_alpha/README.md`** - RL details
5. **`code/lob_exec_sim/README.md`** - Execution modeling

### Directory Tour

```
.
├── code/
│   ├── gld_drl_alpha/       # 👈 Start here: Simple RL example
│   └── lob_exec_sim/        # Execution simulation
│
├── bayn_drl_options/        # Advanced multi-asset system
│   ├── envs/                # Custom Gym environments
│   ├── scripts/             # Training & evaluation
│   └── live/                # Paper trading code
│
├── bayn_qc2/                # QuantConnect strategies
│   └── BaynAmdNvdaAlphaV11/ # Example intraday strategy
│
├── demo/                    # 👈 Run this first
│   └── end_to_end_demo.ipynb
│
└── docs/                    # Architecture & design docs
    └── ARCHITECTURE.md
```

---

## Common Issues & Solutions

### Issue: "No module named 'gymnasium'"

**Solution**:
```bash
pip install gymnasium
# Or if you have old 'gym':
pip uninstall gym
pip install gymnasium
```

### Issue: "CUDA out of memory"

**Solution**: Train on CPU (slower but works)
```python
# In training script, change:
device = torch.device('cpu')  # Instead of 'cuda'
```

### Issue: "TA-Lib not found"

**Solution**: See Step 1 for platform-specific installation

### Issue: "API rate limit exceeded"

**Solution**: 
- Use synthetic data (demo notebook)
- Upgrade to paid API tier
- Add delays between requests: `time.sleep(12)`  # 5 calls/min = 12s between

---

## Next Steps

### Beginner

1. ✅ Run demo notebook
2. ✅ Read `ARCHITECTURE.md`
3. ⬜ Modify hyperparameters in `train_exec.py`
4. ⬜ Try different features
5. ⬜ Visualize learned policy behavior

### Intermediate

1. ⬜ Implement a new trading strategy
2. ⬜ Add a new RL algorithm (SAC, TD3)
3. ⬜ Connect to real market data
4. ⬜ Run walk-forward validation
5. ⬜ Deploy to paper trading (Alpaca)

### Advanced

1. ⬜ Multi-asset portfolio optimization
2. ⬜ Options pricing integration
3. ⬜ Regime detection module
4. ⬜ High-frequency execution modeling
5. ⬜ Distributed training (Ray)

---

## Learning Resources

### Books
- **"Reinforcement Learning: An Introduction"** - Sutton & Barto (free online)
- **"Algorithmic Trading"** - Ernest Chan
- **"Advances in Financial Machine Learning"** - Marcos López de Prado

### Papers
- [Proximal Policy Optimization](https://arxiv.org/abs/1707.06347)
- [Deep Reinforcement Learning for Trading](https://arxiv.org/abs/1911.10107)
- [Optimal Execution of Portfolio Transactions](https://www.math.nyu.edu/faculty/chriss/optliq_f.pdf)

### Online Courses
- [Coursera: Reinforcement Learning Specialization](https://www.coursera.org/specializations/reinforcement-learning)
- [QuantConnect Tutorials](https://www.quantconnect.com/tutorials)
- [Alpaca API Docs](https://alpaca.markets/docs/)

---

## Getting Help

1. **Check the docs**: Most questions are answered in `docs/` folder
2. **Read the code**: All modules have extensive docstrings
3. **GitHub Issues**: Open an issue for bugs or questions
4. **Discord/Slack**: (Add your community links here)

---

## Contributing

Interested in contributing? Great! See `CONTRIBUTING.md` for guidelines.

**Areas we'd love help with**:
- Additional RL algorithms
- More execution models
- Better visualizations
- Documentation improvements
- Bug fixes

---

## Project Status

- ✅ Core RL engine (stable)
- ✅ Execution simulator (stable)
- ✅ QuantConnect integration (stable)
- 🚧 Multi-agent systems (in progress)
- 🚧 Options pricing (in progress)
- 📋 Cloud deployment (planned)

---

**Last Updated**: January 2026  
**Maintainer**: aliasfar7  
**License**: MIT

Happy trading! 🚀📈
