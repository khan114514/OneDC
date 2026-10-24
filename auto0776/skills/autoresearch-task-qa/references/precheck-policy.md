> 当前三期内容口径：先读[2026-10-22扩展豁免](phase3-v4-contract.md#扩展豁免用户授权2026-10-22)。保留此前五项，新增QA05/H02联网及外部查表约束、H03内场镜像选择/交付依据、H05当前调用证据，并汇总到QA17。所列事项无需整改/补跑；未豁免核心问题继续核验。下文旧工具接口不覆盖本口径，原报告和冻结脚本保留原样，豁免PASS不表示实跑验证完成。

# Precheck 兼容说明

precheck 现为 implementation 的兼容别名。旧版“把内容失败统一降级为警告”的逻辑不再用于默认 CLI。

实际使用规则以 [implementation-policy.md](implementation-policy.md) 为准；报告格式见 [implementation-report.md](implementation-report.md)。
