#!/system/bin/sh
set -u

CORE_ROOT=/data/local/openlps/release
APP_BUSYBOX=/data/data/com.openlps.networktoolkit/files/busybox

if [ ! -d "$CORE_ROOT" ]; then
  echo "FAIL:core-root-missing"
  exit 1
fi

if [ ! -x "$APP_BUSYBOX" ]; then
  echo "FAIL:app-busybox-missing"
  exit 1
fi

echo "PASS:core-root-present"
test -f "$CORE_ROOT/4.0" && echo "PASS:install-marker-present" \
  || echo "FAIL:install-marker-missing"
test -d "$CORE_ROOT/usr" && echo "PASS:usr-present" \
  || echo "FAIL:usr-missing"

"$APP_BUSYBOX" chroot "$CORE_ROOT" /bin/sh <<'CHROOT_TESTS'
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

echo "INFO:alpine=$(cat /etc/alpine-release 2>/dev/null || echo unknown)"
echo "INFO:arch=$(uname -m)"

for tool in sh bash busybox python3 pip3 curl wget nmap aircrack-ng macchanger \
  sqlite3 ssh hydra nuclei msfconsole searchsploit
do
  tool_path="$(command -v "$tool" 2>/dev/null || true)"
  if [ -n "$tool_path" ]; then
    echo "PRESENT:$tool:$tool_path"
  else
    echo "MISSING:$tool"
  fi
done

nmap --version 2>/dev/null | head -n 1 | sed 's/^/VERSION:nmap:/'
python3 --version 2>&1 | head -n 1 | sed 's/^/VERSION:python3:/'
curl --version 2>/dev/null | head -n 1 | sed 's/^/VERSION:curl:/'
CHROOT_TESTS
