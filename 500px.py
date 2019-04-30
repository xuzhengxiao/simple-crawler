import requests
import os


def get_page(url,data):
  cookie="device_uuid=d32ae3a6-49a6-4d16-86f7-d264e7c5e558; optimizelyEndUserId=oeu1550746127820r0.675519976353232; csrf_token=jS%2BkY%2BCQlBrXpdEJ%2Fzo3cHozN6QG4oAR5OO2Hr5y16Q%3D; _ga=GA1.2.553512697.1550746210; _gid=GA1.2.1634513126.1550746210; _fbp=fb.1.1550746210258.534063084; __gads=ID=d00a8b1289cffaf3:T=1550746904:S=ALNI_MZNqSC390EmWIUWKhAebkA48kXp4g; amplitude_id_9d249102d4736c5a98373c4526f77ae3500px.com=eyJkZXZpY2VJZCI6ImQzMmFlM2E2LTQ5YTYtNGQxNi04NmY3LWQyNjRlN2M1ZTU1OCIsInVzZXJJZCI6bnVsbCwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNTUwODg4NzA2ODc1LCJsYXN0RXZlbnRUaW1lIjoxNTUwODg4NzA3NTk3LCJldmVudElkIjozLCJpZGVudGlmeUlkIjowLCJzZXF1ZW5jZU51bWJlciI6M30=; amplitude_id500px.com=eyJkZXZpY2VJZCI6ImMxZDg4Y2U5LTZmZDAtNGNkMi1hZTRmLTFlOTQ2NTg2NTU5OVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU1MDg4ODgwMjIxMCwibGFzdEV2ZW50VGltZSI6MTU1MDg4ODgxNTk2MCwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6Mywic2VxdWVuY2VOdW1iZXIiOjR9; _hpx1=BAh7C0kiD3Nlc3Npb25faWQGOgZFVEkiJTg0NTBhZmQ0ZmYzYTc2NTM2ZTIyYjE1YmU3M2M4ZmJmBjsAVEkiCWhvc3QGOwBGIhJhcGkuNTAwcHguY29tSSIZdXNlX29uYm9hcmRpbmdfbW9kYWwGOwBGVEkiGHN1cGVyX3NlY3JldF9waXgzbHMGOwBGRkkiEF9jc3JmX3Rva2VuBjsARkkiMWpTK2tZK0NRbEJyWHBkRUovem8zY0hvek42UUc0b0FSNU9PMkhyNXkxNlE9BjsARkkiEXByZXZpb3VzX3VybAY7AEZJIi8vc2VhcmNoP3N1Ym1pdD1TdWJtaXQmcT1mbG93ZXImdHlwZT1waG90b3MGOwBU--717308ea4362727d904ea34f64fb1d4e1905a524"
  headers = {'Accept': '*/*',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
             'origin': 'https://500px.com',
             'referer': 'https://500px.com/search?q=%E8%8A%B1&type=photos&sort=pulse',
             'cookie':cookie,
             'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
             "x-csrf-token":"LaqUdf6pi3IbIsMaGvgwZl+GhFBOM2RBEIjvkbz3rhGghTAWHjkfaMyHEhPlwgcWJbWz9EjR5FD0a1mPAoV5tQ=="}
  try:
    r = requests.get(url, headers=headers, params=data)
    r.encoding = "utf-8"
    if r.status_code == 200:
      return r.json()
  except:
    print ("error!")

def get_flower(html,img_dir,index):
  photos=html["photos"]
  for photo in photos:
    image_url=photo["image_url"]
    image_url=image_url[8]
    print ("downloading image {}".format(index))
    try:
      content=requests.get(image_url,timeout=10).content
      with open(os.path.join(img_dir, str(index) + '.jpg'), "wb") as f:
        f.write(content)
        index+=1
    except:
      print ("time out,download next image")
      continue
  return index



def main():
  # img_dir = "images"
  # if not os.path.isdir(img_dir):
  #   os.makedirs(img_dir)
  url='https://api.500px.com/v1/photos/search?'
  data={"type":"photos","term":"flower","sort":"highest_rating","image_size":"1,2,32,31,33,34,35,36,2048,4,14","include_states":"true","formats":"jpeg,lytro",
        "include_tags":"true","exclude_nude":"true","page":"1","rpp":"50"}


  terms=["底纹"]  # "自然抽象艺术" ,"水彩","水波"
  for term in terms:
    img_dir = "images/"+term
    if not os.path.isdir(img_dir):
      os.makedirs(img_dir)
    data["term"]=term
    # get first page
    print("page 1")
    html=get_page(url,data)
    pages=html["total_pages"]
    total_items=html["total_items"]
    index = 1
    index=get_flower(html,img_dir,index)
    try:
      for page in range(2,pages):
        print ("page {} out of {}".format(page,pages))
        data["page"]=str(page)
        html = get_page(url, data)
        #print (html)
        index=get_flower(html,img_dir,index)
        if index>=5000:
          break
    except:
      continue

if __name__ == '__main__':
  main()


  




