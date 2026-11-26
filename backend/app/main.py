import os
from app.factory import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("端口", "8500"))
    app.run(host="0.0.0.0", port=port)
