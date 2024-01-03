# Email Client Project

## Send Mail
When a user submits the email composition form, add JavaScript code to send the email. Make a POST request to `/emails`, passing in values for recipients, subject, and body. After sending the email, load the user's sent mailbox.

## Mailbox
- When a user visits their Inbox, Sent mailbox, or Archive, load the appropriate mailbox.
- Make a GET request to `/emails/<mailbox>` to retrieve emails for a particular mailbox.
- The name of the mailbox should appear at the top of the page.
- Each email is rendered in its own box with the sender, subject, and timestamp displayed.
- Unread emails have a white background, while read emails have a gray background.

## View Email
- Clicking on an email takes the user to a view displaying the email's content.
- Make a GET request to `/emails/<email_id>` to retrieve the email.
- Show sender, recipients, subject, timestamp, and body.
- Update code to hide and show the right views when navigation options are clicked.
- Mark the email as read upon viewing by sending a PUT request to `/emails/<email_id>`.

## Archive and Unarchive
- Allow users to archive and unarchive received emails.
- In the Inbox, present an archive button; in the Archive, provide an unarchive button.
- Use a PUT request to `/emails/<email_id>` to mark an email as archived or unarchived.
- After archiving or unarchiving an email, load the user’s inbox.

## Reply
- Allow users to reply to an email.
- Present a "Reply" button when viewing an email.
- Clicking the "Reply" button takes the user to the email composition form.
- Prefill the recipient field with the original email sender.
- Prefill the subject line with "Re: original_subject" if needed.
- Prefill the email body with a reply template.

This project was developed as part of Harvard's CS50 Web Programming course.
