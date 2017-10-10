# EEM Port Up Action to REST

This is an example Python script utilizing EEM integration.

The example EEM is below:

```
event manager applet INTERFACE-DOWN
 event syslog pattern "%LINEPROTO-5-UPDOWN: Line protocol on Interface .*, changed state to up"
 action 0.0 string trimleft "$_syslog_msg"
 action 1.0 cli command "en"
 action 2.0 cli command "guestshell run python2.7 /flash/scripts/eem_python_examples/portup_to_rest/eem_portup_to_rest.py \"$_string_result\""
```
# requirements

* IOS-XE running >/= 16.5.1 also enabled  
  * GuestShell
  * NETCONF/RESTCONF
* Destination REST API Service up, running and available
  * See repo [switchport-provisioning-api](https://github.com/kecorbin/switchport-provisioning-api)


# running
* onbox

# Development Setup and Testing with Vagrant

Included in the base repo is a Vagrantfile that will spin up a local IOS-XE (CSR) device you can test against.  After the device boots, vagrant uses Ansible to provision the device.  You'll need to install Ansible (2.4+) along with some other Python requirements to get started.  

```bash
# Python 2.7.13+ is recommended
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

vagrant up
```

Once the Vagrant completes, follow these steps to setup the device.  

* Log into the CSR and then into Guest Shell.
* Install `git` into Guest shell

```
$ vagrant ssh
csr1kv#guestshell run bash
[guestshell@guestshell ~]$ sudo yum install -y git
```

* Create directory structure for code
* Clone code down

```
[guestshell@guestshell ~]$ mkdir /flash/scripts
[guestshell@guestshell ~]$ cd /flash/scripts/
[guestshell@guestshell scripts]$ git clone https://github.com/hpreston/eem_python_examples
[guestshell@guestshell scripts]$ cd eem_python_examples/
[guestshell@guestshell eem_python_examples]$
```

* Update `eem_portup_to_rest.py` file with correct details for your running instance of the discovery server

```
[guestshell@guestshell portup_to_rest]$ vi eem_portup_to_rest.py
```

* Section of code to update is

```
# REST Server details
# Replace the IP with the IP of the server running the discovery api
discovery_server = "https://10.192.81.112"
headers = {"Content-type": "application/json"}
```

* Install Python 2.7.13 with included bash script
  * This takes a couple minutes
* Install Python requirements for script into Guest Shell for Python2.7

```
[guestshell@guestshell eem_python_examples]$ sudo ./install_python_2.7.13_guestshell.sh
[guestshell@guestshell eem_python_examples]$ cd portup_to_rest/
[guestshell@guestshell portup_to_rest]$ sudo pip install -t /usr/local/lib/python2.7/site-packages -r requirements.txt
```

* Setup EEM Applet in IOS XE (be sure to exit out of guestshell)

```
[guestshell@guestshell portup_to_rest]$ exit
exit

csr1kv#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
csr1kv(config)#

! Configuration block provided here to make easier to copy/paste
event manager applet INTERFACE-DOWN
 event syslog pattern "%LINEPROTO-5-UPDOWN: Line protocol on Interface .*, changed state to up"
 action 0.0 string trimleft "$_syslog_msg"
 action 1.0 cli command "en"
 action 2.0 cli command "guestshell run python2.7 /flash/scripts/eem_python_examples/portup_to_rest/eem_portup_to_rest.py \"$_string_result\""
```

* Test that it is working

```
csr1kv(config)#end
csr1kv#term mon
csr1kv#debug event manager action cli
csr1kv#conf t
csr1kv(config)#int gigabitEthernet 2
csr1kv(config-if)#shut
csr1kv(config-if)#no shut
```

* Expected Debug output from Test

```
*Oct  6 17:08:42.348: %LINK-3-UPDOWN: Interface GigabitEthernet2, changed state to up
*Oct  6 17:08:43.349: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet2, changed state to up
*Oct  6 17:08:43.359: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : CTL : cli_open called.
*Oct  6 17:08:43.369: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : OUT : csr1kv>
*Oct  6 17:08:43.369: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : IN  : csr1kv>en
csr1kv(config-if)#
csr1kv(config-if)#
*Oct  6 17:08:43.380: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : OUT : csr1kv#
*Oct  6 17:08:43.380: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : IN  : csr1kv#guestshell run python2.7 /flash/scripts/eem_python_examples/portup_to_rest/eem_portup_to_rest.py "*Oct  6 17:08:43.349: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet2, changed state to up"
*Oct  6 17:08:46.163: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : OUT :
*Oct  6 17:08:46.163: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : OUT : csr1kv#
*Oct  6 17:08:46.163: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : CTL : cli_close called.
*Oct  6 17:08:46.163:
*Oct  6 17:08:46.163: tty is now going through its death sequence
```

* Verify discovery message received at server

```
$ curl -X GET --header 'Accept: application/json' 'http://localhost/api/discovery/link'

# Output
[
  {
    "id": "59d7b895d46d4d0001912b2a",
    "interface": "GigabitEthernet2",
    "mac_addresses": [
      "0000.aaaa.bbbb"
    ],
    "switch": "csr1kv"
  }
]
```

# Setup on Catalyst 3560/3850

Due to the Cat 3K supporting "Guest Shell Lite" (hardware requirements), there are some changes to the code needed to make this work.  

* Enter Guest Shell

```
cat-3560#guestshell run bash
[guestshell@guestshell ~]$
```

* Create directory for code (mimicing git paths)
<!-- * Copy code down.  (can't install git on 3K) -->

```
mkdir -p /flash/scripts/eem_python_examples/portup_to_rest
[guestshell@guestshell scripts]$ cd /flash/scripts/eem_python_examples/portup_to_rest/
```

* Create empty file for code

```
[guestshell@guestshell portup_to_rest]$ touch eem_portup_to_rest.py
```

* Use `vi` to open file and copy contents of code into file.
  * Update code with the instance of the REST API server before copying in

```
[guestshell@guestshell portup_to_rest]$ vi eem_portup_to_rest.py
```  

**From here same as other platforms**

* Setup EEM Applet in IOS XE (be sure to exit out of guestshell)

```
[guestshell@guestshell portup_to_rest]$ exit
exit

csr1kv#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
csr1kv(config)#

! Configuration block provided here to make easier to copy/paste
event manager applet INTERFACE-DOWN
 event syslog pattern "%LINEPROTO-5-UPDOWN: Line protocol on Interface .*, changed state to up"
 action 0.0 string trimleft "$_syslog_msg"
 action 1.0 cli command "en"
 action 2.0 cli command "guestshell run python2.7 /flash/scripts/eem_python_examples/portup_to_rest/eem_portup_to_rest.py \"$_string_result\""
```

* Test that it is working

```
csr1kv(config)#end
csr1kv#term mon
csr1kv#debug event manager action cli
csr1kv#conf t
csr1kv(config)#int gigabitEthernet 2
csr1kv(config-if)#shut
csr1kv(config-if)#no shut
```

* Expected Debug output from Test

```
*Oct  6 17:08:42.348: %LINK-3-UPDOWN: Interface GigabitEthernet2, changed state to up
*Oct  6 17:08:43.349: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet2, changed state to up
*Oct  6 17:08:43.359: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : CTL : cli_open called.
*Oct  6 17:08:43.369: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : OUT : csr1kv>
*Oct  6 17:08:43.369: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : IN  : csr1kv>en
csr1kv(config-if)#
csr1kv(config-if)#
*Oct  6 17:08:43.380: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : OUT : csr1kv#
*Oct  6 17:08:43.380: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : IN  : csr1kv#guestshell run python2.7 /flash/scripts/eem_python_examples/portup_to_rest/eem_portup_to_rest.py "*Oct  6 17:08:43.349: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet2, changed state to up"
*Oct  6 17:08:46.163: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : OUT :
*Oct  6 17:08:46.163: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : OUT : csr1kv#
*Oct  6 17:08:46.163: %HA_EM-6-LOG: INTERFACE-DOWN : DEBUG(cli_lib) : : CTL : cli_close called.
*Oct  6 17:08:46.163:
*Oct  6 17:08:46.163: tty is now going through its death sequence
```

* Verify discovery message received at server

```
$ curl -X GET --header 'Accept: application/json' 'http://localhost/api/discovery/link'

# Output
[
  {
    "id": "59d7b895d46d4d0001912b2a",
    "interface": "GigabitEthernet2",
    "mac_addresses": [
      "0000.aaaa.bbbb"
    ],
    "switch": "csr1kv"
  }
]
```
