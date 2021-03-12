# eventTranslate
## Translate MQTT "events" from one format to another between two brokers

The insperation behind this was the need to tie the output of ZoneMinder Event Server, which is JSON, to something that Homebridge Camera FFmpeg could use to trigger the Doorbell Alarm on my AppleTV when the front camera detects motion.

Please be gentle, this is my first 100% Python script that I've done.  I'm an "old" C/C++/C# developer, and you will probably notice that in the script.

Any improvements or changes are welcome.

## Basic "install"

1. Copy eventTranslatejson.py to /usr/local/sbin
2. Copy the eventTranslateJson.service to /etc/systemd/system
3. Run the following command
```
    systemctl daemon-reload
    systemctl enable eventTranslateJson.service
    systemctl start eventTranslateJson.service
```
4. Run ***journalctl -xe*** to make sure it's running
5. Edit /usr/local/sbin/eventTranslatejson.py and change *localBroker*, *remoteBroker*, *subscribeTopic*, and *hbtopic* to suit your needs.  *hbTopic* is what will be published to the remote.
6. Restart the service to pick up the changes using
```
systemctl restart eventTranslateJson.service
```
7. Sit back and enjoy!