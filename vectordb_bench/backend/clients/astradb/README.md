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

Now with help of AI assistants I found we need to run below,
```
$ python3 -m pip install -e '.[astradb]'
...
Downloading cassandra_driver-3.29.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 3.1 MB/s eta 0:00:00
...
Successfully installed cassandra-driver-3.29.2 geomet-0.2.1.post1 vectordb-bench-0.1.dev211+gc64e453.d20250404
```
helped resolve the issue.

Alternatively, one can also run `pip install git+https://github.com/msmygit/ZillizVectorDBBench.git`

Now our command works:
```
$ vectordbbench astradb --help
Usage: vectordbbench astradb [OPTIONS]

Options:
...
  --astra-db-id TEXT              Astra DB UUID  [required]
  --astra-token TEXT              Astra DB application token  [default:
                                  ($ASTRA_DB_APPLICATION_TOKEN); required]
  --scb-path TEXT                 Astra DB cluster Secure Connect Bundle
  --astra-env TEXT                Astra DB environment. Valid values:
                                  dev/test/prod
  --keyspace TEXT                 Astra DB cluster keyspace. Default is
                                  'default_keyspace'
  --help                          Show this message and exit.
```

On to next huddle by running `python3 -m vectordb_bench` or `init_bench`,
```
$ init_bench
2025-04-04 02:30:17,212 | INFO: all configs: [('ALIYUN_OSS_URL', 'assets.zilliz.com.cn/benchmark/'), ('AWS_S3_URL', 'assets.zilliz.com/benchmark/'), ('CONCURRENCY_DURATION', 30), ('CONFIG_LOCAL_D
IR', PosixPath('/home/ubuntu/ZillizVectorDBBench/vectordb_bench/config-files')), ('CUSTOM_CONFIG_DIR', PosixPath('/home/ubuntu/ZillizVectorDBBench/vectordb_bench/custom/custom_case.json')), ('DAT
ASET_LOCAL_DIR', '/tmp/vectordb_bench/dataset'), ('DEFAULT_DATASET_URL', 'assets.zilliz.com/benchmark/'), ('DROP_OLD', True), ('K_DEFAULT', 100), ('LOG_LEVEL', 'INFO'), ('NUM_CONCURRENCY', [1, 5,
 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]), ('NUM_PER_BATCH', 100), ('RESULTS_LOCAL_DIR', PosixPath('/home/ubuntu/ZillizVectorDBBench/vectordb_bench/results'))
, ('USE_SHUFFLED_DATA', True)] (__main__.py:12) (4729)

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.31.38.130:8501
  External URL: http://35.91.39.57:8501

2025-04-04 02:36:38.111 Uncaught app execution
Traceback (most recent call last):
  File "/home/ubuntu/ZillizVectorDBBench/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 121, in exec_func_with_error_handling
    result = func()
             ^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 640, in code_to_exec
    exec(code, module.__dict__)
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/frontend/vdb_benchmark.py", line 56, in <module>
    main()
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/frontend/vdb_benchmark.py", line 41, in main
    NavToRunTest(navContainer)
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/frontend/components/check_results/nav.py", line 9, in NavToRunTest
    switch_page("run test")
  File "/home/ubuntu/ZillizVectorDBBench/venv/lib/python3.12/site-packages/streamlit/runtime/metrics_util.py", line 410, in wrapped_func
    result = non_optional_func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/venv/lib/python3.12/site-packages/streamlit_extras/switch_page_button/__init__.py", line 21, in switch_page
    from streamlit.source_util import get_pages
ImportError: cannot import name 'get_pages' from 'streamlit.source_util' (/home/ubuntu/ZillizVectorDBBench/venv/lib/python3.12/site-packages/streamlit/source_util.py)
```

the solution was to downgrade the streamlit version to 1.35.0
```
python3 -m pip install streamlit==1.35.0
```
https://github.com/streamlit/streamlit/pull/5890/files changes this to `st.navigation`.

Also, to disable the streamlit telemetry, do the following,
- Create a file `~/.streamlit/config.toml` on the machine where this is run from.
- Add the following lines to the file:
```
[browser]
gatherUsageStats = false
```

