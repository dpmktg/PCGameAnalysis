

import requests
import re
import json
import pandas 
from datetime import date, datetime, timedelta


today = date.today()
f = '%b %d, %Y'
d1 = today.strftime("%d-%m-%Y")
d2 = datetime.strptime(today.strftime('%b %d, %Y'),f)



i = 0

d = pandas.DataFrame()

print("Select an option (type the number of your option)\n"+("1 - Game/Publisher research (Will show as many as 50 results unless there are less games or the program crashes)\n"+"2 - Similar game (Get infos about games similar to the one you want)")) 
choice = int(input())

if choice == 1:
    
    name = input("Please enter the name of the game you'd like to search\n")
    url = requests.get("https://store.steampowered.com/search/?term="+name+"&category1=998") #default request is https://store.steampowered.com/search/?term="+name+"&category1=998 in case you want to revert to default settings
    htmltext = url.text
    

    pattern = '''data-ds-appid="(.[0-9]*)"+ '''

    regex = re.findall(pattern, htmltext)

    print("nb result :"+ str(len(regex)))
    for appid in regex:

        j = 0
        try :
            url2 = requests.get("https://steamcommunity.com/games/"+appid)
            htmltext2 = url2.text
        
            Title = htmltext2.split('apphub_AppName ellipsis">')[1].split('<')[0] 
            groupID = htmltext2.split("OpenGroupChat( '")[1].split("'")[0]
        
            print(Title)
        
            membersUrl = requests.get("https://steamcommunity.com/gid/"+groupID+"/memberslistxml/?xml=1")
    
            cleanMembers = int(membersUrl.text.split('<memberCount>')[1].split('<')[0])
        
            print("Followers",cleanMembers,"Low Wishlist Estimation", cleanMembers*5, "Average Wishlist Estimation", int(cleanMembers*9.6), "High Wishlist Estimation", cleanMembers*14 )
        
        

            url3 = requests.get("https://store.steampowered.com/api/appdetails?appids="+appid+"&cc=us&l=en")
        
        

            htmltext3 = url3.text

            releaseDate = htmltext3.split('date":"')[1].split('"')[0]
        except IndexError :
            cleanMembers = 0
            
        try:

            daysSinceRelease = d2 - datetime.strptime(releaseDate, f)
        except ValueError:
            daysSinceRelease = 'Game is unreleased'

        reqPlayers = requests.get("https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid="+appid+"?l=english")
        reqPlayersText = reqPlayers.text

        if 'player' in reqPlayersText:
            currentPlayers = reqPlayersText.split('player_count":')[1].split(',')[0]
        else:
            currentPlayers = 0
        
        reqtag = requests.get("https://store.steampowered.com/app/"+appid+"?l=english")
        agecheck = 'CheckAgeGateSubmit'

        if agecheck in reqtag.text:
            sessionId = reqtag.split('var g_sessionID = "')[1].split('"')[0]
            reqtag = requests.post("https://store.steampowered.com/app/"+appid+"?l=english", data={'number': sessionId, 'ageDay': '1', 'ageMonth': 'January', 'ageYear': '1970'})
            
        tagpattern = '''\/tags\/en\/(.[A-Za-z%\-\d]*)'''
        tags = re.findall(tagpattern, reqtag.text)


        reviewCheck = 'ions":{"total":'
        check2 = 'final_formatted'
        isOnSale = 'initial_formatted":"$'
        isFree = '"is_free":true'
        reviewInApi = 'ions":{"total":'
        reviewCheck = 'user reviews'
        noReview ='data-tooltip-html="No user reviews"'
        notEnoughReviews = 'not_enough_reviews'
        recentReviews = '30 days'
        totalReviews ='aggregateRating'
        reviewTrigger = 'userReviews'
        recentReviewPattern = '''style="cursor: pointer;" data-tooltip-html="(.[0-9]*)'''
        url4 = requests.get("https://store.steampowered.com/app/"+appid+"?l=en")

        htmltext4 = url4.text
        allReviewScore = re.findall(recentReviewPattern, htmltext4)

        if reviewTrigger in htmltext4:
            if noReview in htmltext4 :
                print("This game doesn't have any review")
                allReviewScore.insert(1, "No Recent Review")
                allReviewScore.insert(0, "No Recent Review")
                recentRating = 'No Recent Rating'
                rating = 'No Rating'
            elif notEnoughReviews in htmltext4:
                totalReviews = htmltext4.split('num_reviews" value="')[1].split('"')[0]
                totalPositiveReviews = htmltext4.split('positive_reviews" value="')[1].split('"')[0]
                positivePercentage = int(totalPositiveReviews)/int(totalReviews)*100

                print('Positive reviews percentage:', str(round(positivePercentage))+"%", 'Not enough reviews to get a rating')
                allReviewScore.insert(1, "No Recent Review")
                allReviewScore.insert(0, "No Recent Review")
                recentRating = 'No Recent Rating'
                rating = 'No Rating'
            elif totalReviews in htmltext4 and recentReviews not in htmltext4:
                    
                rating = htmltext4.split('are positive.">')[1].split('<')[0]
                print('Positive reviews percentage:', allReviewScore[0]+"%", 'Global evaluation:', rating)
                allReviewScore.insert(1, allReviewScore[0])
                allReviewScore.insert(0, 'No Recent Review')
                recentRating = 'No Recent Rating'
            else:
                    
                    
                rating = htmltext4.split('itemprop="description">')[1].split('<')[0]                    
                recentRating = htmltext4.split('<span class="game_review_summary ')[1].split('<')[0]
                recentRating = recentRating.split('">')[1].split('<')[0]

                print('Positive reviews percentage:', allReviewScore[1]+"%", 'Global evaluation:', rating, 'Recent positive reviews percentage:', allReviewScore[0]+'%', 'Recent evaluation', recentRating)
                

        if reviewCheck in htmltext3 and isFree not in htmltext3:
            reviews = htmltext3.split('ions":{"total":')[1].split('}')[0]
            if isOnSale not in htmltext3:
               price = htmltext3.split('"final_formatted":"$')[1].split('"')[0]
            else:
               price = htmltext3.split('"initial_formatted":"$')[1].split('"')[0]
            
            
            cleanprice = price.replace(',','.')
            grossRevenue = int(reviews)*float(cleanprice)*45
            netRevenue = int(grossRevenue)*0.8*0.92*0.8*0.8*0.7
            print('Gross Revenues:',str(round(grossRevenue,2))+"$",'Net Revenues:',str(round(netRevenue,2))+"$")
            print(*tags)

        elif check2 in htmltext3 and isFree not in htmltext3:
            if isOnSale not in htmltext3:
               price = htmltext3.split('"final_formatted":"$')[1].split('"')[0]
            else:
               price = htmltext3.split('"initial_formatted":"$')[1].split('"')[0]
            
            cleanprice = price.replace(',','.')
            url4 = requests.get("https://store.steampowered.com/app/"+appid)

            htmltext4 = url4.text
            newReviews = htmltext4.split('meta itemprop="reviewCount" content="')[1].split('"')[0]
            grossRevenue = int(newReviews)*float(cleanprice)*45
            netRevenue = int(grossRevenue)*0.8*0.92*0.8*0.8*0.7
            print('Gross Revenues:',str(round(grossRevenue,2))+"$",'Net Revenues:',str(round(netRevenue,2))+"$")
            print(*tags)


        else:
            print("no revenue (Free game or unreleased)")
            grossRevenue = 0
            netRevenue = 0
            print(*tags)
        
            

        print(allReviewScore[1])
        temp = pandas.DataFrame(
            {
                'Game Title': Title,
                'Followers': cleanMembers,
                'Low Wishlist Estimation': cleanMembers*5,
                'Average Wishlist Estimation': int(cleanMembers*9.6), 
                'High Wishlist Estimation': cleanMembers*14,
                'Positive reviews percentage': allReviewScore[1]+"%",
                'Global evaluation': rating,
                'Recent positive reviews percentage': allReviewScore[0]+"%",
                'Recent evaluation': recentRating,
                'Price': price,
                'Gross Revenue (in USD)': round(grossRevenue,2),
                'Net Revenue (in USD)': round(netRevenue,2),
                'Release Date': releaseDate,
                'Days Since Release': daysSinceRelease,
                'Current Players': currentPlayers
                

            },
            index=[i]
           
        )
        

        while j < int(len(tags)):
            temp.insert(j, 'Tag'+str(j), tags[j]) 
            
            j +=1





        d = pandas.concat([d, temp])


        
        i += 1
        


        d.to_excel(name+d1+" research.xlsx")

        

