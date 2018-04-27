#! /bin/bash
### BEGIN INIT INFO
# Provides:			arcadestart
# Required-Start:		$remote_fs $syslog
# Required-Stop:		$remote_fs $syslog
# Default-Start: 		2  3  4  5
# Default-Stop:		0  1  6
# Short-Description:	Start Arcade video
#Description:		DO the thing
### END INIT INFO	

sudo python ~/Desktop/avideo.py &

exit 0
