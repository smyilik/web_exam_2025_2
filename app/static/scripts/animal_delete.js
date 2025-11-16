// document.addEventListener('DOMContentLoaded', function() {
//     const deleteButtons = document.querySelectorAll('.delete-animal');
    
//     deleteButtons.forEach(button => {
//         button.addEventListener('click', function(event) {
//             event.preventDefault();
            
//             const animalLink = this.closest('a').href;
//             const animalId = animalLink.split('/').pop();
            
//             const popUp = document.createElement('div');
//             popUp.className = 'pop-up';
            
//             const popUpFirst = document.createElement('div');
//             popUpFirst.className = 'pop-up-first';
            
//             const signParagraph = document.createElement('p');
//             signParagraph.className = 'pop-up-sign';
//             signParagraph.textContent = 'Уверены, что хотите удалить животное?';
            
//             popUpFirst.appendChild(signParagraph);
            
//             const popUpSecond = document.createElement('div');
//             popUpSecond.className = 'pop-up-second';
            
//             const cancelButton = document.createElement('button');
//             cancelButton.className = 'pop-up-btn cancel-btn';
//             cancelButton.textContent = 'Нет';
            
//             const submitButton = document.createElement('button');
//             submitButton.className = 'pop-up-btn submit-btn';
//             submitButton.textContent = 'Да';
            
//             popUpSecond.appendChild(cancelButton);
//             popUpSecond.appendChild(submitButton);
            
//             const popUpMain = document.createElement('div');
//             popUpMain.className = 'pop-up-main'

//             popUpMain.appendChild(popUpFirst);
//             popUpMain.appendChild(popUpSecond);
//             popUp.appendChild(popUpMain);
            
//             cancelButton.addEventListener('click', function() {
//                 popUp.remove();
//             });
            
//             submitButton.addEventListener('click', function() {
//                 window.location.href = animalLink;
//             });
            
//             document.body.appendChild(popUp);
            
//             popUp.addEventListener('click', function(e) {
//                 if (e.target === popUp) {
//                     popUp.remove();
//                 }
//             });
//         });
//     });
// });


document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-animal');
    const approveButtons = document.querySelectorAll('.approve-request');
    const disapproveButtons = document.querySelectorAll('.disapprove-request');
    
    // Function to create popup
    function createPopup(message, actionUrl) {
        const popUp = document.createElement('div');
        popUp.className = 'pop-up';
        
        const popUpFirst = document.createElement('div');
        popUpFirst.className = 'pop-up-first';
        
        const signParagraph = document.createElement('p');
        signParagraph.className = 'pop-up-sign';
        signParagraph.textContent = message;
        
        popUpFirst.appendChild(signParagraph);
        
        const popUpSecond = document.createElement('div');
        popUpSecond.className = 'pop-up-second';
        
        const cancelButton = document.createElement('button');
        cancelButton.className = 'pop-up-btn cancel-btn';
        cancelButton.textContent = 'Нет';
        
        const submitButton = document.createElement('button');
        submitButton.className = 'pop-up-btn submit-btn';
        submitButton.textContent = 'Да';
        
        popUpSecond.appendChild(cancelButton);
        popUpSecond.appendChild(submitButton);
        
        const popUpMain = document.createElement('div');
        popUpMain.className = 'pop-up-main'

        popUpMain.appendChild(popUpFirst);
        popUpMain.appendChild(popUpSecond);
        popUp.appendChild(popUpMain);
        
        cancelButton.addEventListener('click', function() {
            popUp.remove();
        });
        
        submitButton.addEventListener('click', function() {
            window.location.href = actionUrl;
        });
        
        document.body.appendChild(popUp);
        
        popUp.addEventListener('click', function(e) {
            if (e.target === popUp) {
                popUp.remove();
            }
        });
    }
    
    // Delete animal event
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            const animalLink = this.closest('a').href;
            const animalId = animalLink.split('/').pop();
            
            createPopup('Уверены, что хотите удалить животное?', animalLink);
        });
    });
    
    // Approve request event
    approveButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            const requestLink = this.closest('a').href;
            
            createPopup('Уверены, что хотите подтвердить заявку?', requestLink);
        });
    });
    
    // Disapprove request event
    disapproveButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            const requestLink = this.closest('a').href;
            
            createPopup('Уверены, что хотите отклонить заявку?', requestLink);
        });
    });
});