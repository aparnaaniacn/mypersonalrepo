#!/bin/bash
pwd
user=$3
touch /home/qqwpam7/atm.sh
echo "#!/bin/bash">/home/qqwpam7/atm.sh
echo "export path=$1">>/home/qqwpam7/atm.sh
echo "export software=$2">>/home/qqwpam7/atm.sh
echo "export user=$3">>/home/qqwpam7/atm.sh
echo "export host=$4">>/home/qqwpam7/atm.sh
echo "export id=$5">>/home/qqwpam7/atm.sh
cat /home/qqwpam7/atm.sh
chmod 755 /home/qqwpam7
chmod 777 /home/qqwpam7/atm.sh
sudo su - $user
function fail {
    printf '%s\n' "$*" >&2
    exit 1
}

function wl10 {
        ./WLserver10 stop
        ./WLserver10 start
}

cd /home/qqwpam7
. ./atm.sh
echo $user
echo $path
echo $software
cd "$path" || exit 1
case $software in
   "glassfish") echo "Restarting Glassfish on $host"
               ./GFserver4 stop -i $id &> stop.txt || ./GFserver3 stop -i $id &> stop.txt || ./GFserver stop -i $id &> stop.txt || tmp=1
#                chmod 755 stop.txt
#                tmp=`cat stop.txt | grep "stop-local-instance failed" | wc -l`
                echo "count=$tmp"
                if [ ! -z $tmp ];
                then
                echo "In if condition"
                pid=`./GFserver4 status|grep i$id|cut -d'|' -f3 || ./GFserver3 status|grep i0|cut -d'|' -f3 || ./GFserver status|grep i0|cut -d'|' -f3`
                if [ -z $pid ];
                then
                echo "no pid found, server already stopped."
                else
                cpu=`./GFserver4 status|grep i$id|cut -d'|' -f6 || ./GFserver3 status|grep i0|cut -d'|' -f6 || ./GFserver status|grep i0|cut -d'|' -f6`
                echo "pid=$pid"
                echo "cpu=$cpu"
                cpu1=`echo $cpu|cut -d'%' -f1`
                echo $cpu1
                        if awk -v x=$cpu1 'BEGIN { exit (x >= 95) ? 0 : 1 }'; then
                        echo "checking cpu utilization"
                        echo "PID=$pid"
                        kill -3 $pid
                        kill -9 $pid
                        echo "Process killed"
                        else
                        echo "In inner else loop"
                        load=`cat /proc/loadavg|cut -d' ' -f1`
                        np=`nproc`
                        loadsrv=`echo $((np * 2))`
                        echo "load=$load"
                        echo "loadserver=$loadsrv"
                                if awk -v x=$load -v y=$loadsrv 'BEGIN { exit (x >= y) ? 0 : 1 }'; then
                                echo "Checking load average"
                                echo "PID=$pid"
                                kill -3 $pid
                                kill -9 $pid
                                echo "Process killed"
                                else
                                kill -3 $pid
                                kill -9 $pid
                                echo "Unable to stop the server,CPU and Load is fine.Process killed"
                                fi
                        fi
                        fi
                else
                echo "Server i$id stopped successfully"
                fi
                rm stop.txt
                cd "$path"
               ./GFserver4 start -i $id &> gfout1.txt || ./GFserver3 start -i $id &> gfout1.txt || ./GFserver start -i $id &> gfout1.txt || fail 'Unable to start the server, Manual intervention needed'
                chmod 755 gfout1.txt
                cat gfout1.txt
                grep Successfully gfout1.txt || fail 'Unable to start the server, Manual intervention needed'
                rm gfout1.txt
                ./GFserver4 status || ./GFserver3 status || ./GFserver status
               ;;
       "weblogic") echo "Restarting Weblogic on $host"
                a="status -i $id|cut -d'=' -f3|cut -d' ' -f1"
                pid=`./WLserver12 $a || ./WLserver $a || pgrep -n -u $user -f "java.*(-Dweblogic.Name|-Dwls)=$wlServer_Name"`
                cpu=`ps -p $pid -o %cpu |grep -v CPU`
                load=`cat /proc/loadavg|cut -d' ' -f1`
                np=`nproc`
                loadsrv=`echo $((np * 2))`
                echo "PID=$pid"
                echo "CPU=$cpu"
                echo "load=$load"
                echo "LoadThres=$loadsrv"
                if awk -v x=$cpu 'BEGIN { exit (x >= 95) ? 0 : 1 }'; then
                echo "checking cpu utilization"
                echo "PID=$pid"
                kill -3 $pid
                kill -9 $pid
                echo "Process killed"
                elif awk -v x=$load -v y=$loadsrv 'BEGIN { exit (x >= y) ? 0 : 1 }'; then
                echo "Checking load average"
                echo "PID=$pid"
                kill -3 $pid
                kill -9 $pid
                echo "Process killed"
                else
                echo "Stopping weblogic with script"
                fi
        ./WLserver12 restart -i$id &> wl.txt || ./WLserver restart -i$id &> wl.txt || wl10 &> wl.txt || fail 'Unable to start the server, Manual intervention needed'
        chmod 755 wl.txt
        cat wl.txt
        grep RUNNING wl.txt || fail 'Unable to start the server, Manual intervention needed'
        rm wl.txt
        ./WLserver12 status -i$id || ./WLserver status -i$id || ./WLserver10 status
        ;;
        "apache") echo "Starting apache on $host"
        ./apache24 stop || ./apache stop
        ./apache24 start || ./apache start || fail 'Unable to start the server, Manual intervention needed'
#                ./apache24 start &> aout.txt || ./apache start &> aout.txt || fail 'Unable to start the server, Manual intervention needed'
#                chmod 755 aout.txt
#                cat aout.txt
#                grep successful aout.txt || fail 'Unable to start the server, Manual intervention needed'
#                rm aout.txt
                ./apache24 status || ./apache status
                ;;
   *) echo "Sorry, $software is not present in software list";;
esac
