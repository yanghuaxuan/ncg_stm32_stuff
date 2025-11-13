# Setup to DHCP server to Connect to PI
Using `dnsmasq` to setup a DHCP server. Make sure you specify the correct interface! You might also need to set an IP for you network card that is inside the network space. For the below example, the network is 192.168.4.1/24, so you may need to set up a static address inside this network. On Mac it looked something like this:

<img width="472" height="547" alt="image" src="https://github.com/user-attachments/assets/d61af03d-2738-4784-a47b-f8afe0a4ad6f" />

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
