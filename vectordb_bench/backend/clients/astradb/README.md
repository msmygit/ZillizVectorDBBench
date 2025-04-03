## DataStax Astra DB
This helps testing [**DataStax Astra DB**](https://db.new) vector store service.
### Option 1: Using virtual environment
```
python3 -m venv venv
source venv/bin/activate
pip install vectordb-bench[astradb]
```

### Option 2: Using pipx
```
sudo apt install -y pipx
pipx install vectordb-bench[astradb] [--force]
```
and you will see output as below,
```
$ pipx install vectordb-bench[astradb]
  installed package vectordb-bench 0.0.23, installed using Python 3.12.3
  These apps are now globally available
    - init_bench
    - vectordbbench
⚠️  Note: '/home/ubuntu/.local/bin' is not on your PATH environment variable. These apps will not be globally accessible until your PATH is updated. Run `pipx ensurepath` to automatically add
    it, or manually modify your PATH in your shell's config file (i.e. ~/.bashrc).
done! ✨ 🌟 ✨
```
In which case, we will run `pipx ensurepath` and optionally run `pipx completions` and add it to `~/.bashrc` or `~/.zshrc` file.

You may notice getting the following error when attempting to invoke the tool,
```
$ vectordbbench --help
Traceback (most recent call last):
  File "/home/ubuntu/.local/bin/vectordbbench", line 5, in <module>
    from vectordb_bench.cli.vectordbbench import cli
  File "/home/ubuntu/.local/share/pipx/venvs/vectordb-bench/lib/python3.12/site-packages/vectordb_bench/cli/vectordbbench.py", line 5, in <module>
    from ..backend.clients.milvus.cli import MilvusAutoIndex
  File "/home/ubuntu/.local/share/pipx/venvs/vectordb-bench/lib/python3.12/site-packages/vectordb_bench/backend/clients/milvus/cli.py", line 198, in <module>
    @click_parameter_decorators_from_typed_dict(MilvusGPUBruteForceTypedDict)
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
NameError: name 'MilvusGPUBruteForceTypedDict' is not defined
```
and then tried,
```
$ pipx install vectordb-bench vectordb-bench[astradb] --force
Installing to existing venv 'vectordb-bench'
  installed package vectordb-bench 0.0.23, installed using Python 3.12.3
  These apps are now globally available
    - init_bench
    - vectordbbench
done! ✨ 🌟 ✨
Installing to existing venv 'vectordb-bench'
  installed package vectordb-bench 0.0.23, installed using Python 3.12.3
  These apps are now globally available
    - init_bench
    - vectordbbench
done! ✨ 🌟 ✨
```

but, still got the same error when running `vectordbbench --help`. So, I then tried,
```
$ init_bench
2025-04-03 23:26:46,777 | INFO: all configs: [('ALIYUN_OSS_URL', 'assets.zilliz.com.cn/benchmark/'), ('AWS_S3_URL', 'assets.zilliz.com/benchmark/'), ('CONCURRENCY_DURATION', 30), ('CONFIG_LOCAL_DIR', PosixPath('/home/ubuntu/.local/share/pipx/venvs/vectordb-bench/lib/python3.12/site-packages/vectordb_bench/config-files')), ('CUSTOM_CONFIG_DIR', PosixPath('/home/ubuntu/.local/share/pipx/venvs/vectordb-bench/lib/python3.12/site-packages/vectordb_bench/custom/custom_case.json')), ('DATASET_LOCAL_DIR', '/tmp/vectordb_bench/dataset'), ('DEFAULT_DATASET_URL', 'assets.zilliz.com/benchmark/'), ('DROP_OLD', True), ('K_DEFAULT', 100), ('LOG_LEVEL', 'INFO'), ('NUM_CONCURRENCY', [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]), ('NUM_PER_BATCH', 100), ('RESULTS_LOCAL_DIR', PosixPath('/home/ubuntu/.local/share/pipx/venvs/vectordb-bench/lib/python3.12/site-packages/vectordb_bench/results')), ('USE_SHUFFLED_DATA', True)] (__main__.py:12) (3936)
2025-04-03 23:26:46,779 | WARNING: exit, err=[Errno 2] No such file or directory: 'streamlit'
stack trace=Traceback (most recent call last):
  File "/home/ubuntu/.local/share/pipx/venvs/vectordb-bench/lib/python3.12/site-packages/vectordb_bench/__main__.py", line 32, in run_streamlit
    subprocess.run(cmd, check=True)
  File "/usr/lib/python3.12/subprocess.py", line 548, in run
    with Popen(*popenargs, **kwargs) as process:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/subprocess.py", line 1026, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/usr/lib/python3.12/subprocess.py", line 1955, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'streamlit'
 (__main__.py:36) (3936)
 ```

 Now, I started loosing patience and now trying to the option 1 route now.

 ```
$ pipx uninstall vectordb-bench 
uninstalled vectordb-bench! ✨ 🌟 ✨
```
and then
```
rm -rf venv
```
and then
```
python3 -m venv venv
source venv/bin/activate
pip install vectordb-bench[astradb]
```
and then still no luck,
```
$ vectordbbench --help
Traceback (most recent call last):
  File "/home/ubuntu/ZillizVectorDBBench/venv/bin/vectordbbench", line 5, in <module>
    from vectordb_bench.cli.vectordbbench import cli
  File "/home/ubuntu/ZillizVectorDBBench/venv/lib/python3.12/site-packages/vectordb_bench/cli/vectordbbench.py", line 5, in <module>
    from ..backend.clients.milvus.cli import MilvusAutoIndex
  File "/home/ubuntu/ZillizVectorDBBench/venv/lib/python3.12/site-packages/vectordb_bench/backend/clients/milvus/cli.py", line 198, in <module>
    @click_parameter_decorators_from_typed_dict(MilvusGPUBruteForceTypedDict)
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
NameError: name 'MilvusGPUBruteForceTypedDict' is not defined
```

Now with AI assistants,
```
pip install -e .
```
helped resolve the issue.

Alternatively, one can also run `pip install git+https://github.com/msmygit/ZillizVectorDBBench.git`

---