import plotly.graph_objects as go
import requests
def postsanalytics(insta_id,access_token):
    url= "https://graph.facebook.com/v18.0/"+str(insta_id)+"/media?fields=id%2Cmedia_url%2Ccaption%2Ctimestamp%2Cinsights.metric(reach%2Cimpressions%2Cengagement%2Cvideo_views)&access_token="+access_token

    json_data=requests.get(url).json()


    timestamps = []
    reach_values = []
    impressions_values = []
    engagement_values = []
    video_views_values = []

    # Extract data from JSON
    for post in json_data["data"]:
        timestamps.append(post["timestamp"])
        insights_data = post["insights"]["data"]
        for insight in insights_data:
            if insight["name"] == "reach":
                reach_values.append(insight["values"][0]["value"])
            elif insight["name"] == "impressions":
                impressions_values.append(insight["values"][0]["value"])
            elif insight["name"] == "engagement":
                engagement_values.append(insight["values"][0]["value"])
            elif insight["name"] == "video_views":
                video_views_values.append(insight["values"][0]["value"])

    # Create bar graph using Plotly
    fig = go.Figure()

    fig.add_trace(go.Bar(x=timestamps, y=reach_values, name='Reach'))
    fig.add_trace(go.Bar(x=timestamps, y=impressions_values, name='Impressions'))
    fig.add_trace(go.Bar(x=timestamps, y=engagement_values, name='Engagement'))
    fig.add_trace(go.Bar(x=timestamps, y=video_views_values, name='Video Views'))

    fig.update_layout(barmode='group', title='Post Insights on Specific Date')
    fig.show()
    return json_data,fig


import datetime

def account(insta_id,access_token):
        data_metrics={}

        today = datetime.datetime.now().date()

        # Create a list to store the timestamps
        timestamps = []

        # Loop through the last 30 days
        for i in range(31):
            # Calculate the date i days ago
            date = today - datetime.timedelta(days=i)
            # Convert the date to a Unix timestamp
            timestamp = int(datetime.datetime(date.year, date.month, date.day).timestamp())
            # Append the timestamp to the list
            timestamps.append(timestamp)

        for i in range(30):
            # print(timestamps[i]," : ",timestamps[i+1])
            
            url= "https://graph.facebook.com/v18.0/"+str(insta_id)+"/insights?pretty=0&since="+str(timestamps[i+1])+"&until="+str(timestamps[i])+"&metric=profile_views,reach,impressions,website_clicks&period=day&access_token="+access_token
            
            
            data = requests.get(url).json()
            # print(data)
            # print(access_token)
            

            date=data['data'][0]['values'][0]['end_time'].split("T")[0]
            metrics={}

            for metric in data['data']:
                name=metric['name']
                value=metric['values'][0]['value']
                # print(name," : ",value)
                metrics[name]=value
                

            data_metrics[date]=metrics
            
        dates = list(data_metrics.keys())

        # Extract values for each metric
        profile_views = [entry['profile_views'] for entry in data_metrics.values()]
        reach = [entry['reach'] for entry in data_metrics.values()]
        impressions = [entry['impressions'] for entry in data_metrics.values()]
        website_clicks = [entry['website_clicks'] for entry in data_metrics.values()]

        # Create line plots for each metric
        trace_profile_views = go.Scatter(x=dates, y=profile_views, mode='lines+markers', name='Profile Views', line_shape='spline')
        trace_reach = go.Scatter(x=dates, y=reach, mode='lines+markers', name='Reach', line_shape='spline')
        trace_impressions = go.Scatter(x=dates, y=impressions, mode='lines+markers', name='Impressions', line_shape='spline')
        trace_website_clicks = go.Scatter(x=dates, y=website_clicks, mode='lines+markers', name='website_clicks', line_shape='spline')

        # Create layout for the graph
        layout = go.Layout(
            title='Metrics Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Value')
        )

        # Combine line plots into a single graph
        fig = go.Figure(data=[trace_profile_views, trace_reach, trace_impressions,trace_website_clicks], layout=layout)

        # Show the graph
        return data_metrics,fig        
        


# insights
    
    
    
