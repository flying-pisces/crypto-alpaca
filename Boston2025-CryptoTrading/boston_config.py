#!/usr/bin/env python3
"""
Boston 2025 Configuration
Advanced crypto trading system configuration
"""

import os
import sys

# Add parent directory for crypto streaming imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'references', 'alpaca-crypto-streaming'))

# Import working crypto configuration
from crypto_config import API_KEY, SECRET_KEY, CRYPTO_WS_URL

# Boston 2025 Trading Configuration
BOSTON_2025_CONFIG = {
    "project_name": "Boston 2025 Crypto Trading System",
    "version": "1.0.0",
    "environment": "production",
    
    # API Configuration (inherited from working crypto setup)
    "api": {
        "key": API_KEY,
        "secret": SECRET_KEY,
        "ws_url": CRYPTO_WS_URL,
        "rest_url": "https://data.alpaca.markets/v1beta3/crypto"
    },
    
    # Primary Trading Pairs
    "primary_symbols": [
        "BTC/USD",   # Bitcoin - highest liquidity
        "ETH/USD",   # Ethereum - smart contracts leader
        "SOL/USD"    # Solana - high performance blockchain
    ],
    
    # Secondary Trading Pairs
    "secondary_symbols": [
        "AVAX/USD",  # Avalanche
        "ADA/USD",   # Cardano
        "DOT/USD",   # Polkadot
        "LINK/USD"   # Chainlink
    ],
    
    # Speculative Pairs
    "speculative_symbols": [
        "DOGE/USD",  # Dogecoin - meme potential
        "UNI/USD",   # Uniswap - DeFi leader
        "LTC/USD"    # Litecoin - digital silver
    ],
    
    # Trading Parameters
    "trading": {
        "max_position_size_usd": 10000,      # Maximum per position
        "max_portfolio_exposure": 0.80,       # 80% maximum exposure
        "max_correlation": 0.70,              # Maximum correlation between positions
        "min_positions": 3,                   # Minimum diversification
        "max_positions": 10,                  # Maximum concurrent positions
        "default_stop_loss": 0.02,            # 2% stop loss
        "default_take_profit": 0.05,          # 5% take profit
        "trailing_stop": 0.015,               # 1.5% trailing stop
        "max_hold_time_hours": 24,            # Maximum position hold time
    },
    
    # Risk Management
    "risk": {
        "max_daily_loss": 0.05,               # 5% maximum daily loss
        "max_drawdown": 0.10,                 # 10% maximum drawdown
        "position_sizing_method": "kelly",     # Kelly criterion for sizing
        "var_confidence": 0.95,               # Value at Risk confidence
        "risk_free_rate": 0.045,              # Risk-free rate for Sharpe
    },
    
    # Strategy Configuration
    "strategies": {
        "momentum": {
            "enabled": True,
            "lookback_periods": 20,
            "rsi_overbought": 70,
            "rsi_oversold": 30,
            "volume_spike_threshold": 2.0,    # 2x average volume
            "min_trend_strength": 0.6,
        },
        "mean_reversion": {
            "enabled": True,
            "bollinger_periods": 20,
            "bollinger_std": 2,
            "z_score_threshold": 2.5,
            "reversion_target": 0.5,          # Revert to 50% of range
        },
        "arbitrage": {
            "enabled": False,                 # Requires multi-exchange
            "min_spread": 0.002,              # 0.2% minimum spread
            "execution_time_ms": 100,         # Max execution time
        },
        "ml_predictor": {
            "enabled": False,                 # Requires ML models
            "model_type": "lstm",
            "prediction_horizon": 15,         # 15 minutes ahead
            "confidence_threshold": 0.7,
        }
    },
    
    # Data Configuration
    "data": {
        "stream_types": ["trades", "quotes", "bars"],
        "bar_timeframe": "1Min",
        "historical_days": 30,
        "cache_size_mb": 100,
        "tick_buffer_size": 10000,
    },
    
    # Monitoring & Alerts
    "monitoring": {
        "dashboard_port": 8080,
        "refresh_interval_seconds": 1,
        "alert_methods": ["console", "log"],  # Can add email, SMS
        "performance_log_interval": 60,       # Log performance every minute
        "health_check_interval": 30,          # Health check every 30 seconds
    },
    
    # Backtesting
    "backtesting": {
        "initial_capital": 100000,
        "commission_rate": 0.001,             # 0.1% commission
        "slippage_rate": 0.0005,             # 0.05% slippage
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
    },
    
    # Boston 2025 Specific Features
    "boston_2025": {
        "ai_trading_enabled": True,
        "quantum_ready": False,               # Future quantum computing support
        "defi_integration": True,
        "cross_chain_enabled": False,
        "institutional_mode": False,
        "regulatory_compliance": "USA",
        "target_annual_return": 0.30,        # 30% target return
        "target_sharpe_ratio": 1.5,
    }
}

# Performance Targets
PERFORMANCE_TARGETS = {
    "daily": {
        "min_trades": 10,
        "target_return": 0.01,                # 1% daily
        "max_loss": -0.02,                    # -2% maximum
    },
    "weekly": {
        "min_trades": 50,
        "target_return": 0.05,                # 5% weekly
        "max_loss": -0.05,                    # -5% maximum
    },
    "monthly": {
        "min_trades": 200,
        "target_return": 0.20,                # 20% monthly
        "max_loss": -0.10,                    # -10% maximum
    }
}

# Alert Thresholds
ALERT_THRESHOLDS = {
    "price_spike": 0.05,                      # 5% sudden move
    "volume_spike": 3.0,                      # 3x average volume
    "drawdown_warning": 0.05,                 # 5% drawdown warning
    "drawdown_critical": 0.08,                # 8% drawdown critical
    "connection_timeout": 30,                 # 30 seconds timeout
    "data_gap": 60,                          # 60 seconds no data
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "boston2025_trading.log",
    "max_bytes": 10485760,                    # 10MB per file
    "backup_count": 5,
}

def get_all_trading_symbols():
    """Get all configured trading symbols"""
    return (BOSTON_2025_CONFIG["primary_symbols"] + 
            BOSTON_2025_CONFIG["secondary_symbols"] + 
            BOSTON_2025_CONFIG["speculative_symbols"])

def get_active_strategies():
    """Get list of enabled strategies"""
    return [name for name, config in BOSTON_2025_CONFIG["strategies"].items() 
            if config.get("enabled", False)]

def validate_configuration():
    """Validate configuration settings"""
    errors = []
    
    # Check API credentials
    if not API_KEY or not SECRET_KEY:
        errors.append("Missing API credentials")
    
    # Check risk parameters
    if BOSTON_2025_CONFIG["trading"]["max_portfolio_exposure"] > 1.0:
        errors.append("Portfolio exposure cannot exceed 100%")
    
    # Check position limits
    if BOSTON_2025_CONFIG["trading"]["min_positions"] > BOSTON_2025_CONFIG["trading"]["max_positions"]:
        errors.append("Minimum positions cannot exceed maximum positions")
    
    return errors

# Run validation on import
validation_errors = validate_configuration()
if validation_errors:
    print(f"⚠️ Configuration warnings: {validation_errors}")

print(f"🚀 Boston 2025 Configuration Loaded")
print(f"   Primary symbols: {', '.join(BOSTON_2025_CONFIG['primary_symbols'])}")
print(f"   Active strategies: {', '.join(get_active_strategies())}")
print(f"   Max position size: ${BOSTON_2025_CONFIG['trading']['max_position_size_usd']:,}")