Still end up with the following error,
```
$ python3 -m vectordb_bench
2025-04-04 16:55:07,248 | INFO: all configs: [('ALIYUN_OSS_URL', 'assets.zilliz.com.cn/benchmark/'), ('AWS_S3_URL', 'assets.zilliz.com/benchmark/'), ('CONCURRENCY_DURATION', 30), ('CONFIG_LOCAL_D
IR', PosixPath('/home/ubuntu/ZillizVectorDBBench/vectordb_bench/config-files')), ('CUSTOM_CONFIG_DIR', PosixPath('/home/ubuntu/ZillizVectorDBBench/vectordb_bench/custom/custom_case.json')), ('DAT
ASET_LOCAL_DIR', '/tmp/vectordb_bench/dataset'), ('DEFAULT_DATASET_URL', 'assets.zilliz.com/benchmark/'), ('DROP_OLD', True), ('K_DEFAULT', 100), ('LOG_LEVEL', 'INFO'), ('NUM_CONCURRENCY', [1, 5,
 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]), ('NUM_PER_BATCH', 100), ('RESULTS_LOCAL_DIR', PosixPath('/home/ubuntu/ZillizVectorDBBench/vectordb_bench/results'))
, ('USE_SHUFFLED_DATA', True)] (__main__.py:12) (14423)

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.31.38.130:8501
  External URL: http://35.91.39.57:8501

2025-04-04 16:56:23,423 | INFO: generated uuid for the tasks: caeaccd962144b5da0859f1b49712d9c (interface.py:72) (14424)
2025-04-04 16:56:23,473 | INFO | DB             | CaseType     Dataset               Filter | task_label (task_runner.py:339)
2025-04-04 16:56:23,473 | INFO | -----------    | ------------ -------------------- ------- | -------    (task_runner.py:339)
2025-04-04 16:56:23,473 | INFO | AstraDB        | Performance  Cohere-MEDIUM-1M        None | 2025040416-2025040404-astradb-spt-1m-768dim-run1 (task_runner.py:339)
2025-04-04 16:56:23,473 | INFO: task submitted: id=caeaccd962144b5da0859f1b49712d9c, 2025040416-2025040404-astradb-spt-1m-768dim-run1, case number: 1 (interface.py:242) (14424)
2025-04-04 16:56:24,741 | INFO: [1/1] start case: {'label': <CaseLabel.Performance: 2>, 'dataset': {'data': {'name': 'Cohere', 'size': 1000000, 'dim': 768, 'metric_type': <MetricType.COSINE: 'COS
INE'>}}, 'db': 'AstraDB'}, drop_old=True (interface.py:172) (14474)
2025-04-04 16:56:24,741 | INFO: Starting run (task_runner.py:105) (14474)
2025-04-04 16:56:24,934 | INFO: Connected to Astra DB cluster (astradb.py:75) (14474)
2025-04-04 16:56:24,952 | INFO: Dropping table: vectordb_bench_collection and the index(es) (astradb.py:79) (14474)
2025-04-04 16:56:26,206 | INFO: local dataset root path not exist, creating it: /tmp/vectordb_bench/dataset/cohere/cohere_medium_1m (data_source.py:124) (14474)
2025-04-04 16:56:26,207 | INFO: Start to downloading files, total count: 3 (data_source.py:140) (14474)
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3/3 [01:02<00:00, 20.85s/it]
2025-04-04 16:57:28,765 | INFO: Succeed to download all files, downloaded file count = 3 (data_source.py:145) (14474)
2025-04-04 16:57:28,765 | INFO: Read the entire file into memory: test.parquet (dataset.py:247) (14474)
2025-04-04 16:57:28,790 | INFO: Read the entire file into memory: neighbors.parquet (dataset.py:247) (14474)
2025-04-04 16:57:28,834 | INFO: Start performance case (task_runner.py:147) (14474)
2025-04-04 16:57:28,875 | WARNING: VectorDB load dataset error: cannot pickle '_thread.RLock' object (serial_runner.py:141) (14474)
2025-04-04 16:57:30,249 | WARNING: Failed to run performance case, reason = cannot pickle '_thread.RLock' object (task_runner.py:182) (14474)
Traceback (most recent call last):
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/task_runner.py", line 152, in _run_perf_case
    _, load_dur = self._load_train_data()
                  ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/utils.py", line 43, in inner
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/task_runner.py", line 201, in _load_train_data
    raise e from None
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/task_runner.py", line 199, in _load_train_data
    runner.run()
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/runner/serial_runner.py", line 182, in run
    count, dur = self._insert_all_batches()
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/utils.py", line 43, in inner
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/runner/serial_runner.py", line 142, in _insert_all_batches  
    raise e from e
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/runner/serial_runner.py", line 133, in _insert_all_batches  
    count = future.result(timeout=self.timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/concurrent/futures/_base.py", line 456, in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
    raise self._exception
  File "/usr/lib/python3.12/multiprocessing/queues.py", line 264, in _feed
    obj = _ForkingPickler.dumps(obj)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/multiprocessing/reduction.py", line 51, in dumps
    cls(buf, protocol).dump(obj)
TypeError: cannot pickle '_thread.RLock' object
2025-04-04 16:57:30,254 | WARNING: [1/1] case {'label': <CaseLabel.Performance: 2>, 'dataset': {'data': {'name': 'Cohere', 'size': 1000000, 'dim': 768, 'metric_type': <MetricType.COSINE: 'COSINE'>}}, 'db': 'AstraDB'} failed to run, reason=cannot pickle '_thread.RLock' object (interface.py:194) (14474)
Traceback (most recent call last):
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/interface.py", line 173, in _async_task_v2
    case_res.metrics = runner.run(drop_old)
                       ^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/task_runner.py", line 112, in run
    return self._run_perf_case(drop_old)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/task_runner.py", line 184, in _run_perf_case
    raise e from None
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/task_runner.py", line 152, in _run_perf_case
    _, load_dur = self._load_train_data()
                  ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/utils.py", line 43, in inner
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/task_runner.py", line 201, in _load_train_data
    raise e from None
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/task_runner.py", line 199, in _load_train_data
    runner.run()
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/runner/serial_runner.py", line 182, in run
    count, dur = self._insert_all_batches()
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/utils.py", line 43, in inner
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/runner/serial_runner.py", line 142, in _insert_all_batches  
    raise e from e
  File "/home/ubuntu/ZillizVectorDBBench/vectordb_bench/backend/runner/serial_runner.py", line 133, in _insert_all_batches  
    count = future.result(timeout=self.timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/concurrent/futures/_base.py", line 456, in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^    
  File "/usr/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
    raise self._exception
  File "/usr/lib/python3.12/multiprocessing/queues.py", line 264, in _feed
    obj = _ForkingPickler.dumps(obj)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/multiprocessing/reduction.py", line 51, in dumps
    cls(buf, protocol).dump(obj)
TypeError: cannot pickle '_thread.RLock' object
2025-04-04 16:57:30,256 | INFO |Task summary: run_id=caeac, task_label=2025040416-2025040404-astradb-spt-1m-768dim-run1 (models.py:354)
2025-04-04 16:57:30,256 | INFO |DB      | db_label case              label                                            | load_dur    qps        latency(p99)    recall        max_load_count | label (models.py:354)
2025-04-04 16:57:30,256 | INFO |------- | -------- ----------------- ------------------------------------------------ | ----------- ---------- --------------- ------------- -------------- | ----- (models.py:354)
2025-04-04 16:57:30,256 | INFO |AstraDB |          Performance768D1M 2025040416-2025040404-astradb-spt-1m-768dim-run1 | 0.0         0.0        0.0             0.0           0              | x     (models.py:354)
2025-04-04 16:57:30,256 | INFO: write results to disk /home/ubuntu/ZillizVectorDBBench/vectordb_bench/results/AstraDB/result_20250404_2025040416-2025040404-astradb-spt-1m-768dim-run1_astradb.json (models.py:227) (14474)
2025-04-04 16:57:30,258 | INFO: Success to finish task: label=2025040416-2025040404-astradb-spt-1m-768dim-run1, run_id=caeaccd962144b5da0859f1b49712d9c (interface.py:213) (14474)
```
---