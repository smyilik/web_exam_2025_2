let allFiles = [];
document.getElementById('images').addEventListener('change', function(event) {
    const newFiles = Array.from(event.target.files);
    
    // Filter only image files
    const imageFiles = newFiles.filter(file => file.type.match('image.*'));
    
    // Add new files to our storage
    allFiles = [...allFiles, ...imageFiles];

    // Update preview and input
    updatePreviewAndInput();
});

function updatePreviewAndInput() {
    const previewContainer = document.getElementById('imagePreviewContainer');
    const input = document.getElementById('images');
    
    // Clear and rebuild preview
    previewContainer.innerHTML = '';
    
    allFiles.forEach((file, index) => {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            
            previewItem.innerHTML = `
                <img src="${e.target.result}" alt="Preview ${index + 1}">
                <button type="button" class="remove-btn" data-index="${index}">×</button>
            `;
            
            previewContainer.appendChild(previewItem);
            
            const removeBtn = previewItem.querySelector('.remove-btn');
            removeBtn.addEventListener('click', function() {
                allFiles.splice(index, 1);
                updatePreviewAndInput();
            });
        };
        
        reader.readAsDataURL(file);
    });
    
    // Update input files
    const dt = new DataTransfer();
    allFiles.forEach(file => dt.items.add(file));
    input.files = dt.files;
    
}