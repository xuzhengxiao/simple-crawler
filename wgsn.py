import os
import requests
import json
import copy

cookie = "LOGIN_PAGE_LANG=en; exclusionChecked=True; _gcl_au=1.1.1660611953.1554186114; _ga=GA1.2.629229464.1554186114; _gid=GA1.2.1617704777.1554186114; ss_udid=2e65dacc7abcce96a8c11e581be8ac88; product=WGSN; _fbp=fb.1.1554186131459.1880297905; cp_SubStat=Subscriber; cp_UserID=1602348; PHPSESSID=fe8946i6b6vu4175hl4duldfng; _mkto_trk=id:948-BWZ-312&token:_mch-wgsn.com-1554186141073-91367; LPVID=Y3YzA1NzVhY2ZlYTRlYmM2; cp_browStat=Logged In; cp_hybridBrowStat=Logged In; LPSID-83891085=eGucQIIUT0mZCejvaeRAJA; ss_token=cf442ad45753f7fac8fd0084bbf2ef92; ss_plogin=1602348%7C121261404; XSRF-TOKEN=eyJpdiI6IlRnZDFob1ZXbGlMamE5K3FYSTVcL1dBPT0iLCJ2YWx1ZSI6IlRRdnB5ZmVWWTlpM0xVT1VUUXRuOEJvOTVTRktNbHZ0dlNYK00wTGw0MkI4cGNWa1FiU2RtQW12UU9BR1wvMXp4ZHh5VDNzNVYxcGRoa2xLMEg4QzV3QT09IiwibWFjIjoiYTBhOTgwOTNmNzRiN2IxOTJlMzlkM2I2YjI3MDg1ZjcxYTJmMTJlMWQ0ZDRhMDVkNGY2OTJhMmM1ODYyMmVlYiJ9; peach_session=eyJpdiI6IjlyZzhreHdpdWE5Z00yNkxuWk5ZQ3c9PSIsInZhbHVlIjoiRjJxdmcrY2cxMUxqcU52QUJNTGZrbWh3SU5IT3JJUmh3RmxBSXMxY1I1dGd4ZmVjdkdhWndQQlwvcG0yWkZOVVdWeWFkZHpoOGkxZDlpSnVzalZkR1pRPT0iLCJtYWMiOiJiMWFjMzhkNmYxYjkxMDFmMjJlMDk2ZWIzNTAzOGEzYWMzNmYyNmZjYTkzMDdiYjJjNjQ3ODNjN2ZiMjcyYmEyIn0%3D; ss_lang=cs; trwv.uid=stylesight-1554186115262-98758e81%3A3; trwsa.sid=stylesight-1554193571893-beb4d338%3A11"

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
           'Connection':'keep-alive',
           # 'Origin': 'https://www.wgsn.com',
           'Referer': 'https://www.wgsn.com/library/results/77fbd126ab595504c5270b0485befe0c?lang=cs',
           # 'Cookie': cookie,
           'Host':'www.wgsn.com',
           'Upgrade-Insecure-Requests':'1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
           # "X-XSRF-TOKEN":"eyJpdiI6IlN3SEJDdGVVeW05ZW5od0l6TmE4VHc9PSIsInZhbHVlIjoiRG9xXC9ja3YzaEVPcXBuVHhIaFZ0Sm9vM0JJbUpCQWRrb21qUEZ4ZGVSRDIzd3BUOU5aUjk2WFwvWFcyaU5ucDhYOSt6d1Z3N1ZmWlkzcmsxS1BVbkFodz09IiwibWFjIjoiM2M0NTY4YWJjYjE3NDgzMjlkNTIwMTZjNzg5M2M5MzFhZDc2MzUzMmZjZTE4ZjU0YTMyYTAzMmI3MTI0MzE4MiJ9"}
           }
_headers=copy.deepcopy(headers)
_headers['Content-Type']='application/json;charset=UTF-8'
global session

proxy = '192.168.16.109:13128'
proxy = {'http': 'http://' + proxy, 'https': 'https://' + proxy}

def get_imgId(offset=0):
  url="https://www.wgsn.com/api/cherry/search/query"
  data={"filters":{"categories":["2026693"]},"q":[],"log":False,"lang":"cs","params":{"limit":200,"offset":0,"object_id":None,"sort":[{"field":"add_date"}]}}
  data["params"]["offset"]=offset
  global session
  try:
    r = session.post(url, headers=_headers,data=json.dumps(data))
    r.encoding = "utf-8"
    if r.status_code == 200:
      return r.json()
  except Exception as e:
    print (repr(e))
    return None

def download_single(img_id,file_name):
  try:
    global session
    exe_php="https://www.wgsn.com/myfolders/download.php"
    data={'image_id':'image.'+img_id}
    r = session.post(exe_php, headers=headers,data=data)
    data=r.json()
    file_name+=("."+data["ext"])
    download_img_id=data["dl_id"]
    url="https://www.wgsn.com/myfolders/get_download.php?dl_id="+download_img_id

    r= session.get(url,headers=headers)
    url = "https://www.wgsn.com" + r.history[0].headers["Location"]
    r = session.get(url, headers=headers, timeout=10) # stream=True to set stream downloading,however encounting unexpected end of file problem.
    if r.status_code == 200:
      with open(file_name, "wb") as f:
        # for chunk in r.iter_content(chunk_size=100):
        #   if chunk:
        #     f.write(chunk)
        f.write(r.content)
  except:
    # exit(1)
    print ("download error!")
    return False,file_name
  return True,file_name


def download_one_page(results,total_count,num,img_dir):
  for ix,result in enumerate(results):
    try:
      if ix!=0 and ix%99==0:
        login()
      print ("downloading image {} out of {}".format(num,total_count))
      num+=1
      img_id=result["id"]
      file_name=result["name"]
      caption=result["caption"]
      # caption[0]=caption[0].replace('/','-')
      caption_dir=os.path.join(os.path.join(img_dir,caption[0]),caption[2])
      if not os.path.isdir(caption_dir):
        os.makedirs(caption_dir)
      check_state,_=download_single(str(img_id),os.path.join(caption_dir,file_name))
      # give failed downloaded image second chance
      if not check_state:
        print ("second try")
        check_state,file_name=download_single(str(img_id), os.path.join(caption_dir, file_name))
      if not check_state and os.path.exists(file_name):
        print ("second try fails,remove useless file")
        os.remove(file_name)
    except:
      continue
  return num


def login():
  url="https://www.wgsn.com/api/wham/users/login/?lang=cs"
  data={"username":"******","password":"******","r":None,"remember":"1","submit":"登录"}
  global  session
  session=requests.Session()
  login_headers=copy.deepcopy(headers)
  login_headers["Content-Type"]= "application/x-www-form-urlencoded"
  login_headers["Referer"]="https://www.wgsn.com/cs/login/"
  html=session.post(url,data=data,headers=login_headers)

def main():
  img_dir="/data/其他/wgsn_images"
  num=0
  if not os.path.isdir(img_dir):
    os.makedirs(img_dir)
  login()
  # for c in session.cookies:
  #   print (c.expires)
  offset=0
  data=get_imgId(offset)
  results=data["data"]["results"]
  total_count = data["data"]["count"]
  num=download_one_page(results,total_count,num,img_dir)
  while(offset<total_count):
    try:
      offset+=200
      data = get_imgId(offset)
      results = data["data"]["results"]
      num = download_one_page(results, total_count, num,img_dir)
    except:
      login()
      continue


if __name__ == '__main__':
    main()


