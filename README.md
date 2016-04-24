# sound_service_task
## Задание разработать демон - конвертатор wav в mp3

### Как запустить:
1. Установить FFmepg:
  -  `sudo add-apt-repository ppa:mc3man/trusty-media`
  -  `sudo apt-get update`
  -  `sudo apt-get dist-upgrade`
  -  `sudo apt-get install ffmpeg`

2. `pip install -r requirements.txt`
3. `python daemon.py`

Демон логгирует все в файл LOGGING_FILE, откликается на SIGTERM и SIGINT
