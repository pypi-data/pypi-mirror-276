# web_prink

Print and scan files using web interface

# As service

Go to folder `$HOME/web_prink` and run:

``` bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip3 install web_prink

echo -e '#!/bin/bash\n\n' > run.sh
echo ". $(pwd)/venv/bin/activate" >> run.sh
echo -e '\n\nweb_prink' >> run.sh
chmod ugo+x run.sh
```

Make file `/etc/systemd/system/web_prink.service`:

``` bash
[Unit]
Description=web_prink root mode
After=multi-user.target

[Service]
Type=idle
ExecStart=/path/to/run.sh 0

[Install]
WantedBy=multi-user.target
```

And run:

``` bash
sudo systemctl start web_prink
sudo systemctl enable web_prink
sudo reboot now
```
