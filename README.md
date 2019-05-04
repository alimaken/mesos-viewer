mesos-viewer
============
A `Python` `urwid` based CLI application to view active `Mesos` `frameworks` and `metrics`

[https://github.com/alimaken/mesos-viewer/](https://github.com/alimaken/mesos-viewer/)

![mesos-viewer](https://raw.githubusercontent.com/alimaken/mesos-viewer/master/img/mesos-viewer.png)


A sample `config` file is located under `scripts/config.ini.template`.

Use the following to copy the `config` file to appropriate directory:
```bash
mkdir -p ~/.mesos-viewer
cp scripts/config.ini.template ~/.mesos-viewer/config.ini
```

Make sure to use appropriate values for `master_ip` & `master_port` and replace `username` with current user.

#### Examples

```bash
$ ./run.py  
```

#### Key Bindings
```bash
    h,H,?         Show help
    ctrl + u      Page Up
    ctrl + d      Page Down 
    g             Scroll to First framework 
    G             Scroll to Last framework 
    j             Up 
    k             Down 
    r             Refresh 
    s             Show framework WebUI link 
    S,enter       Open framework WebUI link 
    ctrl + r      Reload config 
    z             Show Mesos Metrics popul
    n             Sort by `Name` 
    c             Sort by `CPU` 
    m             Sort by `Memory` 
    u             Sort by `Uptime` 
    t             Sort by `Upsince` 
    /             Fuzzy Search
```
