#!/usr/bin/env python3
"""
Boston 2025 - Real-Time Crypto Monitor
Core monitoring system for 24/7 crypto market surveillance
"""

import json
import websocket
import threading
import time
from datetime import datetime, timedelta
from collections import deque, defaultdict
import statistics
from boston_config import BOSTON_2025_CONFIG, ALERT_THRESHOLDS, get_all_trading_symbols

class Boston2025CryptoMonitor:
    """Real-time crypto market monitor for Boston 2025 trading system"""
    
    def __init__(self):
        self.config = BOSTON_2025_CONFIG
        self.api_key = self.config["api"]["key"]
        self.secret_key = self.config["api"]["secret"]
        self.ws_url = self.config["api"]["ws_url"]
        
        self.ws = None
        self.is_connected = False
        self.is_monitoring = False
        
        # Market data storage
        self.latest_prices = {}
        self.price_history = defaultdict(lambda: deque(maxlen=1000))
        self.volume_history = defaultdict(lambda: deque(maxlen=100))
        self.trade_counts = defaultdict(int)
        
        # Statistics
        self.stats = {
            "start_time": None,
            "total_trades": 0,
            "total_volume": 0,
            "price_changes": {},
            "volatility": {},
            "momentum": {}
        }
        
        # Alert tracking
        self.alerts = []
        self.alert_callbacks = []
        
    def start_monitoring(self, symbols=None):
        """Start real-time monitoring"""
        if symbols is None:
            symbols = self.config["primary_symbols"]
        
        print(f"🚀 Boston 2025 Crypto Monitor Starting")
        print(f"=" * 60)
        print(f"📊 Monitoring: {', '.join(symbols)}")
        print(f"🎯 Strategies: {', '.join([s for s, c in self.config['strategies'].items() if c['enabled']])}")
        print(f"💰 Max position: ${self.config['trading']['max_position_size_usd']:,}")
        print()
        
        self.stats["start_time"] = datetime.now()
        self.is_monitoring = True
        
        # Connect to WebSocket
        if not self._connect():
            print("❌ Failed to connect to market data")
            return False
        
        # Subscribe to symbols
        if not self._subscribe(symbols):
            print("❌ Failed to subscribe to symbols")
            return False
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitoring_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print("✅ Monitoring started successfully")
        print("🔴 LIVE MARKET SURVEILLANCE ACTIVE")
        print("=" * 60)
        
        return True
    
    def _connect(self):
        """Connect to Alpaca crypto WebSocket"""
        try:
            headers = {
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.secret_key
            }
            
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                header=[f"{k}: {v}" for k, v in headers.items()],
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # Start WebSocket in background
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            
            # Wait for connection
            for _ in range(50):
                if self.is_connected:
                    return True
                time.sleep(0.1)
            
            return False
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def _subscribe(self, symbols):
        """Subscribe to crypto symbols"""
        try:
            subscription = {
                "action": "subscribe",
                "trades": symbols,
                "quotes": symbols,
                "bars": symbols
            }
            
            self.ws.send(json.dumps(subscription))
            time.sleep(1)  # Allow subscription to process
            return True
            
        except Exception as e:
            print(f"❌ Subscription error: {e}")
            return False
    
    def _on_open(self, ws):
        """WebSocket opened"""
        self.is_connected = True
    
    def _on_message(self, ws, message):
        """Process incoming market data"""
        try:
            data = json.loads(message)
            
            if isinstance(data, list):
                for item in data:
                    self._process_market_data(item)
            else:
                self._process_market_data(data)
                
        except Exception as e:
            print(f"❌ Message processing error: {e}")
    
    def _process_market_data(self, msg):
        """Process individual market data message"""
        msg_type = msg.get("T")
        
        if msg_type == "t":  # Trade
            self._process_trade(msg)
        elif msg_type == "q":  # Quote
            self._process_quote(msg)
        elif msg_type == "b":  # Bar
            self._process_bar(msg)
        elif msg_type == "success":
            if "authenticated" in str(msg.get("msg", "")):
                print("✅ Authenticated with Alpaca")
        elif msg_type == "subscription":
            print(f"✅ Subscribed to market data streams")
    
    def _process_trade(self, trade):
        """Process trade data"""
        symbol = trade.get("S")
        price = trade.get("p", 0)
        size = trade.get("s", 0)
        side = trade.get("tks", "")
        
        if symbol and price:
            # Update latest price
            old_price = self.latest_prices.get(symbol, {}).get("price", price)
            self.latest_prices[symbol] = {
                "price": price,
                "size": size,
                "side": side,
                "timestamp": datetime.now()
            }
            
            # Store in history
            self.price_history[symbol].append(price)
            self.volume_history[symbol].append(size)
            
            # Update statistics
            self.stats["total_trades"] += 1
            self.stats["total_volume"] += size * price
            self.trade_counts[symbol] += 1
            
            # Calculate price change
            price_change = (price - old_price) / old_price if old_price else 0
            self.stats["price_changes"][symbol] = price_change
            
            # Check for alerts
            self._check_price_alerts(symbol, price, price_change)
            
            # Display update
            side_emoji = "📈" if side == "B" else "📉"
            print(f"{side_emoji} {symbol}: ${price:,.2f} ({price_change:+.2%}) | "
                  f"Size: {size:.4f} | Trades: {self.trade_counts[symbol]}")
    
    def _process_quote(self, quote):
        """Process quote data"""
        symbol = quote.get("S")
        bid = quote.get("bp", 0)
        ask = quote.get("ap", 0)
        
        if symbol and bid and ask:
            spread = ask - bid
            spread_pct = (spread / bid * 100) if bid else 0
            
            # Update latest quotes
            self.latest_prices[symbol] = self.latest_prices.get(symbol, {})
            self.latest_prices[symbol].update({
                "bid": bid,
                "ask": ask,
                "spread": spread,
                "spread_pct": spread_pct,
                "timestamp": datetime.now()
            })
    
    def _process_bar(self, bar):
        """Process bar data"""
        symbol = bar.get("S")
        open_price = bar.get("o", 0)
        high = bar.get("h", 0)
        low = bar.get("l", 0)
        close = bar.get("c", 0)
        volume = bar.get("v", 0)
        
        if symbol:
            # Calculate volatility
            if high and low:
                volatility = (high - low) / low if low else 0
                self.stats["volatility"][symbol] = volatility
            
            # Calculate momentum
            if len(self.price_history[symbol]) > 20:
                recent_prices = list(self.price_history[symbol])[-20:]
                momentum = (close - recent_prices[0]) / recent_prices[0] if recent_prices[0] else 0
                self.stats["momentum"][symbol] = momentum
    
    def _check_price_alerts(self, symbol, price, price_change):
        """Check for price-based alerts"""
        # Price spike alert
        if abs(price_change) > ALERT_THRESHOLDS["price_spike"]:
            alert = {
                "type": "PRICE_SPIKE",
                "symbol": symbol,
                "price": price,
                "change": price_change,
                "timestamp": datetime.now()
            }
            self._trigger_alert(alert)
        
        # Volume spike alert
        if len(self.volume_history[symbol]) > 10:
            avg_volume = statistics.mean(self.volume_history[symbol])
            current_volume = self.volume_history[symbol][-1]
            if current_volume > avg_volume * ALERT_THRESHOLDS["volume_spike"]:
                alert = {
                    "type": "VOLUME_SPIKE",
                    "symbol": symbol,
                    "volume": current_volume,
                    "avg_volume": avg_volume,
                    "timestamp": datetime.now()
                }
                self._trigger_alert(alert)
    
    def _trigger_alert(self, alert):
        """Trigger an alert"""
        self.alerts.append(alert)
        
        # Display alert
        alert_emoji = "🚨" if alert["type"] == "PRICE_SPIKE" else "📊"
        print(f"\n{alert_emoji} ALERT: {alert['type']} - {alert['symbol']}")
        print(f"   Details: {alert}")
        print()
        
        # Call registered callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"❌ Alert callback error: {e}")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        last_stats_update = time.time()
        
        while self.is_monitoring:
            try:
                # Update statistics periodically
                if time.time() - last_stats_update > 30:
                    self._update_statistics()
                    last_stats_update = time.time()
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
    
    def _update_statistics(self):
        """Update and display statistics"""
        runtime = datetime.now() - self.stats["start_time"]
        
        print(f"\n📊 Boston 2025 Market Statistics")
        print(f"=" * 50)
        print(f"⏱️ Runtime: {runtime}")
        print(f"📈 Total trades: {self.stats['total_trades']:,}")
        print(f"💰 Total volume: ${self.stats['total_volume']:,.2f}")
        
        # Symbol statistics
        for symbol in self.latest_prices.keys():
            if symbol in self.latest_prices:
                data = self.latest_prices[symbol]
                print(f"\n{symbol}:")
                print(f"  Price: ${data.get('price', 0):,.2f}")
                print(f"  Change: {self.stats['price_changes'].get(symbol, 0):+.2%}")
                print(f"  Volatility: {self.stats['volatility'].get(symbol, 0):.2%}")
                print(f"  Momentum: {self.stats['momentum'].get(symbol, 0):+.2%}")
                print(f"  Trades: {self.trade_counts[symbol]}")
        
        print(f"\n🚨 Alerts triggered: {len(self.alerts)}")
        print("=" * 50)
    
    def register_alert_callback(self, callback):
        """Register a callback for alerts"""
        self.alert_callbacks.append(callback)
    
    def get_latest_price(self, symbol):
        """Get latest price for a symbol"""
        return self.latest_prices.get(symbol, {}).get("price", None)
    
    def get_market_stats(self, symbol):
        """Get comprehensive market statistics for a symbol"""
        return {
            "price": self.get_latest_price(symbol),
            "change": self.stats["price_changes"].get(symbol, 0),
            "volatility": self.stats["volatility"].get(symbol, 0),
            "momentum": self.stats["momentum"].get(symbol, 0),
            "trades": self.trade_counts[symbol],
            "history": list(self.price_history[symbol])
        }
    
    def _on_error(self, ws, error):
        """Handle WebSocket errors"""
        if "already authenticated" not in str(error):
            print(f"❌ WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close"""
        self.is_connected = False
        print(f"🔌 Market data connection closed")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        if self.ws:
            self.ws.close()
        print("🛑 Boston 2025 monitoring stopped")

def main():
    """Test the Boston 2025 crypto monitor"""
    monitor = Boston2025CryptoMonitor()
    
    # Define alert handler
    def handle_alert(alert):
        print(f"🔔 Alert handler received: {alert['type']} for {alert['symbol']}")
    
    monitor.register_alert_callback(handle_alert)
    
    # Start monitoring
    if monitor.start_monitoring(["BTC/USD", "ETH/USD", "SOL/USD"]):
        try:
            # Run for 60 seconds
            time.sleep(60)
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        finally:
            monitor.stop_monitoring()
            
            # Display final statistics
            print(f"\n📊 Final Statistics:")
            print(f"Total trades: {monitor.stats['total_trades']}")
            print(f"Total alerts: {len(monitor.alerts)}")

if __name__ == "__main__":
    main()