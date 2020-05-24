import requests, re, time
from bs4 import BeautifulSoup

def get_info(url):
    print("collecting data...")
    r=requests.post(url)
    soup=BeautifulSoup(r.text,'html.parser')
    # get number of pages
    page_txt= soup.find('div', attrs={'class':'pagination'})
    page= int(re.findall(r'(\d+)',page_txt.text)[-1]); print(f'{page} pages founded')
    # get information page to page
    dic={}
    for i in range(1,page+1):
        print(f'we are on page {i}')
        r=requests.post(url+str(i))
        soup=BeautifulSoup(r.text,'html.parser')
        name=soup.find_all('a',attrs={'class':'phone'})
        price=soup.find_all('td',attrs={'class':'price'})
        l,n,p=len(name),name,price

        for j in range(l):
            n=name[j].text; p=price[j].text
            p=int(re.sub(r',','',p).strip())
            if n in list(dic.keys()): dic[n].append(p)
            else: dic[n]=[p]
    return dic


def in_dic(dic_a):
    print('sorting information...')
    dic={}
    for name in list(dic_a.keys()): 
        brand, model= name.split()[0], ' '.join(name.split()[1:])
        if brand not in list(dic.keys()):
            dic[brand]={}
        if model not in list(dic[brand].keys()):
            dic[brand][model]=[min(dic_a[name]),max(dic_a[name])]
            if dic[brand][model][0]==dic[brand][model][1]: del dic[brand][model][1]
    return dic

def result(dic):
    print('final calculations...')
    for b in list(dic.keys()):
        fb=f'\n------\n{b}\n------';print(fb)
        for m in list(dic[b].keys()):
            p=dic[b][m]
            if len(p)==1: s=f'{m:28s}|| {p[0]:<9,d}T'
            else: s=f'{m:28s}|| {p[0]:<9,d}T to {p[1]:<9,d}T'
            print(s)

def txt_file(dic):
    file=open('dic_phones.txt','w')
    file.write(str(dic))
    file.close()

print('\nstart');start=time.time()

url='https://www.mobile.ir/phones/prices.aspx?duration=7&pagesize=500&sort=date&dir=desc&page='

dic_a= get_info(url)
r=in_dic(dic_a)
#txt_file(r) #<-- for create a text file from phones dictionary
result(r)
print(f'\n{time.time() - start:.2f} secconds')
print('done')
