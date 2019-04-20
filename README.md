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

Make sure to use appropriate values for `master_ip` & `master_port`.

# Examples

```bash
$ ./run.py  
```