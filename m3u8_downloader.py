#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
用于流视频下载器
先下载m3u8文件
逐行读取文件
解析
'''
import psutil
import requests
import os
import tkinter as tk
import random
import string
import sys
from urllib.parse import quote,unquote
import time

os.system("mode con cols=35 lines=11")
root=tk.Tk()
root.withdraw()
root.wm_attributes('-topmost',1)
proxies = {}
pxy = ''
fname = ''
cur_path = ''


def check_is_end():
    while True:
        j = 0
        for i in psutil.process_iter():
            if "aria2c.exe" in str(i):
                j += 1
        if j == 0:
            print("不存在aria2c进程,可放心进行文件合并操作!")
            return
        else:
            time.sleep(3)
            continue

            

    
def vname_str():
    ran_str = ''.join(random.sample(string.ascii_letters, 8))
    return ran_str

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')


def select_proxy():
    global proxies
    while True:
        id = input("是否启用代理(默认不启用)?Y/N")
        if id == "Y" or id == "y":
            check()
            os.system("title 【代理模式】")
            return
        elif id == "N" or id == "n":
            proxies = {}
            os.system("title 【直连模式】")
            return
        else:
            proxies = {}
            os.system("title 【直链模式】")
            return
        


def check():
    global proxies,pxy
    if not os.path.exists("proxy.ini"):
        f=open("proxy.ini","w",encoding="utf-8")
        f.close()
        
    f = open("proxy.ini","r",encoding="utf-8")
    line = f.readline()
    f.close()
    if line:
        proxies = {"http":line,"https":line}
        pxy = "--all-proxy=\"http://"+line+"\""
    else:
        print("代理格式:\"127.0.0.1:7890\"")
        os.system("notepad.exe proxy.ini")
        os.system("pause")
        check()
          
        
        
def m3u8_download(url):
    #try:
    hdr = {}
    if "pan.baidu.com" not in str(url):
        r = requests.get(url)
        with open("0.m3u8",'wb') as code:
            code.write(r.content)
    else:
        hdr = {}
                    
    d = GetDesktopPath()
    premain_ = ""
    premain = '/'.join(str(url).split("/")[:3])+'/'
    print(premain)
    if "video-lmn.xhcdn.com" in str(url) or "hls-hw.xvideos-cdn.com" in str(url):
        premain_ = '/'.join(str(url).split("/")[:-1])+'/'
        print("premain_1:"+premain_)
    elif "urlset/" in str(url):
        premain_ = (str(url).split("urlset/")[0])+'urlset/'
        print("premain_2:"+premain_)                    
    r = requests.get(url,headers=hdr,proxies=proxies)
    l = (r.text.split('\n'))
    dl = []
    cl = []
    el = []
    k = 0
    while k < len(l):
        if str(l[k]).startswith('http'):
            pm = '/'.join(str(l[k]).split("/")[:3])+'/'
            if pm != premain:
                premain = pm
            break
        elif not str(l[k]).startswith('http') and not str(l[k]).startswith('/') and str(l[k]).endswith('.ts'):
            premain = '/'.join(str(url).split("/")[:-1])+'/'
            break
        elif str(l[k]).startswith('/') and str(l[k]).endswith('.ts'):
            premain = '/'.join(str(url).split("/")[:3])+'/'
            break
        k += 1
    print(premain)
    
    tl = []
    tl_ = []
    key = ""
    kn = "" 
    #判断是否为加密流
    k = 0
    while k < len(l):
        if str(l[k]).startswith("#") and "AES-128,URI=" in str(l[k]):
            tmp = str(l[k]).split("AES-128,URI=\"")[1].split('\"')[0]
            kn = str(l[k]).split("AES-128,URI=\"")[1].split('\"')[0].split('/')[-1]
            if tmp.startswith('http'):
                key = tmp
            else:
                key = premain+tmp
            break
        k += 1
        
    #下载密钥
    print(key)
    print(kn)
    try:        
        r = requests.get(key,proxies=proxies)
        with open('temp/'+kn,'w',encoding='utf-8') as code:
            code.write(r.text)
            code.close()
    except:
        pass 
    if os.path.exists('0.m3u8'):
        f = open('0.m3u8','r',encoding='utf-8')    
        while True:
            i = f.readline()
            if i:
                if str(i).startswith('#') and "AES-128,URI=\"" in str(i):
                    temp = ""
                    temp = str(i).split("AES-128,URI=\"")[0]+"AES-128,URI=\"temp/"+kn+"\"\n"
                    tl_.append(temp)
                elif not str(i).startswith('#'):
                    temp = ""
                    if premain not in str(i):
                        temp = premain+str(i).lstrip('/')
                    else:
                        temp = str(i).lstrip('/')
                    tl.append(temp)
                    temp = "temp/"+str(i).split("/")[-1]
                    tl_.append(temp)
                else:
                    tl_.append(str(i))
            else:
                break
            

        print(tl)
        print(tl_)
            
    if key != "":
        #用于下载的m3u8文件   
        f = open('1.m3u8',"a",encoding='utf-8')
        for j in tl:
            f.write(j)
        f.close()
        
        #用于合并的m3u8文件
        f = open('2.m3u8','a',encoding='utf-8')
        for j in tl_:
            f.write(j)
        f.close()            
        
    tmp = ""
    mtp = ""
    first=True
    j = 1        
    if "pan.baidu.com" in str(url):
        try:
            tmp = unquote(url,'utf-8')
            if tmp.startswith("https://pan.baidu.com/api/streaming?path=/"):
                print(tmp)
                mtp = tmp.split('?path=')[1].split('&')[0].split(".")[-1]
                tmp = '.'.join(tmp.split('?path=')[1].split('&')[0].split('/')[-1].split(".")[:-1])
                print(tmp)
                print(mtp)   
        except:
            pass

    for i in l:
        if  not str(i).startswith('#') and str(i) != "":
            print(str(i))
            if str(i).startswith("http") and str(i).endswith('m3u8'):
                url2 = str(i)
                print(url2)
                return m3u8_download(url2)
            elif 'ts' not in str(i) and not str(i).startswith("http") and str(i).endswith('m3u8'):
                url2 = premain+str(i).lstrip('/')
                print(url2)
                return m3u8_download(url2)                    
            elif str(i).startswith('http') and str(i).endswith('.ts'):
                dl.append(str(i).strip('/')+"\n")
                cl.append('file \'temp/'+str(i).strip('/').split('.ts')[0].split('/')[-1]+".ts\'\n")
            elif 'urlset/' in str(url) or 'video-lmn.xhcdn.com' in str(url) :
                dl.append(premain_+str(i).strip('/')+"\n")
                cl.append('file \'temp/'+str(i).strip('/').split('.ts')[0].split('/')[-1]+".ts\'\n")
            elif 'hls-hw.xvideos-cdn.com' in str(url):
                dl.append(premain_+str(i).strip('/')+"\n")
                cl.append('file \'temp/'+str(i).strip('/').split('.ts')[0]+".ts\'\n")
            elif str(i).endswith('.js'):
                if str(i).startswith('http'):
                    dl.append(str(i).strip('/')+"\n")
                else:
                    dl.append(premain+str(i).strip('/')+"\n")
                cl.append('file \'temp/'+str(i).strip('/').split('.js')[0].split('/')[-1]+".js\'\n")
            elif str(i).endswith('.image'):
                if str(i).startswith('http'):
                    dl.append(str(i).strip('/')+"\n")
                else:
                    dl.append(premain+str(i).strip('/')+"\n")
                cl.append('file \'temp/'+str(i).strip('/').split('.image')[0].split('/')[-1]+".image\'\n")
            elif "baidupcs.com" in str(i) and str(i).startswith("https://"):
                dl.append("\""+str(i).strip('/')+"\"\n")
                if first == True:                   
                    cl.append('file \'0'+'.'+mtp+"\'\n")
                    el.append('0.'+mtp)
                    first = False
                elif first == False:
                    cl.append('file \''+str(j)+'.'+mtp+"\'\n")
                    el.append(str(j)+'.'+mtp)
                    j += 1
            elif str(i).startswith("https://") and "cibntv.net" in str(i):
                dl.append("\""+str(i).strip('/')+"\"\n")     
                if first == True:
                    cl.append('file \'0'+".ts\'\n")
                    el.append('0.ts')
                    first = False
                else:
                    cl.append('file \''+str(j)+'.ts'+"\'\n")
                    el.append(str(j)+'.ts')
                    j += 1                     
                    
            else:
                dl.append(premain+str(i).strip('/')+"\n")
                cl.append('file \'temp/'+str(i).strip('/').split('.ts')[0].split('/')[-1]+".ts\'\n")                               
              
                                
                
    #print(cl)
    #print(dl)

                
    f = open(fname+'2.txt',"a",encoding='utf-8')    
    for j in cl:
        f.write(j)
    f.close()
    
    f = open(fname+'.txt',"a",encoding='utf-8')    
    for j in dl:
        f.write(j)
    f.close()

    if key == "":
        if "pan.baidu.com" not in str(url) or "janan.net" not in str(url):
            cmdline = 'aria2c.exe -i '+fname+'.txt -c -j32 -s16 -x16 '+pxy+' -d temp/'
            print("cmdline1:"+cmdline)
            os.system(cmdline)
         
        else:
            k = 0
            for j in dl:
                cmdline2 = 'start aria2c.exe -o '+el[dl.index(j)]+" "+j+' -c --max-tries=5 '+pxy
                print("cmdline2:"+cmdline2)
                os.system(cmdline2)
                k += 1
                if k > 127:
                    k = 0
                    time.sleep(5)
        
        check_is_end()
        if "pan.baidu.com" not in str(url):
            cmdline3 = 'ffmpeg.exe -f concat -safe 0 -i '+fname+'2.txt'+' -c copy '+d+'\\'+fname+'.mp4 && del *.txt *.m3u8 *.avi *.mp4 *.flv *.mkv *.rmvb temp\*.* /Q 2>NUL'
            print("cmdline3:"+cmdline3)
            os.system(cmdline3)
        else:
            #cmdline4 = 'ffmpeg.exe -f concat -safe 0 -i '+fname+'2.txt'+' -c copy '+d+'\\'+fname+'.mp4'
            cmdline4 = 'ffmpeg.exe -f concat -safe 0 -i '+fname+'2.txt'+' -c copy '+d+'\\'+fname+'.mp4 && del *.txt *.m3u8 *.avi *.mp4 *.flv *.mkv *.rmvb temp\*.* /Q 2>NUL'
            print("cmdline4:"+cmdline4)
            os.system(cmdline4)                
            
        os.system('cls')
        print("下载完成!")
        return            
    
    else:
        cmdline = 'aria2c.exe -i 1.m3u8 -c -j32 -s16 -x16 '+pxy+' -d temp/'
        print(cmdline)
        os.system(cmdline)
        cmdline2 = 'ffmpeg.exe -allowed_extensions ALL -i 2.m3u8 '+' -c copy -absf aac_adtstoasc '+d+'\\'+fname+'.mp4 && del *.txt *.m3u8 *.avi *.mp4 *.flv *.mkv temp\*.* /Q 2>NUL'
        print("cmdline2:"+cmdline2)
        os.system(cmdline2)
        return

    #except:
        #os.system('taskkill /IM aria2c.exe /F 2>NUL')
        #os.system('del *.txt *.m3u8 temp\*.* /Q 2>NUL')
        #return


if __name__ == '__main__':

    os.system('taskkill /IM aria2c.exe /F 2>NUL')
    select_proxy()
    os.system('cls')
    while True:
        try:
            fname = vname_str()
            url = root.clipboard_get()
            m3u8_download(url)
            wc.OpenClipboard()
            wc.EmptyClipboard()
            wc.CloseClipboard()                    
            os.system('cls')
            print("请复制新m3u8链接以便开启新任务")
            os.system('pause')        
        except:
            os.system('cls')
            print("请复制新m3u8链接以便开启新任务")
            os.system('pause')  
    


    

        

    
    
 
        
        
    


        
  
        

        
        
        

    
