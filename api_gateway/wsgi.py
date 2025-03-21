try:
    from app import create_app
except ModuleNotFoundError:
    import sys
    sys.path.append('/app')
    from app import create_app

app = create_app('production')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
