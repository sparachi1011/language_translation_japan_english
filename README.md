**Project Scop:**
--------------------
This Project was developed on collected syslogs with below features
  --this project read syslog file and have a lookup to filter last 15 days(can be customized untill hours/minutes/seconds) of logs 
  --convertion from Japanese language to English logs 
  --parse the converted logs and save them into json file object.
  Implementation has been done with Python Multiprocessing technique to
    -- increase the efficiency of application
    -- reduce the execution time.

**Packages and tools:**
-----------------------
Developed on python 3 and supports python 3.5 and above.
install python from https://www.python.org/downloads/
googletrans 3.0.0   === https://pypi.org/project/googletrans/
deep-translator 1.11.4   === https://pypi.org/project/deep-translator/
Other python packages like requests,json,datetime,logging,pytz etc.

**Behind the scenes:**
-----------------------

Script will lookup syslog file, filter logs based on provided duration(minutes/hours/days) over all available logs.
Developed and tested with googletrans(https://py-googletrans.readthedocs.io/en/latest/) and deep-translator(https://deep-translator.readthedocs.io/en/latest/) python packages,
but found googletrans has the edge because of taking input of list of logs rather deep-translator allows only one log per processing.

Both packages utilize google translate API in the backround and convert japanese logs to english language.
![image](https://github.com/sparachi1011/language_translation_japan_english/assets/37170486/290d92bb-b641-4345-930c-e9e28c919723)

Disclimer: Though these packages utilized profound and trusted converter application(i.e., Google Translate)If you still more concerned about data security you can enable ssl verification else you can develop your own custome translator from scrach.


**Input to Project:**
----------------------
A log file whose logs looks alike **Feb  3 00:05:43  192.168.11.101[MSWinEventLog#0110#011Security#011-#011土] 03 00:05:43 2024#0114656#011Microsoft-Windows-Security-Auditing#011J1#011N/A#011-#011192.168.11.101#011-#011オブジェクトに対するハンドルが要求されました。  
サブジェクト: #011セキュリティ ID:#011#011S-1-5-21-796759982-425631752-4269433831-1001 #011アカウント名:#011#011J1 #011アカウント ドメイン:#011#011OPS11 #011ログオン ID:#011#0110x28DA7  オブジェクト: #011オブジェクト サーバー:#011#011Security #011オブジェクトの種類:#011#011Process 
#011オブジェクト名:#011#011\Device\HarddiskVolume4\Windows\System32\lsass.exe #011ハンドル ID:#011#0110x79c #011リソース属性:#011-  プロセス情報: #011プロセス ID:#011#0110x3cc #011プロセス名:#011#011C:\diasys\system\DIASYSGlobalCard.exe  アクセス要求情報: #011トランザクション ID:#011
#011{00000000-0000-0000-0000-000000000000} #011アクセス:#011#011プロセス メモリからの読み取り #011#011#011#011プロセス情報の照会 #011#011#011#011未定義のアクセス (影響なし) ビット 12 #011#011#011#011 #011アクセス理由:#011#011- #011アクセス マスク:#011#0110x1410 
#011アクセスの確認に使用した特権:#011- #011制限された SID 数:#0110**

**Output to Project:**
-----------------------
A converted and parsed python dictionary saved in JSON file as below.**
**{
    "1": {
        "event_timestamp": "Feb 03 00:05:43",
        "source_ip": "192.168.11.101",
        "event_log": "[mswineventlog0security-sat] 03 00:05:43 20244656microsoft-windows-security-auditingj1n/a-# a handle to the 011192.168.11.101- object was requested",
        "security_id": "s-1-5-21-796759982-425631752-4269433831-1001",
        "account_name": "j1",
        "account_domain": "ops11",
        "logon_id": "0x28da7",
        "object_server": "security",
        "object_type": "process",
        "object_name": "\\device\\harddiskvolume4\\windows\\system32\\lsass.exe",
        "handle_id": "0x79c",
        "resource_attribute": "-",
        "process_id": "0x3cc",
        "process_name": "c:\\diasys\\system\\diasyssglobalcard.exe",
        "transaction_id": "{00000000-0000-0000-0000-000000000000}",
        "access": "read",
        "access_reason": "-",
        "access_mask": "0x1410",
        "privileges_used_to_verify_access": "-",
        "limited_number_of_sids": "0"
    },
 }**
