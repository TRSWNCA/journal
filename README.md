# Journal

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
