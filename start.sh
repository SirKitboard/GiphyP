#!/bin/sh
systemctl daemon-reload
sudo systemctl restart giphyp
sudo systemctl enable giphyp
