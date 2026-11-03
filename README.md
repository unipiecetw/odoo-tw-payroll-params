# 攲器薪資計算－法規參數（GitHub 參數庫範本）

給 Odoo 模組 `unipiece_payroll_timesheet`（攲器薪資計算-工時制）使用的「政府法規參數」檔。
Odoo 裡按「從 GitHub 更新」，就會下載本程式庫的 `tw_payroll_params.json`，預覽差異後再套用。

## 一、第一次建立（在 GitHub 網站上做）

1. 登入 GitHub →右上角 `+` → **New repository**。
2. Repository name 填 `<程式庫名稱>`（例：`tw-payroll-params`）。
3. **建議選 Public**（Odoo 才能不帶密碼下載；私有程式庫下載會得到 404）。檔案內只有費率與基本工資，沒有機密。
4. 建立後，把本資料夾的所有檔案上傳（`tw_payroll_params.json`、`tools/`、`.github/`、`README.md`、`.gitignore`）。
5. 在 Odoo 的「設定 → 技術 → 系統參數」把 `unipiece_payroll_timesheet.regulation_url` 改成：
   `https://raw.githubusercontent.com/<擁有者>/<程式庫名稱>/main/tw_payroll_params.json`
   ✅ 預期：在瀏覽器貼上這個網址，看得到 JSON 文字。

## 二、檔案格式

```json
{"schema_version": 1,
 "parameters": [
   {"code": "nhi_basic_wage", "effective_date": "2027-01-01", "value": 30000, "note": "基本工資 2027"}
 ]}
```

- `code` 只能是：`nhi_supplement_rate`（補充保費費率 %）、`nhi_basic_wage`（基本工資）、`nhi_supplement_cap`（單次給付上限）、`nhi_general_rate`（一般保險費率 %）、`nhi_employee_share`（員工負擔 %）、`nhi_max_dependents`（眷屬計算上限）。
- `effective_date` 為 `YYYY-MM-DD`，薪資單依「發放日」取該日已生效的最新值。
- **新增法規變動時請「加一筆新生效日」，不要改舊的**，舊薪資單重算才不會變。
- 同一個 `code` + `effective_date` 不可重複；數值超出合理範圍（例：費率 > 10）Odoo 會直接拒絕。

## 三、更新參數的流程

1. 編輯 `tw_payroll_params.json`（GitHub 網頁上按鉛筆圖示即可）。
2. 在自己電腦執行檢查：`python3 tools/sign.py check tw_payroll_params.json` ✅ 預期 `OK: N parameters`。
3. （建議）簽章，見下節。
4. Commit。GitHub Actions 會自動再檢查一次（`.github/workflows/validate.yml`）。

## 四、簽章（強烈建議）

沒有簽章時，Odoo 只靠「GitHub 帳號沒被盜」保護這個檔。有簽章時，即使帳號被盜，沒有私鑰也無法讓 Odoo 接受竄改後的檔案。

```bash
pip install cryptography
python3 tools/sign.py keygen        # 產生 private.key，畫面印出「公開金鑰」
```
1. `private.key` 是**私鑰，絕不可上傳 GitHub**（已列入 `.gitignore`），請存在密碼管理員或離線處。
2. 把印出的公開金鑰貼到 Odoo「系統參數」`unipiece_payroll_timesheet.regulation_public_key`。
3. 每次改完 JSON：`python3 tools/sign.py sign tw_payroll_params.json private.key`，
   會產生 `tw_payroll_params.json.sig`，**兩個檔案一起 commit**。
4. 只要填了公開金鑰，Odoo 就**強制**要求簽章；簽章不符會拒絕更新。

## 五、保護分支（建議）

GitHub → Settings → Branches → Add rule（`main`）→ 勾選 *Require a pull request before merging*，並開啟帳號兩步驟驗證（2FA）。

## 六、這個範本沒有實際驗證的部分

數值取自作者整理的公開資料，**發佈前請對照健保署／勞動部公告再確認**。