def country_func(insta_id,access_token):
    url = "https://graph.facebook.com/v18.0/{}/insights?metric=follower_demographics&period=lifetime&metric_type=total_value&breakdown=country&access_token={}".format(insta_id, access_token)
    country=requests.get(url).json()
    country_data={}


    for cou in country['data'][0]['total_value']['breakdowns'][0]['results']:
        country_data[cou['dimension_values'][0]]=cou['value']
        




    country_data = dict(sorted(country_data.items(), key=lambda item: item[1], reverse=True))

    plotting_data=dict(list(country_data.items())[:7])
    plotting_data['Others']=sum(dict(list(country_data.items())[7:]).values())

    plotting_data
    labels = [key for key in plotting_data.keys()]
    values = [value for value in plotting_data.values()]

    colors = ['darkorange','gold', 'lightgreen','mediumturquoise']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(    title_text="Country distribution",)

    
    
    return country_data,fig






import plotly.express as px
def age_func(insta_id, access_token):

  # Endpoint URL with age breakdown
  url = "https://graph.facebook.com/v18.0/{}/insights?metric=follower_demographics&period=lifetime&metric_type=total_value&breakdown=age&access_token={}".format(insta_id, access_token)

  # Fetch data using requests library
  response = requests.get(url).json()

  # Initialize empty dictionary for age data
  age_data = {}

  # Check if data is available
  if 'data' in response and len(response['data']) > 0:
    # Parse data for breakdowns
    for age_range in response['data'][0]['total_value']['breakdowns'][0]['results']:
      age_group = age_range['dimension_values'][0]
      age_count = age_range['value']
      age_data[age_group] = age_count
      

  # Your data as a dictionary

  # Extract data for the chart
  age_groups = list(age_data.keys())  # Get age group labels
  follower_counts = list(age_data.values())  # Get follower counts

  # Create a bar chart
  bar_chart = px.bar(x=age_groups, y=follower_counts, text_auto='.2s',
             title="Follower Distribution by Age Group")
  bar_chart.update_traces(textfont_size=12, textangle=0,width=.3, textposition="outside", cliponaxis=False)


  return age_data,bar_chart




def city_func(insta_id, access_token):
  """
  Fetches follower city demographics for an Instagram Business Account.

  Args:
      insta_id: The ID of the Instagram Business Account.
      access_token: A valid access token for the Facebook Graph API.

  Returns:
      A dictionary containing city names as keys and corresponding follower counts as values.
      If data is unavailable, returns an empty dictionary.
  """

  # Endpoint URL with city breakdown
  url = "https://graph.facebook.com/v18.0/{}/insights?metric=follower_demographics&period=lifetime&metric_type=total_value&breakdown=city&access_token={}".format(insta_id, access_token)

  # Fetch data using requests library
  response = requests.get(url).json()

  # Initialize empty dictionary for city data
  city_data = {}

  # Check if data is available
  if 'data' in response and len(response['data']) > 0:
    # Parse data for breakdowns
    for city in response['data'][0]['total_value']['breakdowns'][0]['results']:
      city_name = city['dimension_values'][0]
      city_count = city['value']
      city_data[city_name] = city_count
      
  city_data = dict(sorted(city_data.items(), key=lambda item: item[1], reverse=True))
  
  plotting_data=dict(list(city_data.items())[:7])
  plotting_data['Others']=sum(dict(list(city_data.items())[7:]).values())
  
  labels = [key for key in plotting_data.keys()]
  values = [value for value in plotting_data.values()]
  
  colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        
  fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
  fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
  fig.update_layout(    title_text="City distribution",)
  

  return city_data,fig




import plotly.graph_objects as go

def gender_func(insta_id,access_token):
    gender= "https://graph.facebook.com/v18.0/{}/insights?metric=follower_demographics&period=lifetime&metric_type=total_value&breakdown=gender&access_token={}".format(insta_id,access_token)
    
    gen_data=requests.get(gender).json()
    gender_data={}
    
    
    for gen in gen_data['data'][0]['total_value']['breakdowns'][0]['results']:
        gender_data[gen['dimension_values'][0]]=gen['value']
        
    labels = [key for key in gender_data.keys()]
    values = [value for value in gender_data.values()]
        
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
    fig.update_layout(    title_text="Gender distribution",)

        
    return gender_data,fig

    



