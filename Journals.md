# Journals
## 2021

### 5.23

#### pandas plot

Use pandas to draw picture

```python
#/usr/bin/python

import pandas as pd
import matplotlib.pyplot as plt

file = open('result.txt', 'r')

lines = file.readlines()

train_data = []
test_data = []

for line in lines:
    if line[1] == 'r': # train
        train_data.append(float(line.split()[-1]))
    else: # test
        test_data.append(float(line.split()[-1]))

train_set = pd.Series(train_data)
test_set = pd.Series(test_data)

train_set.plot(title = 'IWAU-Net diceloss', legend = True, label = 'train diceloss')
test_set.plot(legend = True, label = 'test diceloss')

plt.savefig('result.png')
```

#### count down helper

In order to train my coding speed, write a count down helper.

Think twice code once.

```python
#!/usr/bin/python3                                                                                                      
# -*- coding: UTF-8 -*-                                                                                         
import time  
import shutil                                                                                                           
                                                                                                                       
def countdown(m):
    colums = shutil.get_terminal_size().columns                                                                         
    m = int(m)                                                                                                          
    for minute in range(m, -1, -1):                                                                                     
        if minute == 0:                                                                      
            break                                                        
        for second in range(59, -1, -1):                                                                               
            time.sleep(1)  
            sys.stdout.write("\r")                       
            sys.stdout.write(('{}:{}'.format(minute-1, second)).center(colums))                                         
            sys.stdout.flush()                                                                                         
                                                                                                                        
    sys.stdout.write(('END').center(colums))                                                                           
                                                                                                                        
if __name__ == '__main__':                                                                                              
    countdown(sys.argv[1])
```

### 5.24

#### Latex

Install Latex on Ubuntu 18.04:

```bash
$ sudo apt-get install texlive-full
```

### 5.26

#### Pandas

Program to help merge excel forms.

Use `pandas` and its data frame to work.

To read .xlsx need to use xrld <= 1.2.0

```bash
$ pip uninstall xlrd
$ pip install xlrd==1.2.0
```

```python
import pandas as pd
import os
pathDir = os.listdir('data')

def solve(filename):
    global al
    print("On: ", filename)
    fi = pd.read_excel('data/' + filename, index_col = 1) #, converters = {'学号' : str})
    stu = fi.index
    teacher = filename.split('.')[0]
    for person in stu:
        print(person)
        al.loc[person, '最终成绩'] = fi.loc[person, '最终成绩'] #fi.loc[person, '最终成绩']
        al.loc[person, '批卷人'] = teacher

    print("Read: ", fi.shape)


if __name__ == '__main__':
    global al
    al = pd.read_excel('2021毕业学生名单.xls', index_col = 0) #, converters = {'学号' : str})
    al['批卷人'] = 'unkown'
    for x in pathDir:
        solve(x)
    writer = pd.ExcelWriter('result.xls')
    al.to_excel(writer)
    writer.save()

```

However its converters dont work, use dtype to replace it.

### 5.28

Prepare for the zhihuishu

repo: github/trswnca/zhihuishu

### 5.30

#### Vue
config vue's axios setting. To differ the json request and the form data request

```javascript
axios.interceptors.request.use(
  config => {
    let token = localStorage.getItem('token')
    if (token) {
      config.headers.common['Authentication-Token'] = token
    }
    if (config.useQs) {
      config.data = qs.stringify(config.data)
    }
    return config
  },
  err => {
    return Promise.reject(err)
  }
)
```


### 6.2

#### Latex

When I instsall some packages with perl dependency, the error warning:

```bash
perl: warning: Please check that your locale settings:
	LANGUAGE = (unset),
	LC_ALL = (unset),
	LC_COLLATE = "C",
	LANG = "zh_CN.UTF-8"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
```

so I just `export LC_AL=C`

