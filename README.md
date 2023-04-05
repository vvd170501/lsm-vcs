# lsm-vcs

Not Git

## Установка

```bash
git clone https://github.com/vvd170501/lsm-vcs.git
cd lsm-vcs
pip install -e .
cd ..
```

## Использование

1. Запустить сервер

```bash
git clone https://github.com/InfJoker/helicopter
cd helicopter
go mod download
make build
./bin/helicopter -config configs/config.yml
```

2. Сконфигурировать адрес сервера

```bash
export HELICOPTER_PORT=1228
export HELICOPTER_ADDRESS=0.0.0.0
```

3. Использовать!

## Команды

- `ngit init [project_id]`
- `ngit checkout [-b] <branch/commit>`
- `ngit branch [branch]`
- `ngit commit -m "commit message"`
- `ngit log`

## Пример использования

```bash
$ mkdir repo
$ cd repo
$ ngit init
$ ngit checkout -b main
$ ngit commit -m "empty commits are allowed"
Commit IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUwOQ==
Message 'empty commits are allowed'
$ touch empty-file
$ mkdir empty-directory
$ ngit commit -m "add empty files"
Commit IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUxNw==
Message 'add empty files'
$ rm -d ./*
$ ngit commit -m "remove everything"
Commit IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUyNQ==
Message 'remove everything'
$ ngit log
IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUyNQ== remove everything
IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUxNw== add empty files
IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUwOQ== empty commits are allowed
$ ngit checkout -b branch
$ echo -e '123\n235\n345' >a
$ ngit commit -m "write smth to a"
Commit IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUzNw==
Message 'write smth to a'
$ echo -e '123\n234\n345' >a
$ ngit commit -m "fix typo in a"
Commit IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTU0NQ==
Message 'fix typo in a'
$ ngit checkout IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUzNw==
HEAD is now at IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTUzNw== (detached)
$ ls
a
$ cat a
123
235
345
$ ngit checkout branch
Switched to branch 'branch'
$ ls
a
$ cat a
123
234
345
$ mkdir dir
$ touch dir/b
$ ngit commit -m 'add file b in directory dir'
Commit IzAwMDAwMDAwMjAwMDAwMDAwMDAwMTU1Mw==
Message 'add file b in directory dir'
$ ngit checkout main
Switched to branch 'main'
$ ls
$ ngit checkout branch
Switched to branch 'branch'
$ ls
a  dir
$ ls dir
b
```

## Особенности работы

- HEAD при инициализации находится в состоянии detached, так как ветки по умолчанию нет
