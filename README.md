# bashmon

An extremely lightweight terminal based Jenkins build monitor written using Bash.

## Usage

```bash
$ ./bashmon.sh -b jenkinsurl -j "job-one job-two job-three"
```

### If your Jenkins needs authentication

```bash
$ ./bashmon.sh -u username -p password -b jenkinsurl -j "job-one job-two job-three"
```



