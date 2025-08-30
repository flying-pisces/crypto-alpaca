#!/usr/bin/env python3
"""
Crypto Connection Diagnostics
Phase 3 of Pulse Element Project

Comprehensive diagnostic tool to troubleshoot crypto streaming issues:
- API credential validation
- WebSocket connection testing
- Authentication flow debugging
- Error analysis and solutions
"""

import json
import websocket
import time
import threading
from datetime import datetime
import sys
import os

# Add path for imports
sys.path.append(os.path.dirname(__file__))

from env_config import API_KEY, SECRET_KEY, CRYPTO_WS_URL

class CryptoDiagnostics:
    """Diagnostic tool for crypto streaming issues"""
    
    def __init__(self):
        self.ws = None
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.ws_url = CRYPTO_WS_URL
        self.connection_events = []
        self.messages_received = []
        self.errors_encountered = []
        
    def run_comprehensive_diagnostics(self):
        """Run complete diagnostic suite"""
        print("🔍 Crypto Streaming Diagnostics")
        print("=" * 60)
        print("Investigating API authentication and connection issues...")
        print()
        
        # Step 1: Basic credential validation
        self._check_credentials()
        
        # Step 2: Test WebSocket URL accessibility
        self._test_websocket_url()
        
        # Step 3: Attempt connection with detailed logging
        self._test_connection_with_logging()
        
        # Step 4: Compare with working stock/options config
        self._compare_with_working_config()
        
        # Step 5: Generate diagnostic report
        self._generate_diagnostic_report()
    
    def _check_credentials(self):
        """Step 1: Validate API credentials"""
        print("🔐 Step 1: API Credential Validation")
        print("-" * 40)
        
        # Check if credentials exist
        if not self.api_key or not self.secret_key:
            print("❌ CRITICAL: API credentials missing!")
            print("   Check .env file for API_KEY and SECRET_KEY")
            return False
        
        print(f"✅ API Key: {self.api_key[:8]}...{self.api_key[-4:]}")
        print(f"✅ Secret Key: {self.secret_key[:8]}...{self.secret_key[-4:]}")
        
        # Check credential format
        if len(self.api_key) < 20:
            print("⚠️ WARNING: API key seems too short")
        
        if len(self.secret_key) < 20:
            print("⚠️ WARNING: Secret key seems too short")
        
        print("✅ Credentials format appears valid")
        print()
        return True
    
    def _test_websocket_url(self):
        """Step 2: Test WebSocket URL accessibility"""
        print("🌐 Step 2: WebSocket URL Validation")
        print("-" * 40)
        
        print(f"Target URL: {self.ws_url}")
        
        # Validate URL format
        if not self.ws_url.startswith("wss://"):
            print("❌ ERROR: WebSocket URL should start with 'wss://'")
            return False
        
        if "v1beta3/crypto/us" not in self.ws_url:
            print("❌ ERROR: Wrong endpoint - should contain 'v1beta3/crypto/us'")
            return False
        
        print("✅ WebSocket URL format is correct")
        print("✅ Endpoint: v1beta3/crypto/us (Alpaca crypto API)")
        print()
        return True
    
    def _test_connection_with_logging(self):
        """Step 3: Detailed connection test with full logging"""
        print("🔌 Step 3: Live Connection Test")
        print("-" * 40)
        
        print("Attempting WebSocket connection with detailed logging...")
        
        # Enable WebSocket debug
        websocket.enableTrace(True)
        
        try:
            # Create headers
            headers = {
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.secret_key
            }
            
            print(f"🔗 Connecting to: {self.ws_url}")
            print(f"🔑 Using headers: APCA-API-KEY-ID, APCA-API-SECRET-KEY")
            
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                header=[f"{k}: {v}" for k, v in headers.items()],
                on_open=self._diagnostic_on_open,
                on_message=self._diagnostic_on_message,
                on_error=self._diagnostic_on_error,
                on_close=self._diagnostic_on_close
            )
            
            # Run WebSocket in thread
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            
            print("⏳ Waiting for connection (10 seconds max)...")
            
            # Wait and monitor for 10 seconds
            start_time = time.time()
            while time.time() - start_time < 10:
                time.sleep(0.5)
                
                # Check for connection success
                if any("authenticated" in str(event) for event in self.connection_events):
                    print("✅ Connection and authentication successful!")
                    break
                    
                # Check for errors
                if self.errors_encountered:
                    break
            
            # Close connection
            if self.ws:
                self.ws.close()
            
        except Exception as e:
            print(f"❌ Connection exception: {e}")
            self.errors_encountered.append(f"Connection exception: {e}")
        
        print()
    
    def _diagnostic_on_open(self, ws):
        """WebSocket opened - send auth"""
        event = f"[{datetime.now().strftime('%H:%M:%S')}] WebSocket opened"
        print(f"✅ {event}")
        self.connection_events.append(event)
        
        # Send authentication
        auth_message = {
            "action": "auth",
            "key": self.api_key,
            "secret": self.secret_key
        }
        
        print(f"🔐 Sending authentication message...")
        ws.send(json.dumps(auth_message))
    
    def _diagnostic_on_message(self, ws, message):
        """Log all messages received"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        try:
            data = json.loads(message)
            
            # Log message
            event = f"[{timestamp}] Message: {data}"
            print(f"📨 {event}")
            self.messages_received.append(event)
            
            # Check for authentication success
            if isinstance(data, dict) and data.get("T") == "success":
                if "authenticated" in str(data.get("msg", "")):
                    print(f"✅ [{timestamp}] AUTHENTICATION SUCCESSFUL!")
                    
                    # Try to subscribe to test BTC/USD
                    test_sub = {
                        "action": "subscribe",
                        "trades": ["BTC/USD"],
                        "quotes": ["BTC/USD"]
                    }
                    print(f"📡 [{timestamp}] Subscribing to BTC/USD test...")
                    ws.send(json.dumps(test_sub))
            
            # Check for subscription confirmation
            elif isinstance(data, dict) and data.get("T") == "subscription":
                print(f"✅ [{timestamp}] SUBSCRIPTION CONFIRMED!")
            
            # Check for actual data
            elif isinstance(data, dict) and data.get("T") in ["t", "q", "b"]:
                symbol = data.get("S", "N/A")
                price = data.get("p") or data.get("bp") or data.get("c", "N/A")
                print(f"💰 [{timestamp}] LIVE DATA: {symbol} ${price}")
            
            # Check for errors
            elif isinstance(data, dict) and data.get("T") == "error":
                error_msg = data.get("msg", "Unknown error")
                print(f"❌ [{timestamp}] API ERROR: {error_msg}")
                self.errors_encountered.append(f"API Error: {error_msg}")
                
        except json.JSONDecodeError as e:
            event = f"[{timestamp}] JSON decode error: {e}"
            print(f"❌ {event}")
            self.errors_encountered.append(event)
    
    def _diagnostic_on_error(self, ws, error):
        """Log WebSocket errors"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        event = f"[{timestamp}] WebSocket error: {error}"
        print(f"❌ {event}")
        self.errors_encountered.append(event)
    
    def _diagnostic_on_close(self, ws, close_status_code, close_msg):
        """Log WebSocket close"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        event = f"[{timestamp}] WebSocket closed: {close_status_code} - {close_msg}"
        print(f"🔌 {event}")
        self.connection_events.append(event)
    
    def _compare_with_working_config(self):
        """Step 4: Compare with working stock/options configuration"""
        print("🔄 Step 4: Comparing with Stock/Options Config")
        print("-" * 40)
        
        try:
            # Try to import stock config
            sys.path.append("../alpaca-market-data-streaming-api")
            from config import API_KEY as STOCK_API_KEY, SECRET_KEY as STOCK_SECRET_KEY
            
            if self.api_key == STOCK_API_KEY and self.secret_key == STOCK_SECRET_KEY:
                print("✅ Crypto using same credentials as working stock config")
            else:
                print("⚠️ WARNING: Crypto credentials differ from stock config")
                print(f"   Stock API key: {STOCK_API_KEY[:8]}...{STOCK_API_KEY[-4:]}")
                print(f"   Crypto API key: {self.api_key[:8]}...{self.api_key[-4:]}")
            
        except ImportError:
            print("⚠️ Could not import stock config for comparison")
        
        # Check endpoint differences
        stock_endpoint = "wss://stream.data.alpaca.markets/v2/delayed_sip"
        options_endpoint = "wss://stream.data.alpaca.markets/v1beta1/indicative"
        crypto_endpoint = self.ws_url
        
        print(f"\n📊 Endpoint Comparison:")
        print(f"   Stock:   {stock_endpoint}")
        print(f"   Options: {options_endpoint}")
        print(f"   Crypto:  {crypto_endpoint}")
        print(f"✅ All endpoints use same base domain: stream.data.alpaca.markets")
        print()
    
    def _generate_diagnostic_report(self):
        """Step 5: Generate comprehensive diagnostic report"""
        print("📋 Step 5: Diagnostic Report")
        print("=" * 60)
        
        print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Connection events: {len(self.connection_events)}")
        print(f"📨 Messages received: {len(self.messages_received)}")
        print(f"❌ Errors encountered: {len(self.errors_encountered)}")
        print()
        
        # Analysis
        has_auth_success = any("authenticated" in str(event).lower() for event in self.messages_received)
        has_subscription = any("subscription" in str(event).lower() for event in self.messages_received)
        has_live_data = any("LIVE DATA" in str(event) for event in self.messages_received)
        has_errors = len(self.errors_encountered) > 0
        
        print("🎯 Test Results Analysis:")
        print(f"   Authentication: {'✅ SUCCESS' if has_auth_success else '❌ FAILED'}")
        print(f"   Subscription: {'✅ SUCCESS' if has_subscription else '❌ FAILED'}")
        print(f"   Live Data: {'✅ RECEIVED' if has_live_data else '❌ NO DATA'}")
        print(f"   Errors: {'❌ YES' if has_errors else '✅ NONE'}")
        print()
        
        # Detailed error analysis
        if self.errors_encountered:
            print("🔍 Error Details:")
            for i, error in enumerate(self.errors_encountered, 1):
                print(f"   {i}. {error}")
            print()
            
            # Common error solutions
            print("💡 Common Solutions:")
            if "already authenticated" in str(self.errors_encountered).lower():
                print("   • 'Already authenticated' error:")
                print("     - Wait 30+ seconds between connection attempts")
                print("     - Alpaca may rate-limit authentication requests")
                print("     - Try restarting the application")
            
            if "403" in str(self.errors_encountered) or "forbidden" in str(self.errors_encountered).lower():
                print("   • 403/Forbidden error:")
                print("     - Check API key permissions in Alpaca dashboard")
                print("     - Ensure crypto data access is enabled")
                print("     - Verify account subscription level")
            
            if "timeout" in str(self.errors_encountered).lower():
                print("   • Timeout error:")
                print("     - Check internet connection")
                print("     - Try different network/VPN")
                print("     - Alpaca servers may be under load")
            
            print()
        
        # Overall verdict
        if has_auth_success and has_subscription and not has_errors:
            print("🎉 VERDICT: Crypto streaming is working correctly!")
            print("   Your API credentials support crypto data streaming.")
            print("   The connection and authentication process is successful.")
        elif has_auth_success and has_errors:
            print("⚠️ VERDICT: Partial success with some issues")
            print("   Authentication works but there are operational issues.")
            print("   Review error details above for specific problems.")
        else:
            print("❌ VERDICT: Crypto streaming has significant issues")
            print("   Connection or authentication is failing.")
            print("   Check API credentials and account permissions.")
        
        print()
        print("📞 Next Steps:")
        if not has_auth_success:
            print("   1. Verify API credentials in Alpaca dashboard")
            print("   2. Check if crypto data access is enabled on your account")
            print("   3. Ensure account has appropriate subscription level")
        else:
            print("   1. Try running: python basic_crypto_streamer.py")
            print("   2. Test with different crypto pairs (BTC/USD, ETH/USD)")
            print("   3. If issues persist, contact Alpaca support")

def main():
    """Run crypto connection diagnostics"""
    print("🚀 Starting Crypto Connection Diagnostics...")
    print("This will test live connections to Alpaca's crypto WebSocket API")
    print()
    
    diagnostics = CryptoDiagnostics()
    diagnostics.run_comprehensive_diagnostics()
    
    print("\n" + "=" * 60)
    print("🔍 Diagnostics Complete!")
    print("\nIf issues persist:")
    print("  • Check Alpaca account dashboard for crypto permissions")
    print("  • Verify API key status and rate limits") 
    print("  • Try again in a few minutes (rate limiting)")

if __name__ == "__main__":
    main()