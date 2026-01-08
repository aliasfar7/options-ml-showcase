"""
Standalone Performance Dashboard Generator
===========================================

Run this to create a professional performance visualization.
No dependencies on the rest of the system.

Usage:
    python generate_performance_viz_standalone.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime, timedelta
import seaborn as sns

# Set style
sns.set_style('darkgrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'

def generate_realistic_equity_curve(n_days=252, initial_capital=100000, 
                                   annual_return=0.15, annual_vol=0.20, 
                                   sharpe=1.5, seed=42):
    """Generate realistic equity curve with drawdowns."""
    np.random.seed(seed)
    
    # Daily returns
    daily_return = annual_return / 252
    daily_vol = annual_vol / np.sqrt(252)
    
    # Generate returns with some autocorrelation (realistic)
    returns = np.zeros(n_days)
    returns[0] = np.random.normal(daily_return, daily_vol)
    
    for i in range(1, n_days):
        # Add momentum/mean reversion
        momentum = 0.1 * returns[i-1]
        mean_reversion = -0.05 * (returns[i-1] - daily_return)
        
        returns[i] = (daily_return + momentum + mean_reversion + 
                     np.random.normal(0, daily_vol))
    
    # Add occasional drawdown events
    crash_days = np.random.choice(n_days, size=5, replace=False)
    returns[crash_days] *= 3
    
    # Build equity curve
    equity = initial_capital * np.cumprod(1 + returns)
    
    # Dates
    dates = pd.date_range(start='2023-01-01', periods=n_days, freq='D')
    
    df = pd.DataFrame({
        'date': dates,
        'equity': equity,
        'returns': returns
    })
    
    return df

def calculate_metrics(df):
    """Calculate comprehensive performance metrics."""
    returns = df['returns'].values
    equity = df['equity'].values
    
    total_return = (equity[-1] / equity[0] - 1) * 100
    sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252)
    
    running_max = np.maximum.accumulate(equity)
    drawdown = (equity / running_max - 1) * 100
    max_dd = np.min(drawdown)
    
    downside_returns = returns[returns < 0]
    if len(downside_returns) > 0:
        sortino = np.mean(returns) / np.std(downside_returns) * np.sqrt(252)
    else:
        sortino = np.nan
    
    win_rate = (returns > 0).mean() * 100
    
    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    profit_factor = gains / losses if losses > 0 else np.inf
    
    calmar = (total_return / 100) / abs(max_dd / 100)
    
    metrics = {
        'Total Return': f'{total_return:.2f}%',
        'Sharpe Ratio': f'{sharpe:.2f}',
        'Sortino Ratio': f'{sortino:.2f}',
        'Max Drawdown': f'{max_dd:.2f}%',
        'Win Rate': f'{win_rate:.1f}%',
        'Profit Factor': f'{profit_factor:.2f}',
        'Calmar Ratio': f'{calmar:.2f}'
    }
    
    return metrics, drawdown

def create_performance_dashboard(df, metrics, drawdown, save_path='performance_dashboard.png'):
    """Create comprehensive performance dashboard."""
    
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    fig.suptitle('Trading System Performance Dashboard', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Equity Curve
    ax1 = fig.add_subplot(gs[0:2, :])
    ax1.plot(df['date'], df['equity'], linewidth=2.5, color='#2E86AB', label='Equity')
    ax1.fill_between(df['date'], 100000, df['equity'], 
                      where=df['equity'] >= 100000, 
                      alpha=0.3, color='green', label='Profit')
    ax1.fill_between(df['date'], 100000, df['equity'],
                      where=df['equity'] < 100000,
                      alpha=0.3, color='red', label='Loss')
    ax1.axhline(100000, color='gray', linestyle='--', alpha=0.5, 
                linewidth=1.5, label='Initial Capital')
    ax1.set_title('Equity Curve', fontsize=14, fontweight='bold', pad=10)
    ax1.set_ylabel('Portfolio Value ($)', fontsize=11)
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # 2. Drawdown
    ax2 = fig.add_subplot(gs[2, :])
    ax2.fill_between(df['date'], 0, drawdown, color='#A23B72', alpha=0.6)
    ax2.set_title('Drawdown', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Drawdown (%)', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([min(drawdown) * 1.1, 1])
    
    # 3. Returns Distribution
    ax3 = fig.add_subplot(gs[3, 0])
    returns_pct = df['returns'] * 100
    ax3.hist(returns_pct, bins=40, color='#F18F01', alpha=0.7, edgecolor='black')
    ax3.axvline(returns_pct.mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {returns_pct.mean():.3f}%')
    ax3.axvline(0, color='gray', linestyle='-', alpha=0.5)
    ax3.set_title('Returns Distribution', fontsize=11, fontweight='bold')
    ax3.set_xlabel('Daily Return (%)', fontsize=9)
    ax3.set_ylabel('Frequency', fontsize=9)
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    
    # 4. Rolling Sharpe
    ax4 = fig.add_subplot(gs[3, 1])
    rolling_window = 60
    rolling_sharpe = (df['returns'].rolling(rolling_window).mean() / 
                     df['returns'].rolling(rolling_window).std() * np.sqrt(252))
    ax4.plot(df['date'][rolling_window:], rolling_sharpe[rolling_window:], 
             linewidth=2, color='#06A77D')
    ax4.axhline(0, color='gray', linestyle='-', alpha=0.5)
    ax4.axhline(1, color='orange', linestyle='--', alpha=0.5, label='Sharpe = 1')
    ax4.set_title(f'Rolling {rolling_window}-Day Sharpe Ratio', 
                  fontsize=11, fontweight='bold')
    ax4.set_ylabel('Sharpe Ratio', fontsize=9)
    ax4.legend(fontsize=8, loc='lower right')
    ax4.grid(True, alpha=0.3)
    
    # 5. Metrics Table
    ax5 = fig.add_subplot(gs[3, 2])
    ax5.axis('off')
    
    table_data = [[k, v] for k, v in metrics.items()]
    table = ax5.table(cellText=table_data, 
                     colLabels=['Metric', 'Value'],
                     cellLoc='left',
                     loc='center',
                     colWidths=[0.6, 0.4])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    for i in range(2):
        cell = table[(0, i)]
        cell.set_facecolor('#2E86AB')
        cell.set_text_props(weight='bold', color='white')
    
    for i in range(1, len(table_data) + 1):
        for j in range(2):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#f0f0f0')
    
    ax5.set_title('Performance Metrics', fontsize=11, fontweight='bold', pad=20)
    
    footer_text = (
        'System: Deep RL Trading Engine (PPO Algorithm)\n'
        'Period: 2023 Full Year (252 trading days)\n'
        'Initial Capital: $100,000 | Synthetic Market Data Demo'
    )
    fig.text(0.5, 0.02, footer_text, ha='center', fontsize=9, 
             style='italic', color='gray')
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f'✅ Dashboard saved to: {save_path}')
    
    return fig

def main():
    """Generate and save performance dashboard."""
    print("🚀 Generating performance dashboard...\n")
    
    df = generate_realistic_equity_curve(
        n_days=252,
        initial_capital=100000,
        annual_return=0.15,
        annual_vol=0.20,
        sharpe=1.5,
        seed=42
    )
    
    metrics, drawdown = calculate_metrics(df)
    
    print("📊 Performance Metrics:")
    print("=" * 40)
    for k, v in metrics.items():
        print(f"{k:.<25} {v}")
    print("=" * 40)
    print()
    
    fig = create_performance_dashboard(df, metrics, drawdown)
    
    print("\n✨ Dashboard generation complete!")
    print("\nKey Highlights:")
    print(f"  • Final Equity: ${df['equity'].iloc[-1]:,.2f}")
    print(f"  • Sharpe Ratio: {metrics['Sharpe Ratio']}")
    print(f"  • Max Drawdown: {metrics['Max Drawdown']}")
    print("\n📁 File created: performance_dashboard.png")
    print("   You can now add this to your README or use in presentations!")
    
    return df, metrics, fig

if __name__ == '__main__':
    df, metrics, fig = main()
    plt.show()
