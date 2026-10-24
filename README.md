# OneDC 源码、权重与返修交接

本仓库集中保存 **One-Step Diffusion-Based Image Compression with Semantic Distillation** 的官方源码快照、λ=4.6 权重恢复材料和 auto0776 专家交接。作者的官方项目在 [onedc-codec/onedc](https://github.com/onedc-codec/onedc)；本仓库是用户自己的恢复与交接副本。

## 先看这些入口

| 需要做什么 | 入口 |
|---|---|
| 下载 λ=4.6 两份权重及所需公共缓存 | [资产下载说明](docs/ASSETS.md)、[Release](https://github.com/khan114514/OneDC/releases/tag/onedc-assets-20261024) |
| 下载完整交接、源码与恢复工具 | [OneDC_recovery_source.zip](https://github.com/khan114514/OneDC/releases/download/onedc-assets-20261024/OneDC_recovery_source.zip)，或直接 clone 本仓库 main |
| 核对传输和包内全部文件 | `python3 tools/restore_assets.py --archive downloads/onedc-assets.tar.gz` |
| 查看官方推理和训练代码 | [upstream/onedc/readme.md](upstream/onedc/readme.md)；[固定提交](upstream/provenance.json) |
| 接手 auto0776 返修 | [auto0776/START_HERE.md](auto0776/START_HERE.md)、[当前口径](auto0776/handoff/00_CURRENT_REVIEW_POLICY.md) |
| 核对这次补了什么、还缺什么 | [完整性与缺口](docs/COMPLETENESS.md)、[交付状态](verification/DELIVERY_STATUS.json) |

权重包包含 `lambda4.6/model.safetensors`、`model_1.safetensors`、SD1.5 UNet 与 scheduler、SD2.1 VAE、TAESD，以及 AlexNet/VGG16 缓存。原始归档 **9,193,898,241 字节**，SHA-256 为 `adf37d23103580414fe4df8f51d6e8ca642b79af717d758717b21d2b316a3a1d`。9 个 Release 分片已全部核对 GitHub 端 SHA-256；本次原包及全部 16 个成员也已核验，回执见 `verification/`。

另补回 8 张原始 Hidden 图和原始 manifest，位于 `trusted_verifier_inputs/hidden_assets/`，9 个文件逐一匹配历史 SHA-256。它们仅供可信 Verifier 准备；整个仓库包含 Reference、轨迹和专家证据，**不能直接挂载或整体交给研究 Actor**。

## 运行准备

在有足够空间的机器上下载并解包：

```bash
python3 tools/download_assets.py --output downloads/onedc-assets.tar.gz
python3 tools/restore_assets.py --archive downloads/onedc-assets.tar.gz --output restored_assets
```

下载脚本按固定清单校验每个分片和完整归档；恢复脚本校验全部 16 个成员后才解包，不执行模型反序列化。压缩包约 9.19 GB，解压文件约 9.88 GB；同时保留两者需预留约 22 GB 空间。

普通论文推理按官方 README 安装 Linux/CUDA 环境并编译熵编码器。auto0776 使用自身冻结源码与 lock 文件，不能直接用上游最新快照替换历史评测代码。GPU、Harbor 和最终质检的实际完成情况见缺口说明。

## 许可与来源

保留 [OneDC 原许可证](upstream/onedc/LICENSE.md) 和 [第三方许可说明](licenses/README.md)。上游代码、各模型和数据分别遵守自身条款；本恢复仓库不重新许可第三方内容。SD 模型的用途限制继续适用。
