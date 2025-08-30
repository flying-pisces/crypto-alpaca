#!/usr/bin/env python3
"""
Boston 2025 - Trading Dashboard
Real-time dashboard for monitoring and controlling the trading system
"""

import time
import threading
import json
from datetime import datetime, timedelta
from trading_engine import Boston2025TradingEngine, TradeType, TradeStatus
from boston_config import BOSTON_2025_CONFIG

class Boston2025Dashboard:
    """Real-time trading dashboard"""
    
    def __init__(self):
        self.engine = Boston2025TradingEngine()
        self.is_running = False
        self.display_mode = "overview"  # overview, trades, performance, positions
        
    def start_dashboard(self):
        """Start the dashboard"""
        print("🚀 Boston 2025 Trading Dashboard")
        print("=" * 80)
        print("🎯 Advanced Crypto Trading System")
        print("📊 Real-time monitoring and control")
        print()
        
        self.is_running = True
        
        # Start trading engine
        if not self.engine.start_trading():
            print("❌ Failed to start trading engine")
            return
        
        # Start dashboard display loop
        display_thread = threading.Thread(target=self._display_loop)
        display_thread.daemon = True
        display_thread.start()
        
        # Command interface
        self._command_interface()
    
    def _display_loop(self):
        """Main display loop"""
        while self.is_running:
            try:
                # Clear screen (basic)
                print("\n" * 2)
                
                if self.display_mode == "overview":
                    self._display_overview()
                elif self.display_mode == "trades":
                    self._display_trades()
                elif self.display_mode == "performance":
                    self._display_performance()
                elif self.display_mode == "positions":
                    self._display_positions()
                
                time.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"❌ Display error: {e}")
    
    def _display_overview(self):
        """Display main overview"""
        print("=" * 80)
        print(f"🚀 BOSTON 2025 TRADING DASHBOARD - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # System status
        status_color = "🟢" if self.engine.is_trading else "🔴"
        print(f"{status_color} System Status: {'ACTIVE' if self.engine.is_trading else 'STOPPED'}")
        
        # Capital information
        total_equity = self._calculate_total_equity()
        pnl_today = self.engine.daily_pnl
        pnl_color = "📈" if pnl_today >= 0 else "📉"
        
        print(f"💰 Total Equity: ${total_equity:,.2f}")
        print(f"💵 Available Capital: ${self.engine.available_capital:,.2f}")
        print(f"{pnl_color} Today's P&L: ${pnl_today:+,.2f}")
        
        # Market overview
        print(f"\n📊 MARKET OVERVIEW")
        print("-" * 40)
        
        for symbol in BOSTON_2025_CONFIG["primary_symbols"]:
            stats = self.engine.monitor.get_market_stats(symbol)
            if stats and stats["price"]:
                change = stats.get("change", 0)
                change_color = "📈" if change >= 0 else "📉"
                volatility = stats.get("volatility", 0)
                
                print(f"{change_color} {symbol:10} ${stats['price']:>8,.2f} "
                      f"({change:+6.2%}) Vol: {volatility:5.2%}")
        
        # Active positions
        print(f"\n🔄 ACTIVE POSITIONS ({len(self.engine.open_trades)})")
        print("-" * 40)
        
        if not self.engine.open_trades:
            print("   No open positions")
        else:
            for trade in list(self.engine.open_trades.values())[:5]:  # Show first 5
                current_price = self.engine.monitor.get_latest_price(trade.symbol)
                if current_price:
                    unrealized_pnl = trade.get_current_pnl(current_price)
                    pnl_color = "📈" if unrealized_pnl >= 0 else "📉"
                    
                    print(f"{pnl_color} {trade.symbol} {trade.trade_type.value:4} "
                          f"{trade.size:8.4f} @ ${trade.entry_price:8.2f} "
                          f"P&L: ${unrealized_pnl:+8.2f}")
        
        # Recent trades
        print(f"\n📋 RECENT TRADES ({len(self.engine.closed_trades)})")
        print("-" * 40)
        
        recent_trades = self.engine.closed_trades[-5:] if self.engine.closed_trades else []
        if not recent_trades:
            print("   No completed trades")
        else:
            for trade in reversed(recent_trades):
                pnl_color = "📈" if trade.pnl >= 0 else "📉"
                print(f"{pnl_color} {trade.symbol} {trade.trade_type.value:4} "
                      f"{trade.size:8.4f} @ ${trade.entry_price:8.2f} "
                      f"P&L: ${trade.pnl:+8.2f}")
        
        # Alerts
        recent_alerts = self.engine.monitor.alerts[-3:] if self.engine.monitor.alerts else []
        if recent_alerts:
            print(f"\n🚨 RECENT ALERTS")
            print("-" * 40)
            for alert in recent_alerts:
                alert_time = alert.get("timestamp", datetime.now()).strftime("%H:%M:%S")
                print(f"   {alert_time} {alert['type']} - {alert['symbol']}")
        
        print("\n💡 Commands: overview | trades | performance | positions | stop")
        print("=" * 80)
    
    def _display_trades(self):
        """Display detailed trade information"""
        print("=" * 80)
        print("📋 DETAILED TRADES VIEW")
        print("=" * 80)
        
        # Open trades
        print(f"🔄 OPEN TRADES ({len(self.engine.open_trades)})")
        print("-" * 80)
        print(f"{'Symbol':<10} {'Type':<4} {'Size':<10} {'Entry':<10} {'Current':<10} {'P&L':<10} {'Time'}")
        print("-" * 80)
        
        for trade in self.engine.open_trades.values():
            current_price = self.engine.monitor.get_latest_price(trade.symbol)
            if current_price:
                unrealized_pnl = trade.get_current_pnl(current_price)
                hold_time = datetime.now() - trade.entry_time
                
                print(f"{trade.symbol:<10} {trade.trade_type.value:<4} {trade.size:<10.4f} "
                      f"${trade.entry_price:<9.2f} ${current_price:<9.2f} "
                      f"${unrealized_pnl:<+9.2f} {str(hold_time).split('.')[0]}")
        
        # Closed trades
        print(f"\n✅ CLOSED TRADES ({len(self.engine.closed_trades)})")
        print("-" * 80)
        print(f"{'Symbol':<10} {'Type':<4} {'Size':<10} {'Entry':<10} {'Exit':<10} {'P&L':<10} {'Strategy'}")
        print("-" * 80)
        
        recent_closed = self.engine.closed_trades[-10:] if self.engine.closed_trades else []
        for trade in reversed(recent_closed):
            print(f"{trade.symbol:<10} {trade.trade_type.value:<4} {trade.size:<10.4f} "
                  f"${trade.entry_price:<9.2f} ${trade.exit_price:<9.2f} "
                  f"${trade.pnl:<+9.2f} {trade.strategy.value}")
        
        print("=" * 80)
    
    def _display_performance(self):
        """Display performance analytics"""
        print("=" * 80)
        print("📈 PERFORMANCE ANALYTICS")
        print("=" * 80)
        
        total_trades = len(self.engine.closed_trades)
        if total_trades == 0:
            print("No completed trades for analysis")
            print("=" * 80)
            return
        
        # Calculate metrics
        winning_trades = self.engine.performance_stats["winning_trades"]
        losing_trades = self.engine.performance_stats["losing_trades"]
        total_pnl = self.engine.performance_stats["total_pnl"]
        
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        avg_win = sum(t.pnl for t in self.engine.closed_trades if t.pnl > 0) / max(1, winning_trades)
        avg_loss = sum(t.pnl for t in self.engine.closed_trades if t.pnl < 0) / max(1, losing_trades)
        profit_factor = abs(avg_win * winning_trades / (avg_loss * losing_trades)) if losing_trades > 0 else float('inf')
        
        total_equity = self._calculate_total_equity()
        total_return = (total_equity - self.engine.total_capital) / self.engine.total_capital
        
        print(f"📊 TRADING STATISTICS")
        print(f"-" * 40)
        print(f"Total Trades:     {total_trades}")
        print(f"Winning Trades:   {winning_trades} ({win_rate:.1%})")
        print(f"Losing Trades:    {losing_trades} ({1-win_rate:.1%})")
        print(f"Win Rate:         {win_rate:.1%}")
        print(f"Profit Factor:    {profit_factor:.2f}")
        
        print(f"\n💰 FINANCIAL PERFORMANCE")
        print(f"-" * 40)
        print(f"Initial Capital:  ${self.engine.total_capital:,.2f}")
        print(f"Current Equity:   ${total_equity:,.2f}")
        print(f"Total Return:     {total_return:+.2%}")
        print(f"Total P&L:        ${total_pnl:+,.2f}")
        print(f"Average Win:      ${avg_win:+,.2f}")
        print(f"Average Loss:     ${avg_loss:+,.2f}")
        
        print(f"\n📅 TODAY'S PERFORMANCE")
        print(f"-" * 40)
        print(f"Trades Today:     {self.engine.trades_today}")
        print(f"P&L Today:        ${self.engine.daily_pnl:+,.2f}")
        print(f"Max Drawdown:     {self.engine.max_drawdown_today:.2%}")
        
        # Strategy breakdown
        print(f"\n🎯 STRATEGY BREAKDOWN")
        print(f"-" * 40)
        strategy_stats = {}
        for trade in self.engine.closed_trades:
            strategy = trade.strategy.value
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {"trades": 0, "pnl": 0, "wins": 0}
            
            strategy_stats[strategy]["trades"] += 1
            strategy_stats[strategy]["pnl"] += trade.pnl
            if trade.pnl > 0:
                strategy_stats[strategy]["wins"] += 1
        
        for strategy, stats in strategy_stats.items():
            win_rate = stats["wins"] / stats["trades"] if stats["trades"] > 0 else 0
            print(f"{strategy:<15} Trades: {stats['trades']:3} "
                  f"Win Rate: {win_rate:5.1%} P&L: ${stats['pnl']:+8.2f}")
        
        print("=" * 80)
    
    def _display_positions(self):
        """Display portfolio positions"""
        print("=" * 80)
        print("📊 PORTFOLIO POSITIONS")
        print("=" * 80)
        
        print(f"💰 CAPITAL ALLOCATION")
        print(f"-" * 40)
        total_equity = self._calculate_total_equity()
        print(f"Total Equity:     ${total_equity:,.2f}")
        print(f"Available Cash:   ${self.engine.available_capital:,.2f}")
        print(f"Deployed Capital: ${total_equity - self.engine.available_capital:,.2f}")
        
        deployment_pct = (total_equity - self.engine.available_capital) / total_equity if total_equity > 0 else 0
        print(f"Deployment %:     {deployment_pct:.1%}")
        
        print(f"\n📈 POSITION DETAILS")
        print(f"-" * 40)
        print(f"{'Symbol':<10} {'Position':<12} {'Market Value':<15} {'Unrealized P&L':<15} {'%'}")
        print("-" * 70)
        
        total_unrealized = 0
        for symbol, position_size in self.engine.portfolio.items():
            if abs(position_size) < 0.0001:  # Skip negligible positions
                continue
            
            current_price = self.engine.monitor.get_latest_price(symbol)
            if current_price:
                market_value = position_size * current_price
                
                # Calculate unrealized P&L for this symbol
                symbol_unrealized = sum(
                    trade.get_current_pnl(current_price)
                    for trade in self.engine.open_trades.values()
                    if trade.symbol == symbol
                )
                
                total_unrealized += symbol_unrealized
                portfolio_pct = market_value / total_equity * 100 if total_equity > 0 else 0
                
                print(f"{symbol:<10} {position_size:<12.4f} ${market_value:<14,.2f} "
                      f"${symbol_unrealized:<+14.2f} {portfolio_pct:5.1f}%")
        
        print("-" * 70)
        print(f"{'Total':<37} ${total_unrealized:<+14.2f}")
        
        print(f"\n🎯 RISK METRICS")
        print(f"-" * 40)
        max_position_value = max(
            abs(pos * self.engine.monitor.get_latest_price(symbol))
            for symbol, pos in self.engine.portfolio.items()
            if abs(pos) > 0.0001 and self.engine.monitor.get_latest_price(symbol)
        ) if self.engine.portfolio else 0
        
        concentration_risk = max_position_value / total_equity if total_equity > 0 else 0
        
        print(f"Max Position:     ${max_position_value:,.2f} ({concentration_risk:.1%})")
        print(f"Open Positions:   {len(self.engine.open_trades)}")
        print(f"Portfolio Heat:   {len(self.engine.open_trades) / BOSTON_2025_CONFIG['trading']['max_positions']:.1%}")
        
        print("=" * 80)
    
    def _calculate_total_equity(self):
        """Calculate total equity (cash + unrealized P&L)"""
        unrealized_pnl = sum(
            trade.get_current_pnl(self.engine.monitor.get_latest_price(trade.symbol) or trade.entry_price)
            for trade in self.engine.open_trades.values()
        )
        
        return self.engine.available_capital + unrealized_pnl
    
    def _command_interface(self):
        """Command line interface for dashboard control"""
        print("\n💡 Dashboard Commands:")
        print("   overview  - Main overview (default)")
        print("   trades    - Detailed trades view")  
        print("   performance - Performance analytics")
        print("   positions - Portfolio positions")
        print("   stop      - Stop trading system")
        print("   help      - Show commands")
        
        while self.is_running:
            try:
                command = input("\nCommand: ").strip().lower()
                
                if command == "overview":
                    self.display_mode = "overview"
                    print("📊 Switched to overview mode")
                    
                elif command == "trades":
                    self.display_mode = "trades"
                    print("📋 Switched to trades view")
                    
                elif command == "performance":
                    self.display_mode = "performance"  
                    print("📈 Switched to performance analytics")
                    
                elif command == "positions":
                    self.display_mode = "positions"
                    print("📊 Switched to positions view")
                    
                elif command == "stop":
                    print("🛑 Stopping trading system...")
                    self.stop_dashboard()
                    break
                    
                elif command == "help":
                    print("\n💡 Available Commands:")
                    print("   overview, trades, performance, positions, stop, help")
                    
                elif command == "":
                    continue  # Just refresh current view
                    
                else:
                    print(f"❌ Unknown command: {command}. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user")
                self.stop_dashboard()
                break
            except EOFError:
                print("\n🛑 EOF received")
                self.stop_dashboard()
                break
    
    def stop_dashboard(self):
        """Stop the dashboard and trading system"""
        self.is_running = False
        self.engine.stop_trading()
        
        print("\n🎯 Final Boston 2025 Session Summary")
        print("=" * 60)
        
        total_trades = len(self.engine.closed_trades)
        if total_trades > 0:
            total_pnl = self.engine.performance_stats["total_pnl"]
            win_rate = self.engine.performance_stats["winning_trades"] / total_trades
            total_equity = self._calculate_total_equity()
            total_return = (total_equity - self.engine.total_capital) / self.engine.total_capital
            
            print(f"📊 Trades executed: {total_trades}")
            print(f"🎯 Win rate: {win_rate:.1%}")
            print(f"💰 Total P&L: ${total_pnl:+,.2f}")
            print(f"📈 Total return: {total_return:+.2%}")
            print(f"💵 Final equity: ${total_equity:,.2f}")
        else:
            print("📊 No trades were executed during this session")
        
        print(f"🚨 Alerts triggered: {len(self.engine.monitor.alerts)}")
        print("✅ Boston 2025 session completed")

def main():
    """Launch Boston 2025 dashboard"""
    dashboard = Boston2025Dashboard()
    
    try:
        dashboard.start_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard interrupted")
        dashboard.stop_dashboard()

if __name__ == "__main__":
    main()