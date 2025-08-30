#!/usr/bin/env python3
"""
Boston 2025 - Trading Engine
Core trading system with multiple strategies and risk management
"""

import time
import threading
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum
import statistics
from crypto_monitor import Boston2025CryptoMonitor
from boston_config import BOSTON_2025_CONFIG, PERFORMANCE_TARGETS

class TradeType(Enum):
    BUY = "BUY"
    SELL = "SELL"

class TradeStatus(Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

class Strategy(Enum):
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    ML_PREDICTOR = "ml_predictor"

class Trade:
    """Individual trade representation"""
    def __init__(self, symbol, trade_type, size, price, strategy, stop_loss=None, take_profit=None):
        self.id = f"{int(time.time() * 1000)}"  # Timestamp-based ID
        self.symbol = symbol
        self.trade_type = trade_type
        self.size = size
        self.entry_price = price
        self.strategy = strategy
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        
        self.status = TradeStatus.PENDING
        self.entry_time = datetime.now()
        self.exit_time = None
        self.exit_price = None
        self.pnl = 0.0
        
    def update_exit(self, exit_price):
        """Update trade with exit information"""
        self.exit_price = exit_price
        self.exit_time = datetime.now()
        self.status = TradeStatus.EXECUTED
        
        # Calculate P&L
        if self.trade_type == TradeType.BUY:
            self.pnl = (exit_price - self.entry_price) * self.size
        else:
            self.pnl = (self.entry_price - exit_price) * self.size
    
    def get_current_pnl(self, current_price):
        """Calculate current unrealized P&L"""
        if self.trade_type == TradeType.BUY:
            return (current_price - self.entry_price) * self.size
        else:
            return (self.entry_price - current_price) * self.size
    
    def should_stop_loss(self, current_price):
        """Check if stop loss should trigger"""
        if not self.stop_loss:
            return False
        
        if self.trade_type == TradeType.BUY:
            return current_price <= self.stop_loss
        else:
            return current_price >= self.stop_loss
    
    def should_take_profit(self, current_price):
        """Check if take profit should trigger"""
        if not self.take_profit:
            return False
        
        if self.trade_type == TradeType.BUY:
            return current_price >= self.take_profit
        else:
            return current_price <= self.take_profit

class Boston2025TradingEngine:
    """Advanced crypto trading engine for Boston 2025"""
    
    def __init__(self):
        self.config = BOSTON_2025_CONFIG
        self.monitor = Boston2025CryptoMonitor()
        
        # Trading state
        self.is_trading = False
        self.portfolio = {}  # Symbol -> position size
        self.open_trades = {}  # Trade ID -> Trade
        self.closed_trades = []
        self.total_capital = 100000  # Starting capital
        self.available_capital = self.total_capital
        
        # Strategy modules
        self.strategies = {
            Strategy.MOMENTUM: self._momentum_strategy,
            Strategy.MEAN_REVERSION: self._mean_reversion_strategy,
            Strategy.ARBITRAGE: self._arbitrage_strategy,
            Strategy.ML_PREDICTOR: self._ml_predictor_strategy,
        }
        
        # Risk management
        self.daily_pnl = 0.0
        self.max_drawdown_today = 0.0
        self.trades_today = 0
        
        # Performance tracking
        self.performance_stats = {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_pnl": 0.0,
            "max_drawdown": 0.0,
            "start_capital": self.total_capital
        }
        
    def start_trading(self, symbols=None):
        """Start the trading engine"""
        if symbols is None:
            symbols = self.config["primary_symbols"]
        
        print(f"🚀 Boston 2025 Trading Engine Starting")
        print(f"=" * 60)
        print(f"💰 Capital: ${self.total_capital:,}")
        print(f"📊 Symbols: {', '.join(symbols)}")
        print(f"🎯 Strategies: {', '.join([s.value for s in self.strategies.keys() if self._is_strategy_enabled(s)])}")
        print()
        
        # Start market monitor
        if not self.monitor.start_monitoring(symbols):
            print("❌ Failed to start market monitoring")
            return False
        
        # Register for market alerts
        self.monitor.register_alert_callback(self._handle_market_alert)
        
        # Start trading loop
        self.is_trading = True
        trading_thread = threading.Thread(target=self._trading_loop)
        trading_thread.daemon = True
        trading_thread.start()
        
        print("✅ Trading engine started successfully")
        print("🔴 LIVE TRADING ACTIVE")
        print("=" * 60)
        
        return True
    
    def _trading_loop(self):
        """Main trading loop"""
        last_strategy_run = time.time()
        last_performance_update = time.time()
        
        while self.is_trading:
            try:
                current_time = time.time()
                
                # Run strategies every 10 seconds
                if current_time - last_strategy_run > 10:
                    self._run_strategies()
                    last_strategy_run = current_time
                
                # Update performance every 60 seconds
                if current_time - last_performance_update > 60:
                    self._update_performance()
                    last_performance_update = current_time
                
                # Check open positions
                self._manage_open_positions()
                
                # Risk checks
                self._perform_risk_checks()
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Trading loop error: {e}")
    
    def _run_strategies(self):
        """Execute all enabled strategies"""
        for strategy_type in self.strategies.keys():
            if self._is_strategy_enabled(strategy_type):
                try:
                    self.strategies[strategy_type]()
                except Exception as e:
                    print(f"❌ Strategy {strategy_type.value} error: {e}")
    
    def _momentum_strategy(self):
        """Momentum-based trading strategy"""
        if not self._is_strategy_enabled(Strategy.MOMENTUM):
            return
        
        config = self.config["strategies"]["momentum"]
        
        for symbol in self.config["primary_symbols"]:
            stats = self.monitor.get_market_stats(symbol)
            if not stats or stats["price"] is None:
                continue
            
            momentum = stats.get("momentum", 0)
            volatility = stats.get("volatility", 0)
            price = stats["price"]
            
            # Momentum buy signal
            if (momentum > 0.02 and  # 2% upward momentum
                volatility < 0.05 and  # Low volatility
                len(stats.get("history", [])) > config["lookback_periods"]):
                
                if self._can_open_position(symbol, TradeType.BUY):
                    size = self._calculate_position_size(symbol, price, volatility)
                    self._place_trade(symbol, TradeType.BUY, size, price, Strategy.MOMENTUM)
            
            # Momentum sell signal (if we have position)
            elif (momentum < -0.02 and  # 2% downward momentum
                  self._get_position_size(symbol) > 0):
                
                if self._can_open_position(symbol, TradeType.SELL):
                    current_position = self._get_position_size(symbol)
                    self._place_trade(symbol, TradeType.SELL, current_position, price, Strategy.MOMENTUM)
    
    def _mean_reversion_strategy(self):
        """Mean reversion trading strategy"""
        if not self._is_strategy_enabled(Strategy.MEAN_REVERSION):
            return
        
        config = self.config["strategies"]["mean_reversion"]
        
        for symbol in self.config["primary_symbols"]:
            stats = self.monitor.get_market_stats(symbol)
            if not stats or stats["price"] is None:
                continue
            
            history = stats.get("history", [])
            if len(history) < config["bollinger_periods"]:
                continue
            
            # Calculate Bollinger Bands
            recent_prices = history[-config["bollinger_periods"]:]
            mean_price = statistics.mean(recent_prices)
            std_dev = statistics.stdev(recent_prices)
            
            upper_band = mean_price + (config["bollinger_std"] * std_dev)
            lower_band = mean_price - (config["bollinger_std"] * std_dev)
            
            current_price = stats["price"]
            
            # Oversold condition (buy signal)
            if current_price < lower_band and self._can_open_position(symbol, TradeType.BUY):
                size = self._calculate_position_size(symbol, current_price, std_dev / mean_price)
                target_price = mean_price * config["reversion_target"]
                self._place_trade(symbol, TradeType.BUY, size, current_price, 
                                Strategy.MEAN_REVERSION, take_profit=target_price)
            
            # Overbought condition (sell signal)
            elif current_price > upper_band and self._can_open_position(symbol, TradeType.SELL):
                size = self._calculate_position_size(symbol, current_price, std_dev / mean_price)
                target_price = mean_price * config["reversion_target"]
                self._place_trade(symbol, TradeType.SELL, size, current_price,
                                Strategy.MEAN_REVERSION, take_profit=target_price)
    
    def _arbitrage_strategy(self):
        """Cross-exchange arbitrage strategy (placeholder)"""
        # Requires multiple exchange connections
        pass
    
    def _ml_predictor_strategy(self):
        """Machine learning prediction strategy (placeholder)"""
        # Requires ML model implementation
        pass
    
    def _place_trade(self, symbol, trade_type, size, price, strategy, stop_loss=None, take_profit=None):
        """Place a trade"""
        # Calculate stop loss and take profit if not provided
        if not stop_loss:
            stop_loss_pct = self.config["trading"]["default_stop_loss"]
            if trade_type == TradeType.BUY:
                stop_loss = price * (1 - stop_loss_pct)
            else:
                stop_loss = price * (1 + stop_loss_pct)
        
        if not take_profit:
            take_profit_pct = self.config["trading"]["default_take_profit"]
            if trade_type == TradeType.BUY:
                take_profit = price * (1 + take_profit_pct)
            else:
                take_profit = price * (1 - take_profit_pct)
        
        # Create trade
        trade = Trade(symbol, trade_type, size, price, strategy, stop_loss, take_profit)
        
        # Check if we have sufficient capital
        trade_value = size * price
        if trade_value > self.available_capital:
            print(f"⚠️ Insufficient capital for {symbol} {trade_type.value}: ${trade_value:,.2f} > ${self.available_capital:,.2f}")
            return None
        
        # Execute trade (simulated)
        self.open_trades[trade.id] = trade
        self.available_capital -= trade_value
        
        # Update portfolio position
        if symbol not in self.portfolio:
            self.portfolio[symbol] = 0
        
        if trade_type == TradeType.BUY:
            self.portfolio[symbol] += size
        else:
            self.portfolio[symbol] -= size
        
        self.trades_today += 1
        
        print(f"📈 TRADE EXECUTED: {trade_type.value} {size:.4f} {symbol} @ ${price:,.2f}")
        print(f"   Strategy: {strategy.value} | Stop: ${stop_loss:,.2f} | Target: ${take_profit:,.2f}")
        print(f"   Available capital: ${self.available_capital:,.2f}")
        
        return trade
    
    def _manage_open_positions(self):
        """Manage open positions (stop loss, take profit, time exits)"""
        positions_to_close = []
        
        for trade_id, trade in self.open_trades.items():
            current_price = self.monitor.get_latest_price(trade.symbol)
            if not current_price:
                continue
            
            should_exit = False
            exit_reason = ""
            
            # Check stop loss
            if trade.should_stop_loss(current_price):
                should_exit = True
                exit_reason = "STOP_LOSS"
            
            # Check take profit
            elif trade.should_take_profit(current_price):
                should_exit = True
                exit_reason = "TAKE_PROFIT"
            
            # Check time limit
            elif datetime.now() - trade.entry_time > timedelta(hours=self.config["trading"]["max_hold_time_hours"]):
                should_exit = True
                exit_reason = "TIME_LIMIT"
            
            if should_exit:
                positions_to_close.append((trade_id, current_price, exit_reason))
        
        # Close positions
        for trade_id, exit_price, reason in positions_to_close:
            self._close_position(trade_id, exit_price, reason)
    
    def _close_position(self, trade_id, exit_price, reason="MANUAL"):
        """Close a position"""
        if trade_id not in self.open_trades:
            return
        
        trade = self.open_trades[trade_id]
        trade.update_exit(exit_price)
        
        # Update portfolio
        if trade.trade_type == TradeType.BUY:
            self.portfolio[trade.symbol] -= trade.size
        else:
            self.portfolio[trade.symbol] += trade.size
        
        # Update capital
        trade_value = trade.size * exit_price
        self.available_capital += trade_value
        
        # Update performance
        self.daily_pnl += trade.pnl
        self.performance_stats["total_pnl"] += trade.pnl
        
        if trade.pnl > 0:
            self.performance_stats["winning_trades"] += 1
        else:
            self.performance_stats["losing_trades"] += 1
        
        # Move to closed trades
        self.closed_trades.append(trade)
        del self.open_trades[trade_id]
        
        print(f"🔄 POSITION CLOSED: {trade.symbol} | Reason: {reason}")
        print(f"   P&L: ${trade.pnl:+,.2f} | Exit: ${exit_price:,.2f}")
        print(f"   Available capital: ${self.available_capital:,.2f}")
    
    def _perform_risk_checks(self):
        """Perform risk management checks"""
        # Daily loss limit
        if self.daily_pnl < -self.total_capital * self.config["risk"]["max_daily_loss"]:
            print(f"🚨 DAILY LOSS LIMIT REACHED: ${self.daily_pnl:,.2f}")
            self._emergency_close_all()
        
        # Maximum drawdown
        current_equity = self.available_capital + sum(
            trade.get_current_pnl(self.monitor.get_latest_price(trade.symbol) or trade.entry_price)
            for trade in self.open_trades.values()
        )
        
        drawdown = (self.total_capital - current_equity) / self.total_capital
        if drawdown > self.config["risk"]["max_drawdown"]:
            print(f"🚨 MAX DRAWDOWN REACHED: {drawdown:.2%}")
            self._emergency_close_all()
    
    def _emergency_close_all(self):
        """Emergency close all positions"""
        print("🚨 EMERGENCY: Closing all positions")
        
        for trade_id in list(self.open_trades.keys()):
            trade = self.open_trades[trade_id]
            current_price = self.monitor.get_latest_price(trade.symbol)
            if current_price:
                self._close_position(trade_id, current_price, "EMERGENCY")
        
        self.is_trading = False
    
    def _calculate_position_size(self, symbol, price, volatility):
        """Calculate position size using Kelly criterion"""
        max_position_value = self.config["trading"]["max_position_size_usd"]
        max_size = max_position_value / price
        
        # Adjust for volatility (higher volatility = smaller position)
        volatility_adjustment = max(0.1, 1 - (volatility * 10))
        adjusted_size = max_size * volatility_adjustment
        
        return min(adjusted_size, self.available_capital / price * 0.1)  # Max 10% of capital per trade
    
    def _can_open_position(self, symbol, trade_type):
        """Check if we can open a position"""
        # Check maximum positions
        if len(self.open_trades) >= self.config["trading"]["max_positions"]:
            return False
        
        # Check portfolio exposure
        total_exposure = sum(abs(pos) for pos in self.portfolio.values())
        if total_exposure > self.total_capital * self.config["trading"]["max_portfolio_exposure"]:
            return False
        
        return True
    
    def _get_position_size(self, symbol):
        """Get current position size for symbol"""
        return self.portfolio.get(symbol, 0)
    
    def _is_strategy_enabled(self, strategy):
        """Check if strategy is enabled"""
        return self.config["strategies"].get(strategy.value, {}).get("enabled", False)
    
    def _handle_market_alert(self, alert):
        """Handle market alerts from monitor"""
        print(f"🔔 Trading engine received alert: {alert['type']} for {alert['symbol']}")
        
        # Could trigger specific trading actions based on alerts
        if alert["type"] == "PRICE_SPIKE":
            # Maybe close positions or adjust stops
            pass
    
    def _update_performance(self):
        """Update and display performance statistics"""
        total_trades = len(self.closed_trades)
        if total_trades == 0:
            return
        
        win_rate = self.performance_stats["winning_trades"] / total_trades
        avg_pnl = self.performance_stats["total_pnl"] / total_trades
        
        current_equity = self.available_capital + sum(
            trade.get_current_pnl(self.monitor.get_latest_price(trade.symbol) or trade.entry_price)
            for trade in self.open_trades.values()
        )
        
        total_return = (current_equity - self.total_capital) / self.total_capital
        
        print(f"\n💹 Boston 2025 Performance Update")
        print(f"=" * 50)
        print(f"📊 Total trades: {total_trades}")
        print(f"🎯 Win rate: {win_rate:.1%}")
        print(f"💰 Total P&L: ${self.performance_stats['total_pnl']:,.2f}")
        print(f"📈 Total return: {total_return:+.2%}")
        print(f"💵 Current equity: ${current_equity:,.2f}")
        print(f"🔄 Open positions: {len(self.open_trades)}")
        print(f"📅 Today's P&L: ${self.daily_pnl:+,.2f}")
        print("=" * 50)
    
    def stop_trading(self):
        """Stop trading engine"""
        print("🛑 Stopping Boston 2025 trading engine...")
        self.is_trading = False
        
        # Close all open positions
        for trade_id in list(self.open_trades.keys()):
            trade = self.open_trades[trade_id]
            current_price = self.monitor.get_latest_price(trade.symbol)
            if current_price:
                self._close_position(trade_id, current_price, "SHUTDOWN")
        
        self.monitor.stop_monitoring()
        
        # Final performance report
        self._update_performance()
        print("✅ Trading engine stopped")

def main():
    """Test the Boston 2025 trading engine"""
    engine = Boston2025TradingEngine()
    
    if engine.start_trading(["BTC/USD", "ETH/USD"]):
        try:
            # Run for 5 minutes
            time.sleep(300)
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        finally:
            engine.stop_trading()

if __name__ == "__main__":
    main()