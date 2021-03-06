from structureReader import structureReader as sr
import os
import sys
import pandas as pd

supported_website_url_list = ["proxy-030.dc3.dailymotion.com"] #ADD url
supported_website_name_list = ["dailymotion"] #ADD website
supported_extension_list = [".ts"] #ADD Extension

def combine(path, tuples):
    assemble_data = b""
    for (file_name, dummy) in tuples:
        target = os.path.join(path, str(file_name))
        with open(target, "rb") as file:
            data = file.read()
            assemble_data = assemble_data + data

    return assemble_data

# oupput_filename = dailymotion_sec(##).ts
def write(website,section,data):
    
    #TODO Determine extensin by reading data
    extension = ".ts"
    
    output_filename = website + "_" + section + extension
    with open(output_filename, "wb") as file:
        file.write(data)
        print(output_filename+" success!")

# check validity of data(url)
def pre_analysis(url):
    for extension_list in supported_extension_list:
        if url.find(extension_list) > 0 :
            return True
        else :
            return False

def get_website_url(url):
    # website Categorize
    website_url = url.split("/")[2]
    if website_url == supported_website_url_list[0] :
        return supported_website_name_list[0]
    else :
        pass

def get_section_from_url(url):
    section_url = ""
    split_url = url.split("/")
    website_url = url.split("/")[2]
    if website_url == supported_website_url_list[0] :
        section_url = split_url[3]
    else:
        pass
    return section_url

def get_fragment_from_url(url):
    fragment_url=""
    split_url = url.split("/")
    website_url = url.split("/")[2]
    if website_url == supported_website_url_list[0]:
        temp = split_url[4] # frag(#), video
        a = temp.find("(")
        b = temp.find(")")
        if a>=0 :
            fragment_url = temp[a+1:b]
            return int(fragment_url)
        else :
            pass
    else:
        pass

def parse_url(data_list):
    categorized_by_web_and_section = dict() # Video[web]
    for (video, url) in data_list:
        if not pre_analysis(url): #Proceed only with url that has '.mp4' and '.ts'
            continue
        if url in supported_website_url_list : #Proceed only with supported website
            continue

        website_information = get_website_url(url) #website get Information e.g)dailymotin, youtube...
        section_information = get_section_from_url(url) #seciton get Information

        if website_information not in categorized_by_web_and_section.keys() :
            categorized_by_web_and_section.setdefault(website_information, dict())
        if section_information not in categorized_by_web_and_section[website_information].keys():
            categorized_by_web_and_section[website_information].setdefault(section_information, list())
        #ADD dictionary key
        
        categorized_by_section = categorized_by_web_and_section[website_information][section_information] 
        categorized_by_section.append((video, get_fragment_from_url(url)))

    return categorized_by_web_and_section

def sorting(categorized_by_dictionary):
    #frag sort
    keys = categorized_by_dictionary.keys()
    for key in keys:
        unwrapped_data = categorized_by_dictionary[key]

        second_keys = unwrapped_data.keys()
        for second_key in second_keys:
            core_data_lists = categorized_by_dictionary[key][second_key]
            core_data_lists.sort(key=lambda element : element[1])

    return categorized_by_dictionary

def get_url(path):
    cs = sr.cref(["magic","version","urllength","md5"],[8,4,4,4],[False,False,False,False],None,"Cache_Header") << sr.cref.structure
    with  open(str(path), 'rb') as file:
        buffer = file.read(1024)
        if(buffer==b''):
            print("EOF")
            sys.exit()
    cs << buffer
    length = cs.byte2int((cs >> ("urllength",)))
    return buffer[cs.sizeof():cs.sizeof()+length].decode('utf-8').strip()

def csv_write(path, _list):
    df = pd.DataFrame(_list)
    df.to_csv(path,index=False,mode="w")

if __name__ == '__main__':

    basepath = ""
    data = []
    result = []
    
    for file_name in os.listdir(basepath) :
        if file_name == "$I30" or file_name == "index":
            continue
        target = os.path.join(basepath, file_name)
        data.append(file_name)
        data.append(get_url(target))
        
    n=2
    file_name_and_url = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n )]
    
    result_of_parse = parse_url(file_name_and_url) #url parsing
    result_of_sort = sorting(result_of_parse) # sorting

    keys = result_of_sort.keys()
    for key in keys:
        unwrapped_data = result_of_sort[key]
        second_keys = unwrapped_data.keys()
        for second_key in second_keys:
            core_data_list = result_of_sort[key][second_key]
            combined_data = combine(basepath,core_data_list) #assemble
            write(key,second_key, combined_data) #write








