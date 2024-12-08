# 前言

由于基于autoDL+ollama进行大模型本地化部署存在一些问题，现在就这些问题机型补充。

# 如何修改 ollama的默认端口

用autoDL想要对外发布服务，必须将服务端口改为`6006`, 由于ollama的默认端口是`11434`,要想外部访问你部署的ollama服务，你也必须将ollama的端口修改为`6006`,

## export命令临时更改

必须设置：
`export OLLAMA_HOST="0.0.0.0:6006"`

（可选项）通常为了更好的管理模型文件，一般还需要设置这个OLLAMA_MODELS
`export OLLAMA_MODELS=/root/autodl-tmp/models` 

然后安装和启动ollama：

安装：`curl -fsSL https://ollama.com/install.sh | sh`

启动:`ollama serve`

启动之后应该能在启动日志中找到 6006的端口号(`OLLAMA_HOST:http://0.0.0.0:6006`):

如下，日志中能搜到6006：

```bash
root@autodl-container-b3a44b837c-82697298:~# ollama serve
2024/12/02 15:11:09 routes.go:1197: INFO server config env="map[CUDA_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_DEBUG:false OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://0.0.0.0:6006 OLLAMA_INTEL_GPU:false OLLAMA_KEEP_ALIVE:5m0s OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/root/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:0 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://*] OLLAMA_SCHED_SPREAD:false OLLAMA_TMPDIR: ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
```

但是注意，千万不要关闭这个终端，因为autoDL的机器本身就是一个docker服务，不存在常驻服务，你关闭了窗口就说明服务结束了。

这就说明已经按照我们要求的`6006`启动了ollama服务。

接下来找一个小一些的模型来测试一下，就用`qwen:0.5b`：

执行命令：`ollama run qwen:0.5b`

启动完成之后，重开一个终端窗口,执行命令:

```bash
curl -X POST http://localhost:6006/api/generate -H "Content-Type: application/json" -d '{
  "model": "qwen:0.5b",
  "prompt": "Hello, world!"
}'
```

能看到如下输出，就说明模型启动正常：

```bash
root@autodl-container-b3a44b837c-82697298:~# curl -X POST http://localhost:6006/api/generate -H "Content-Type: application/json" -d '{
  "model": "qwen:0.5b",
  "prompt": "Hello, world!"
}'
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.135887809Z","response":"Welcome","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.167247938Z","response":" to","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.171793647Z","response":" the","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.176557097Z","response":" programming","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.181136263Z","response":" language","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.185417172Z","response":" you","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.189748941Z","response":" chose","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.194235306Z","response":".","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.198697546Z","response":" If","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.206829988Z","response":" you","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.214619023Z","response":" have","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.222548865Z","response":" any","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.230513483Z","response":" questions","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.238110966Z","response":" or","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.246513295Z","response":" need","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.254580909Z","response":" further","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.262807894Z","response":" assistance","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.271102766Z","response":",","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.279624335Z","response":" please","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.287897964Z","response":" feel","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.296273798Z","response":" free","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.311326605Z","response":" to","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.317477385Z","response":" ask","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.323305161Z","response":".","done":false}
{"model":"qwen:0.5b","created_at":"2024-12-02T07:32:24.328776973Z","response":"","done":true,"done_reason":"stop","context":[151644,872,198,9707,11,1879,0,151645,198,151644,77091,198,13936,311,279,15473,4128,498,14554,13,1416,498,614,894,4755,476,1184,4623,12994,11,4486,2666,1910,311,2548,13],"total_duration":2065240719,"load_duration":1657854005,"prompt_eval_count":12,"prompt_eval_duration":209000000,"eval_count":25,"eval_duration":196000000}
```

# 如何开放autoDL上部署的ollama服务

autoDL本身就支持 通过隧道链接到远程服务，只不过他这个开放远程服务的端口写死了是6006，这也就是我们启动ollama必须用6006端口的原因。

第一步：
执行命令：`ssh -CNg -L 6006:127.0.0.1:6006 root@connect.westc.gpuhub.com -p 13607`
但是注意，这里的域名`connect.westc.gpuhub.com` 以及 端口`13607`是根据每一个机器的实际情况来填写的，具体的点击每台机器的`快捷工具`->`自定义服务`弹出的窗口去查看。
![alt text](image-1.png)

执行之后，会要求你输入密码，密码则是上图中的密码。手动输入它，然后回车。

如果回车之后没有任何反应，那就是正常的，说明隧道已经连接。如果弹出其他的，就说明填写的密码有问题。

此时，你部署在autoDL上的ollama服务已经可以对外访问了。

如果此时，你在你本机浏览器中输入：`http://localhost:6006/`，应该能看到 `Ollama is running`。

# SSH同时转发多个端口

使用SSH命令可以转发远程机器的一个端口，也可以开启多个终端，同时监听多个不同的端口。

只不过AutoDL有可能限制了，仅仅开放了6006. 
如果是一台普通的linux机器，应该是可以同时转发多个端口的。

比如，我在linux机器上同时启动了 fastGPT，one-api，以及xInference，3个应用分别在不同的端口，我想在我本机同时访问这3个端口，就可以打开多个终端，分别转发不同端口。
