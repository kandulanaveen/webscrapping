import requests
from scrapinghelp import htmlhelper
from datetime import datetime
import hashlib
import json
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def transform_name(name):
        name=name.replace("  ","")
        name=name.replace("\r","")
        name=name.replace("\t","")
        name=name.replace('\n','')
        name = name.replace("_", "")
        name = name.replace("Shri ", "")
        name = name.replace("SRI ", "")
        name = name.replace("Smt. ", "")
        name = name.replace("Dr. ", "")
        name = name.replace("Dr ", "")
        name = name.replace("Capt. ", "")
        name = name.replace("Sh. ", "")
        name = name.replace("Sri ","")
        name = name.replace("Smt ","")
        name = name.replace("Smti. ","")
        name = name.replace("Smti ","")
        name = name.replace("Mr. ","")
        name = name.replace("Sri. ","")
        name = name.replace("H.E. ","")
        name = name.replace("Sir ","")
        name = name.replace("Sh ","")
        name = name.replace("Shri&nbsp; ","")
        name = name.replace("&nbsp;","")
        name = name.replace("<o:p></o:p>","")
        name = name.replace("<o:p>  </o:p>","")
        name = name.replace("<o:p> </o:p>","")
        name = name.replace("<br>","")
        name = name.replace("Shri","")
        name = name.replace("<b>. ","")
        name = name.replace("</b>","")
        name = name.replace("Smt. ","")
        name = name.split(',')
        name = name[0]
        name = name.strip()
 
        return name
 
def alias_name(name):
    alias_list=[]
    subname = name.split(' ')
    l = len(subname)
    if l>=3:
        name1 = subname[l-1] + " " + subname[0]
        name2 = subname[l-2] + " " + subname[0]
        alias_list.append(transform_name(name1))
        alias_list.append(transform_name(name2))
    if l==2:
        name1 = subname[1] + " " + subname[0]
        alias_list.append(transform_name(name1))
    
    return alias_list


if __name__=="__main__":

    url="http://www.niyamasabha.org/codes/members.htm"

    res=requests.get(url)

    get_small_source = htmlhelper.returnformatedhtml(res.text)

    get_individuals = htmlhelper.collecturl(get_small_source,"<tbody>","</tbody>")
    print(get_individuals)
    mylist = []

    for ele in get_individuals:

        source_data = htmlhelper.collecturl(ele,"<tr>","</tr>")
        print(source_data)
        for go in source_data:

                d = {
                        "uid": "",
                        "name": "",
                        "alias_name": [],
                        "gender": "",
                        "date_of_birth": [],
                        "country": [
                            "India"
                        ],
                        "family-tree": {
                            "parent": "",
                            "sibling": "",
                            "children": "",
                            "spouse": ""
                        },
                        "designation": "",
                        "last_updated": last_updated_string,
                        "address": [
                            {
                                "complete_address": "kerela,india",
                                "state": "kerela",
                                "city": "",
                                "country": "India"
                            }
                        ],
                        "nns_status": "False",
                        "organisation": "",
                        "documents": {},
                        "source": {
                            "host_country": "India",
                            "name": "",
                            "description": "",
                            "type": "PEP",
                            "url": "http://www.niyamasabha.org/codes/members.htm"
                        },
                        "comment": ""
                }

                try:
                    get_last_name = htmlhelper.collecturl(go, "<font size=\"3\" face=\"Liberation Serif\" color=\"#0000FF\">","</font>")
                    print(get_last_name)
                    print("kj")
                except:
                    print("hi")
                    pass

                try:
                    first_name = get_last_name[0]
                    if first_name!="":
                        d['name']=transform_name(first_name)
                        d['alias_name']=alias_name(d['name'])
                except:
                    pass
                
                try:
                    designation = get_last_name[2]
                    if first_name!="":
                        d['designation']= designation
                except:
                    pass
                

                try:
                    d["uid"] = hashlib.sha256(
                        ((d["name"] + d["source"]["type"]).lower()).encode()).hexdigest()
                except:
                    pass

                try:
                    mylist.append(d)
                    print("k")
                except:
                    pass

    with open('w1.json', 'w', encoding="utf-8") as file:
        json.dump(mylist, file, ensure_ascii=False, indent=4)











