# odoo-tw-payroll-params：台灣薪資法規參數

攲器有限公司（UniPiece）　https://www.unipiece.com.tw

Odoo 18 模組 **`unipiece_payroll_timesheet`（攲器薪資計算-工時制）** 使用的台灣法規參數：二代健保補充保費費率、基本工資、一般健保費率等。

模組使用者在 Odoo 按【從 GitHub 更新】，會下載本程式庫的 `tw_payroll_params.json`，先顯示與目前數值的差異預覽，**經薪資管理員確認後才寫入**。不會自動更新。

> 數值依健保署、勞動部公告整理，**不是法律或財務意見**，異動時請對照官方公告確認。

## 模組如何使用這些參數

- 每筆參數都有「生效日」。薪資單依**發放日**取用當天已生效的最新一筆，所以法規異動後，已結算的舊薪資單重算不會變。
- 預覽表會標示每筆是「新增」、「變更」、「與手動輸入的數值不同」或「相同」。與手動輸入不同的預設不勾選，避免蓋掉人工修改。
- 下載內容只當 JSON 解析，並逐筆驗證代碼、日期與數值範圍；超出範圍或格式不符，整批拒絕。
- 只接受 `https://raw.githubusercontent.com/…….json` 網址，驗證 TLS 憑證，不跟隨轉址，逾時與大小有上限。
- 若在 Odoo 設定了公開金鑰，必須附上正確的 Ed25519 簽章（`tw_payroll_params.json.sig`），否則整批拒絕。

## 檔案格式

```json
{
  "schema_version": 1,
  "parameters": [
    {"code": "nhi_basic_wage", "effective_date": "2027-01-01", "value": 30000, "note": "基本工資 2027"}
  ]
}
```

| `code` | 意義 | 允許範圍 |
|---|---|---|
| `nhi_supplement_rate` | 二代健保補充保費費率（%） | 0 ～ 10 |
| `nhi_basic_wage` | 基本工資（兼職薪資扣取門檻） | 0 ～ 100,000 |
| `nhi_supplement_cap` | 補充保費單次給付上限（0＝不設上限） | 0 ～ 1,000,000,000 |
| `nhi_general_rate` | 一般健保費率（%） | 0 ～ 15 |
| `nhi_employee_share` | 員工負擔一般健保費比率（%） | 0 ～ 100 |
| `nhi_max_dependents` | 眷屬計算人數上限 | 0 ～ 10 |

- `schema_version` 固定為 `1`；`effective_date` 格式 `YYYY-MM-DD`；`note` 選填，200 字以內。
- 同一個 `code` ＋ 同一個 `effective_date` 不可重複。
- **法規異動時新增一筆新的生效日，不要改舊的那筆。**

## 更新參數

1. 編輯 `tw_payroll_params.json`，在 `parameters` 末尾新增一筆。
2. 檢查格式：`python3 tools/sign.py check tw_payroll_params.json`（預期 `OK: N parameters`）。
3. 若有啟用簽章：`python3 tools/sign.py sign tw_payroll_params.json private.key`，將產生的 `.sig` 與 JSON 一起 commit。
4. Commit 後，GitHub Actions（`.github/workflows/validate.yml`）會自動再檢查一次。

## 簽章

```bash
pip install cryptography
python3 tools/sign.py keygen    # 產生 private.key（私鑰）並印出公開金鑰
```

- `private.key` 是私鑰，**不可上傳 GitHub**（`.gitignore` 已排除 `*.key`），請另行妥善保管。
- 公開金鑰填入 Odoo 系統參數 `unipiece_payroll_timesheet.regulation_public_key`。
