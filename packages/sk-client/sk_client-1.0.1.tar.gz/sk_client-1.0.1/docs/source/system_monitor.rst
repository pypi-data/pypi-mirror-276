.. _system_monitoring:

System Monitoring
=================

.. _syslog_monitoring:

Setup Syslog
------------

Syslog is used for system event logging see :ref:`syslog_configuration`.

.. _system_enpoints:

System Monitoring API 
---------------------

The REST API `/sys/` endpoints are used to retrieve information about the system state.
It can be used to gather information about the current state of the system
including security relevant information.


System Endpoints are accessible using the REST API:

* Loing as an administrator to access all system endpoints 
* GET ``/sys/status`` returns the current status for all major sub-systems
* GET ``/sys/system-report`` includes information about security settings and open ports.
* GET ``/sys/time`` returns the current system time
* GET ``/sys/version`` returns the system software version
* GET ``/sys/machine-id`` returns the unique identifier for the machine
* GET ``/sys/hostname`` returns the system Hostname
* POST ``/sys/hostname`` set the system Hostname
* POST ``/sys/reboot`` to reboot the system immediately
* POST ``/sys/swupdate`` to upload a new version of system software
* POST ``/sys/swupdate-install`` to install the system software

System endpoints for TLS settings: see :ref:`tls_config`
System endpoints for syslog settings: see :ref:`syslog_configuration`
System endpoints for DNS: see :ref:`dns_config`

.. _system_logs:

System Logs 
-----------

System Logs are managed using the REST API:

* Get the system logs: GET ``/sys/logs/[log_name]``

.. note::
  The logs may be rotated if they grow too large and need to be trimmed.
  The default log size is 10MB, if any log is larger than 10MB it will be trimmed.

  Syslog is the most common way of logging system events and 
  is recommended for production systems.

.. _statistics:

System Statistics 
-----------------
System Statistics are available to retrieve informaton about the system and current 

System Statistics can be viewed using the REST API:

* Get system statistics: GET ``/stats/[stat_name]``

System Statics can also be viewed in the CLI:

* View system statistics: ``show_stats_*``