The latex package manager `tlmgr` is not supported for the Linux distros. According to the [Wiki](https://wiki.archlinux.org/title/TeX_Live), I install `tllocalmgr`.

#### Shell & Gitlab

To delete dozens of Project, I wrote a shell.

Firstly, get the token from the gitlab.

```bash
#!/bin/bash

for ((i = 146; i <= 175; ++i));
do
  curl -X DELETE "http://192.168.1.6/api/v4/projects/"$i"?private_token=NAM-bxCucwHxuZtjGsEH"
done
```

#### Javascript

I realized that async/await is the core concept that the Javascript held.

When we want to do things step by step, we need to let it be a Promise. And:

```javascript
async function doRequests(requests) {
    for(let r of requests) {
        let result = await r
        console.log(result)
    }  
}
```

And for the axios's series, just:

```javascript
      let YML = await this.$http.post("/api/function/saveFile", {
          fileContent: ymlFile, 
          relativePath: "/deploy.yml",
          functionName: this.myFunction.name,
        }).then(res => {
          console.log("YML生成：", res.message)
        })

      // 提交数据库
      let NEWDATABASE = await
        this.$http.post('/api/contribute/new/v2', {
          category: this.myFunction.category,
          description: this.myFunction.introduction ,
          id: gitlab_id,
          lang: this.myFunction.lang ,
          memory: 40,
          name: this.myFunction.name ,
          params: "", //this.params,
          realName: "",
          timeout: 40
      }).then(res => {
        this.$message("数据库生成：", res.data.message)
      })
      ...
      doRequests([NEWFOLDER, GITLAB, YML, NEWDATABASE, GETCODE, ROUTE])
```


### 6.10

#### Nginx

```bash
# find config location (or) test config file
nginx -t
# reload nginx
nginx -s reload
```

### 6.11

#### Go

Download latest one [Golang](https://golang.google.cn/doc/install?download=go1.16.5.linux-amd64.tar.gz)

```bash
$ rm -rf /usr/local/go && tar -C /usr/local -xzf go1.14.3.linux-amd64.tar.gz
$ echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.profile && source ~/.profile
```

Use goproxy.cn to accelerate

```bash
$ go env -w GO111MODULE=on
$ go env -w GOPROXY=https://goproxy.cn,direct
$ echo "export GOPROXY=https://goproxy.cn" >> ~/.profile && source ~/.profile
```

### 6.14

#### Go
```bash
$ go build foo/bar/baz
package foo/bar/baz is not in GOROOT (/usr/local/go/src/foo/bar/baz)
$ go env              
GO111MODULE="on"
GOARCH="amd64"
GOBIN=""
GOCACHE="/home/trswnca/.cache/go-build"
GOENV="/home/trswnca/.config/go/env"
GOEXE=""
GOFLAGS=""
GOHOSTARCH="amd64"
GOHOSTOS="linux"
GOINSECURE=""
GOMODCACHE="/home/trswnca/go/pkg/mod"
GONOPROXY=""
GONOSUMDB=""
GOOS="linux"
GOPATH="/home/trswnca/go/"
GOPRIVATE=""
GOPROXY="https://goproxy.cn,direct"
GOROOT="/usr/local/go"
GOSUMDB="sum.golang.org"
GOTMPDIR=""
GOTOOLDIR="/usr/local/go/pkg/tool/linux_amd64"
GOVCS=""
GOVERSION="go1.16.5"
GCCGO="gccgo"
AR="ar"
CC="gcc"
CXX="g++"
CGO_ENABLED="1"
GOMOD="/dev/null"
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -m64 -pthread -fmessage-length=0 -fdebug-prefix-map=/tmp/go-build775828347=/tmp/go-build -gno-record-gcc-switches"
```

Just turn off the `GO111MODULE="on"` to include $GOPATH

```bash
$ go env -w GO111MODULE=auto  
```


### 6.15

#### Go & Vscode

Enable the go autocomplete, Add:

```json
{
  "go.autocompleteUnimportedPackages": true,
  "go.gocodePackageLookupMode": "go",
  "go.gotoSymbol.includeImports": true,
  "go.useCodeSnippetsOnFunctionSuggest": true,
  "go.inferGopath": true,
  "go.gopath": "/home/trswnca/go",
  "go.useCodeSnippetsOnFunctionSuggestWithoutType": true,
}
```

### 7.3

#### Mysql

Install mysql on Ubuntu:

```bash
$ sudo apt install mysql-server
```

#### Ssh & Server

See which port for ssh

```bash
$ netstat -tnlp | grep sshd
```

Config the Flowing `~/.ssh/config`

```
Host TX
  HostName 49.232.70.168
  Port 22022
  User root

Host AliBlogServer
  HostName 8.141.68.129
  Port 22
  User root
```

And upload the public key:
```bash
$ ssh-copy-id -p22022 root@49.232.70.168
```

### 7.7

#### Update Vimrc

```vimscript
" Plugins
source ~/.config/vim/plugged.vim

" Spaces & tabs
set tabstop=2	        " number of visual spaces per TAB
set softtabstop=2       " number of spaces in tab when editing
set expandtab           " tabs are spaces

" Ui config
set number              " show line numbers
set cursorline          " highlight current line
set wildmenu            " visual autocomplete for command menu
set shiftwidth=2        " automatic indent space
set laststatus=2        " for lightline
" set modeline=1
filetype indent on      " load filetype-specific indent files

" Leader Shortcut
let mapleader=','       " leader is comma
inoremap jj <esc>

" Searching
set incsearch           " search as characters are entered
set hlsearch            " highlight matches
" turn off search highlight
nnoremap <leader><space> :nohlsearch<CR>

" Folding
set foldenable          " enablefolding
set foldlevelstart=10   " open most folds by default
set foldnestmax=10      " 10 nested fold max
" space open/closes folds
nnoremap <space> za
set foldmethod=indent   " fold based on indent level

" Key Bindings
" move vertically by visual line
nnoremap j gj
nnoremap k gk

" move to beginning/end of line
nnoremap B ^
nnoremap E $

" $/^ doesn't do anything
nnoremap $ <nop>
nnoremap ^ <nop>

" move windows
nnoremap <space> <c-w>

" highlight last inserted text
nnoremap gV `[v`]
" toggle gundo
nnoremap <leader>u :GundoToggle<CR>

" open ag.vim
nnoremap <leader>a :Ag

" open NerdTree.vim
nnoremap <C-o> :NERDTreeToggle<CR>

" jump to declaraion feature
nnoremap <leader>g :YcmCompleter GoToDefinitionElseDeclaration<CR>

" BackUps
set backup
set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set backupskip=/tmp/*,/private/tmp/*
set directory=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set writebackup

" CtrlP settings
let g:ctrlp_match_window = 'bottom,order:ttb'
let g:ctrlp_switch_buffer = 0
let g:ctrlp_working_path_mode = 0
let g:ctrlp_user_command = 'ag %s -l --nocolor --hidden -g ""'

" Lightline settings
let g:lightline = {
  \     'active': {
  \         'left': [['mode', 'paste' ], ['readonly', 'filename', 'modified']],
  \         'right': [['lineinfo'], ['percent'], ['fileformat', 'fileencoding']]
  \     }
  \ }

" Set Colors
colorscheme molokai      " https://github.com/sjl/badwolf/blob/master/colors/badwolf.vim
syntax enable            " enable syntax processing

" vim:foldmethod=marker:foldlevel=0
"
"

" Functions
function Compile()
	if &filetype ==# 'cpp'
		exec "!g++ % -o %< -g -Wall -Wextra -Wconversion -std=c++11"
	elseif &filetype ==# 'c'
		exec "!gcc % -o %< -g -Wall -Wextra -Wconversion"
	elseif &filetype ==# 'tex'
		exec "!xelatex '%'"
	elseif &filetype ==# 'java'
		exec "!javac %"
	endif
endfunction

function Debug()
	if &filetype ==# 'cpp' 
		exec "!lldb ./%<"
	elseif &filetype ==# 'tex'
		exec "!open './%<.pdf'"
	elseif &filetype ==# 'java'
		exec "!jdb %<"
	endif
endfunction

function Run()
	if &filetype ==# 'cpp'
		exec "!time ./%<"
	elseif &filetype ==# 'tex'
		exec "!open -a Preview.app './%<.pdf'"
	elseif &filetype ==# 'java'
		exec "!java %<"
	elseif &filetype ==# 'html'
		exec "!firefox %"
	elseif &filetype ==# 'php'
		exec "!php %"
	elseif &filetype ==# 'sh'
		exec "!bash %"
	endif
endfunction

" WSL yank support
let s:clip = '/mnt/c/Windows/System32/clip.exe'  " change this path
if executable(s:clip)
  augroup WSLYank
    autocmd!
    autocmd TextYankPost * if v:event.operator ==# 'y' | call system(s:clip, @0) | endif
  augroup END
endif

map <F9> : call Compile() <CR>
map <C-o> : call Compile() <CR>
map <F5> : call Debug() <CR>
map <F6> : call Run() <CR>
map <F2> : ! python3 % <CR>
```

### 7.23

#### CUPS

CUPS printers do not autoscale.

```bash
Option fitplot True
```

### 7.29

#### Selenium

Install Selenium on my CentOS:

```bash
$ wget https://npm.taobao.org/mirrors/chromedriver/88.0.4324.27/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ chmod 755 chromedriver
```

### 8.1

#### Latex

Add style file:

```tex


\newlength{\thelinewidth}
\thelinewidth=\textwidth

\newlength{\exmpwidinf}
\newlength{\exmpwidouf}


\exmpwidinf=0.43\thelinewidth
\exmpwidouf=0.43\thelinewidth


\def\s@tm@cr@s{
    \def\widthin##1{\exmpwidinf=##1\relax}
    \def\widthout##1{\exmpwidouf=##1\relax}
    \def\stretchin##1{\advance\exmpwidinf by ##1\relax}
    \def\stretchout##1{\advance\exmpwidouf by ##1\relax}
    \@ifstar{
        \error Star must not be used in example environment any more
    }
}

%% Example with counter
\newenvironment{example}[1][]{

  \par\noindent \paragraph*{样例}$ $  \\
    %\s@tm@cr@s
    \ttfamily\obeylines\obeyspaces\frenchspacing
    \newcommand{\exmp}[2]{
        \begin{minipage}[t]{\exmpwidinf}\rightskip=0pt plus 1fill\relax##1\medskip\end{minipage}&
        \begin{minipage}[t]{\exmpwidouf}\rightskip=0pt plus 1fill\relax##2\medskip\end{minipage}\\
        \hline
    }

    \newcommand{\exmpfile}[2]{
       \exmp{
          \verbatiminput{##1}
       }{
          \verbatiminput{##2}
       }%%
    }


    \begin{tabular}{|l|l|}
        \hline
        \multicolumn{1}{|c|}{\bf\texttt{Input}}&
        \multicolumn{1}{|c|}{\bf\texttt{Output}}\\
        \hline
        }{
    \end{tabular}%
}
```

So we should use that like this:

```tex
\begin{example}
	\exmp{
        6
        8555 3 2
        2
        4815 0 0
        2999 3 3
        0
	}{
	0.00
	291.90
	}%
\end{example}
```

should notice that the  `%` should not miss.

### 8.2

#### Pandas

DataFrame's row :

```python
import pandas as pd
import os

def solve(filename):
    global al
    print("On: ", filename)
    fi = pd.read_excel(filename, index_col = 0) 
    stu = fi.index
    #print(stu)
    for person in stu:
        try:
            fi.loc[person, '学院'] = al.loc[person, '学院']
            fi.loc[person, '学号'] = al.loc[person, '学号']
            fi.loc[person, '联系电话'] = al.loc[person, '联系电话']
        except:
            try:
                all_can = al.loc[person]
                for index, row in all_can.iterrows():
                    if (row['居住地址'] == fi.loc[person, '居住地址'] or row['户籍地址'] == fi.loc[person, '户籍地址']):
                        fi.loc[person, '学院'] = row['学院']
                        fi.loc[person, '学号'] = row['学号']
                        fi.loc[person, '联系电话'] = row['联系电话']
            except:
                print(person, "Not Found")

    writer = pd.ExcelWriter('res' + filename)
    fi.to_excel(writer)
    writer.save()

if __name__ == '__main__':
    global al
    al = pd.read_excel('all2.xls', index_col = 2)
    solve("q.xls")
```

### 8.5

#### Vue

```
error  in ./src/views/Home.vue?vue&type=style&index=0&lang=less&
Syntax Error: TypeError: this.getOptions is not a function
```

Because my version of less is too high.

```bash
npm uninstall --save less-loader
npm install -D less-loader@7.3.0
```
### 8.6

#### Latex

Use straight signle quote

```tex
\usepackage{textcomp}
\lstset{upquote=true}
```

### 8.8

#### Proxy

Install `proxychains` to reset the proxy:

```bash
$ sudo pacman -S proxychains-ng 
```

Edit the configuration on `/etc/proxychains.conf`:

```
- socks4 	127.0.0.1 1950
+ socks5 	127.0.0.1 20170
```

Test:

```bash
$ proxychains curl ip.cn                                    
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.15
[proxychains] Strict chain  ...  127.0.0.1:20170  ...  ip.cn:80  ...  OK
```

Set for terminal, edit .zshrc:

```bash
alias pc="proxychains"
```

### 8.23

#### termite & ssh

When Termite is used for SSH connections to a remote system which does not have its Terminfo, various issues (such as non-working backspace and weird cursor behaviour) could happen. The solution is to send your Terminfo to the remote host.

On the local host, using Termite:

```bash
$ infocmp > termite.terminfo  # export Termite's Terminfo
$ scp termite.terminfo user@remote-host:~/  # or any other method to copy to the remote host
```

On the remote host, in the directory where you copied termite.terminfo:

```bash
$ tic -x termite.terminfo  # import Terminfo for current user
$ rm termite.terminfo  # optional: remove Terminfo file
$ exit # close this session
```


### 8.27

#### Recover /var/lib/dpkg

```bash
$ sudo mkdir -p /var/lib/dpkg/{alternatives,info,parts,triggers,updates}
$ sudo cp /var/backups/dpkg.status.0 /var/lib/dpkg/status
$ apt download dpkg base-files
$ sudo dpkg -i *.deb
$ dpkg --audit
```

### 9.3

#### Use Astyle to format cpp code

Add ft command:

```bash
alias ft="astyle --style=google -t2 -p -H -U -k1"
```

### 9.23

#### Rename the git tag

```bash
$ git tag newtagname oldtagname # build new tag at the same position
$ git -d oldtagname # delete local old tag 
$ git push origin :refs/tags/oldtagname # delete remote old tag
$ git push --tags # upload the new tag
```

### 9.27

#### Solve problems oreignted by icu package

```bash
$ pamac update
pamac: error while loading shared libraries: libicuuc.so.68: cannot open shared object file: No such file or directory

# Solution:
$ sudo mkdir -p ~/pkg/tmp && tar -I zstd -xvf /var/cache/pacman/pkg/icu-68.2-1-x86_64.pkg.tar.zst -C ~/pkg/tmp
$ sudo mkdir -p ~/pkg/tmp && tar -I zstd -xvf /var/cache/pacman/pkg/icu-69.1-1-x86_64.pkg.tar.zst -C ~/pkg/tmp
$ sudo cp ~/pkg/tmp/usr/lib/libicu*.68 /usr/lib/
$ sudo cp ~/pkg/tmp/usr/lib/libicu*.69 /usr/lib/
```

### 9.30

#### RAM

For some reason my system only detects 5.71G out of the 8G I've actually got installed on my laptop.
My BIOS detects the 8G of RAM I've got installed (so did my old Windows install), and the BIOS memory test doesn't show any errors.

I had my doubts about the old ram I had, so I bought two new sticks of 8G each. Turns out, instead of having 16G, I have 13.6G of RAM, so something weird is going on here.

THAT IS BECAUSE 2GB go to the APU, 437MB are reserved for other purposes. LAPTOP PROBLEM.

#### Pip

Pip installed but show command not found

Beacuse my python work on my own path, just export it:

```bash
export PATH=$PATH:/home/trswnca/.local/bin
```

#### Shell

Extented  complie:

```
compile() {
  ext=${1##*.}
  fame=${1%.*}
  if [ $1 != $fame ]
  then
    echo "g++ $1 -o $fame -DLOCAL -g -Wall -Wextra"
    g++ $1 -o $fame -DLOCAL -g -Wall -Wextra
  elif [[ -a $1.cpp ]]
  then
    echo "g++ $1.cpp -o $1 -DLOCAL -g -Wall -Wextra"
    g++ $1.cpp -o $1 -DLOCAL -g -Wall -Wextra
  elif [[ -a $1.cc ]]
  then
    echo "g++ $1.cc -o $1 -DLOCAL -g -Wall -Wextra"
    g++ $1.cc -o $1 -DLOCAL -g -Wall -Wextra
  else
    echo "No Such file!"
  fi
}
```

### 10.20

#### Accelerate the vim-plug

Edit `plug.vim`:

```
- let fmt = get(g:, 'plug_url_format', 'https://git::@github.com/%s.git')
+ let fmt = get(g:, 'plug_url_format', 'https://git::@hub.fastgit.org/%s.git')

- \ '^https://git::@github\.com', 'https://github.com', '')
+ \ '^https://git::@hub.fastgit\.org', 'https://hub.fastgit.org', '')
```

#### Options for neovim installation

```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\*\shell\nvim-qt]
@="Open Neovim"
"Icon"="\"C:\\tools\\neovim\\Neovim\\bin\\nvim-qt.exe\""

[HKEY_CLASSES_ROOT\*\shell\nvim-qt\command]
@="\"C:\\tools\\neovim\\Neovim\\bin\\nvim-qt.exe\" \"%1\""

[HKEY_CLASSES_ROOT\Directory\shell\nvim-qt]
@="Open Neovim Here"
"Icon"="\"C:\\tools\\neovim\\Neovim\\bin\\nvim-qt.exe\""

[HKEY_CLASSES_ROOT\Directory\shell\nvim-qt\command]
@="\"C:\\tools\\neovim\\Neovim\\bin\\nvim-qt.exe\" \"%1\""

[HKEY_CLASSES_ROOT\Directory\Background\shell\nvim-qt]
@="&Neovim here"
"Icon"="\"C:\\tools\\neovim\\Neovim\\bin\\nvim-qt.exe\""

[HKEY_CLASSES_ROOT\Directory\Background\shell\nvim-qt\command]
@="\"C:\\tools\\neovim\\Neovim\\bin\\nvim-qt.exe\" \"%v\""
```

### 10.21

#### Goland with WSL2

`Setting -> Terminal -> Shell Path` use `wsl.exe`  

### 10.24

#### Vercel

Add environment variable at vercel.com
Regenerate the token **Only occur once and on generation**

### 10.26

#### OSS

Download all oss files from aliyun:

```python
# encoding=utf8
import oss2
import os

endpoint = "oss-cn-shenzhen.aliyuncs.com"
accesskey_id = "LT*P"
accesskey_secret = "Rh*"
bucket_name = "breaktech"

# 本地文件保存路径前缀
download_local_save_prefix = "/mnt/e/"

'''
列举prefix全部文件
'''


def prefix_all_list(bucket, prefix):
    print("开始列举" + prefix)
    oss_file_size = 0
    for obj in oss2.ObjectIterator(bucket, prefix='%s/' % prefix):
        oss_file_size = oss_file_size + 1
        download_to_local(bucket, obj.key, obj.key)

    print(prefix + " file size " + str(oss_file_size))


'''
列举全部的根目录文件夹、文件
'''


def root_directory_list(bucket):
    # 设置Delimiter参数为正斜线（/）。
    num = 0
    for obj in oss2.ObjectIterator(bucket, delimiter='/'):
        # 通过is_prefix方法判断obj是否为文件夹。
        if obj.is_prefix():  # 文件夹
            print('directory: ' + obj.key)
            prefix_all_list(bucket, str(obj.key).strip("/")) # 去除/
        else:  # 文件
            print('file: ' + obj.key)
            download_to_local(bucket, str(obj.key), str(obj.key))
            num += 1
            print(num)


'''
下载文件到本地
'''


def download_to_local(bucket, object_name, local_file):
    url = download_local_save_prefix + local_file
    # 文件名称
    file_name = url[url.rindex("/") + 1:]

    file_path_prefix = url.replace(file_name, "")
    #print(os.path.exists(file_path_prefix))
    if False == os.path.exists(file_path_prefix):
        os.makedirs(file_path_prefix)
        #print("make dir" + file_path_prefix)

    # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
    try:
        bucket.get_object_to_file(object_name, download_local_save_prefix + local_file)
    except:
        print("ERR:")

if __name__ == '__main__':
    auth = oss2.Auth(accesskey_id, accesskey_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    # 单个文件夹下载
    #prefix_all_list(bucket, "20201223")
    root_directory_list(bucket)
    print("end")

```

### 10.28

#### nvim-qt

Set font size:

add line in `ginit.vim`

```vimscript
execute join(["GuiFont! ", split(GuiFont, ":")[0], ":h14"], "")
```

### 10.30

#### Python

```python
p = lamda a, b: print(a + 1, b + 1)
```


### 11.3

#### Bash

attention that `()` means using a son proccess to proceed, and `{}` just mean a code segment

```bash
DIR=./test
  pwd
  [ -d $DIR ] && (
    cd $DIR
    echo "Current Directory is `pwd`"
    echo "`ls –l *.h | wc –l ` files (*.h)"
    pwd
    )
pwd
```

### 11.4

#### Go Protobuf

Install:

```bash
$ go get -d -u github.com/golang/protobuf/protoc-gen-go
```

### 11.5

#### Go Protobuf

```bash
$ make go
mkdir -p tutorial # make directory for go package
protoc $PROTO_PATH --go_out=tutorial addressbook.proto
google/protobuf/timestamp.proto: File not found.
addressbook.proto: Import "google/protobuf/timestamp.proto" was not found or had errors.
addressbook.proto:49:3: "google.protobuf.Timestamp" is not defined.
Makefile:32: recipe for target 'protoc_middleman_go' failed
make: *** [protoc_middleman_go] Error 1
```

The problem is I forgot here
> If you intend to use the included well known types then don't forget to copy the contents of the 'include' directory somewhere as well, for example into '/usr/local/include/'.

### 12.2

#### docker

Install:

```bash
$ curl -sSL https://get.daocloud.io/docker | sh
```

Try:

```bash
$ sudo docker run hello-world
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
See 'docker run --help'.
```

```bash
# trswnca # @ # LAPTOP-5DSBBEQG # in @ Y7000P in /mnt/c/Users/TRSWNCA [14:07:44] C:125
$ sudo service docker start
 * Starting Docker: docker                                                                                       [ OK ]

# trswnca # @ # LAPTOP-5DSBBEQG # in @ Y7000P in /mnt/c/Users/TRSWNCA [14:08:06]
$ sudo docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete
Digest: sha256:cc15c5b292d8525effc0f89cb299f1804f3a725c8d05e158653a563f15e4f685
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

**Network error**

```docker
$ cat Dockerfile
# syntax=docker/dockerfile:1
FROM node:12-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
# Add this
RUN apk add --no-cache python3 g++ make
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
```

### 12.12

#### Crontab

```
$ crontab -e
# add line to the crontab
$ crontabl -l
# list the jobs
```


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

## 2023

### September
- Close the audio radar of the sound card

Press `ctrl+shift+o`

- How to update Obsidian subdirectories to the remote repositories automatically?

One simple solution is "update everything" command in original Obsidian-Git plugin. Keep tracing the problem of simply using this command.

```
docker run --name dst-admin -d -p8080:8080 -p10888:10888/udp -p10998-10999:10998-10999/udp registry.cn-hangzhou.aliyuncs.com/dzzhyk/dst-admin:latest
docker logs dst-admin
```

## 2024

### March

#### ssh terminal not highlighted

```bash
$ dircolors
LS_COLORS='';
export LS_COLORS
```

add following lines to `~/.zshrc`

```zsh
LS_COLORS='rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=00:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.avif=01;35:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:*~=00;90:*#=00;90:*.bak=00;90:*.crdownload=00;90:*.dpkg-dist=00;90:*.dpkg-new=00;90:*.dpkg-old=00;90:*.dpkg-tmp=00;90:*.old=00;90:*.orig=00;90:*.part=00;90:*.rej=00;90:*.rpmnew=00;90:*.rpmorig=00;90:*.rpmsave=00;90:*.swp=00;90:*.tmp=00;90:*.ucf-dist=00;90:*.ucf-new=00;90:*.ucf-old=00;90:';
export LS_COLORS
```

