# CLI AI Assist

CLI AI Assist 是一個 AI 助手，專門幫你把人類語言翻譯成命令列指令。就像一位超有經驗的系統管理員，熟悉 Windows 和 Linux，幫你快速搞定各種檔案壓縮、目錄管理的需求。

## 功能特色
- 按指示生成 Bash 和 PowerShell 指令。
- 提供詳細又貼心的解決方案。
- 即時互動模式，隨時問隨時答。
- 基準測試(benchmark)模式，測試多種 AI 模型。
- 環境變數設定，方便整合 API。

## 安裝方式
可先於[openrouter.ai](https://openrouter.ai/)註冊帳號並取得 API 金鑰，然後使用以下步驟安裝：

1. 先把專案下載下來：
   ```bash
    git clone https://github.com/your-repo/cli-AI-assist.git
    cd cli-AI-assist
   ```
2. 安裝需要的套件：
   ```bash
    python setup.py install
   ```
3. 設定環境變數：
   ```bash
    ai --setup
   ```


## 基本用法
直接輸入你的需求，AI 會幫你生成命令列指令：
建議指令模式: 用<工具>做<工作>，例如：
1. 用 tar 壓縮 project
2. 顯示在 https://pastebin.com/raw/Mycq5TpC 中哪个IP的请求次数最多及查詢其來自哪個國家
3. 用 curl 下載 https://example.com/file.zip 並解壓縮

```bash
ai "用 tar 和 gzip 把 'project' 資料夾壓縮起來。"
```

### 範例輸出
```plaintext
Think step:
1. 確認使用者的作業系統和 Shell 類型。
2. 決定壓縮格式（例如：tar、zip、7z）。
3. 檢查有沒有特殊需求（例如：壓縮等級、排除某些檔案）。
4. 根據需求生成指令。
5. 確保指令穩健，能處理檔名有空格、隱藏檔案等情況。
6. 如果有需要，提供替代指令。
7. 包含作業系統特定的指令。
8. 提供 **最終的一行指令**，完整又能直接用。

command > tar -czvf project.tar.gz "project"
```

## 互動模式
啟動互動模式，隨時輸入需求：
```bash
ai --interactive
```
在互動模式下輸入指令，還可以直接執行。

## 基準測試模式
用基準測試模式試試多種 AI 模型：
```bash
ai -b -m models.txt "生成20個隨機ip和機名"
```

# 針對Openrouter上比較熱門的模型測試(Gemini 2.5 pro 分析生成😁)

## 模型評測分析報告：Bash 日誌分析與 IP 地理位置查詢

### 引言

本報告旨在根據提供的基準測試數據 (`生成數據.txt`)、價格信息 (`price.txt`) 以及系統提示 (`systemprompt.txt`)，客觀評估不同 AI 模型在執行特定 Bash 腳本任務時的表現。該任務要求模型生成一個 Bash 命令，用於分析來自指定 URL 的日誌數據，找出請求次數最多的 IP 地址，並查詢該 IP 所屬的國家。評估將涵蓋代碼質量、可讀性、對問題的理解、成本、模型規模、特性、運行結果等多個維度，最終選出表現最佳的 MVP (Minimum Viable Product) 模型，並針對不同優先級提供建議方案。

### 評估標準

*   **代碼質量 (Code Quality):** 生成的 Bash 命令是否高效、健壯、正確？是否能處理潛在問題（如工具缺失、API 失敗）？是否恰當使用標準工具？
*   **可讀性與解釋 (Readability/Explanation):** `[explain]` 標籤中的解釋是否清晰易懂？`[command]` 本身是否格式良好？`[context]` 是否準確？
*   **問題理解 (Problem Understanding):** 模型是否準確理解用戶需求（下載日誌、找 Top IP、查國家）？
*   **成本 (Cost):** 根據 `price.txt`，生成回應的成本是多少？（部分模型可能無對應成本數據）
*   **模型規模/特性 (Model Scale/Features):** 模型的大致規模（如 mini, 72b）及其可能具備的特性。
*   **遵循指示 (Adherence to Prompt):** 是否遵循 `systemprompt.txt` 的結構要求（`[context]`, `[explain]`, `[command]` 標籤）？是否提供了備選方案或安裝說明？
*   **運行結果 (Execution Result):** `生成數據.txt` 中顯示的命令執行結果是否成功？是否輸出了正確的 IP (95.108.151.244) 和國家 (RU/Russia)？
*   **執行時間/速度 (Execution Time/Speed):** 模型生成回應所需時間 (`生成數據.txt`)。
*   **Token 效率 (Token Efficiency):** 相對於任務複雜度，輸出 Token 數量是否合理？

### 數據源

*   `生成數據.txt`: 各模型針對用戶提示的基準測試結果。
*   `price.txt`: 部分模型在特定時間點的 API 調用成本、Token 數及速度。
*   `systemprompt.txt`: 指導 AI 模型回應格式和內容的系統提示。

### 不同優先級推薦方案

根據上述分析，針對不同需求，推薦以下模型：

1.  **最高性價比 (平衡 - MVP): `openai/gpt-4.1-mini`**
    *   **理由:** 成功使用可靠的公共 API 解決問題，避免了本地工具依賴。命令簡潔高效，解釋清晰，遵循指示。在所有成功的 API 方案中，成本相對較低 ($0.00101)，生成速度快，輸出 Token 合理。提供了最佳的質量、可靠性與成本的平衡點。

2.  **質量優先: `google/gemini-2.5-pro-preview-03-25`**
    *   **理由:** 生成了高質量的解決方案，使用可靠 API，並在 `awk` 命令中巧妙地嵌入了 `curl` 調用進行國家查詢，無需額外步驟。解釋非常詳細和清晰，對問題理解透徹。雖然成本 ($0.00904) 和執行時間 (23.95s) 相對較高，但優先考慮代碼質量和解釋深度時，它是極佳的選擇。(`openai/o3-mini-high` 作為備選，同樣優秀但成本更高)。

3.  **價錢優先: `google/gemini-2.0-flash-001`**
    *   **理由:** 在所有 *成功執行並返回正確結果* 的模型中，此模型成本最低 ($0.000369)。它使用了 `whois` 命令查詢國家，雖然此方法健壯性不如 API 調用（依賴 `whois` 安裝和輸出格式），但在本次測試環境下是有效的。如果首要目標是盡可能降低成本，並且可以接受 `whois` 的潛在限制，則此模型是首選。如果必須使用 API 且追求低價，`meta-llama/llama-4-maverick` ($0.000511) 是次優選擇，但需要額外安裝 `jq`。

### 模型表現摘要表

| 模型 (Model)                           | 執行結果 (Execution Result)                  | 代碼質量 (Code Quality) | 可讀性/解釋 (Readability/Explanation) | 成本 (Cost)¹ | 執行時間 (Sec) | Tokens (In/Out) | 備註 (Notes)                                                                 |
| :------------------------------------- | :------------------------------------------- | :---------------------- | :------------------------------------ | :----------- | :------------- | :-------------- | :--------------------------------------------------------------------------- |
| google/gemini-2.0-flash-001            | 成功 (whois, RU)                             | 中 (依賴 whois)         | 好                                    | $0.000369    | 6.19           | 877 / 703       | 使用 whois，結果正確。提供了 geoiplookup 作為備選。 **(價錢優先選項)**         |
| openai/gpt-4o-mini                     | 失敗 (geoiplookup 未找到)                    | 差 (依賴未安裝工具)     | 好                                    | $0.000336    | 4.48           | 815 / 357       | 依賴 geoiplookup，在測試環境中失敗。                                         |
| google/gemini-2.5-pro-preview-03-25    | 成功 (ipinfo.io API, RU)                     | 好 (API, awk 解析)    | 優                                    | $0.00904     | 23.95          | 877 / 794       | 使用可靠 API，awk 內嵌 curl 調用，解釋詳細，但成本較高、耗時較長。 **(質量優先選項)** |
| meta-llama/llama-4-maverick            | 成功 (ip-api.com API, Russia, 需 jq)         | 中 (需 jq)            | 好                                    | $0.000511    | 4.78           | 822 / 456       | 使用可靠 API，但依賴額外工具 jq。 (價錢優先的 API 方案備選)                  |
| mistralai/mistral-7b-instruct-v0.2     | 無命令輸出                                   | 差                      | 無解釋                                | $0.000329    | 5.76           | 997 / 649       | 未能生成有效命令。                                                           |
| anthropic/claude-3.7-sonnet            | 成功 (ipinfo.com API, RU, 部分成功)²         | 中 (重複 curl)          | 中                                    | $0.0119      | 11.91          | 957 / 600       | 成功輸出 IP 和次數，但國家查詢部分似乎未完整執行或顯示，且重複執行了日誌分析。 |
| anthropic/claude-3.7-sonnet:thinking   | 成功 (ip-api.com API, Russia)                | 好 (API, 變量存儲)    | 優                                    | $0.0575      | 49.63          | 986 / 3636      | 使用可靠 API，步驟清晰，存儲變量，但成本非常高，耗時長，輸出 Token 多。        |
| x-ai/grok-3-beta                       | 部分成功 (輸出 "success" 而非國家)           | 差 (解析錯誤)           | 好                                    | $0.0119      | 19.14          | 805 / 630       | IP 和計數正確，但國家解析錯誤，輸出 "success"。成本較高。                      |
| x-ai/grok-3-mini-beta                  | 無命令輸出                                   | 差                      | 無解釋                                | $0.000455    | 14.27          | 806 / 426       | 未能生成有效命令。                                                           |
| deepseek/deepseek-chat-v3-0324         | 成功 (whois, RU)                             | 中 (依賴 whois)         | 好                                    | $0.00057     | 31.24          | 837 / 324       | 使用 whois，結果正確，但耗時較長。                                           |
| qwen/qwen-2.5-72b-instruct           | 失敗 (geoiplookup 未找到)                    | 差 (依賴未安裝工具)     | 好                                    | $0.000234    | 10.30          | 815 / 321       | 依賴 geoiplookup，在測試環境中失敗。                                         |
| qwen/qwq-32b                           | 成功 (ipinfo.io API, RU)                     | 好 (API, cut 解析)      | 無解釋                                | $0.000705    | 99.18          | 818 / 2913      | 使用可靠 API，結果正確，但執行時間極長，輸出 Token 多，缺少解釋。             |
| meta-llama/llama-4-scout               | 失敗 (geoiplookup 未找到)                    | 差 (依賴未安裝工具)     | 好                                    | $0.000189    | 6.88           | 810 / 413       | 依賴 geoiplookup，在測試環境中失敗。                                         |
| qwen/qwen-turbo                        | 失敗 (geoiplookup 未找到)                    | 差 (依賴未安裝工具)     | 好                                    | $0.000123    | 4.91           | 815 / 409       | 依賴 geoiplookup，在測試環境中失敗。成本最低。                               |
| deepseek/deepseek-r1-distill-llama-70b | 失敗 (geoiplookup 未找到)                    | 差 (依賴未安裝工具)     | 好                                    | $0.000364    | 21.47          | 813 / 666       | 依賴 geoiplookup，在測試環境中失敗。命令包含 `[[ $? -ne 0 ]]` 語法，但在 sh 中可能報錯。 |
| openai/gpt-4.1                         | 錯誤 (Provider Error 403)                    | N/A                     | N/A                                   | $0.00098     | 1.98           | 815 / 409       | 提供商返回錯誤，無法評估。                                                   |
| openai/gpt-4.1-mini                    | 成功 (ipinfo.io API, RU) (第二次運行)        | 優 (API, 簡潔)        | 優                                    | $0.00101     | 5.39 / 6.81    | 815 / 409 / 430 | 兩次運行均成功。解釋佳，命令簡潔有效，使用可靠 API。成本適中。 **(性價比選項/MVP)** |
| openai/o4-mini-high                    | 成功 (whois, RU)                             | 中 (依賴 whois)         | 優                                    | $0.0193      | 39.92          | 814 / 4180      | 使用 whois，結果正確。解釋詳細，遵循指示，但成本高，耗時長，輸出 Token 異常多。 |
| openai/o3                              | 錯誤 (Provider Error 403)                    | N/A                     | N/A                                   | N/A          | 0.92           | N/A             | 提供商返回錯誤，需要 Key。                                                   |
| openai/o4-mini                         | 錯誤 (Syntax error: redirection unexpected)  | 差 (語法錯誤)           | 好                                    | N/A          | 16.24          | 814 / 1277      | 嘗試使用 `read` 重定向，產生語法錯誤。                                       |
| openai/o3-mini-high                    | 成功 (ip-api.com API, Russia)                | 優 (API, grep 解析)     | 優                                    | $0.0109      | 16.97          | 814 / 2279      | 使用可靠 API，grep 解析 JSON，解釋詳細，遵循指示，但成本較高，輸出 Token 較多。 (質量優先選項備選) |
| openai/o3-mini                         | 成功 (ipinfo.io API, RU)                     | 優 (API, 簡潔)        | 優                                    | $0.00798     | 10.57          | 814 / 1609      | 使用可靠 API，命令簡潔有效，解釋清晰，遵循指示。成本相對較高。                 |
| openai/gpt-4.1-nano                    | 無命令輸出                                   | 差                      | 無解釋                                | $0.000253    | 3.25           | 815 / 428       | 未能生成有效命令。成本非常低。                                               |

**註:**
1.  成本數據來自 `price.txt`，可能與 `生成數據.txt` 中的 Token 數不完全匹配，僅作參考。部分模型無成本數據。
2.  `claude-3.7-sonnet` 的輸出結果顯示了 IP 和次數，但 `grep country | cut -d '"' -f4` 這部分似乎沒有正確執行或顯示國家。

### 詳細分析

1.  **成功執行的模型:**
    *   **API 方案:** `google/gemini-2.5-pro-preview-03-25`, `meta-llama/llama-4-maverick` (需 jq), `anthropic/claude-3.7-sonnet:thinking`, `openai/gpt-4.1-mini` (兩次運行), `qwen/qwq-32b`, `openai/o3-mini-high`, `openai/o3-mini` 都成功使用了 `ipinfo.io` 或 `ip-api.com` 等公共 API 查詢國家信息。這通常是最可靠的方法，不受本地工具或數據庫的限制。這些模型生成的日誌分析部分（`curl | awk | sort | uniq | sort | head`）邏輯基本一致且正確。
    *   **Whois 方案:** `google/gemini-2.0-flash-001`, `deepseek/deepseek-chat-v3-0324`, `openai/o4-mini-high` 使用了 `whois` 命令查詢。雖然在此次測試中成功，但 `whois` 的輸出格式可能不標準化，依賴 `grep` 提取特定字段（如 "country:"）的健壯性相對較差，且 `whois` 工具可能需要單獨安裝。

2.  **依賴特定工具或失敗的模型:**
    *   **`geoiplookup` 依賴:** 大量模型（`openai/gpt-4o-mini`, `qwen/qwen-2.5-72b-instruct`, `meta-llama/llama-4-scout`, `qwen/qwen-turbo`, `deepseek/deepseek-r1-distill-llama-70b`）選擇了 `geoiplookup` 工具。然而，該工具並非所有系統預裝，且需要 GeoIP 數據庫。在本次測試環境中，這些命令均因找不到 `geoiplookup` 而失敗。雖然部分模型提示了安裝方法，但直接提供的命令無法運行。
    *   **解析錯誤:** `x-ai/grok-3-beta` 在解析 API 返回的 JSON 時出錯，未能提取國家名稱。`anthropic/claude-3.7-sonnet` 的國家查詢部分似乎未成功執行或顯示。
    *   **語法錯誤:** `openai/o4-mini` 使用了 `read` 命令和重定向，導致了 Bash 語法錯誤。
    *   **無輸出或 Provider 錯誤:** `mistralai/mistral-7b-instruct-v0.2`, `x-ai/grok-3-mini-beta`, `openai/gpt-4.1-nano` 未能生成任何有效命令。`openai/gpt-4.1` 和 `openai/o3` 遇到了提供商錯誤。

3.  **成本與效率考量:**
    *   **低成本選項:** `qwen/qwen-turbo` ($0.000123), `meta-llama/llama-4-scout` ($0.000189), `qwen/qwen-2.5-72b-instruct` ($0.000234), `openai/gpt-4.1-nano` ($0.000253), `mistralai/mistral-7b-instruct-v0.2` ($0.000329), `openai/gpt-4o-mini` ($0.000336) 等成本極低，但多數未能成功解決問題（依賴 `geoiplookup` 或無輸出）。
    *   **中等成本且成功:** `openai/gpt-4.1-mini` ($0.00101) 在成功解決問題的模型中成本相對較低。`meta-llama/llama-4-maverick` ($0.000511) 成本也較低，但需額外安裝 `jq`。
    *   **高成本選項:** `google/gemini-2.5-pro` ($0.00904), `anthropic/claude-3.7-sonnet` ($0.0119), `x-ai/grok-3-beta` ($0.0119), `openai/o3-mini-high` ($0.0109), `openai/o4-mini-high` ($0.0193), `anthropic/claude-3.7-sonnet:thinking` ($0.0575) 成本顯著更高。其中 `sonnet:thinking`, `o4-mini-high`, `qwq-32b`, `o3-mini-high`, `o3-mini` 的輸出 Token 數量也偏多。
    *   **執行時間:** `qwen/qwq-32b` (99s), `anthropic/claude-3.7-sonnet:thinking` (49s), `openai/o4-mini-high` (39s), `deepseek/deepseek-chat-v3-0324` (31s), `google/gemini-2.5-pro` (23s) 耗時較長。其他模型大多在 10 秒以內完成生成。

4.  **遵循指示情況:**
    *   大多數成功運行的模型都較好地遵循了 `systemprompt.txt` 的要求，提供了 `[context]`, `[explain]`, `[command]` 標籤。
    *   部分模型（如 `qwen/qwq-32b`, `mistralai/mistral-7b`, `x-ai/grok-3-mini`, `openai/gpt-4.1-nano`）未能提供完整的解釋或命令。
    *   提供備選方案或安裝說明的模型（如 `google/gemini-2.0-flash-001`, `meta-llama/llama-4-maverick`, `deepseek/deepseek-chat-v3-0324`）體現了更好的健壯性考慮。


### 結論

本次評測顯示，不同 AI 模型在處理具體的、帶有實際執行需求的技術任務時，表現差異顯著。
*   對於需要與外部環境交互（如下載文件、調用 API、檢查本地工具）的任務，模型的選擇對結果的成功率至關重要。
*   基於公共 API (如 `ipinfo.io`, `ip-api.com`) 的解決方案通常比依賴本地特定工具 (`geoiplookup`, `whois`) 的方案更具通用性和健壯性。
*   模型成本與性能並非完全正相關，部分中低成本模型（如 `openai/gpt-4.1-mini`）在特定任務上可以達到甚至超過高成本模型的表現。
*   輸出 Token 數量和生成時間也是評估模型效率的重要指標，部分模型可能過於冗長或耗時過長。

選擇模型時，應根據具體任務需求、對外部依賴的容忍度、預算限制以及對解釋詳細程度的要求進行權衡。以上提供的推薦方案旨在幫助用戶根據自身優先級做出更合適的選擇。


## 授權
這個專案是用 MIT 授權的，詳情請看 LICENSE 檔案。