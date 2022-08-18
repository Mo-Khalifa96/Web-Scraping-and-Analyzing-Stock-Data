#WEB SCRAPING AND ANALYZING STOCK DATA 


#Importing the modules to be used 
import requests 
import yfinance as yf 
import pandas as pd 
from bs4 import BeautifulSoup
import plotly.graph_objects as go 
from plotly.subplots import make_subplots



#Part One: Using yfinance to Extract Stock Data 
#For this part, I will use the yfinance module to extract Tesla's and GameStop's stock data from Yahoo Finance. 
#I will specify the interval of time to preview the stock data across as 'max' which will provide the stock data 
#dated since 2009.  

#First, extracting Tesla's stock data from Yahoo Finance  
#Creating a Ticker object for Tesla's data 
tesla = yf.Ticker('TSLA')

#extracting Tesla's stock data (dated since the beginning)
tesla_data = tesla.history(period='max')

#resetting the index (and retrieving dates as a coloumn, 'Date')
tesla_data.reset_index(inplace=True)

#to preview the first 5 enteries of Tesla's stock data
tesla_data.head()


#Now extracting GameStop's stock data 
#Creating a ticker object for GameStop's data 
gme = yf.Ticker('GME')

#extracting GameStop's stock data
gme_data = gme.history(period='max')

#resetting the index (and retrieving dates)
gme_data.reset_index(inplace=True)

#to preview the first 5 enteries of Gamestop's stock data
gme_data.head()



#Part Two: Web Scraping Tesla's and Gamestop's Revenue Data 
#In this section, I will use the Python libraries, requests, pandas, and beautiful soup to scrape Tesla's and 
#GameStop's historical revenue data

#First, retrieving Tesla's historical revenue data 
#specifying the web page to scrape the data from
tesla_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

#making a get request to extract the html document
tesla_html_data = requests.get(tesla_url).text

#creating a beautiful soup object to parse html document
tesla_soup = BeautifulSoup(tesla_html_data)


#Two methods to retrieve the revenue data:
#i. Using Python's pandas library:
#The first technique involves using pandas read_html() method to specify the html document and name of the table 
#in order to scrape the revenue table in one step.

#Extracting revenue table 'Tesla Quarterly Revenue'
#Extracting revenue table 'Tesla Quarterly Revenue'
table_list = pd.read_html(tesla_html_data,    #specifying the html document
                          match='Tesla Quarterly Revenue',    #specifying the table to look for
                          flavor='bs4')     #specifying the parsing engine

#Converting the revenue table into a dataframe
tesla_revenue = table_list[0]

#Renaming the dataframe coloumns appropriately
tesla_revenue.rename(columns={'Tesla Quarterly Revenue(Millions of US $)': 'Date', 'Tesla Quarterly Revenue(Millions of US $).1': 'Revenue'}, inplace=True)

#Displaying the dataframe
tesla_revenue


#ii. Using Python's Beautiful Soup library:
#Alternatively, we can use beautiful soup to parse the html document and extract the table, 
#before assigning the data into a pandas dataframe 

#First, creating an empty dataframe with the necessary coloumns
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

#extracting the table using its tag name ('tbody') and index
tesla_revenue_table = tesla_soup.find_all('tbody')[1]

#looping through the table rows and extracting the data
for row in tesla_revenue_table.find_all('tr'):
    #accessing the coloumns along row
    col = row.find_all('td')
    date = col[0].text
    revenue = col[1].text

    #appending date and revenue to dataframe, 'tesla_revenue'
    tesla_revenue = tesla_revenue.append({'Date': date, 'Revenue': revenue}, ignore_index=True)

#displaying the dataframe
tesla_revenue


#Now retrieving Gamestop's revenue data 
#specifying the url to GameStop's revenue data 
gme_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

#extracting html document 
gme_html_data = requests.get(gme_url).text