elif choice == 2:

    appid = input("Please enter the AppID of the game you'd like to search\n")
    url = requests.get("https://store.steampowered.com/recommended/morelike/app/"+appid)
    htmltext = url.text
    name = htmltext.split(' <h2 class="pageheader">')[1].split('<')[0]
    pattern = '''data-ds-appid="(.[0-9]*)"+ '''
    
    price = 0
    regex = re.findall(pattern, htmltext)

    print("nb result :"+ str(len(regex)))
    for appid in regex:

        j = 0
        try :
            url2 = requests.get("https://steamcommunity.com/games/"+appid)
            htmltext2 = url2.text
        
            Title = htmltext2.split('apphub_AppName ellipsis">')[1].split('<')[0] 
            groupID = htmltext2.split("OpenGroupChat( '")[1].split("'")[0]
        
            print(Title)
        
            membersUrl = requests.get("https://steamcommunity.com/gid/"+groupID+"/memberslistxml/?xml=1")
    
            cleanMembers = int(membersUrl.text.split('<memberCount>')[1].split('<')[0])
        
            print("Followers",cleanMembers,"Low Wishlist Estimation", cleanMembers*5, "Average Wishlist Estimation", int(cleanMembers*9.6), "High Wishlist Estimation", cleanMembers*14 )
        
        

            url3 = requests.get("https://store.steampowered.com/api/appdetails?appids="+appid+"&cc=us&l=en")
        
        

            htmltext3 = url3.text

            releaseDate = htmltext3.split('date":"')[1].split('"')[0]
        except IndexError :
            cleanMembers = 0
            
        try:

            daysSinceRelease = d2 - datetime.strptime(releaseDate, f)
        except ValueError:
            daysSinceRelease = 'Game is unreleased'

        reqPlayers = requests.get("https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid="+appid+"?l=english")
        reqPlayersText = reqPlayers.text

        if 'player' in reqPlayersText:
            currentPlayers = reqPlayersText.split('player_count":')[1].split(',')[0]
        else:
            currentPlayers = 0
        
        reqtag = requests.get("https://store.steampowered.com/app/"+appid+"?l=english")
        agecheck = 'CheckAgeGateSubmit'

        if agecheck in reqtag.text:
            sessionId = reqtag.split('var g_sessionID = "')[1].split('"')[0]
            reqtag = requests.post("https://store.steampowered.com/app/"+appid+"?l=english", data={'number': sessionId, 'ageDay': '1', 'ageMonth': 'January', 'ageYear': '1970'})
            
        tagpattern = '''\/tags\/en\/(.[A-Za-z%\-\d]*)'''
        tags = re.findall(tagpattern, reqtag.text)


        reviewCheck = 'ions":{"total":'
        check2 = 'final_formatted'
        isOnSale = 'initial_formatted":"$'
        isFree = '"is_free":true'
        reviewInApi = 'ions":{"total":'
        reviewCheck = 'user reviews'
        noReview ='data-tooltip-html="No user reviews"'
        notEnoughReviews = 'not_enough_reviews'
        recentReviews = '30 days'
        totalReviews ='aggregateRating'
        reviewTrigger = 'userReviews'
        recentReviewPattern = '''style="cursor: pointer;" data-tooltip-html="(.[0-9]*)'''
        url4 = requests.get("https://store.steampowered.com/app/"+appid+"?l=en")

        htmltext4 = url4.text
        allReviewScore = re.findall(recentReviewPattern, htmltext4)

        if reviewTrigger in htmltext4:
            if noReview in htmltext4 :
                print("This game doesn't have any review")
                allReviewScore.insert(1, "No Recent Review")
                allReviewScore.insert(0, "No Recent Review")
                recentRating = 'No Recent Rating'
                rating = 'No Rating'
            elif notEnoughReviews in htmltext4:
                totalReviews = htmltext4.split('num_reviews" value="')[1].split('"')[0]
                totalPositiveReviews = htmltext4.split('positive_reviews" value="')[1].split('"')[0]
                positivePercentage = int(totalPositiveReviews)/int(totalReviews)*100

                print('Positive reviews percentage:', str(round(positivePercentage))+"%", 'Not enough reviews to get a rating')
                allReviewScore.insert(1, "No Recent Review")
                allReviewScore.insert(0, "No Recent Review")
                recentRating = 'No Recent Rating'
                rating = 'No Rating'
            elif totalReviews in htmltext4 and recentReviews not in htmltext4:
                    
                rating = htmltext4.split('are positive.">')[1].split('<')[0]
                print('Positive reviews percentage:', allReviewScore[0]+"%", 'Global evaluation:', rating)
                allReviewScore.insert(1, allReviewScore[0])
                allReviewScore.insert(0, 'No Recent Review')
                recentRating = 'No Recent Rating'
            else:
                    
                    
                rating = htmltext4.split('itemprop="description">')[1].split('<')[0]                    
                recentRating = htmltext4.split('<span class="game_review_summary ')[1].split('<')[0]
                recentRating = recentRating.split('">')[1].split('<')[0]

                print('Positive reviews percentage:', allReviewScore[1]+"%", 'Global evaluation:', rating, 'Recent positive reviews percentage:', allReviewScore[0]+'%', 'Recent evaluation', recentRating)
                

        if reviewCheck in htmltext3 and isFree not in htmltext3:
            reviews = htmltext3.split('ions":{"total":')[1].split('}')[0]
            if isOnSale not in htmltext3:
               price = htmltext3.split('"final_formatted":"$')[1].split('"')[0]
            else:
               price = htmltext3.split('"initial_formatted":"$')[1].split('"')[0]
            
            
            cleanprice = price.replace(',','.')
            grossRevenue = int(reviews)*float(cleanprice)*45
            netRevenue = int(grossRevenue)*0.8*0.92*0.8*0.8*0.7
            print('Gross Revenues:',str(round(grossRevenue,2))+"$",'Net Revenues:',str(round(netRevenue,2))+"$")
            print(*tags)

        elif check2 in htmltext3 and isFree not in htmltext3:
            if isOnSale not in htmltext3:
               price = htmltext3.split('"final_formatted":"$')[1].split('"')[0]
            else:
               price = htmltext3.split('"initial_formatted":"$')[1].split('"')[0]
            
            cleanprice = price.replace(',','.')
            url4 = requests.get("https://store.steampowered.com/app/"+appid)

            htmltext4 = url4.text
            newReviews = htmltext4.split('meta itemprop="reviewCount" content="')[1].split('"')[0]
            grossRevenue = int(newReviews)*float(cleanprice)*45
            netRevenue = int(grossRevenue)*0.8*0.92*0.8*0.8*0.7
            print('Gross Revenues:',str(round(grossRevenue,2))+"$",'Net Revenues:',str(round(netRevenue,2))+"$")
            print(*tags)


        else:
            print("no revenue (Free game or unreleased)")
            grossRevenue = 0
            netRevenue = 0
            print(*tags)
        
            

        print(allReviewScore[1])
        temp = pandas.DataFrame(
            {
                'Game Title': Title,
                'Followers': cleanMembers,
                'Low Wishlist Estimation': cleanMembers*5,
                'Average Wishlist Estimation': int(cleanMembers*9.6), 
                'High Wishlist Estimation': cleanMembers*14,
                'Positive reviews percentage': allReviewScore[1]+"%",
                'Global evaluation': rating,
                'Recent positive reviews percentage': allReviewScore[0]+"%",
                'Recent evaluation': recentRating,
                'Price': price,
                'Gross Revenue (in USD)': round(grossRevenue,2),
                'Net Revenue (in USD)': round(netRevenue,2),
                'Release Date': releaseDate,
                'Days Since Release': daysSinceRelease,
                'Current Players': currentPlayers
                

            },
            index=[i]
           
        )
        

        while j < int(len(tags)):
            temp.insert(j, 'Tag'+str(j), tags[j]) 
            
            j +=1





        d = pandas.concat([d, temp])


        
        i += 1
        


        d.to_excel(name+d1+" research.xlsx")
            



else:
    print("This isn't a valid choice")
