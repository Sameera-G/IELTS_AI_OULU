document.addEventListener("DOMContentLoaded", function() {
    // Firebase configuration
    const firebaseConfig = {
      apiKey: "YOUR_API_KEY",
      authDomain: "YOUR_AUTH_DOMAIN",
      projectId: "YOUR_PROJECT_ID",
      storageBucket: "YOUR_STORAGE_BUCKET",
      messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
      appId: "YOUR_APP_ID"
    };
  
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    const db = firebase.firestore();
  
    // Reference to HTML elements
    const userIdInput = document.getElementById('userId');
    const userNameInput = document.getElementById('userName');
    const addUserBtn = document.getElementById('addUserBtn');
    const statusMessage = document.getElementById('statusMessage');
    const nextButton = document.getElementById('nextButton');
  
    // Add event listener to the Add User button
    addUserBtn.addEventListener('click', function() {
      const userId = userIdInput.value.trim();
      const userName = userNameInput.value.trim();
  
      if (userId && userName) {
        // Add user data to Firestore
        db.collection('users').doc(userId).set({
          name: userName
        })
        .then(function() {
          statusMessage.textContent = 'User added successfully.';
          statusMessage.style.color = 'green';
        })
        .catch(function(error) {
          statusMessage.textContent = 'Error adding user: ' + error.message;
          statusMessage.style.color = 'red';
        });
      } else {
        statusMessage.textContent = 'Please enter both ID and name.';
        statusMessage.style.color = 'red';
      }
    });
  
    // Add event listener to the Next button (to navigate to the next page)
    nextButton.addEventListener('click', function() {
      // Replace 'next_page.html' with the actual URL of your next page
      window.location.href = 'webapp/templates/third_page';
    });
  });
