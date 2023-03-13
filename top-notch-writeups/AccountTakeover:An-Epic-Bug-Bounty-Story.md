# Account Takeover: An Epic Bug Bounty Story
[Link for the writeup](https://medium.com/bugbountywriteup/account-takeover-an-epic-bug-bounty-story-dd5468d5773d)


Hello Folks! I am back after a long time with an interesting (pre) Account Takeover bug and how I chained this with XSS. You might get confused as this is a long writeup, but don’t worry, stick it till the end; I’ve simplified the things at the end for better understanding.

In this blog, I am going to share my interesting Pre - Account Takeover story that happened due to the Broken Access Control and How I managed to make this a valid issue.<br>
I was hunting on an old private bug bounty program. I knew in my mind that I needed to find a unique issue to avoid duplicates. As usual, fired up my burp and randomly started to browse the target. 
I came across a profile section of the site. There was an option to edit only Names and Passwords and not Emails.
<br>
<br>
I noticed and started playing with UserAttributes. First, I changed the name to update_email and the value to an existing account’s mail. <br>
I got an error — <br>
{<br>
“__type”:”InvalidParameterException”,<br>
”message”:”user.update_email: Attribute does not exist in the schema.\n”<br>
}<br>
<br>
<br>
<br>
Again, I changed the name to change_email and sent the request, but I got the same error — <br>
{<br>
“__type”:”InvalidParameterException”,<br>
”message”:”user.change_email: Attribute does not exist in the schema.\n”<br>
}<br>
Then I went back to the signup flow request and observed that the application was sending a new email address in the Username attribute while signing up.<br>
I changed the name to Username but got the same error again -<br>
{<br>
“__type”:”InvalidParameterException”,<br>
”message”:”user.Username: Attribute does not exist in the schema.\n”<br>
}<br>
I was about to give up, but as a last try, I sent a request again with only an email, and I got a new error!<br>
<br>
<br>
I switched my focus to Pre — Account Takeover as this error confirmed that I can’t takeover another user’s account. I changed the email address to an unregistered email, and It worked.<br>
<br>
I received verification OTP on a new email. However, I was able to successfully change the email address to a new one without undergoing the verification process and got an account without any verification.<br>
<br>
Wow! I got too excited, made a report and submitted it :)<br>
Within some hours, they changed it to Not Applicable and sent me this reply:<br>

