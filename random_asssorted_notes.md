# Setup to DHCP server to Connect to PI
```
dnsmasq -d -i en13 -F 192.168.4.1,192.168.4.254
```

# Stream Camera with FFmpeg
```
ffmpeg  -f v4l2  -input_format mjpeg -i /dev/video0 -preset ultrafast -tune zerolatency  -f mpegts 'udp://192.168.4.1:42923'
```

# Get Video from Remote Computer with FFPlay
```
ffplay -flags low_delay  -f mpegts -loglevel debug   -probesize 32 -analyzeduration 0 -tune zerolatency  -framedrop  -max_delay 0 -sync ext  'udp://192.168.4.1:42923'
```