def postsanalytics(insta_id,access_token):
    url= "https://graph.facebook.com/v18.0/"+str(insta_id)+"/media?fields=id%2Cmedia_url%2Ccaption%2Ctimestamp%2Cinsights.metric(reach%2Cimpressions%2Cengagement%2Cvideo_views)&access_token="+access_token

    json_data=requests.get(url).json()


    timestamps = []
    reach_values = []
    impressions_values = []
    engagement_values = []
    video_views_values = []

    # Extract data from JSON
    for post in json_data["data"]:
        timestamps.append(post["timestamp"])
        insights_data = post["insights"]["data"]
        for insight in insights_data:
            if insight["name"] == "reach":
                reach_values.append(insight["values"][0]["value"])
            elif insight["name"] == "impressions":
                impressions_values.append(insight["values"][0]["value"])
            elif insight["name"] == "engagement":
                engagement_values.append(insight["values"][0]["value"])
            elif insight["name"] == "video_views":
                video_views_values.append(insight["values"][0]["value"])

    # Create bar graph using Plotly
    fig = go.Figure()

    fig.add_trace(go.Bar(x=timestamps, y=reach_values, name='Reach'))
    fig.add_trace(go.Bar(x=timestamps, y=impressions_values, name='Impressions'))
    fig.add_trace(go.Bar(x=timestamps, y=engagement_values, name='Engagement'))
    fig.add_trace(go.Bar(x=timestamps, y=video_views_values, name='Video Views'))

    fig.update_layout(barmode='group', title='Post Insights on Specific Date')
    return json_data,fig



def posts_url(insta_id,access_token):
    
    url= "https://graph.facebook.com/v18.0/"+str(insta_id)+"/media?fields=id%2Cmedia_type,media_url%2Ccaption%2Ctimestamp%2Cchildren.fields(media_url%2Cmedia_type%20)&access_token="+access_token

    data=requests.get(url).json()   
    images=[]
    videos=[]
        

    for post in data['data']:
        # Add main post media URL
        if post['media_type']=="IMAGE":
            images.append(post['media_url'])
        if post['media_type']=='VIDEO':
            videos.append(post['media_url'])

        # Check if the post has children (carousel)
        if 'children' in post:
            children_data = post['children']['data']
            # Add media URLs of children
            for child in children_data:
                
                if child['media_type']=="IMAGE":
                    images.append(child['media_url'])
                if child['media_type']=='VIDEO':
                    videos.append(child['media_url'])

    return images,videos


import google.generativeai as genai
genai.configure(api_key = 'AIzaSyC0O4dCvtLxrXg3BMBciSzrXhO3Vkb5Irw')
model = genai.GenerativeModel('gemini-pro')

def comment_analysis(insta_id,access_token):
    
    url= "https://graph.facebook.com/v18.0/"+str(insta_id)+"/media?access_token="+access_token

    dir={}

    data=requests.get(url).json()

    for id in data['data']:
        
        comments={}
        
        url= "https://graph.facebook.com/v18.0/"+str(id['id'])+"/comments?access_token="+access_token
        
        comdata=requests.get(url).json()
        comm=[]
        for comment in comdata['data']:
            comm.append(comment['text'])
            
        comments["comments"]=(comm)
            
        dir[id['id']]=[comments]

        res={}
        res['response'] = (model.generate_content("over all positive,negative or neutral? "+str(comments))).text
        dir[id['id']]+=[res]
        
            
        
    return(dir)




def media_urls(insta_id,access_token):
    url="https://graph.facebook.com/v18.0/"+str(insta_id)+"/media?fields=media_url&access_token="+access_token
    
    media=requests.get(url).json()
    media_url={}

    for url in media['data']:
        media_url[url['id']]=(url['media_url'])

    return media_url




def get_comments(post_id,access_token):
    url= "https://graph.facebook.com/v18.0/"+str(post_id)+"/comments?fields=id%2Ctext%2Cusername%2Creplies%7Busername%2Ctext%7D&origin_graph_explorer=1&transport=cors&access_token="+access_token

    comments_data=requests.get(url).json()['data']
    comments_list = []
    # print(comments_data)
    for comment in comments_data:
        comment_dict = {"id": comment["id"], "comment": comment["text"]}
        comments_list.append(comment_dict)
        if "replies" in comment:
            for reply in comment["replies"]["data"]:
                reply_dict = {"id": reply["id"], "comment": reply["text"]}
                comments_list.append(reply_dict)

    # print(comments_list)
    return comments_list



def generate_reply(comm_id,access_token):
    url= "https://graph.facebook.com/v18.0/"+str(comm_id)+"?fields=id%2Ctext&access_token="+access_token

    data=requests.get(url).json()
    
    comments_replies = model.generate_content(str(data)+"understand the comment and create reply in the language and slang used and return a string response  (provide the replies in the same language or slang used in the comment )")
    
    return comments_replies


