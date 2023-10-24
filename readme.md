# Cplusplus Tool

一個為競技程式設計的C++本地執行小工具

推薦搭配VSCode使用

## 功能

+ 自動編譯執行並隱藏執行檔
+ 用檔案作為程式輸出入
+ 一些整理程式碼之類的功能(詳見下方介紹)

### 最新程式

此處有很多功能都會用最新程式\
未註明表示為當前目錄下掃描最後編輯的.cpp檔案\
請注意當前目錄裡不要太多東東\
否則會卡給你看\
P.S.建立檔案也是一種編輯

## 依賴項

1. gcc(必須)\
你可以從任何來源安裝，只要保證g++指令可用即可\
推薦MSYS
2. Python(必須)\
版本影響不大(吧)\
裝完把requirements.txt裡的東東裝一下就好了
3. clang-format(非必須)\
裡面有整合這東東\
想用就裝吧

## 安裝與使用

### 安裝

下載zip或直接git clone就好\
推薦git clone\
然後裝好依賴項\
並把安裝目錄放進PATH就可以了

### 一些相容性

1. 系統\
這是為Windows設計的\
因為Python無法直接呼叫PATH中的.py檔\
所以我寫了個cpt.cpp來處理\
但裡面用了windows.h所以不相容其他系統\
其他系統使用者就自己想辦法吧
2. 檔名\
中文檔名基本上只要gcc版本正確能處裡就OK\
含空格的路徑則是只要不需要輸入就不會有問題\
但需要輸入時就不一定了

### 自動讀取測資

下方的自動測試指令能自動讀取範測並執行\
但需要一些額外設定\
首先，雙擊listener.pyw或listener.bat可開啟接收器\
發射部分需要瀏覽器能在開啟題目時\
向"http://127.0.0.1:5555/writetestcase" 自動發指定格式的POST REQUEST\
"http://127.0.0.1:5555/presenttestcase" 也是另一個選擇\
這部分我在listeners資料夾中提供了一些Tempermonkey腳本的範例\
如有缺漏可自行嘗試編寫

### 使用

在cmd/PowerShell打"cpt"加空格接指令內容

## 指令表

{}表必填參數
()表非必填參數

### 設定類

全部用法都是"cpt 設定名稱 值"

1. v\
C++版本，可以是11,14,17,20\
但若gcc裝到較舊的版本可能無法使用C++20
2. args\
編譯參數

### 基本執行

執行時皆會自動判定是否需編譯\
但更改設定不會自動重新編譯

1. run\
執行最新程式
2. c\
強制重新編譯最新程式
3. r {程式檔} (輸入檔) (輸出檔)\
執行並使用檔案輸出入\
省略輸出檔則直接輸出\
省略輸入則持續輸入直到"\eof"
4. rf (輸入檔) (輸出檔)\
同上、但使用最新程式
5. rt\
執行最新程式並計時\
使用PowerShell的計時功能
6. gdb\
用gdb開最新程式

### 程式檔處理

1. template\
用template.cpp覆寫最新程式
2. format\
用clang-format整理最新程式
3. usaco (程式檔) {名稱}\
使main裡的cin/cout在OJ上指向"名稱.in"/"名稱.out"
4. import 名稱\
載入import裡的範例

### 檔案整理

以下的皆為"cpt tidy"的子指令\
分類時不分大小寫
1. fold {name}\
把同樣前綴的檔案打包成資料夾
2. unfold {name}\
把資料夾檔案拆出
3. foldaz\
把a~z/0~9前綴的檔案打包成資料夾\
foldAZ則是以A~Z/0~9
4. unfoldaz\
上面那個的反操作

### 自動測試
以下的皆為"cpt auto"的子指令\
1. test\
自動全部執行過一遍並顯示完整數據
2. judge\
自動全部執行過一遍並顯示評測結果\
非嚴格檢查，但若答案不唯一建議用test再自己看

### 其他

1. mhc (路徑)\
執行最新程式並使用檔案輸出入(變化版)\
路徑若為空或資料夾則列出檔案用於輸入\
否則直接使用該檔案輸入\
注意：此處不掃描子資料夾\
除此之外，這指令會特判zip檔並解壓縮\
還可以輸入解壓縮密碼\
確定輸入後可鍵入輸出檔名\
特別的是，程式會先開始執行後再確認輸出入檔\
但確認完輸出檔名後程式才會拿到輸入