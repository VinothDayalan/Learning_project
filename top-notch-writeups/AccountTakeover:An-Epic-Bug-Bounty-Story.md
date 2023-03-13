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

After receiving this response, I returned to the application and tried to login with the victim's mail (Cyborj27+9@gmail.com) and the attacker’s password and got an error — “username or password is incorrect”

Then, I tried resetting the password to see if it sent any OTP. 
But got a new error — “The password could not be reset, since the email is not registered or verified.”

I made notes of all the errors I got and went to sleep. The next day I started again from the beginning but found nothing new. Again opened my notes and read them 2–3 times. After reading this error — “The password could not be reset, since the email is not registered or verified.” 
I decided to try to register with the victim’s email. When I registered, the application threw a new error — “ Your account is temporarily not available. Please try to log in in 15 minutes.”

After 15 mins, I tried to login with the victim’s email and password used during registration. But I still got this error — “username or password is incorrect.”
Then I tried to log in with the victim’s email (cyborj27+9@gmail.com) and the attacker's (wrestlingmaster27+2@gmail.com) password. And to my surprise, I got access to the account!
Now the main problem was —
“The password can be rested by the owner of the email address at any time”
So I went back to the reset password feature, I tried to reset the password and got an error — “The password could not be reset, since the email is not registered or verified.”

Then I tried to get a new verification code on the victim’s email and got an error — “ Invalid username.”

I was like:

Problem solved! User can’t reset their password through the password reset link.
This might not have been very clear till now, but I’ll summarise this in short:
Two emails: 
Attacker — Wrestlingmaster27+2@gmail.com
Victim (Unregistered account) — Cyborj27+9@gmail.com
The application does not have the functionality to change the email.
From the attacker account, change the email address to the victim’s by enumerating the UserAttributes value.
“UserAttributes”:[
{“Name”:”email”,
”Value”:”cyborj27+9@gmail.com”
}
When the attacker changes the mail, the victim will receive the OTP code for verification.
But no need to verify the mail, the attacker already got the victim’s email linked to their account.
The attacker logs out and tries to log in with the victim’s email and attacker’s password. The application will not allow this as the victim’s email is not registered yet.
The attacker navigates to the registration and registers with the victim’s email. The application throws an error — “ Your account is temporarily not available. Please try to log in in 15 minutes.”
After 15 mins, the attacker goes back to the login panel and logs in successfully with the victim’s email and attacker’s password.
When the victim tries to reset their password or try to verify the account application throws an error — “Invalid username”, meaning that the victim has lost all their ways to retrieve their account.
Due to the heavy misconfiguration (Broken Access Control), the attacker has the account linked to the victim’s email. The attacker only registered the email and did not verify the account, that’s why the backend server does not have a record of the victim’s email. (This is my guess only, not sure)
I blocked all the ways for the victim to retrieve their account:
The victim can’t reset their password by “reset password functionality.”
If the victim tries to contact the support team to reset the password, most probably, the chances are the support team will not be able to find the victim’s email in the backend as it is an unverified email — (My guess based on the error I got during password reset and verification resend)
But still, there was one “If” condition, what if the victim manages to regain their account?
I found an HTML injection in the name field when I started hunting on the application. I ignored it because there was no impact. 
Then I got an idea if somehow I managed to convert this into stored XSS and put XSS payload in the victim’s account, then whenever the victim manages to retrieve their account, the XSS will get triggered.
I put basic XSS payload in the last name field, but the application showed blank white space and no alert.


After trying for some hours, I figured out that the application has only basic protection against XSS, and it filters only <script>, <img>, alert, etc.
Then I constructed a payload, replaced alert with prompt, and it worked!
<a onmouseover=”prompt(document.cookie)”>Here</a>

As soon as the victim scrolls over the last name, XSS will get triggered.



I blocked all the ways for the victim to retrieve their password, and even if they managed to do it (Which is almost impossible), then the XSS is waiting in the profile section.
Business Impact:
The application has a critical vulnerability that allows attackers to bypass the authentication mechanisms and create an account without OTP verification.
The vulnerability also allows an attacker to abuse application functionalities, such as changing the email address in the profile section, which is not intentionally allowed by the application.
As an attacker, I could set the Name of a victim as stored XSS payloads, as the application is vulnerable to stored XSS. When victim reset their password (Which is almost impossible), they will log in to their account. As soon as the victim logs in, the XSS payload will get triggered, leading to exposing the cookies.
Bypassing the authentication mechanisms of this application allows an attacker to (pre) takeover the victim's account. As an attacker, I could use any victim’s email address to register/link the account and perform the actions on the victim's behalf.
“If you’ve made it this far, I want to say thank you for reading this long story!”
