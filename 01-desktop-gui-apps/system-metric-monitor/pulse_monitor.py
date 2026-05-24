#!/usr/bin/env python
from app.ui import MetricMonitorApp

if __name__ == "__main__":
    print("="*50)
    print(" PULSE MONITOR ENGINE: STARTING SERVICE TELEMETRY")
    print("="*50)
    
    # Initialize component frame loop
    app = MetricMonitorApp()
    app.mainloop()