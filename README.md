Test listening socket (aka server socket) migration from one process to another
with zero-downtime for clients

1st shell:
```
$ python old.py
```

2st shell: (connect to server)
```
$ telnet localhots 5566
```

3rd shell (trigger the migration)
```
$ python new.py
```
At this point, `new.py` will take over the listening socket (:5566) and the `old.py` process will cease control and terminate


