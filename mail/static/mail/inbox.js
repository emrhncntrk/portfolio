document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', submit_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function display_email(id) {
  //Display a singe email
  document.querySelector('#email-display').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      
      console.log(email);

      document.querySelector("#email-display").innerHTML = `
        <div class="mailinfo">
        <h6><strong>From:</strong> ${email.sender}</h6>
        <h6><strong>From:</strong> ${email.recipients}</h6>
        <h6><strong>Subject:</strong> ${email.subject}</h6>
        <h6><strong>At:</strong> ${email.timestamp}</h6>
        </div>
        <br>
        <div class="mailbody">
        <h4>${email.body}</h4>
        </div>
        `;
        //Mark email as read
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
        //Archive Button
        const arcbutton = document.createElement('button');
        if (email.archived){
          arcbutton.innerHTML = "Un-Archive"
        }else{
          arcbutton.innerHTML = "Archive"
        }

        arcbutton.addEventListener('click', function() {
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: !email.archived
            })
          })
          .then(()=>{load_mailbox("inbox");})

        });
        document.querySelector('#email-display').append(arcbutton);

        //Reply Button
        const replybutton = document.createElement('button');
        replybutton.innerHTML = "Reply"
        replybutton.addEventListener('click', function() {
          compose_email();
          let mailsubject = email.subject
          if(!mailsubject.startsWith("Re:")){
            mailsubject = `Re: ${mailsubject}`
          }
          
          document.querySelector('#compose-recipients').value = email.sender;
          document.querySelector('#compose-subject').value = mailsubject;
          document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
        })
        document.querySelector('#email-display').append(replybutton);
          


  });
  
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-display').style.display = 'none';
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-display').style.display = 'none';

  //get mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Create Divs for each email
      emails.forEach(email => {
        const mail = document.createElement('div');
        mail.innerHTML = `
        <h6>From:${email.sender}</h6>
        <h6>Subject:${email.subject}</h6>
        <h8>At:${email.timestamp}</h8>
        `;
        mail.addEventListener('click', function() {
            display_email(email.id);
        });
        document.querySelector('#emails-view').append(mail);
        if (email.read == true){
          mail.style.backgroundColor = "grey"
        }
      })
  });

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function submit_mail(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      load_mailbox("sent");
      
  });

}