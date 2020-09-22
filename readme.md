## Learn More
Learn more about how this works by visiting my blog post: [Someone Stole My DEV Article! How To Build a Python Script to Detect Stolen Content]()

## How to Use
Set up a local config.py file and add your Dev.to API key, google API key and serahc engine ID, following this format:

```
GOOGLE_API_KEY = "< Enter key here >"

SEARCH_ENGINE_ID = "< Enter ID here >"

DEV_API_KEY = "< Enter key here >"
```

To run the script, enter the following into the command line:
`python search.py`

Next, manually open any links that look like they may include stolen content.

# Someone Stole My DEV Article! How To Build a Python Script to Detect Stolen Content
(originally posted on Dev.to at the link above)

Last spring, [one of my blog posts](https://dev.to/jessesbyers/react-and-d3-dynamic-covid-19-visualizations-part-2-country-comparison-dashboard-f9n) got a lot of views and likes, and was ultimately featured on the Top 7 List for that week. As a new blogger, I wanted to figure out what had made it so popular, so I could build on that success. However, in the process of investigation I stumbled upon my own writing...IN SOMEONE ELSE'S BLOG!!! And then I also stumbled upon their 12 Twitter accounts which were all tweeting out my content, AND TAKING CREDIT FOR IT AS THEIR OWN WORK!!! The wonderful folks at DEV helped me out and sent out a request to have the stolen content removed ...but ever since, I've been nervous about posting, fearing this might happen again.

Fast forward a few months, and my job involves the task of building a Python script to search for web content that could be used for cheating. I immediately realized a similar script could be used to monitor the web to detect any unauthorized scraping and re-posting of DEV posts. I had also recently read @saschat's post, [Get Historical Stats for your Dev.to Articles](https://dev.to/saschat/get-historical-stats-for-your-dev-to-articles-2efn), which uses the Dev.to API to fetch data on each of your articles. So I got to work, building a script that leverages both the Dev.to API to fetch my article data, as well as the Google Custom Search Engine API to manage the custom searches. 

Below, I'll share my process and my code. I hope you'll follow along and build your own script, using Python, the Dev.to API, and the Google Custom Search Engine API. This tutorial assumes some basic knowledge of Python fundamentals, and general familiarity with fetching data from external APIs.

# Build a Python Script to Check if Anyone Has Stolen Your DEV Posts

## Initial Set-Up
### Create Project Folder and Repository
First, you'll need to create a project folder, create a few placeholder files, initialize your repository and push it to GitHub.
![Imgur](https://i.imgur.com/yVVbq77.png)

We will organize our dependencies in the `requirements.txt` file. In this project, we will start by installing the `requests` package (for requesting data from the APIs) and `colorama` package (for formatting text printed to the terminal). Add these names to the file, and run `pip3 install -r requirements.txt` to install all of the dependencies at once.
![Imgur](https://i.imgur.com/wy85cpa.png)

## Set up the Google Custom Search Engine API
![Imgur](https://i.imgur.com/dJSd7SN.png)
In order to use this API to manage your custom searches, you will need to have a google account. Follow the link on the [Google Custom Search JSON API Documentation](https://developers.google.com/custom-search/v1/overview) to set up an API key for your project, and jot it down. Then click on the [Google Programmable Search Control Panel](https://programmablesearchengine.google.com/cse/all) link to set up your custom search and generate your Search Engine ID. You will need to choose at least one website domain to include in your search, so for now, just set it to `dev.to/*`, and any other sites where your articles *should* be showing up in a web search. Since I post my articles to Twitter (and occasionally to LinkedIn and GitHub), I added those domains as well. This will get us started for testing the script, and we can add/refine the custom search parameters once we are confident the script works.
![Imgur](https://i.imgur.com/slCBwff.png)

After you press "Create", follow the link to your Control Panel to finish setting up the search and to get your Search Engine ID. Save the Search Engine ID for later, and keep the Control Panel open, as we'll modify the settings later on.

## Set up the Dev.to API
Next, you will need to get your API key for the Dev.to API. In order to do this, go to your DEV settings page, click on Account, and scroll to the DEV API keys section. Just add a project title, and it will generate a new key. Jot down this key as well. For more details, visit the [Documentation for the DEV API](https://docs.forem.com/api/).
![Imgur](https://i.imgur.com/8J15qkV.png)

### Save API keys and Search Engine ID to config.py
First, make sure you have added the `config.py` file to your `.gitignore` file to prevent it from being tracked by GitHub. Next, add all of the keys and IDs you just generated to the `config.py` file, to keep them secure. 

When you're finished, the file should look like this, with each key/ID stored as a string.
![Imgur](https://i.imgur.com/XkZfV3t.png)

*If you need a resource on securing API keys, I recommend BlackTechDiva's article [Hide Your API Keys](http://www.blacktechdiva.com/hide-api-keys/) for a clear and concise tutorial.*

## Fetch Article Data from the Dev.to API
Now we're ready to start putting those API keys to work! First, we'll make a fetch to the Dev.to API to retrieve all of our articles published on DEV, and then use the response data to create a list of article titles, which we will be able to  use in our custom search.

![Imgur](https://i.imgur.com/t45q33q.png)

In the `search.py` file, we will need to `import requests`, which will allow us to request the data from the Dev.to API. We will also `import config` so that we can access our API key which is locally stored in that file. 

Our request will return our article data in this format:
![Imgur](https://i.imgur.com/DZgUbO8.png)

By looping through the data object, we then create a list of titles of all published articles (article_list) by accessing `article["title"]`. We can also create a list of recent_articles, so that we can conduct searches on a sub-set of the ten most recent articles (recent_articles):
![Imgur](https://i.imgur.com/fEtcfTd.png)

## Build a General Search Script 
Once we have a list of articles, we are ready to set up a general search script which will use each article title as a search term, and will print out the top 10 google hits (based on the settings in our Custom Search Engine) to the terminal. 

![Imgur](https://i.imgur.com/siKmrG7.png)
First, we will import and initiate colorama, which will allow us to add color formatting to our search results when they print out to the terminal. The argument `autoreset=True` will set the color back to the default after each line.

![Imgur](https://i.imgur.com/6XoNo65.png)
Next, we will set up our search logic. We will need to iterate through the list of recent articles, and make a request to the Google Custom Search API for each title. The response for each article title search will be a large dictionary, and the hits will be housed inside the "items" key. We can set the hits variable to include the top 10 hits by indexing the results.

Next, we can iterate through the hits list to set up our logic for printing results to the terminal. By adding the `try:` and `except:` logic, we can avoid throwing errors when a search term fails to get hits.

*Note: So far in this example, I have limited the recent_articles list to 10 articles, and the hits list to 10 hits. This is based on the API's daily query limits, which allow for 100 queries per day. Feel free to adjust these numbers, but be mindful of the daily limit as you make your choices. More information about the daily limit can be found in the [documentation](https://developers.google.com/custom-search/v1/overview#pricing).*

When we run the script at this point, we will get a printout of the top 10 hits for each of the 10 article titles, from any of the domains that we identified in our Google Custom Search Control Panel during an earlier step. In my example, my printout shows links to my articles on Dev.to, Twitter, LinkedIn and Github. For example: 
![Imgur](https://i.imgur.com/UIjx1h3.png)

## Putting it All Together
At this point, we have a script that works to detect our recent posts *on the sites where we want and would expect to see the posts*. However, if the ultimate goal is to search the web for stolen blog content, we will need to alter our settings in the Google Custom Search Engine Control Panel. Click on Setup, and then Advanced. You can now revise your previous settings, add domains that you would like to EXCLUDE from your search. After some manual testing, I ended up revising my settings to look like this, so that I would be searching the entire web, but excluding my own content shared via my own accounts:

![Imgur](https://i.imgur.com/OTeUJcT.png)

Here is an example of the new search output, which highlights some additional places where my article titles are showing up on the web:

![Imgur](https://i.imgur.com/mbKILZT.png)

While the first two are harmless shares or re-posts, the third one is concerning, as that matches the twitter handles and blog address of the original stolen content.

## Final Thoughts
It definitely takes some trial and error to refine the Google Programmable Search settings in your control panel - you need to find the sweet spot between *excluding* your own posts and shares, and *including* other domains and other people's references to your work. You'll then have to manually skim through the output of the search. Most of your hits will be harmless, like the first two above - people (or bots) who find and like your work will share it! But you may also detect sites that have scraped your writing and re-posted it without attributing it to you, and those are the sites that should be reported, with a request to remove the stolen content. 

## Try This!
After you finish your script, there are a number of modifications and refinements you can make to make it even better:
- Play around with search terms: Maybe try searching for a snippet of your blog content rather than just the title.
- Refine the settings in the Control Panel: What settings give you the most relevant number of hits?
- Change the numbers in the script: Do you want to see the more hits, for a fewer number of posts? Just fiddle around with how your index your lists.
- Create a Script to search for different content: What else could you use a Google Custom Search for?

## Check out the Repository
Thanks for reading! If you'd like to check out my repo, you can check it out [here](https://github.com/jessesbyers/dev_article_search).

## Resources
Since this whole article is focused on protecting intellectual property, it's important to give credit where credit is due! I used the following resources to help put together this project:
- [How to Use Google Custom Search Engine API in Python](https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python) - a tutorial that helped me put together the basics for integrating the Google API into a Python script.
- [Tutorial GitHub repo](https://github.com/x4nth055/pythoncode-tutorials/tree/master/general/using-custom-search-engine-api) - The source code from the above tutorial
- [Google Custom Search JSON API Documentation](https://developers.google.com/custom-search/v1/overview) - includes details on obtaining an API key and usage limits.
- [Google Programmable Search Control Panel](https://programmablesearchengine.google.com/cse/all) - where you will create/edit/manage your search domains through your google account
- [Get Historical Stats for your Dev.to Articles](https://dev.to/saschat/get-historical-stats-for-your-dev-to-articles-2efn) - for inspiration and information on accessing the DEV API for article data.
- [Documentation for the DEV API](https://docs.forem.com/api/) - covers authentication and endpoints for accessing data on DEV articles.
- [Hide Your API Keys](http://www.blacktechdiva.com/hide-api-keys/) - clear and concise summary of how to secure your API keys in a python project.

