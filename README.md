# Downloader
File downloader command line tool

# Usage
`python3 main.py --config=config.json`

see config.sample.json 


# Tests
`./run_tests.sh` 

change permission if needed `chmod +x run_tests.sh`

# Modules

`mulitple_downloader.download` handles download of multiple files using `single_downloader`. To extend for new protocols implement a `single_downloader.download` and pass it as a argument to `mulitple_downloader.download`

`single_downloader.download` handles download of one file, if support is needed for new protocol or auth, modify or create a new `single_downloader.download` method and pass it to `mulitple_downloader.download`

# Example

See `main.py`

# Example Output 

```
ftp://speedtest.tele2.net/10GB.zip
 [                    ] 0.2%
abcd://abcd.efg/hij
 [ Failed to download ]
ftp://speedtest.tele2.net/1GB.zip
 [                    ] 1.39%
http://www.google.com
 [====================] 100.0%
 ```
