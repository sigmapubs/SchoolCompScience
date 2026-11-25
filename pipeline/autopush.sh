#!/bin/bash
# autopush.sh slug1 slug2 ... : push each finished video (status ALLDONE) to GitHub as it completes
cd /mnt/project-files/cs-channel
pending="$*"
while [ -n "$pending" ]; do
  left=""
  for s in $pending; do
    if tail -1 /tmp/status_$s.txt 2>/dev/null | grep -q ALLDONE; then
      flock /tmp/push.lock bash pipeline/push_repo.sh "Add $s" >/tmp/push_$s.log 2>&1 && echo "pushed $s $(date -u +%H:%M)" || echo "PUSHFAIL $s"
    else left="$left $s"; fi
  done
  pending=$(echo $left)
  [ -n "$pending" ] && sleep 120
done
echo all pushed
