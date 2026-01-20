console.log('The file is loading')

const openDeleteModal = () => {
    document.getElementById('deleteModal').classList.add('active')
}

const closeDeleteModal = () => {
    document.getElementById('deleteModal').classList.remove('active')
}

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeDeleteModal();
            }
        });
    }
});