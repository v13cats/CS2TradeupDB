import requests
import time

note = "\033[37m[\033[96m¬\033[37m] "

# https://tradeupdb.com -> login -> web developer tools -> cookies -> auth
auth_cookie = {'auth': r''}


print(note + "Starting...")

buffer_b = [] # not technically buffers.
buffer = []
sub = []
profitability_found = 0
index_found         = 0

for pagenum in range(1000000):
    time.sleep(0.5)
    page = requests.get(f"https://tradeupdb.com/database?page={pagenum}", cookies=auth_cookie)

    if (page.status_code == 200):
        pagelines = (page.text).replace(" ","").split("\n")

        sanity_check = 0

        for lines in pagelines: # this part may need to be changed if the website changes layout
            if "div_db_frame_entry" in lines:
                sanity_check += 1
                parase = lines.split("div_db_frame_entry")
                for i in range(len(parase)):
                    if parase[i].startswith("_"):
                        #print(parase[i])
                        #print("=====================================================================================================================")
                        if "Tier" in parase[i]:
                            sub.append(parase[i+1].replace("""_stats"><pclass="p_freetier">""", "").replace('</p></div></div><divclass="', "").replace('''_stats"><pclass="p_Premium2">''', ''))
                        if "Cost" in parase[i]:
                            sub.append(parase[i+1].replace("""_stats"><pclass='p_stats'>$""", "").replace('</p></div></div><divclass="', ''))
                        if "Profitibility" in parase[i]:
                            sub.append(parase[i+1].replace("""_stats"><pclass='p_stats'>""", "").replace('%</p></div></div><divclass="', ''))
                        if "Odds" in parase[i]:
                            sub.append(parase[i+1].replace("""_stats"><pclass='p_stats'>""", "").replace('%</p></div></div><divclass="', ''))
                        if "view_tradeup" in parase[i]:
                            if "tradeup?t=" in parase[i]:
                                sub.append(parase[i].replace("""_w3"alt=""><aclass="view_tradeup"href="tradeup?t=""", "")[:64])

                            buffer.append(sub)
                            sub = []
                            profitability_found = 0
                            index_found         = 0

        if (sanity_check == 0): # exit if we cant access the webpage 
            print(note + "No login, (or another error preventing access to html).")
            exit()


        for i in range(len(buffer)):
        # print(buffer[i][2])
            if (float(buffer[i][2]) > float(profitability_found)):
                index_found = i
                profitability_found = buffer[i][2]

        if (index_found != 0):
            #print(buffer[index_found])

            if len(buffer) == 4:
                reflink = "unobtainable (likely no premium access)"
            else:
                reflink = "https://tradeupdb.com/tradeup?t=" + buffer[index_found][4]

            print(note + "[" + str(page.status_code) + f"] checked page {pagenum}, best tradeup: [ \033[36mcost:\033[37m ${buffer[index_found][1]}, \033[32mprofitability\033[37m: {buffer[index_found][2]}%, \033[33modds:\033[37m {buffer[index_found][3]}%, href: '{reflink}' ]")

            buffer_b.append(buffer[index_found])
            buffer = []
    else:
        choose = input(note + "recieved non 200 status code, would you like to print the tradeups found so far? Y/n")

        if choose.lower() == "y" or choose.lower() == "":
            for entry in buffer_b:
                print(entry)

        exit(1)