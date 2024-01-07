const messageContainer = document.getElementById("message-container");
const form = document.getElementById("chatbot-form");
const inputField = document.getElementById("message-input");
var chatbotContainer = document.getElementById("chatbot-container");
var chatbotForm = document.getElementById("chatbot-form");
var complaintFormContainer = document.getElementById("complaint-form-container");
var chatbotIcon = document.getElementById("chatbot-icon");

chatbotIcon.onclick = function () {
  chatbotIcon.style.display = "none";
  chatbotContainer.style.display = "block";
}

// Get a reference to the close and refresh chat buttons
const closeChatButton = document.getElementById("closeChatButton");
const refreshChatButton = document.getElementById("refreshChatButton");

// Add click event listeners to the buttons
closeChatButton.addEventListener("click", () => {
  chatbotContainer.style.display = "none";
});

refreshChatButton.addEventListener("click", () => {
  location.reload();
});

// function to submit the complaint form
function submitComplaint(event) {
  event.preventDefault();

  // get the values from the form
  const name = document.getElementById("name-input").value;
  const email = document.getElementById("email-input").value;
  const phone = document.getElementById("phone-input").value;
  const description = document.getElementById("description-input").value;

  // validate the form
  if (name.trim() === "" || email.trim() === "" || phone.trim() === "" || description.trim() === "") {
    alert("Please fill out all fields.");
    return;
  }

  // send the complaint to the server using AJAX
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/complaints/");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      // add a new message to the message container indicating that the complaint has been submitted
      const responseDiv = document.createElement("div");
      responseDiv.classList.add("message", "bot");
      responseDiv.textContent = "Your complaint has been submitted. Thank you for your feedback!";
      messageContainer.appendChild(responseDiv);

      // clear the input fields and focus on the message input field
      document.getElementById("complaint-form").reset();
      inputField.focus();
    }
  };
  xhr.send(JSON.stringify({
    name: name,
    email: email,
    phone: phone,
    description: description,
  }));
}

// function to send a message to the chatbot
function sendMessage(message) {
  event.preventDefault(); // prevent the form from submitting
  var form = document.getElementById('chatbot-form');
  addUserMessage(message)
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/chatbot/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      handleResponse(xhr.responseText);
    }
  };
  xhr.send('message=' + encodeURIComponent(message));
  document.getElementById('message-input').value = '';
}

// add the user's message to the chat container
function addUserMessage(message) {
  var messageContainer = document.createElement('div');
  messageContainer.classList.add('message');
  messageContainer.classList.add('user');
  var messageText = document.createTextNode(message);
  messageContainer.appendChild(messageText);
  document.getElementById('message-container').appendChild(messageContainer);
  document.getElementById('message-container').scrollTop = document.getElementById('message-container').scrollHeight;
}

// handle the response received from the server
function handleResponse(response) {
  var messageContainer = document.createElement('div');
  messageContainer.classList.add('message');
  messageContainer.classList.add('bot');
  var responseData = JSON.parse(response);
  var messageText = document.createTextNode(responseData.response);
  messageContainer.appendChild(messageText);
  document.getElementById('message-container').appendChild(messageContainer);
  document.getElementById('message-container').scrollTop = document.getElementById('message-container').scrollHeight;
}

// Get a reference to the "Report a Complaint" button
const reportButton = document.querySelector('#reportButton');

// Add a click event listener to the button
reportButton.addEventListener('click', () => {
  // Display the complaint form inside the chatbot container
  const formHtml = '<form id="complaintForm">' +
    '<label for="name" class="mt-1">Name:</label>' +
    '<input type="text" class="form-control mb-1" id="name-c" name="name" required>' +
    '<label for="phone">Phone:</label>' +
    '<input type="text" maxlength="10" class="form-control mb-1" id="phone-c" name="phone" required>' +
    '<label for="complaint">Complaint:</label>' +
    '<textarea class="form-control mb-1" name="complaint" required></textarea>' +
    '<button class="btn btn-primary mt-1" type="submit">Submit</button>' +
    '</form>';
  const chatbotContainer = document.querySelector('#chatbot-container');
  chatbotContainer.style.height = "350px";
  chatbotContainer.innerHTML = formHtml;

  // Add a submit event listener to the complaint form
  const complaintForm = document.querySelector('#complaintForm');
  complaintForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(complaintForm);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'complaint/', true);
    xhr.onload = () => {
      if (xhr.status === 200) {
        // Display a success message inside the chatbot container
        console.log(xhr.response);
        chatbotContainer.innerHTML = `
        <h3 class="mt-3">Your ticket ID is: ${xhr.response.ticket_id_main}</h3>
        <br>
        Please Note this Ticket Id For Reference to Your Complaint!
        `;
      } else if (xhr.status === 405) {
        // Display an error message inside the chatbot container
        chatbotContainer.innerHTML = '<p>Something went wrong. Please try again later.</p>';
      } else if (xhr.status === 410) {
        chatbotContainer.innerHTML = '<p>Invalid Phone Number</p>';
      }
    };
    xhr.responseType = 'json';
    xhr.send(formData);
  });
});