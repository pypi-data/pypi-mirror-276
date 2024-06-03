PORT=8002
/Applications/Tailscale.app/Contents/MacOS/Tailscale funnel --bg --set-path attention $PORT
cd `dirname $0`/../src
uvicorn examples.attention:app --port $PORT --reload