#creating a beautiful soup object for parsing the document
gme_soup = BeautifulSoup(gme_html_data)


#Again, we could parse and extract the revenue data in two ways:
#i. Using Python's pandas library:
#Extracting revenue table 'GameStop Quarterly Revenue'
table_list = pd.read_html(gme_html_data,  # specifying the html document
                          match='GameStop Quarterly Revenue',  # specifying the table to look for
                          flavor='bs4')  # specifying the parse engine

#converting the revenue table into a dataframe
gme_revenue = table_list[0]

#renaming the dataframe coloumns appropriately
gme_revenue.rename(columns={'GameStop Quarterly Revenue(Millions of US $)': 'Date', 'GameStop Quarterly Revenue(Millions of US $).1': 'Revenue'}, inplace=True)

#displaying the dataframe
gme_revenue


#ii. Using Python's Beautiful Soup library:

#first, creating an empty dataframe with the necessary coloumns
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

#extracting the table using its tag name ('tbody') and index
gme_revenue_table = gme_soup.find_all('tbody')[1]

#looping through the table rows and extracting the data
for row in gme_revenue_table.find_all('tr'):
    #accessing the coloumns along row
    col = row.find_all('td')
    date = col[0].text
    revenue = col[1].text

    #appending date and revenue to dataframe, gme_revenue
    gme_revenue = gme_revenue.append({'Date': date, 'Revenue': revenue}, ignore_index=True)

#displaying the dataframe
gme_revenue



#Part Three: Cleaning Up the Data 
#Having extracted the revenue data for Tesla and GameStop, it seems that some enteries are 
#missing or include inappropriate or non-numerical characters (as in the Revenue coloumn).
#As such, it's time to clean up and prepare the data for analysis.

#First, cleaning up Tesla's revenue data 
#removing the non-numeric/special characters from 'Revenue' coloumn 
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$', "")

#second, removing Nan (not a number) and empty enteries 
tesla_revenue.dropna(inplace=True)
true_revenues = tesla_revenue['Revenue'] != "" 
tesla_revenue = tesla_revenue[true_revenues]

#previewing the dataframe 
tesla_revenue.head()


#Now cleaning up GameStop's data 
#first, removing special characters from 'Revenue' coloumn 
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$', "")

#second, removing Nan (not a number) and empty enteries 
gme_revenue.dropna(inplace=True)
true_revenues = gme_revenue['Revenue'] != "" 
gme_revenue = gme_revenue[true_revenues]

#previewing the dataframe 
gme_revenue.head()



#Part Four: Visualizing Tesla and GameStop's Stock Data 
#For this section, I'll use plotly, a powerful graphing library, to create an interactive dashboard with the 
#stocks and revenue data that were extracted for each of Tesla and GameStop. The data for each company will 
#be plotted separately.  

#To do so, first, I'll define a function for visualization the data on a subplot. The subplot will consist 
#of two scatter plots, the first displaying a company's historical share prices (above), whilst the second 
#displaying a company's historical revenue (below), and both are separated by a range slider that allows 
#the user to navigate freely and zero-in on any particular segment of data within a particular range of time. 


#First, defining the graph function for visualizing the data
def make_graph(stock_data, revenue_data, stock):
    """This function takes a dataframe with the stock data (must include Date and Close prices), 
    a dataframe with the revenue data (must include Date and Revenue amounts), and the name of 
    the stock, and plots the historical share price and revenue data on a subplot comprised of  
    two scatter plot graphs, one for each."""

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data
    revenue_data_specific = revenue_data
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


#Now, visualizing Tesla's stock and revenue data 
#Executing the make_graph() function to plot GameStop's historical data
make_graph(tesla_data, tesla_revenue, 'Tesla Stock Data')


#Visualizing GameStop's stock and revenue data 
#Again, executing the make_graph() function to plot GameStop's historical data
make_graph(gme_data, gme_revenue, 'GameStop Stock Data')


#END
