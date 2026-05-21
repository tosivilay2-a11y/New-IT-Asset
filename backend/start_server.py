"""
Start the backend server with proper error handling
"""
import uvicorn
import sys

if __name__ == "__main__":
    try:
        print("=" * 70)
        print("Starting IT Asset Management Backend Server")
        print("=" * 70)
        print()
        print("Server will be available at:")
        print("  - http://localhost:8000")
        print("  - http://127.0.0.1:8000")
        print("  - http://0.0.0.0:8000")
        print()
        print("API Documentation: http://localhost:8000/docs")
        print()
        print("Press CTRL+C to stop the server")
        print("=" * 70)
        print()
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
