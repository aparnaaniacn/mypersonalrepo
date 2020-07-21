#!/bin/bash

service='@option.Service@'
host='@option.Host@'

function fail {
    printf '%s\n' "$*" >&2
    exit 1
}


test -n "$service" || fail 'service is empty'
test -n "$host" || fail 'host is empty'

software=`echo $service| cut -d'_' -f3`
field6=`echo $service|cut -d'_' -f6`
field7=`echo $service|cut -d'_' -f7`
re='^[0-9]+$'
if [[ $field6 =~ $re ]] ; then
   port=$field6
else
   port=$field7
fi
echo "Software= $software"
echo "Port= $port"

test -n "$software" || fail 'software is empty'

ip=`nslookup $host | grep Address | tail -1 | cut -d':' -f2`
echo "IP= $ip"

#if [[ $ip == *#* && $port -eq 80 ]] || [[ $ip == *#* && $port -eq 443 ]];then
#echo "DNS lookup failed"
#exit 1
#fi

if [[ $software == "apache" ]];then
    if [[ $service == *https* ]]; then
    echo "Checking apache https port in nagios."
    ssh -i /www/rdeckweb/.ssh/id_rsa -o StrictHostKeyChecking=no qqwpam7@lpwebmon5 "sudo su - qqnag11 -c'/omd/sites/qqnag11/lib/nagios/plugins/check_http --ssl -e 200,300,301,302,304,307,401,403,404 -N -H $host -I $ip -p $port > test.txt
    cat test.txt
    if grep "OK" test.txt > /dev/null; then
    echo "Alert resolved, Bot can close the incident now." 
    exit 0
    else 
                echo "Alert not resolved, execute rest of  the script"
                exit 1
                fi
    '"
   else
    echo "Checking apache http port in nagios."
    ssh -i /www/rdeckweb/.ssh/id_rsa -o StrictHostKeyChecking=no qqwpam7@lpwebmon5 "sudo su - qqnag11 -c'/omd/sites/qqnag11/lib/nagios/plugins/check_http -e 200,300,301,302,304,307,401,403,404 -N -H $host -I $ip -p $port > test.txt
    if grep "OK" test.txt > /dev/null; then
    echo "Alert resolved, Bot can close the incident now."
                exit 0
                else 
                echo "Alert not resolved, execute rest of  the script"
                exit 1
                fi
    '"
    fi
    if [[ $? -eq 0 ]];then
    exit 0
    fi
else
echo "Trigger a normal restart"
fi

swdbUser="itpsweb"
swdbHost="pldb342.bmwgroup.net"
swdbPort="1542"
swdbSID="swdb"
swdbpass='@option.swdbpass@'

export ORACLE_HOME=/lfs/oracle/ora12102c/

var=`/lfs/oracle/ora12102c/bin/sqlplus $swdbUser/$swdbpass@"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=$swdbHost)(PORT=$swdbPort))(CONNECT_DATA=(SID=$swdbSID)))" <<EOD
set linesize 32767
set feedback off
set heading off
select distinct  projektuser,dir,port,multihoming_number from (
select a.projektuser,a.dir,a.port ,a.multihoming_number from appinstanz a, server b
where b.id=a.server_id  and hostname='$host' and a.port ='$port'
union
select a.projektuser,a.dir,a.sslport ,a.multihoming_number from appinstanz a, server b
where b.id=a.server_id  and hostname='$host' and a.sslport ='$port'
union all
select a.projektuser,a.dir,a.port, 0 from webinstanz a, server b
where b.id=a.server_id and hostname='$host' and a.port ='$port'
union
select a.projektuser,a.dir,a.sslport, 0 from webinstanz a, server b
where b.id=a.server_id and hostname='$host' and a.sslport ='$port')
exit;
EOD`

a=`echo "output: ${var}"| tail -2| head -1`

if [[ ! -z $a ]];then
user=`echo $a| cut -d' ' -f1`
path=`echo $a| cut -d' ' -f2`
id=`echo $a|cut -d' ' -f4`
echo "User= $user"
echo "path= $path"
echo "Instance Id= $id"

ssh -i /www/rdeckweb/.ssh/id_rsa -o StrictHostKeyChecking=no qqwpam7@$host "bash -s" -- < /home/qqrdec1/automation/script.sh $path $software $user $host $id
if [[ $? -eq 0 ]];then
ssh -i /www/rdeckweb/.ssh/id_rsa -o StrictHostKeyChecking=no qqwpam7@lpwebmon5 "bash -s" -- </home/qqrdec1/automation/postcheck.sh $host $port
else
exit 1
fi

else

vard=`/lfs/oracle/ora12102c/bin/sqlplus -s $swdbUser/$swdbpass@"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=$swdbHost)(PORT=$swdbPort))(CONNECT_DATA=(SID=$swdbSID)))" <<EOD
set linesize 32767
set heading off
select a.projektuser,a.dir,b.HOSTNAME from webinstanz a, server b where b.id=a.server_id and a.TESTURL like '%$host%' and port = '$port';
EOD`
echo $vard

if [[ "`echo $vard`" == "no rows selected" ]];then
vard=`/lfs/oracle/ora12102c/bin/sqlplus -s $swdbUser/$swdbpass@"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=$swdbHost)(PORT=$swdbPort))(CONNECT_DATA=(SID=$swdbSID)))" <<EOD
set linesize 32767
set heading off
select a.projektuser,a.dir,b.HOSTNAME from webinstanz a, server b where b.id=a.server_id and a.TESTURL like '%$host:$port%';
EOD`
echo $vard

if [[ "`echo $vard`" == "no rows selected" ]];then
vard=`/lfs/oracle/ora12102c/bin/sqlplus -s $swdbUser/$swdbpass@"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=$swdbHost)(PORT=$swdbPort))(CONNECT_DATA=(SID=$swdbSID)))" <<EOD
set linesize 32767
set heading off
select a.projektuser,a.dir,b.HOSTNAME from webinstanz a, server b where b.id=a.server_id and a.TESTURL like '%$host%';
EOD`
echo $vard
fi
fi

user=`echo $vard| cut -d' ' -f1`
path=`echo $vard| cut -d' ' -f2`
server=`echo $vard| cut -d' ' -f3`
user1=`echo $vard| cut -d' ' -f4`
path1=`echo $vard| cut -d' ' -f5`
server1=`echo $vard| cut -d' ' -f6`

echo $user
echo $path
echo $server
echo $user1
echo $path1
echo $server1

test -n "$user" || fail 'no User returned from DB.'
test -n "$path" || fail 'no Path returned from DB.'
test -n "$host" || fail 'no Path returned from DB.'

ssh -i /www/rdeckweb/.ssh/id_rsa -o StrictHostKeyChecking=no qqwpam7@$server "bash -s" -- < /home/qqrdec1/automation/script.sh $path $software $user $server $id
if [[ $? -eq 0 ]];then
ssh -i /www/rdeckweb/.ssh/id_rsa -o StrictHostKeyChecking=no qqwpam7@$server1 "bash -s" -- < /home/qqrdec1/automation/script.sh $path1 $software $user1 $server1 $id
if [[ $? -eq 0 ]];then
ssh -i /www/rdeckweb/.ssh/id_rsa -o StrictHostKeyChecking=no qqwpam7@lpwebmon5 "bash -s" -- </home/qqrdec1/automation/postcheck.sh $host $port
else
exit 1
fi
else
exit 1
fi
fi
