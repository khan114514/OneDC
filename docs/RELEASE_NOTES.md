# OneDC 原始资产恢复与完整交接

9 个权重分片合计 **9,193,898,241 字节**。每片大小和 GitHub 端 SHA-256 已核对；合并后的原包 SHA-256 为：

`adf37d23103580414fe4df8f51d6e8ca642b79af717d758717b21d2b316a3a1d`

原包中的 16 个模型/配置/清单文件也已逐一通过历史哈希核验，包含 λ=4.6 两份核心权重及 SD1.5、SD2.1 VAE、TAESD、AlexNet/VGG16 缓存。

## 下载与恢复

1. 下载 **`OneDC_recovery_source.zip`** 和 **`SOURCE_SHA256SUMS`**，核对并解压源码包。GitHub 自动生成的 Source code ZIP 是初始 tag 快照，完整更新请使用这个专用源码包或 main。
2. 在源码包根目录运行：

```bash
python3 tools/download_assets.py --output downloads/onedc-assets.tar.gz
python3 tools/restore_assets.py --archive downloads/onedc-assets.tar.gz --output restored_assets
```

工具支持按已验证分片恢复中断的下载，并拒绝哈希不符的文件。不需要 OneDrive 登录。离线转交权重时一并保留 **`THIRD_PARTY_LICENSES.zip`**。

## 同时提供

- 官方源码固定快照、auto0776 历史源码和完整交接、六份 B/R 原始评分日志、计时/轨迹记录与当前技能。
- 8 张原始 Hidden 图及原始 manifest，逐文件匹配历史 SHA-256，仅供可信 Verifier 准备。
- 完整性回执、下载/校验工具、当前恢复与剩余工作说明。

这是资产和材料交付，不是新一轮正式任务验收。研究时间/轨迹修复、旧部署实现适配及未取得的官方工具等状态见 [COMPLETENESS.md](https://github.com/khan114514/OneDC/blob/main/docs/COMPLETENESS.md)。
