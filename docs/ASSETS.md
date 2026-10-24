# 权重与缓存恢复

目标 Release：<https://github.com/khan114514/OneDC/releases/tag/onedc-assets-20261024>。上传状态由 `verification/DELIVERY_STATUS.json` 记录；未完成时脚本不会把计划链接当成已可用下载。

源码与交接请选择 Release 的 `OneDC_recovery_source.zip`，按 `SOURCE_SHA256SUMS` 校验，或 clone 本仓库 main。该 Release 的 tag 为初始发布锚点，GitHub 自动生成的 Source code ZIP 是早期快照；恢复工具的完整更新在上述专用源码包及 main 中。

`assets/archive_manifest.json` 保存原始 16 个 tar 成员的精确字节数与 SHA-256；`assets/release_manifest.json` 保存传输分片及实际 Release 元数据。归档不改包，分片按数字顺序连接后与网盘原包完全相同。Release 同时附带 `THIRD_PARTY_LICENSES.zip`，离线转交权重时一并保留。

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| `lambda4.6/model.safetensors` | 3714647200 | `5986ca3ab874c886044a316dce72a6fff6d924fa1825c98a4455f84afe6614ee` |
| `lambda4.6/model_1.safetensors` | 1576680148 | `6dd4dc0d02ae00d8b7b24bfcd4d8acbf043c72a33042f270afccd539144bc6f3` |
| 完整 `onedc-assets.tar.gz` | 9193898241 | `adf37d23103580414fe4df8f51d6e8ca642b79af717d758717b21d2b316a3a1d` |

```bash
python3 tools/download_assets.py --output downloads/onedc-assets.tar.gz
python3 tools/restore_assets.py --archive downloads/onedc-assets.tar.gz
python3 tools/restore_assets.py --archive downloads/onedc-assets.tar.gz --output restored_assets
```

第一步从 GitHub Release 下载，第二步只读验证，第三步验证后解包。`restored_assets` 可作为旧 Dockerfile 的 `model_assets` named build context；独立推理的 checkpoint 路径为其下的 `lambda4.6/`，HF_HOME 为其下的 `hf/`，TORCH_HOME 为其下的 `torch/`。SD2.1 的历史缓存 revision 使用占位标签，不能据此冒充上游提交来源；文件一致性以 SHA-256 为准。

旧 `onedc-env-v8.tar.gz` 为 A10 的历史容器镜像备份，不是 H20/L20 镜像。现有源码及 Dockerfile 已随仓库提供；旧镜像不是模型恢复的必要下载。它的网盘位置及历史哈希保留在 `auto0776/assets/RECOVERY.md`。

本归档覆盖既有推理与评分依赖，不包含训练用 VQGAN tokenizer 或所有 λ 工作点。若目标改为重新训练或其他码率点，按官方训练配置另行取得对应资产，不能把 λ=4.6 当成全模型发布。
