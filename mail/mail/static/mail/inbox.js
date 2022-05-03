document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#detail-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#detail-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/'+ mailbox)
  .then(response => response.json())
  .then(emails => {  
    console.log(emails)  ;
    emails.forEach(function(mail){      
      let div = document.createElement('div');
      div.className = "email-list-item ";
      if(mail.read){
        div.className += "email-list-item-read";
      } else{
        div.className += "email-list-item-unread";
      }

      let senderdiv = document.createElement('div');
      senderdiv.textContent = mail.sender;
      div.appendChild(senderdiv);

      let subjectdiv = document.createElement('div');
      subjectdiv.textContent = mail.subject;
      div.appendChild(subjectdiv);

      let timestampdiv = document.createElement('div');
      timestampdiv.textContent = mail.timestamp;
      div.appendChild(timestampdiv);
      
      document.querySelector('#emails-view').appendChild(div);
      div.addEventListener('click', () => load_mail(mail.id));
    });
  })
  .catch(error => {
    console.log(error);
  });  
}

function send_email(){
  event.preventDefault();
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  fetch('emails',{
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .catch(function(){
    console.log("error");
  })
  .then(result => {
    console.log(result);
  });

  load_mailbox('sent')
}

function load_mail(mailId){
  document.querySelector('#detail-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  fetch('/emails/' + mailId,{
    method: 'GET'
  })
  .then(response => response.json())
  .then(mail => {
    let div = document.createElement('div');

    let senderdiv = document.createElement('div');
    senderdiv.textContent = mail.sender;
    div.appendChild(senderdiv);

    let recdiv = document.createElement('div');
    recdiv.textContent = mail.recipients;
    div.appendChild(recdiv);

    let subjectdiv = document.createElement('div');
    subjectdiv.textContent = mail.subject;
    div.appendChild(subjectdiv);

    let timestampdiv = document.createElement('div');
    timestampdiv.textContent = mail.timestamp;
    div.appendChild(timestampdiv);

    let bodydiv = document.createElement('div');
    bodydiv.textContent = mail.body;
    div.appendChild(bodydiv);

    let readdiv = document.createElement('div');
    readdiv.textContent = mail.read;
    div.appendChild(readdiv);

    let user = document.getElementsByTagName('h2')[0].innerHTML;    
    if(mail.recipients.includes(user)){
      let buttonArchive = document.createElement('button');
      buttonArchive.innerHTML = mail.archived ? 'unarchive' : 'archive';
      buttonArchive.addEventListener('click', () => archive_mail(mailId, mail.archived));      
      div.appendChild(buttonArchive);
    }
    
    
    document.querySelector('#detail-view').innerHTML = "";
    document.querySelector('#detail-view').appendChild(div);  
  })
  .catch(error => console.log(error));

  fetch('/emails/' + mailId, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });
}

function archive_mail(mailId, isArchived){  
  fetch("/emails/" + mailId, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !isArchived
    })
  })

 load_mailbox("inbox") 
}