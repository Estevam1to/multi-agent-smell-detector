# This bot unfollows users who don't follow you back on instagram
# This bot was made by DocKaz with the use of github copilot

# Importing the libraries
from instapy import InstaPy
from instapy import smart_run

# Logging in
insta_username = 'your_username'
insta_password = 'your_password'

# Setting up the bot
session = InstaPy(username=insta_username,
                  password=insta_password, headless_browser=True)
with smart_run(session):
    # Unfollow non followers
    session.set_dont_unfollow_active_users(enabled=True, posts=1)
    session.set_quota_supervisor(enabled=True,
                                 sleep_after=["unfollows", "server_calls"],
                                 sleepyhead=True,
                                 stochastic_flow=True,
                                 notify_me=True,
                                 peak_unfollows_hourly=20,
                                 peak_unfollows_daily=250,
                                 peak_server_calls_hourly=200,
                                 peak_server_calls_daily=2500)
    session.unfollow_users(amount=250, nonFollowers=True,
                           style="FIFO", unfollow_after=24*60*60, sleep_delay=600)

# DM me @CannaKaz on twitter if you have any questions
