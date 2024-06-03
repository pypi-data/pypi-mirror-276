PORT=8022
/Applications/Tailscale.app/Contents/MacOS/Tailscale funnel --bg --set-path attention2 $PORT
cd `dirname $0`/../src
uvicorn examples.attention:app --port $PORT --reload
