# Journal

## 2022

### 1.5

**Aliyun OSS Service**

```python
#!/usr/bin/env python3.6
#coding=utf-8
import os
import urllib.request, json, datetime, time
import ssl
from aliyunsdkcore.client import AcsClient
from aliyunsdkr_kvstore.request.v20150101.DescribeBackupsRequest import DescribeBackupsRequest
from aliyunsdkr_kvstore.request.v20150101.DescribeInstancesRequest import DescribeInstancesRequest
  
  
client = AcsClient('********************', '**************************', 'cn-xxx')
  
  
#获取阿里云redis实例列表
def get_redis_insts():
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    request.set_PageNumber(1)
    request.set_PageSize(100)
    response = client.do_action_with_exception(request)
    return json.loads(response).get('Instances')['KVStoreInstance']
  
  
#根据实例ID获取备份下载地址列表
def get_bak_urls(instId, startTime, endTime):
    request = DescribeBackupsRequest()
    request.set_accept_format('json')
    request.set_StartTime(startTime)
    request.set_EndTime(endTime)
    request.set_InstanceId(instId)
    response = client.do_action_with_exception(request)
    return json.loads(response).get('Backups').get('Backup')
  
  
#根据下载地址下载备份到本地（IDC备份机111.11.11.11）
def get_redis_bak(folder_path,url):
    if not os.path.exists(folder_path):
        print("Selected folder not exist, try to create it.")
        os.makedirs(folder_path)
    filename = url.split('/')[-1].split('?')[0]
    filepath = folder_path + '/' + filename
    if os.path.exists(filepath):
        print("File have already exist. skip")
    else:
        try:
            print("Try downloading file: {}".format(url))
            ssl._create_default_https_context = ssl._create_unverified_context #导入ssl时关闭证书验
            urllib.request.urlretrieve(url, filename=filepath)
            print("Done")
        except Exception as e:
            print("Error occurred when downloading file, error message:")
            print(e)
  
  
#清理30天前的备份文件
 
def fileremove(filename, remove_time):
    timeInt = os.path.getmtime(filename)
    sec = remove_time * 86400
    cc = time.time()
    if int(timeInt) < int(cc) - int(sec):
        if 'aliyun_redis_bak.py' not in filename :
            print("remove file 30 days ago :")
            os.remove(filename)
            print(filename)
 
 
def delFilesOfDirAndSubdir(filedir, deltime):
    if os.path.isfile(filedir):
        fileremove(filedir, deltime)
    else:
        try:
            for i in os.listdir(filedir):
                if os.path.isfile(filedir + '/' + i):
                    fileremove(filedir + '/' + i, deltime)
                else:
                    new_dir = filedir + '/' + i
                    delFilesOfDirAndSubdir(new_dir, deltime)
        except Exception as e:
            print("Error occurred when remove file, error message:")
            print(e)
 
 
if __name__ == "__main__":
    bak_home = '/backup/aliyun_redis_bak/'
    delFilesOfDirAndSubdir(bak_home, 30)
    now = datetime.datetime.now()
    thirtyDaysAgo = (datetime.datetime.now() - datetime.timedelta(days=30))
    endTime = now.strftime("%Y-%m-%dT%H:%MZ")
    startTime = thirtyDaysAgo.strftime("%Y-%m-%dT%H:%MZ")
    for kvs in get_redis_insts():
        print('Begin get baks of: ' + kvs['InstanceName'])
        bakList = get_bak_urls(kvs['InstanceId'], startTime, endTime)
        for bak in bakList:
            get_redis_bak(bak_home + kvs['InstanceName'], bak['BackupDownloadURL'])
        print('End  get baks of: ' + kvs['InstanceName'])
 
 
#pip3 install requests
#pip3 install request
#pip3 install aliyunsdkcore
#pip3 install aliyunsdkr_kvstore
#pip3 install aliyun-python-sdk-r-kvstore
#pip3 install aliyun-python-sdk-core-v3
```

Promise.reject(new Error(data.rmsg));

### 2.20

** Double click **

```vue
    hdlClick(node, data) {
      const nodeData = node;
      this.clickCount++;
      const fnEmitDblClick = debounce(() => {
        if (this.clickCount > 1) { // 双击跳转并设置下载的文件
          this.changeNode(nodeData);
          this.setDownloadFile(data);
        }
        this.clickCount = 0;
      }, 200);
      fnEmitDblClick();
    },
```

** promt's validator **

```vue
      this.$prompt('新建' + (type === 'buildFolder' ? '文件夹名' : '文件名:'), '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValidator(value) {
          const nodeParent =
              node.parent.data instanceof Array
                ? node.parent.data
                : node.parent.data.children;
          const obj = nodeParent.find((item) => {
            return (
              item.isFile === node.data.isFile &&
                item.label === value &&
                item.id !== node.data.id
            );
          });
          if (obj) {
            return '已有' + (node.data.isFile ? '文件' : '文件夹') + '同名';
          }
        }
```

### 2.24

**Git ^M to \n**

```
git config --global core.autocrlf false
git config --global core.safecrlf true
```

### 4.9

**Python unzip** 

```python
import os
import shutil
import zipfile
from os.path import join, getsize

def unzip_file(zip_src, dst_dir):
    if os.path.exists(zip_src):
        r = zipfile.is_zipfile(zip_src)
        if r:
            print("unzip: ", zip_src)
            fz = zipfile.ZipFile(zip_src, 'r')
            for file in fz.namelist():
                fz.extract(file, dst_dir)
        else:
            print('This is not zip')
            return
        try:
            filename = dst_dir.split('/')[-1];
            if os.path.exists(dst_dir + "/index.py"):
                os.rename(dst_dir + "/index.py", dst_dir + "/" + filename + ".py")
            else:
                print("watchout: ", dst_dir + "/index.py")
        except:
            pass

def doit(path, father):
    if os.path.exists(path):
        if os.path.isfile(path):
            unzip_file(path, father)
            return
        print("doit:", path)
        for filename in os.listdir(path):
            doit(path + "/" + filename, path)

doit("./userLibrary", ".")
```

