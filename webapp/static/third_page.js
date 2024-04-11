document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display reading text
    fetch('paragraphs/reading_passage.txt')
      .then(response => response.text())
      .then(text => document.getElementById('readingText').innerText = text);
  
    // Fetch and display questions text
    fetch('paragraphs/questions.txt')
      .then(response => response.text())
      .then(text => document.getElementById('questionsText').innerText = text);
  
    // Create draggable cards
    const cardsContainer = document.getElementById('cardsContainer');
    const cardTexts = ['TRUE', 'TRUE', 'TRUE', 'FALSE', 'FALSE', 'FALSE'];
    cardTexts.forEach(text => {
      const card = document.createElement('div');
      card.classList.add('card');
      card.innerText = text;
      cardsContainer.appendChild(card);
      makeDraggable(card);
    });
  
    function makeDraggable(element) {
      let offsetX, offsetY;
  
      function onMouseDown(e) {
        e.preventDefault();
        offsetX = e.clientX - element.getBoundingClientRect().left;
        offsetY = e.clientY - element.getBoundingClientRect().top;
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
      }
  
      function onMouseMove(e) {
        element.style.left = e.clientX - offsetX + 'px';
        element.style.top = e.clientY - offsetY + 'px';
      }
  
      function onMouseUp() {
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        snapToCage(element);
      }
  
      element.addEventListener('mousedown', onMouseDown);
    }
  
    function snapToCage(card) {
      const cages = document.querySelectorAll('.cage');
      let closestCage = null;
      let minDistance = Infinity;
      cages.forEach(cage => {
        const rect = cage.getBoundingClientRect();
        const distance = Math.abs(card.getBoundingClientRect().top - rect.top);
        if (distance < minDistance) {
          minDistance = distance;
          closestCage = cage;
        }
      });
      if (closestCage) {
        const rect = closestCage.getBoundingClientRect();
        card.style.left = rect.left + rect.width / 2 - card.offsetWidth / 2 + 'px';
        card.style.top = rect.top + rect.height / 2 - card.offsetHeight / 2 + 'px';
      }
    }
  });
  