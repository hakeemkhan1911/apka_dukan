function toggleMenu(button) {
    // Find the closest menu container and toggle the dropdown
    const menuContainer = button.closest('.menu-container');
    const dropdownMenu = menuContainer.querySelector('.dropdown-menu');
    
    // Close all other dropdowns
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        if (menu !== dropdownMenu) {
            menu.style.display = 'none';
        }
    });

    // Toggle the current dropdown
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.menu-container')) {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.style.display = 'none';
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.copy-btn').forEach(button => {
    button.addEventListener('click', function () {
      const targetId = this.getAttribute('data-target');
      const input = document.getElementById(targetId);

      input.select();
      input.setSelectionRange(0, 99999); // For mobile support

      navigator.clipboard.writeText(input.value).then(() => {
        alert('نمبر کاپی ہو گیا ہے: ' + input.value);
        const originalText = this.innerText;
        this.innerText = 'کاپی ہو گیا';
        setTimeout(() => {
          this.innerText = originalText;
        }, 2000);
      }).catch(err => {
        console.error('کاپی کرنے میں ناکامی: ', err);
      });
    });
  });
});