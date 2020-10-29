import tweepy
import account

screen_id = "netatank"
user = account.Account(screen_id)
print(user.existsAccount())
